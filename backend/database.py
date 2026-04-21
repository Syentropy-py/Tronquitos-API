"""
Gestión de Conexiones a Base de Datos y Operaciones CRUD
Incluye: branches, daily_capacity, tables, reservations, events, contacts
PostgreSQL version
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# Configuración de conexión a PostgreSQL
DB_HOST = os.getenv('DB_HOST', 'aws-1-us-east-1.pooler.supabase.com')
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres.kzdlspaneugbymuzsber')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Tronquitos2026')


@contextmanager
def get_db_connection():
    """Context manager para conexiones a BD PostgreSQL."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='require'
    )
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=True):
    """Ejecuta una query a la base de datos PostgreSQL."""
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
            if commit:
                conn.commit()
            return result
        elif fetch_all:
            result = cursor.fetchall()
            if commit:
                conn.commit()
            return result
        else:
            # Retorna el ID del último registro insertado ANTES de hacer commit
            # LASTVAL() debe estar en la misma transacción que el INSERT
            last_id = None
            if "INSERT" in query.upper():
                cursor.execute("SELECT LASTVAL()")
                last_id_row = cursor.fetchone()
                last_id = last_id_row['lastval'] if last_id_row else None
            if commit:
                conn.commit()
            return last_id


# =============================================
# OPERACIONES CRUD - BRANCHES (SEDES)
# =============================================

def get_branch_by_name(name):
    """Obtiene una sede por nombre."""
    return execute_query('SELECT * FROM branches WHERE name = %s', (name,), fetch_one=True)


def get_all_branches():
    """Retorna todas las sedes activas."""
    return execute_query('SELECT * FROM branches WHERE active = 1 ORDER BY name', fetch_all=True)


def get_branch_schedule(name):
    """Retorna los horarios de una sede."""
    branch = get_branch_by_name(name)
    if not branch:
        return None
    return {
        'name': branch['name'],
        'open_time': branch['open_time'],
        'close_time': branch['close_time'],
        'default_capacity': branch['default_capacity']
    }


# =============================================
# OPERACIONES CRUD - DAILY CAPACITY
# =============================================

def get_daily_capacity(branch_id, date):
    """
    Retorna el límite de capacidad para una sede/día.
    Si no hay registro, usa la capacidad por defecto de la sede.
    """
    row = execute_query(
        'SELECT * FROM daily_capacity WHERE branch_id = %s AND date = %s',
        (branch_id, date), fetch_one=True
    )
    if row:
        return dict(row)
    # Usar capacidad por defecto de la sede
    branch = execute_query('SELECT * FROM branches WHERE id = %s', (branch_id,), fetch_one=True)
    if branch:
        return {
            'branch_id': branch_id,
            'date': date,
            'capacity_limit': branch['default_capacity'],
            'blocked': False,
            'note': None
        }
    return None


def get_reserved_people(branch_name, date):
    """
    Suma total de personas con reservas confirmadas para una sede/día.
    """
    result = execute_query("""
        SELECT COALESCE(SUM(personas), 0) as total
        FROM reservations
        WHERE sede = %s AND fecha = %s AND status IN ('confirmed', 'completed')
    """, (branch_name, date), fetch_one=True)
    return result['total'] if result else 0


def can_accept_reservation(branch_name, date, people):
    """
    Verifica si se puede aceptar una reserva para una sede/día dado el número de personas.
    Retorna dict con 'allowed', 'capacity', 'reserved', 'available'.
    """
    branch = get_branch_by_name(branch_name)
    if not branch:
        return {'allowed': False, 'error': 'Sede no encontrada'}

    cap_info = get_daily_capacity(branch['id'], date)
    if cap_info is None:
        return {'allowed': False, 'error': 'No se pudo obtener capacidad'}

    if cap_info['blocked']:
        return {
            'allowed': False,
            'capacity': cap_info['capacity_limit'],
            'reserved': get_reserved_people(branch_name, date),
            'available': 0,
            'blocked': True,
            'note': cap_info.get('note', 'Día bloqueado')
        }

    reserved = get_reserved_people(branch_name, date)
    available = cap_info['capacity_limit'] - reserved

    return {
        'allowed': (available >= people),
        'capacity': cap_info['capacity_limit'],
        'reserved': reserved,
        'available': available,
        'blocked': False
    }


