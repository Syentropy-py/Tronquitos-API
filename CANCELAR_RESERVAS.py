#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Interactivo para CANCELAR RESERVAS
Los Tronquitos - Sistema de Gestión
"""

import requests
import json
from datetime import datetime

# Colores para terminal
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

BACKEND_URL = 'http://localhost:5000'

def print_header():
    print("\n" + "="*60)
    print("  🍽️  SISTEMA DE CANCELACIÓN DE RESERVAS")
    print("  Los Tronquitos - Gestión de Mesas")
    print("="*60)
    print(f"  Fecha: {datetime.now().strftime('%d de %b %Y - %H:%M:%S')}")
    print("="*60 + "\n")

def print_menu():
    print("\n" + Colors.CYAN + "OPCIONES:" + Colors.RESET)
    print("  1. Buscar reserva por ID")
    print("  2. Listar todas las reservas de hoy")
    print("  3. Cancelar una reserva")
    print("  4. Ver disponibilidad de mesas")
    print("  5. Salir")
    print()

def get_reservations_today():
    """Obtiene las reservas de hoy"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f'{BACKEND_URL}/api/availability?fecha={today}')
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('reservations', [])
        else:
            print(f"{Colors.RED}❌ Error: {response.status_code}{Colors.RESET}")
            return []
    except Exception as e:
        print(f"{Colors.RED}❌ Error al conectar: {e}{Colors.RESET}")
        return []

def list_reservations():
    """Lista todas las reservas"""
    reservations = get_reservations_today()
    
    if not reservations:
        print(f"{Colors.YELLOW}ℹ️  No hay reservas para hoy{Colors.RESET}\n")
        return
    
    print(f"\n{Colors.BLUE}═══ RESERVAS DE HOY ═══{Colors.RESET}\n")
    
    for res in reservations:
        is_special = res['personas'] > 30
        status_icon = "✨" if is_special else "✓"
        
        print(f"  ID: {Colors.CYAN}{res['id']}{Colors.RESET} | {res['nombre']}")
        print(f"     Personas: {res['personas']} {status_icon} | Hora: {res['hora']}")
        print(f"     Teléfono: {res['telefono']}")
        
        if res['table_number']:
            print(f"     Mesa: #{res['table_number']}")
        else:
            print(f"     Mesa: GRUPO ESPECIAL (sin límite)")
        
        print()

def search_reservation_by_id():
    """Busca una reserva por ID"""
    res_id = input(f"\n{Colors.CYAN}Ingresa el ID de reserva: {Colors.RESET}").strip()
    
    if not res_id.isdigit():
        print(f"{Colors.RED}❌ ID inválido{Colors.RESET}")
        return None
    
    reservations = get_reservations_today()
    
    for res in reservations:
        if res['id'] == int(res_id):
            return res
    
    print(f"{Colors.RED}❌ Reserva no encontrada{Colors.RESET}")
    return None

def cancel_reservation():
    """Cancela una reserva"""
    print(f"\n{Colors.YELLOW}═══ CANCELAR RESERVA ═══{Colors.RESET}\n")
    
    # Búsqueda
    reservation = search_reservation_by_id()
    if not reservation:
        return
    
    # Confirmar datos
    print(f"\n{Colors.BLUE}Datos de la reserva:{Colors.RESET}")
    print(f"  Nombre: {reservation['nombre']}")
    print(f"  Teléfono: {reservation['telefono']}")
    print(f"  Personas: {reservation['personas']}")
    print(f"  Hora: {reservation['hora']}")
    
    if reservation['table_number']:
        print(f"  Mesa: #{reservation['table_number']}")
    else:
        print(f"  Mesa: ESPECIAL (sin mesa asignada)")
    
    # Confirmación
    confirm = input(f"\n{Colors.RED}¿Estás seguro de cancelar esta reserva? (s/n): {Colors.RESET}").strip().lower()
    
    if confirm != 's':
        print(f"{Colors.YELLOW}❌ Cancelación abortada{Colors.RESET}")
        return
    
    # Mensaje opcional
    message = input(f"\n{Colors.CYAN}Mensaje personalizado para el cliente (opcional, presiona Enter para omitir):{Colors.RESET}\n> ").strip()
    
    # Procesar cancelación
    try:
        print(f"\n{Colors.YELLOW}⏳ Procesando cancelación...{Colors.RESET}")
        
        response = requests.post(
            f'{BACKEND_URL}/api/cancel-reservation',
            json={'reservation_id': reservation['id']},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n{Colors.GREEN}✅ RESERVA CANCELADA EXITOSAMENTE{Colors.RESET}")
            print(f"\n  📋 Detalles:")
            print(f"     Reserva ID: {reservation['id']}")
            
            if reservation['table_number']:
                print(f"     Mesa liberada: #{reservation['table_number']}")
            
            print(f"     Cliente: {reservation['nombre']}")
            print(f"     Teléfono: {reservation['telefono']}")
            
            if message:
                print(f"\n  💬 Mensaje enviado:")
                print(f"     {message}")
            else:
                print(f"\n  📱 Mensaje automático enviado al cliente")
            
            print(f"\n{Colors.GREEN}✓ N8N notificó al cliente automáticamente{Colors.RESET}\n")
            
        else:
            error = response.json()
            print(f"{Colors.RED}❌ Error: {error['message']}{Colors.RESET}")
    
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ Error de conexión. ¿El backend está corriendo?{Colors.RESET}")
        print(f"   Ejecuta: python -Xutf8=1 app.py")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")

def show_availability():
    """Muestra disponibilidad de mesas"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f'{BACKEND_URL}/api/availability?fecha={today}')
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n{Colors.BLUE}═══ DISPONIBILIDAD DE MESAS ═══{Colors.RESET}\n")
            print(f"  Total de mesas: {data['total_tables']}")
            print(f"  {Colors.RED}Reservadas: {data['reserved_tables']}{Colors.RESET}")
            print(f"  {Colors.GREEN}Disponibles: {data['available_tables']}{Colors.RESET}")
            print()
        else:
            print(f"{Colors.RED}❌ Error al obtener disponibilidad{Colors.RESET}")
    
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")

def main():
    """Loop principal"""
    print_header()
    
    # Verificar conexión
    try:
        response = requests.get(f'{BACKEND_URL}/api/tables', timeout=2)
        if response.status_code != 200:
            print(f"{Colors.RED}⚠️  Backend no responde correctamente{Colors.RESET}")
    except:
        print(f"{Colors.RED}⚠️  Backend no está disponible en {BACKEND_URL}{Colors.RESET}")
        print(f"   Ejecuta: python backend/app.py\n")
    
    while True:
        print_menu()
        choice = input(f"{Colors.CYAN}Selecciona una opción (1-5): {Colors.RESET}").strip()
        
        if choice == '1':
            reservation = search_reservation_by_id()
            if reservation:
                is_special = reservation['personas'] > 30
                print(f"\n{Colors.GREEN}✓ Reserva encontrada:{Colors.RESET}")
                print(f"  Nombre: {reservation['nombre']}")
                print(f"  Personas: {reservation['personas']} {'(ESPECIAL)' if is_special else ''}")
                print(f"  Hora: {reservation['hora']}")
                print(f"  Teléfono: {reservation['telefono']}")
        
        elif choice == '2':
            list_reservations()
        
        elif choice == '3':
            cancel_reservation()
        
        elif choice == '4':
            show_availability()
        
        elif choice == '5':
            print(f"\n{Colors.GREEN}¡Hasta pronto!{Colors.RESET}\n")
            break
        
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.RESET}")
        
        input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.RESET}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Programa interrumpido por el usuario{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}\n")
