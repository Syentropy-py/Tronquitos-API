#!/usr/bin/env python3
"""
GUÍA DE DEMOSTRACIÓN EN VIVO - Los Tronquitos
Ejecutable paso a paso para la presentación de mañana
"""

import subprocess
import time
import json
import requests
from datetime import datetime, timedelta

# COLORES
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

def print_step(num, title):
    print(f"\n{BLUE}{'='*70}{ENDC}")
    print(f"{BLUE}PASO {num}: {title}{ENDC}")
    print(f"{BLUE}{'='*70}{ENDC}\n")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{ENDC}")

def print_success(msg):
    print(f"{GREEN}✅ {msg}{ENDC}")

def print_error(msg):
    print(f"{RED}❌ {msg}{ENDC}")

def print_action(msg):
    print(f"{YELLOW}→ {msg}{ENDC}")

# ============================================================
# PASO 1: VERIFICACIÓN INICIAL
# ============================================================
def paso_1_verificacion():
    print_step(1, "VERIFICACIÓN INICIAL DEL SISTEMA")
    
    print_info("Ejecutando verificación automática...")
    print_action("$ python VERIFICAR_SISTEMA.py\n")
    
    try:
        resultado = subprocess.run(
            ['python', 'VERIFICAR_SISTEMA.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if resultado.returncode == 0:
            print_success("Sistema verificado exitosamente")
            print(resultado.stdout[-200:])  # Últimas líneas
        else:
            print_error("Verificación falló")
            print(resultado.stderr)
            
    except Exception as e:
        print_error(f"Error al verificar: {e}")

# ============================================================
# PASO 2: BACKEND INFO
# ============================================================
def paso_2_backend_info():
    print_step(2, "INFORMACIÓN DEL BACKEND")
    
    print_info("Backend corriendo en: http://localhost:5000")
    print_info("N8N corriendo en:      http://localhost:5678 (si activado)")
    print()
    
    print_action("Probando conexión a Backend...\n")
    
    try:
        respuesta = requests.get('http://localhost:5000/api/tables', timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            print_success(f"Backend respondiendo - {len(datos['data'])} mesas disponibles")
            
            # Mostrar 3 mesas
            print("\nPrimeras 3 mesas:")
            for mesa in datos['data'][:3]:
                print(f"  Mesa #{mesa['table_number']:2d} | Capacidad: {mesa['capacity']:2d} | Estado: {mesa['status']}")
            print("  ...")
        else:
            print_error(f"Backend retornó status {respuesta.status_code}")
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar a Backend (¿está ejecutando python app.py?)")
    except Exception as e:
        print_error(f"Error: {e}")

# ============================================================
# PASO 3: DEMO - RESERVA NORMAL
# ============================================================
def paso_3_reserva_normal():
    print_step(3, "DEMOSTRACIÓN 1: RESERVA NORMAL (4 personas)")
    
    fecha = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    print_action("Crear reserva para:")
    print(f"  - Nombre: María González")
    print(f"  - Personas: 4")
    print(f"  - Fecha: {fecha}")
    print(f"  - Hora: 19:00")
    print()
    
    datos = {
        'Nombre': 'María González',
        'Teléfono': '+573102326407',
        'Email': 'maria@ejemplo.com',
        'Personas': 4,
        'Fecha': fecha,
        'Hora': '19:00',
        'Sede': 'Centro',
        'Mensaje': 'Demostración en vivo'
    }
    
    print_action(f"POST /api/reservation\n")
    
    try:
        respuesta = requests.post(
            'http://localhost:5000/api/reservation',
            json=datos,
            timeout=10
        )
        
        if respuesta.status_code == 201:
            resultado = respuesta.json()
            print_success("✅ RESERVA CREADA EXITOSAMENTE")
            print(f"\n  Número de Reserva:  {resultado['reservation_id']}")
            print(f"  Mesa Asignada:      #{resultado['table_number']}")
            print(f"  Personas:           {datos['Personas']}")
            print(f"  Fecha:              {datos['Fecha']}")
            print(f"  Hora:               {datos['Hora']}")
            print(f"  Grupo Especial:     {resultado['is_special_group']}")
            
            return resultado['reservation_id']
        else:
            print_error(f"Error: {respuesta.status_code}")
            print(respuesta.json())
            
    except Exception as e:
        print_error(f"Error: {e}")
    
    return None

# ============================================================
# PASO 4: DEMO - RESERVA GRUPAL ESPECIAL
# ============================================================
def paso_4_reserva_especial():
    print_step(4, "DEMOSTRACIÓN 2: RESERVA GRUPAL ESPECIAL (60 personas)")
    
    fecha = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    
    print_action("Crear reserva para:")
    print(f"  - Empresa: Tech Solutions Ltd")
    print(f"  - Personas: 60 ⭐ (GRUPO ESPECIAL)")
    print(f"  - Fecha: {fecha}")
    print(f"  - Tipo: Evento corporativo")
    print()
    
    datos = {
        'Nombre': 'Tech Solutions Ltd',
        'Teléfono': '+573102326407',
        'Email': 'eventos@techsolutions.com',
        'Personas': 60,
        'Fecha': fecha,
        'Hora': '12:00',
        'Sede': 'Centro',
        'Mensaje': 'Almuerzo de equipo - Requiere coordinación especial'
    }
    
    print_action("POST /api/reservation\n")
    
    try:
        respuesta = requests.post(
            'http://localhost:5000/api/reservation',
            json=datos,
            timeout=10
        )
        
        if respuesta.status_code == 201:
            resultado = respuesta.json()
            print_success("⭐ RESERVA GRUPAL ESPECIAL REGISTRADA")
            print(f"\n  Número de Reserva:  {resultado['reservation_id']}")
            print(f"  Personas:           {datos['Personas']}")
            print(f"  Mesa Asignada:      {resultado['table_number']} (SIN LÍMITE)")
            print(f"  Grupo Especial:     {resultado['is_special_group']} ✅")
            print(f"\n  Mensaje del Sistema:")
            print(f"    {resultado['message']}")
            
            if 'note' in resultado:
                print(f"\n  Nota:")
                print(f"    {resultado['note']}")
            
            return resultado['reservation_id']
        else:
            print_error(f"Error: {respuesta.status_code}")
            
    except Exception as e:
        print_error(f"Error: {e}")
    
    return None

# ============================================================
# PASO 5: DISPONIBILIDAD
# ============================================================
def paso_5_disponibilidad():
    print_step(5, "DEMOSTRACIÓN 3: VERIFICAR DISPONIBILIDAD")
    
    fecha = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    print_action(f"GET /api/availability?fecha={fecha}\n")
    
    try:
        respuesta = requests.get(
            f'http://localhost:5000/api/availability?fecha={fecha}',
            timeout=10
        )
        
        if respuesta.status_code == 200:
            datos = respuesta.json()['data']
            
            print_success("DISPONIBILIDAD ACTUALIZADA")
            print(f"\n  Fecha:                {datos['fecha']}")
            print(f"  Total de Mesas:       {datos['total_tables']}")
            print(f"  Mesas Disponibles:    {datos['available_tables']} ✓")
            print(f"  Mesas Reservadas:     {datos['reserved_tables']}")
            print(f"  Mesas Ocupadas:       {datos['occupied_tables']}")
            
            print(f"\n  Reservas para esa fecha:")
            if datos.get('reservations'):
                for res in datos['reservations'][:3]:
                    print(f"    - {res.get('nombre', '?'):20s} | {res.get('hora', '?'):5s} | {res.get('personas', '?')} personas")
                if len(datos.get('reservations', [])) > 3:
                    print(f"    ... y {len(datos['reservations']) - 3} más")
            else:
                print("    (Sin reservas aún)")
                
    except Exception as e:
        print_error(f"Error: {e}")

# ============================================================
# PASO 6: EVENTOS (AUDITORÍA)
# ============================================================
def paso_6_eventos():
    print_step(6, "DEMOSTRACIÓN 4: LOG DE EVENTOS (AUDITORÍA)")
    
    print_action("GET /api/events?limit=5\n")
    
    try:
        respuesta = requests.get(
            'http://localhost:5000/api/events?limit=5',
            timeout=10
        )
        
        if respuesta.status_code == 200:
            eventos = respuesta.json()['data']
            
            print_success("ÚLTIMOS 5 EVENTOS REGISTRADOS")
            print()
            
            tipos = {
                'reservation': '📝 Reserva',
                'cancellation': '❌ Cancelación',
                'table_freed': '🪑 Mesa liberada',
                'no_show': '⚠️  No presentarse'
            }
            
            for evt in eventos[-5:]:
                tipo = tipos.get(evt['event_type'], evt['event_type'])
                print(f"  {tipo}")
                print(f"    {evt['description']}")
                print(f"    Hora: {evt['created_at']}")
                print()
                
    except Exception as e:
        print_error(f"Error: {e}")

# ============================================================
# PASO 7: RESUMEN N8N
# ============================================================
def paso_7_n8n():
    print_step(7, "N8N: INTEGRACIÓN DE WEBHOOKS (OPCIONAL)")
    
    print_info("Si N8N está corriendo en http://localhost:5678:")
    print()
    print_action("Ver workflow:")
    print("  1. Abrir http://localhost:5678")
    print("  2. Ver workflow 'Los Tronquitos - Reservas'")
    print("  3. Click en 'Webhook' → Copiar URL")
    print()
    
    print_action("Workflow actual:")
    print("  [Webhook] → [Switch] → [HTTP POST] → [Set] → [Responder]")
    print()
    
    print_info("El Backend envía automáticamente a:")
    print("  http://localhost:5678/webhook/tronquitos")
    print()
    
    print_info("Ver ejecuciones en N8N:")
    print("  1. Tab 'Executions' (abajo)")
    print("  2. Expandir ejecución más reciente")
    print("  3. Ver datos en cada nodo")

# ============================================================
# MAIN
# ============================================================
def main():
    print(f"\n{BLUE}")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "🍽️  LOS TRONQUITOS - DEMOSTRACIÓN EN VIVO" + " "*11 + "║")
    print("║" + " "*15 + "Sistema de Gestión de Reservas v1.0" + " "*17 + "║")
    print("╚" + "="*68 + "╝")
    print(f"{ENDC}")
    
    print(f"\n{YELLOW}Fecha: {datetime.now().strftime('%d de Marzo de 2026')}{ENDC}")
    print(f"{YELLOW}Hora: {datetime.now().strftime('%H:%M:%S')}{ENDC}\n")
    
    # Ejecutar pasos
    try:
        paso_1_verificacion()
        time.sleep(2)
        
        paso_2_backend_info()
        time.sleep(2)
        
        res1 = paso_3_reserva_normal()
        time.sleep(2)
        
        res2 = paso_4_reserva_especial()
        time.sleep(2)
        
        paso_5_disponibilidad()
        time.sleep(2)
        
        paso_6_eventos()
        time.sleep(2)
        
        paso_7_n8n()
        
        # Resumen final
        print_step(8, "RESUMEN FINAL")
        print(f"{GREEN}{'='*70}{ENDC}")
        print(f"\n{GREEN}✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE{ENDC}\n")
        
        print(f"{BLUE}Características Demostradas:{ENDC}")
        print(f"  ✓ Sistema de reservas funcional")
        print(f"  ✓ Validación de disponibilidad")
        print(f"  ✓ Asignación automática de mesas")
        print(f"  ✓ Soporte para grupos especiales (>30 personas)")
        print(f"  ✓ BD SQLite actualizada en tiempo real")
        print(f"  ✓ Integración N8N preparada")
        print(f"  ✓ API RESTful completa")
        print(f"  ✓ Log de auditoría automático")
        
        print(f"\n{BLUE}Números Importantes:{ENDC}")
        print(f"  • Teléfono: +57 3102326407")
        print(f"  • Backend: http://localhost:5000")
        print(f"  • N8N: http://localhost:5678")
        
        print(f"\n{BLUE}Pasos Para Mañana:{ENDC}")
        print(f"  1. Ejecutar: python VERIFICAR_SISTEMA.py")
        print(f"  2. Ejecutar: python backend/app.py")
        print(f"  3. Ejecutar: python DEMO_PRESENTACION.py (este script)")
        print(f"  4. Abrir: http://localhost:5000")
        
        print(f"\n{GREEN}{'='*70}{ENDC}\n")
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Demostración cancelada por el usuario{ENDC}\n")
    except Exception as e:
        print_error(f"Error general: {e}")

if __name__ == '__main__':
    main()
