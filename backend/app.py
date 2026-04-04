from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv
import smtplib
import threading
from email.message import EmailMessage
from datetime import datetime, timedelta
import requests
import logging
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

# Importar módulos de negocio
import database as db
from reservation_service import ReservationService
from models import EventType

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# CONFIGURACIÓN DE CORREO SMTP
# ==========================================
EMAIL_ADDRESS = "nico35134@gmail.com"
EMAIL_PASSWORD = "wmmk zraj cept gphl"

def send_email_smtp(subject, data):
    try:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = subject
        cuerpo = f"{subject}\n\n"
        for key, value in data.items():
            if key != 'timestamp' and not key.startswith('_'):
                cuerpo += f"{key}: {value}\n"
        msg.set_content(cuerpo)
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("[v] Correo enviado exitosamente vía SMTP.")
    except Exception as e:
        print(f"[!] Error al enviar el correo SMTP: {e}")

# ==========================================
# CONFIGURACIÓN DE N8N PARA WHATSAPP
# ==========================================
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'https://syentropy.app.n8n.cloud/webhook-test/6f64fe1d-0d22-471a-aeaf-02eba7f7e4d8')
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '573127923219') # Número de WhatsApp asociado a N8N (con código de país, sin +)

def send_to_n8n(message_type, data, meta=None):
    """Envía datos a N8N para procesamiento con WhatsApp"""
    try:
        payload = {
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            "whatsapp_number": WHATSAPP_NUMBER,
            "data": data
        }
        if meta:
            payload["meta"] = meta
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[v] Datos enviados a N8N exitosamente. Tipo: {message_type}")
        else:
            print(f"[!] Error en N8N: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error conectando con N8N: {e}")
def _row_to_dict(row):
    """Convierte fila de BD a dict y serializa fechas y horas para JSON"""
    if not row:
        return None
    d = dict(row)
    for k, v in d.items():
        if isinstance(v, (dt.date, dt.time, dt.datetime)):
            d[k] = str(v)
    return d

app = Flask(__name__)
CORS(app)

# ======================================================
# RUTAS PARA SERVIR ARCHIVOS ESTÁTICOS
# ======================================================
@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'styles.css')

@app.route('/scripts.js')
def scripts():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'scripts.js')

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets'), filename)

@app.route('/<path:filename>')
def serve_file(filename):
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', filename)
    if os.path.exists(frontend_path):
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), filename)
    root_path = os.path.join(os.path.dirname(__file__), '..', filename)
    if os.path.exists(root_path):
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), filename)
    return "File not found", 404


def append_to_csv(filename, data_dict):
    csv_path = os.path.join(os.path.dirname(__file__), filename)
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_dict)


# ====================================================
# ENDPOINTS DE HORARIOS / SCHEDULE
# ====================================================

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    """
    Retorna horarios de apertura/cierre y slots disponibles para una sede.
    Query Params: sede (nombre)
    Response:
    {
      "name": "Centro",
      "open_time": "12:00",
      "close_time": "18:00",
      "slots": ["12:00", "12:30", ..., "17:30"]
    }
    """
    sede = request.args.get('sede', 'Centro')
    schedule = db.get_branch_schedule(sede)
    if not schedule:
        return jsonify({"status": "error", "message": "Sede no encontrada"}), 404

    # Generar slots de 30 min en el rango de horario
    slots = []
    open_h, open_m = map(int, schedule['open_time'].split(':'))
    close_h, close_m = map(int, schedule['close_time'].split(':'))
    current = datetime(2000, 1, 1, open_h, open_m)
    end = datetime(2000, 1, 1, close_h, close_m)
    # No mostrar el último slot si está muy cerca del cierre
    while current < end - timedelta(minutes=30):
        slots.append(current.strftime('%H:%M'))
        current += timedelta(minutes=30)

    return jsonify({
        "status": "success",
        "data": {
            "name": schedule['name'],
            "open_time": schedule['open_time'],
            "close_time": schedule['close_time'],
            "default_capacity": schedule['default_capacity'],
            "slots": slots
        }
    }), 200


# ====================================================
# ENDPOINTS DE DISPONIBILIDAD
# ====================================================

