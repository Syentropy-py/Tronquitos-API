#!/usr/bin/env python3
"""
🔍 VERIFICADOR DE SISTEMA - Los Tronquitos
Script para verificar que todo funciona antes de presentación
"""

import sys
import os
import subprocess
from datetime import datetime, timedelta

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.ENDC}\n")

def check(name, condition, error_msg=""):
    status = f"{Colors.GREEN}✅ OK{Colors.ENDC}" if condition else f"{Colors.RED}❌ FALLO{Colors.ENDC}"
    print(f"{status} - {name}")
    if not condition and error_msg:
        print(f"   {Colors.RED}→ {error_msg}{Colors.ENDC}")
    return condition

def main():
    print_header("VERIFICACIÓN PRE-PRESENTACIÓN")
    print(f"Verificación realizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    # 1. Verificar estructura de archivos
    print_header("1. ESTRUCTURA DE ARCHIVOS")
    files_to_check = {
        'backend/app.py': 'Aplicación Flask',
        'backend/database.py': 'Modulo de BD',
        'backend/models.py': 'Modelos de datos',
        'backend/reservation_service.py': 'Lógica de reservas',
        'frontend/index.html': 'Frontend',
        'n8n_doc/N8N_QUICK_START.md': 'Guía N8N',
    }
    
    for file, description in files_to_check.items():
        path = file
        exists = os.path.exists(path)
        results.append(check(f"{description} ({file})", exists, 
                           f"Archivo no encontrado: {file}"))
    
    # 2. Verificar configuraciones
    print_header("2. CONFIGURACIÓN DE VARIABLES")
    
    # Leer app.py para verificar número de WhatsApp
    try:
        with open('backend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            has_whatsapp = '573102326407' in content
            results.append(check("Número WhatsApp actualizado (+57 3102326407)", 
                               has_whatsapp,
                               "El número WhatsApp no está configurado correctamente"))
            
            has_n8n_url = 'N8N_WEBHOOK_URL' in content
            results.append(check("URL de N8N configurada", has_n8n_url,
                               "No se encontró N8N_WEBHOOK_URL"))
    except Exception as e:
        results.append(False)
        print(f"{Colors.RED}❌ Error al leer app.py: {e}{Colors.ENDC}")
    
    # 3. Verificar dependencias
    print_header("3. DEPENDENCIAS PYTHON")
    required_packages = ['flask', 'flask-cors', 'requests', 'sqlite3']
    
    try:
        import flask
        results.append(check("Flask instalado", True))
    except:
        results.append(check("Flask instalado", False, "pip install flask"))
    
    try:
        import flask_cors
        results.append(check("Flask-CORS instalado", True))
    except:
        results.append(check("Flask-CORS instalado", False, "pip install flask-cors"))
    
    try:
        import requests
        results.append(check("Requests instalado", True))
    except:
        results.append(check("Requests instalado", False, "pip install requests"))
    
    # 4. Verificar base de datos
    print_header("4. BASE DE DATOS")
    db_path = 'backend/database.db'
    results.append(check("Base de datos existe", os.path.exists(db_path),
                       f"Ejecutar: python backend/init_db.py"))
    
    # 5. Resumen
    print_header("RESUMEN DE VERIFICACIÓN")
    total = len(results)
    passed = sum(1 for r in results if r)
    
    print(f"Verificaciones pasadas: {passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✅ ¡SISTEMA LISTO PARA PRESENTACIÓN!{Colors.ENDC}\n")
        print("Pasos siguientes:")
        print("1. Ejecutar: python backend/app.py")
        print("2. Abrir: http://localhost:5000")
        print("3. Verificar: http://localhost:5000/api/tables")
        return 0
    else:
        print(f"\n{Colors.RED}❌ Hay {total - passed} problemas por resolver{Colors.ENDC}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
