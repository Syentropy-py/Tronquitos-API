#!/usr/bin/env python3
"""Migración: Agregar columna is_special_group a tabla reservations"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Verificar si la columna ya existe
    cursor.execute("PRAGMA table_info(reservations)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'is_special_group' not in columns:
        print("[*] Agregando columna is_special_group a tabla reservations...")
        cursor.execute("""
            ALTER TABLE reservations 
            ADD COLUMN is_special_group INTEGER DEFAULT 0
        """)
        conn.commit()
        print("[✓] Columna is_special_group agregada exitosamente")
    else:
        print("[✓] Columna is_special_group ya existe")
        
    conn.close()
    
except Exception as e:
    print(f"[!] Error: {e}")
    conn.close()
