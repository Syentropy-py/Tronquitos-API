#!/usr/bin/env python3
"""
Setup Script para Los Tronquitos Backend
Ejecuta esta script una sola vez para inicializar todo el sistema
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅  {text}")

def print_error(text):
    print(f"❌  {text}")

def print_info(text):
    print(f"ℹ️   {text}")

def main():
    print_header("🍽️ SETUP - Los Tronquitos Backend")
    
    backend_path = Path(__file__).parent
    os.chdir(backend_path)
    
    # Step 1: Verificar Python version
    print_info("Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or version.minor < 8:
        print_error(f"Se requiere Python 3.8+, tienes Python {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
    
    # Step 2: Verificar requirements.txt existe
    print_info("Verificando archivo requirements.txt...")
    if not Path("requirements.txt").exists():
        print_error("requirements.txt no encontrado")
        return False
    print_success("requirements.txt encontrado ✓")
    
    # Step 3: Verificar que los módulos existen
    print_info("Verificando módulos de aplicación...")
    modules = ["models.py", "database.py", "reservation_service.py", "app.py", "init_db.py"]
    for module in modules:
        if Path(module).exists():
            print_success(f"{module} ✓")
        else:
            print_error(f"{module} no encontrado")
            return False
    
    # Step 4: Compilar módulos
    print_info("Compilando módulos Python...")
    try:
        modules_to_compile = ["models.py", "database.py", "reservation_service.py"]
        for module in modules_to_compile:
            compile(open(module, encoding='utf-8').read(), module, 'exec')
            print_success(f"{module} compilado ✓")
    except Exception as e:
        print_error(f"Error compilando: {e}")
        return False
    
    # Step 5: Inicializar BD
    print_header("Inicializando Base de Datos")
    try:
        print_info("Ejecutando init_db.py...")
        import init_db
        init_db.init_db()
        print_success("Base de datos inicializada ✓")
    except Exception as e:
        print_error(f"Error inicializando BD: {e}")
        return False
    
    # Step 6: Verificar BD
    print_info("Verificando BD...")
    try:
        import database as db
        tables_list = db.get_all_tables()
        count = len(tables_list)
        print_success(f"BD verificada con {count} mesas ✓")
    except Exception as e:
        print_error(f"Error verificando BD: {e}")
        return False
    
    # Step 7: Summary
    print_header("✨ CONFIGURACIÓN COMPLETADA")
    print("""
    El backend está listo para usar. Próximos pasos:

    1. Iniciar el servidor:
       python app.py

    2. El servidor estará disponible en:
       http://localhost:5000

    3. Para configurar n8n:
       - Lee N8N_SETUP_GUIDE.md
       - Importa n8n_workflow.json en n8n
       - Configura tus credenciales de WhatsApp

    4. Documentación completa:
       - API_DOCUMENTATION.md
       - INSTALLATION_GUIDE.md

    5. Pruebas rápidas:
       curl http://localhost:5000/api/tables
       curl http://localhost:5000/api/availability?fecha=2026-03-20
    """)
    
    print_success("¡Todo listo! 🎉")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