def set_daily_capacity(branch_id, date, capacity_limit, note=None):
    """Inserta o actualiza el límite de capacidad para un día específico."""
    existing = execute_query(
        'SELECT id FROM daily_capacity WHERE branch_id = %s AND date = %s',
        (branch_id, date), fetch_one=True
    )
    if existing:
        execute_query("""
            UPDATE daily_capacity SET capacity_limit = %s, note = %s
            WHERE branch_id = %s AND date = %s
        """, (capacity_limit, note, branch_id, date))
    else:
        execute_query("""
            INSERT INTO daily_capacity (branch_id, date, capacity_limit, note)
            VALUES (%s, %s, %s, %s)
        """, (branch_id, date, capacity_limit, note))


def block_day(branch_id, date, note=None):
    """Bloquea un día completo para una sede."""
    existing = execute_query(
        'SELECT id FROM daily_capacity WHERE branch_id = %s AND date = %s',
        (branch_id, date), fetch_one=True
    )
    if existing:
        execute_query("""
            UPDATE daily_capacity SET blocked = 1, note = %s
            WHERE branch_id = %s AND date = %s
        """, (note or 'Día bloqueado', branch_id, date))
    else:
        execute_query("""
            INSERT INTO daily_capacity (branch_id, date, capacity_limit, blocked, note)
            SELECT %s, %s, default_capacity, 1, %s
            FROM branches WHERE id = %s
        """, (branch_id, date, note or 'Día bloqueado', branch_id))


def unblock_day(branch_id, date):
    """Desbloquea un día para una sede."""
    execute_query("""
        UPDATE daily_capacity SET blocked = 0, note = NULL
        WHERE branch_id = %s AND date = %s
    """, (branch_id, date))


