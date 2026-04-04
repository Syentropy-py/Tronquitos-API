#!/usr/bin/env python3
"""
Script maestro para configurar todo el sistema con las 6 nuevas sedes.
Este script:
1. Limpia la base de datos anterior
2. Reinitializa la base de datos con las nuevas sedes
3. Muestra un resumen
"""

import os
import sys

# Add backend directory to path
backend_dir = os.path.dirname(__file__)
sys.path.insert(0, backend_dir)

from limpiar_datos import clean_data
from init_db import init_db

def setup_system():
    print("=" * 60)
    print("🔧 CONFIGURACIÓN DEL SISTEMA - LOS TRONQUITOS")
    print("=" * 60)
    print()
    
    # Paso 1: Eliminar base de datos vieja
    print("PASO 1: Limpiando base de datos anterior...")
    print("-" * 60)
    clean_data(remove_db=True)
    print()
    
    # Paso 2: Reinitializar base de datos
    print("PASO 2: Reinitializando base de datos con nuevas sedes...")
    print("-" * 60)
    init_db()
    print()
    
    # Paso 3: Resumen
    print("=" * 60)
    print("✅ SISTEMA CONFIGURADO EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Sedes creadas:")
    print("  ✓ Principal")
    print("  ✓ Terraza")
    print("  ✓ Restrepo")
    print("  ✓ Nieves")
    print("  ✓ 7ma con 22")
    print("  ✓ Av Rojas")
    print()
    print("Características:")
    print("  ✓ 10 mesas por sede")
    print("  ✓ Capacidad total por sede: ~92 personas")
    print("  ✓ Horarios dinámicos según la sede")
    print("  ✓ Gestión de capacidad diaria")
    print()
    print("Próximos pasos:")
    print("  1. Instalar dependencias: pip install -r requirements.txt")
    print("  2. Ejecutar el backend: python app.py")
    print("  3. Acceder a: http://localhost:5000")
    print()

if __name__ == '__main__':
    try:
        setup_system()
    except Exception as e:
        print(f"\n[ERROR] Error durante la configuración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