@app.route('/api/availability', methods=['GET'])
def get_availability():
    """
    Retorna cupos disponibles para una sede/fecha.
    Query Params: fecha (YYYY-MM-DD), sede (nombre)
    """
    try:
        fecha = request.args.get('fecha')
        sede = request.args.get('sede', 'Centro')

        if not fecha:
            return jsonify({
                "status": "error",
                "message": "El parámetro 'fecha' es requerido (formato: YYYY-MM-DD)"
            }), 400

        cap_check = db.can_accept_reservation(sede, fecha, 0)

        if 'error' in cap_check:
            return jsonify({"status": "error", "message": cap_check['error']}), 400

        reservations = db.get_reservations_by_date(fecha, sede)

        return jsonify({
            "status": "success",
            "data": {
                "fecha": fecha,
                "sede": sede,
                "capacity": cap_check['capacity'],
                "reserved": cap_check['reserved'],
                "available": cap_check['available'],
                "blocked": cap_check.get('blocked', False),
                "reservations": [_row_to_dict(r) for r in reservations]
            }
        }), 200

    except Exception as e:
        logger.error(f"[!] Error al obtener disponibilidad: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/calendar', methods=['GET'])
def get_calendar():
    """
    Retorna resumen de capacidad de todos los días de un mes.
    Query Params: sede, year, month
    """
    try:
        sede = request.args.get('sede', 'Centro')
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))

        summary = db.get_calendar_summary(sede, year, month)
        return jsonify({
            "status": "success",
            "data": {
                "sede": sede,
                "year": year,
                "month": month,
                "days": summary
            }
        }), 200
    except Exception as e:
        logger.error(f"[!] Error al obtener calendar: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ====================================================
# ENDPOINTS ADMIN - CAPACIDAD Y BLOQUEOS
# ====================================================

@app.route('/api/capacity', methods=['POST'])
def set_capacity():
    """
    Cambia la capacidad de un día específico para una sede.
    JSON Body: { "sede": "Centro", "date": "2026-03-25", "capacity": 60, "note": "Evento especial" }
    """
    try:
        data = request.json
        sede = data.get('sede')
        date = data.get('date')
        capacity = data.get('capacity')

        if not sede or not date or capacity is None:
            return jsonify({"status": "error", "message": "sede, date y capacity son requeridos"}), 400

        branch = db.get_branch_by_name(sede)
        if not branch:
            return jsonify({"status": "error", "message": "Sede no encontrada"}), 404

        db.set_daily_capacity(branch['id'], date, int(capacity), data.get('note'))
        return jsonify({"status": "success", "message": f"Capacidad actualizada a {capacity} para {sede} el {date}"}), 200
    except Exception as e:
        logger.error(f"[!] Error al actualizar capacidad: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/block-day', methods=['POST'])
def block_day():
    """
    Bloquea o desbloquea un día completo para una sede.
    JSON Body: { "sede": "Centro", "date": "2026-03-25", "block": true, "note": "Cerrado por festivo" }
    """
    try:
        data = request.json
        sede = data.get('sede')
        date = data.get('date')
        block = data.get('block', True)
        note = data.get('note', '')

        if not sede or not date:
            return jsonify({"status": "error", "message": "sede y date son requeridos"}), 400

        branch = db.get_branch_by_name(sede)
        if not branch:
            return jsonify({"status": "error", "message": "Sede no encontrada"}), 404

        if block:
            db.block_day(branch['id'], date, note)
            msg = f"Día {date} bloqueado para {sede}"
        else:
            db.unblock_day(branch['id'], date)
            msg = f"Día {date} desbloqueado para {sede}"

        return jsonify({"status": "success", "message": msg}), 200
    except Exception as e:
        logger.error(f"[!] Error al bloquear/desbloquear día: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/branches', methods=['GET'])
def get_branches():
    """Retorna todas las sedes activas."""
    try:
        branches = db.get_all_branches()
        return jsonify({
            "status": "success",
            "data": [_row_to_dict(b) for b in branches]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ====================================================
# ENDPOINTS DE RESERVAS - SISTEMA MEJORADO
# ====================================================

@app.route('/api/reservation', methods=['POST'])
def create_reservation():
    """
    Crea una nueva reserva con control de disponibilidad y horarios.
    JSON Body:
    {
        "Nombre": "Juan Pérez",
        "Teléfono": "+573001234567",
        "Email": "juan@example.com",
        "Personas": 4,
        "Fecha": "2026-03-20",
        "Hora": "14:00",
        "Sede": "Centro",
        "Mensaje": "Sin gluten por favor"
    }
    """
    try:
        data = request.json
        logger.info(f"[*] Datos recibidos: {data}")

        # Validaciones básicas
        required_fields = ['Nombre', 'Teléfono', 'Personas', 'Fecha', 'Hora', 'Sede']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                "status": "error",
                "message": f"Campos requeridos faltantes: {', '.join(missing_fields)}"
            }), 400

        # Validar personas
        try:
            personas = int(data.get('Personas', 0))
            if personas <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({
                "status": "error",
                "message": f"Personas debe ser un número mayor a 0"
            }), 400

        sede = data.get('Sede', 'Centro')
        fecha = data.get('Fecha')
        hora = data.get('Hora')

        # ── VALIDAR HORARIO DE LA SEDE ─────────────────────────────
        schedule = db.get_branch_schedule(sede)
        if not schedule:
            return jsonify({"status": "error", "message": f"Sede '{sede}' no encontrada"}), 400

        try:
            # Normalizar hora (puede venir como "2:00 pm", "14:00", etc.)
            hora_normalized = _normalize_hora(hora)
            open_h, open_m = map(int, schedule['open_time'].split(':'))
            close_h, close_m = map(int, schedule['close_time'].split(':'))
            res_h, res_m = map(int, hora_normalized.split(':'))

            open_mins  = open_h  * 60 + open_m
            close_mins = close_h * 60 + close_m
            res_mins   = res_h   * 60 + res_m

            # La reserva debe estar dentro del horario
            # Mínimo: hora de apertura
            # Máximo: 1 hora antes del cierre (para que alcance a comer)
            if res_mins < open_mins:
                return jsonify({
                    "status": "error",
                    "message": f"El restaurante abre a las {schedule['open_time']}. No se pueden hacer reservas antes."
                }), 400

            if res_mins > close_mins - 60:
                close_display = f"{close_h:02d}:{close_m:02d}"
                return jsonify({
                    "status": "error",
                    "message": (
                        f"Última reserva disponible: {close_h-1:02d}:{close_m:02d}. "
                        f"El restaurante cierra a las {close_display}."
                    )
                }), 400

        except Exception as e:
            return jsonify({"status": "error", "message": f"Hora inválida: {hora}"}), 400

        # ── VALIDAR CAPACIDAD DEL DÍA ──────────────────────────────
        cap_check = db.can_accept_reservation(sede, fecha, personas)

        if cap_check.get('blocked'):
            return jsonify({
                "status": "error",
                "message": f"El restaurante no recibe reservas ese día. {cap_check.get('note', '')}"
            }), 400

        if not cap_check['allowed']:
            return jsonify({
                "status": "error",
                "message": (
                    f"No hay cupos disponibles para {personas} personas en {sede} el {fecha}. "
                    f"Disponibles: {cap_check['available']} cupos."
                )
            }), 400

        # ── CREAR RESERVA ──────────────────────────────────────────
        result = ReservationService.create_reservation(
            nombre=data.get('Nombre'),
            telefono=data.get('Teléfono'),
            email=data.get('Email', ''),
            personas=personas,
            fecha=fecha,
            hora=hora_normalized,
            sede=sede,
            mensaje=data.get('Mensaje', '')
        )

        if not result['success']:
            return jsonify({"status": "error", "message": result['message']}), 400

        # ── CALCULAR CUPOS RESTANTES (para n8n) ───────────────────
        remaining = cap_check['available'] - personas

        reservation_data = {
            'reservation_id': result['reservation_id'],
            'Nombre': data.get('Nombre'),
            'Teléfono': data.get('Teléfono'),
            'Email': data.get('Email', ''),
            'Personas': personas,
            'Fecha': fecha,
            'Hora': hora_normalized,
            'Sede': sede,
            'Mensaje': data.get('Mensaje', ''),
            'table_number': result.get('table_number'),
            'is_special_group': result.get('is_special_group', False),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Guardar en CSV
        append_to_csv('reservations.csv', reservation_data)

        # Enviar Email en background
        threading.Thread(
            target=send_email_smtp,
            args=("Nueva Reservación - Los Tronquitos", reservation_data)
        ).start()

        # Enviar a N8N con cupos restantes
        threading.Thread(
            target=send_to_n8n,
            args=(EventType.RESERVATION_CREATED, reservation_data, {"remaining_capacity": remaining})
        ).start()

        return jsonify({
            "status": "success",
            "message": result['message'],
            "reservation_id": result['reservation_id'],
            "is_special_group": result.get('is_special_group', False),
            "table_number": result.get('table_number'),
            "note": result.get('note', ''),
            "remaining_capacity": remaining
        }), 201

    except Exception as e:
        import traceback
        logger.error(f"[!] Exception al crear reserva: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"status": "error", "message": f"Error interno: {str(e)}"}), 500


def _normalize_hora(hora_str):
    """
    Convierte hora a formato 24h HH:MM.
    Acepta: '14:00', '2:00 pm', '2:00 PM', '2pm', etc.
    """
    hora_str = str(hora_str).strip().lower()
    # Ya tiene formato 24h sin am/pm
    if ':' in hora_str and 'am' not in hora_str and 'pm' not in hora_str:
        h, m = hora_str.split(':')
        return f"{int(h):02d}:{int(m):02d}"
    # Tiene am o pm
    import re
    match = re.match(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', hora_str)
    if match:
        h = int(match.group(1))
        m = int(match.group(2) or 0)
        period = match.group(3)
        if period == 'pm' and h != 12:
            h += 12
        elif period == 'am' and h == 12:
            h = 0
        return f"{h:02d}:{m:02d}"
    raise ValueError(f"No se pudo parsear la hora: {hora_str}")


@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    """Retorna todas las reservas activas."""
    try:
        reservations = db.get_all_active_reservations()
        return jsonify({
            "status": "success",
            "data": [_row_to_dict(r) for r in reservations]
        }), 200
    except Exception as e:
        logger.error(f"[!] Error al obtener reservas: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/free-table', methods=['POST'])
def free_table():
    """Libera manualmente una mesa."""
    try:
        data = request.json
        table_id = data.get('table_id')
        if not table_id:
            return jsonify({"status": "error", "message": "table_id es requerido"}), 400

        result = ReservationService.free_table(table_id)
        if result['success']:
            threading.Thread(
                target=send_to_n8n,
                args=(EventType.TABLE_FREED, {'table_id': table_id})
            ).start()

        return jsonify({
            "status": "success" if result['success'] else "error",
            "message": result['message']
        }), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/cancel-reservation', methods=['POST'])
def cancel_reservation():
    """Cancela una reserva y libera la mesa asociada."""
    try:
        data = request.json
        reservation_id = data.get('reservation_id')
        if not reservation_id:
            return jsonify({"status": "error", "message": "reservation_id es requerido"}), 400

        result = ReservationService.cancel_reservation(reservation_id)
        if result['success']:
            reservation = db.get_reservation(reservation_id)
            threading.Thread(
                target=send_to_n8n,
                args=(EventType.RESERVATION_CANCELLED, {
                    'reservation_id': reservation_id,
                    'Nombre': reservation['nombre'],
                    'Teléfono': reservation['telefono'],
                    'Fecha': reservation['fecha'],
                    'Hora': reservation['hora']
                })
            ).start()

        return jsonify({
            "status": "success" if result['success'] else "error",
            "message": result['message']
        }), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/delete-reservation', methods=['POST'])
def delete_reservation():
    """Elimina una reserva de la BD y libera la mesa asociada."""
    try:
        data = request.json
        reservation_id = data.get('reservation_id')
        if not reservation_id:
            return jsonify({"status": "error", "message": "reservation_id es requerido"}), 400

        reservation = db.get_reservation(reservation_id)
        if not reservation:
            return jsonify({"status": "error", "message": "Reserva no encontrada"}), 404

        success = db.delete_reservation(reservation_id)
        if not success:
            return jsonify({"status": "error", "message": "No se pudo eliminar la reserva"}), 400

        return jsonify({
            "status": "success",
            "message": f"Reserva {reservation_id} eliminada correctamente"
        }), 200
    except Exception as e:
        logger.error(f"[!] Error al eliminar reserva: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/contacts', methods=['POST'])
def create_contact():
    """Crea un nuevo mensaje de contacto."""
    try:
        data = request.json
        required_fields = ['Nombre', 'Teléfono', 'Email', 'Mensaje']
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Campos requeridos: {', '.join(required_fields)}"
            }), 400

        db.create_contact(
            nombre=data.get('Nombre'),
            telefono=data.get('Teléfono'),
            email=data.get('Email'),
            mensaje=data.get('Mensaje')
        )

        contact_data = {
            'Nombre': data.get('Nombre'),
            'Teléfono': data.get('Teléfono'),
            'Email': data.get('Email'),
            'Mensaje': data.get('Mensaje'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        append_to_csv('contacts.csv', contact_data)

        threading.Thread(
            target=send_email_smtp,
            args=("Nuevo Mensaje de Contacto - Los Tronquitos", contact_data)
        ).start()
        threading.Thread(
            target=send_to_n8n,
            args=("contact", contact_data)
        ).start()

        return jsonify({"status": "success", "message": "Mensaje enviado correctamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/tables', methods=['GET'])
def get_tables():
    """Retorna todas las mesas."""
    try:
        tables = db.get_all_tables()
        return jsonify({"status": "success", "data": [_row_to_dict(t) for t in tables]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    """Retorna el log de eventos."""
    try:
        limit = request.args.get('limit', 50, type=int)
        events = db.get_events(limit)
        return jsonify({"status": "success", "data": [_row_to_dict(e) for e in events]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Verificar conexión y crear tablas si no existen (PostgreSQL)
    try:
        branches = db.get_all_branches()
        if not branches:
            logger.info("[*] Base de datos vacía, inicializando...")
            import init_db
            init_db.init_db()
    except Exception as e:
        logger.warning(f"[!] Error al verificar BD, intentando inicializar: {e}")
        import init_db
        init_db.init_db()

    logger.info("[*] Iniciando backend de Los Tronquitos...")
    logger.info(f"[*] URL de N8N: {N8N_WEBHOOK_URL}")
    logger.info(f"[*] Mesas disponibles: {db.get_available_tables_count()}")

    app.run(debug=True, port=5000)