def get_calendar_summary(branch_name, year, month):
    """
    Retorna resumen de capacidad para todos los días de un mes.
    [{date, capacity, reserved, available, blocked}]
    """
    branch = get_branch_by_name(branch_name)
    if not branch:
        return []

    # Obtener reservas del mes agrupadas por día
    rows = execute_query("""
        SELECT fecha, COALESCE(SUM(personas), 0) as reserved
        FROM reservations
        WHERE sede = %s
          AND EXTRACT(YEAR FROM fecha) = %s
          AND EXTRACT(MONTH FROM fecha) = %s
          AND status IN ('confirmed', 'completed')
        GROUP BY fecha
    """, (branch_name, year, month), fetch_all=True)

    reserved_by_date = {str(r['fecha']): r['reserved'] for r in rows}

    # Obtener capacidades customizadas del mes
    cap_rows = execute_query("""
        SELECT dc.date, dc.capacity_limit, dc.blocked, dc.note
        FROM daily_capacity dc
        WHERE dc.branch_id = %s
          AND EXTRACT(YEAR FROM dc.date) = %s
          AND EXTRACT(MONTH FROM dc.date) = %s
    """, (branch['id'], year, month), fetch_all=True)
    cap_by_date = {str(r['date']): dict(r) for r in cap_rows}

    # Construir lista de días del mes
    import calendar
    days_in_month = calendar.monthrange(year, month)[1]
    result = []
    for day in range(1, days_in_month + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        reserved = reserved_by_date.get(date_str, 0)
        if date_str in cap_by_date:
            cap_info = cap_by_date[date_str]
            cap = cap_info['capacity_limit']
            blocked = cap_info['blocked']
            note = cap_info['note']
        else:
            cap = branch['default_capacity']
            blocked = 0
            note = None
        result.append({
            'date': date_str,
            'capacity': cap,
            'reserved': reserved,
            'available': max(0, cap - reserved),
            'blocked': bool(blocked),
            'note': note
        })
    return result


# =============================================
# OPERACIONES CRUD - TABLAS (MESAS)
# =============================================

def create_table(table_number, capacity, sede='Centro'):
    """Crea una nueva mesa en la BD"""
    query = '''
        INSERT INTO tables (table_number, capacity, status, sede)
        VALUES (%s, %s, 'free', %s)
    '''
    return execute_query(query, (table_number, capacity, sede))


def get_table(table_id):
    """Obtiene información de una mesa específica"""
    query = 'SELECT * FROM tables WHERE id = %s'
    return execute_query(query, (table_id,), fetch_one=True)


def get_all_tables():
    """Obtiene todas las mesas"""
    query = 'SELECT * FROM tables ORDER BY table_number'
    return execute_query(query, fetch_all=True)


def get_available_tables(people_count, fecha, hora, sede='Centro'):
    """Obtiene mesas disponibles para un número de personas, datetime y sede."""
    query = '''
        SELECT t.* FROM tables t
        WHERE t.sede = %s
        AND t.capacity >= %s
        AND t.id NOT IN (
            SELECT table_id FROM reservations
            WHERE fecha = %s 
            AND hora = %s
            AND sede = %s
            AND status IN ('confirmed', 'completed')
            AND table_id IS NOT NULL
        )
        ORDER BY t.capacity ASC
    '''
    return execute_query(query, (sede, people_count, fecha, hora, sede), fetch_all=True)


def update_table_status(table_id, status):
    """Actualiza el estado de una mesa"""
    query = '''
        UPDATE tables 
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    '''
    execute_query(query, (status, table_id))


def get_available_tables_count():
    """Retorna el número de mesas disponibles"""
    query = "SELECT COUNT(*) as count FROM tables WHERE status = 'free'"
    result = execute_query(query, fetch_one=True)
    return result['count'] if result else 0


# =============================================
# OPERACIONES CRUD - RESERVAS
# =============================================

def create_reservation(nombre, telefono, email, personas, fecha, hora, tabla_id, sede='Centro', mensaje='', is_special_group=0):
    """Crea una nueva reserva en una sede específica"""
    query = '''
        INSERT INTO reservations 
        (nombre, telefono, email, personas, fecha, hora, table_id, sede, mensaje, status, is_special_group)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'confirmed', %s)
    '''
    return execute_query(query, (nombre, telefono, email, personas, fecha, hora, tabla_id, sede, mensaje, is_special_group))


def get_reservation(reservation_id):
    """Obtiene información de una reserva específica"""
    query = 'SELECT * FROM reservations WHERE id = %s'
    return execute_query(query, (reservation_id,), fetch_one=True)


def get_all_active_reservations():
    """Obtiene todas las reservas activas (confirmadas) sin filtrar por fecha"""
    query = '''
        SELECT r.*, t.table_number FROM reservations r
        LEFT JOIN tables t ON r.table_id = t.id
        WHERE r.status IN ('confirmed', 'completed')
        ORDER BY r.fecha ASC, r.hora ASC
    '''
    return execute_query(query, fetch_all=True)


def get_reservations_by_date(fecha, sede=None):
    """Obtiene todas las reservas para una fecha específica (y opcionalmente sede)"""
    if sede:
        query = '''
            SELECT r.*, t.table_number FROM reservations r
            LEFT JOIN tables t ON r.table_id = t.id
            WHERE r.fecha = %s AND r.sede = %s AND r.status IN ('confirmed', 'completed')
            ORDER BY r.hora
        '''
        return execute_query(query, (fecha, sede), fetch_all=True)
    else:
        query = '''
            SELECT r.*, t.table_number FROM reservations r
            LEFT JOIN tables t ON r.table_id = t.id
            WHERE r.fecha = %s AND r.status IN ('confirmed', 'completed')
            ORDER BY r.hora
        '''
        return execute_query(query, (fecha,), fetch_all=True)


def cancel_reservation(reservation_id):
    """Cancela una reserva y libera la mesa asociada"""
    reservation = get_reservation(reservation_id)
    if not reservation:
        return False
    query = '''
        UPDATE reservations 
        SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    '''
    execute_query(query, (reservation_id,))
    if reservation['table_id']:
        update_table_status(reservation['table_id'], 'free')
    return True


def delete_reservation(reservation_id):
    """Elimina una reserva de la BD, sus eventos asociados y libera la mesa asociada"""
    reservation = get_reservation(reservation_id)
    if not reservation:
        return False
    if reservation['table_id']:
        update_table_status(reservation['table_id'], 'free')
        
    # Eliminar eventos asociados primero para evitar violar la llave foránea
    execute_query('DELETE FROM events WHERE reservation_id = %s', (reservation_id,))
    
    query = 'DELETE FROM reservations WHERE id = %s'
    execute_query(query, (reservation_id,))
    return True


def complete_reservation(reservation_id):
    """Marca una reserva como completada"""
    query = '''
        UPDATE reservations 
        SET status = 'completed', updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    '''
    execute_query(query, (reservation_id,))


def mark_no_show(reservation_id):
    """Marca una reserva como no presentada (no-show)"""
    reservation = get_reservation(reservation_id)
    if not reservation:
        return False
    query = '''
        UPDATE reservations 
        SET status = 'no_show', updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    '''
    execute_query(query, (reservation_id,))
    if reservation['table_id']:
        update_table_status(reservation['table_id'], 'free')
    return True


def get_late_reservations(minutes_late=20):
    """Obtiene reservas que están más de X minutos tarde."""
    # Nota: minutes_late es un entero interno (no input de usuario), seguro usar f-string
    # para construir el literal INTERVAL ya que psycopg2 no puede parametrizar literales de tipo
    minutes_late = int(minutes_late)  # garantizar tipo
    query = f'''
        SELECT r.* FROM reservations r
        WHERE r.status = 'confirmed'
        AND r.table_id IS NOT NULL
        AND (r.fecha::TIMESTAMP + r.hora::TIME) < NOW() - INTERVAL '{minutes_late} minutes'
    '''
    return execute_query(query, fetch_all=True)


# =============================================
# OPERACIONES CRUD - EVENTOS
# =============================================

def create_event(event_type, reservation_id=None, table_id=None, description=''):
    """Crea un registro de evento para auditoría"""
    query = '''
        INSERT INTO events (event_type, reservation_id, details)
        VALUES (%s, %s, %s)
    '''
    return execute_query(query, (event_type, reservation_id, description))


def get_events(limit=100):
    """Obtiene los últimos eventos"""
    query = '''
        SELECT * FROM events
        ORDER BY created_at DESC
        LIMIT %s
    '''
    return execute_query(query, (limit,), fetch_all=True)


# =============================================
# OPERACIONES PARA CONTACTOS Y OPINIONES
# =============================================

def create_contact(nombre, telefono, email, mensaje):
    """Crea un nuevo contacto"""
    query = '''
        INSERT INTO contacts (nombre, telefono, email, mensaje)
        VALUES (%s, %s, %s, %s)
    '''
    return execute_query(query, (nombre, telefono, email, mensaje))


def create_opinion(autor, rating, comentario):
    """Crea una nueva opinión"""
    query = '''
        INSERT INTO opinions (autor, rating, comentario)
        VALUES (%s, %s, %s)
    '''
    return execute_query(query, (autor, rating, comentario))


# =============================================
# OPERACIONES CRUD - PRODUCTOS (MENÚ)
# =============================================

def get_all_products(categoria=None, solo_disponibles=False):
    """Obtiene todos los productos, con filtro opcional por categoría."""
    if categoria and solo_disponibles:
        query = 'SELECT * FROM products WHERE categoria = %s AND disponible = TRUE ORDER BY categoria, nombre'
        return execute_query(query, (categoria,), fetch_all=True)
    elif categoria:
        query = 'SELECT * FROM products WHERE categoria = %s ORDER BY categoria, nombre'
        return execute_query(query, (categoria,), fetch_all=True)
    elif solo_disponibles:
        query = 'SELECT * FROM products WHERE disponible = TRUE ORDER BY categoria, nombre'
        return execute_query(query, fetch_all=True)
    else:
        query = 'SELECT * FROM products ORDER BY categoria, nombre'
        return execute_query(query, fetch_all=True)


def get_product(product_id):
    """Obtiene un producto por ID."""
    query = 'SELECT * FROM products WHERE id = %s'
    return execute_query(query, (product_id,), fetch_one=True)


def get_product_by_sku(sku):
    """Obtiene un producto por SKU."""
    query = 'SELECT * FROM products WHERE sku = %s'
    return execute_query(query, (sku,), fetch_one=True)


def create_product(sku, nombre, precio, categoria, descripcion=None, imagen_url=None, disponible=True):
    """Crea un nuevo producto en la BD."""
    query = '''
        INSERT INTO products (sku, nombre, precio, categoria, descripcion, imagen_url, disponible)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    return execute_query(query, (sku, nombre, precio, categoria, descripcion, imagen_url, disponible))


def update_product(product_id, **fields):
    """Actualiza un producto. Solo actualiza los campos proporcionados."""
    allowed_fields = {'sku', 'nombre', 'precio', 'categoria', 'descripcion', 'imagen_url', 'disponible'}
    update_fields = {k: v for k, v in fields.items() if k in allowed_fields}

    if not update_fields:
        return False

    set_clause = ', '.join(f'{k} = %s' for k in update_fields.keys())
    values = list(update_fields.values()) + [product_id]

    query = f'UPDATE products SET {set_clause} WHERE id = %s'
    execute_query(query, tuple(values))
    return True


def delete_product(product_id):
    """Elimina un producto de la BD."""
    product = get_product(product_id)
    if not product:
        return False
    query = 'DELETE FROM products WHERE id = %s'
    execute_query(query, (product_id,))
    return True


def toggle_product_availability(product_id):
    """Alterna la disponibilidad de un producto."""
    product = get_product(product_id)
    if not product:
        return None
    new_status = not product['disponible']
    query = 'UPDATE products SET disponible = %s WHERE id = %s'
    execute_query(query, (new_status, product_id))
    return new_status
