"""
Migración: Agrega tablas branches y daily_capacity a la BD existente.
Ejecutar una sola vez: python migrate_capacity.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ── 1. Tabla branches (sedes) ──────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            location TEXT,
            open_time TEXT NOT NULL DEFAULT '12:00',
            close_time TEXT NOT NULL DEFAULT '18:00',
            default_capacity INTEGER NOT NULL DEFAULT 50,
            active INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Insertar las 3 sedes si no existen
    branches = [
        ('Centro', 'Av. Calle 3 #53-07, Bogotá',   '12:00', '18:00', 50),
        ('Usaquén', 'Av. Rojas 63C #03, Bogotá',    '12:00', '18:00', 50),
        ('Chapinero', 'Trav. 42 #3-08, Bogotá',     '12:00', '18:00', 50),
    ]
    for name, loc, ot, ct, cap in branches:
        cursor.execute("""
            INSERT OR IGNORE INTO branches (name, location, open_time, close_time, default_capacity)
            VALUES (?, ?, ?, ?, ?)
        """, (name, loc, ot, ct, cap))

    # ── 2. Tabla daily_capacity (capacidad por día por sede) ───────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_capacity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            capacity_limit INTEGER NOT NULL,
            blocked INTEGER NOT NULL DEFAULT 0,
            note TEXT,
            FOREIGN KEY (branch_id) REFERENCES branches(id),
            UNIQUE (branch_id, date)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_cap_branch_date ON daily_capacity(branch_id, date)")

    # ── 3. Agregar columna 'sede' a tables si no existe ───────────
    try:
        cursor.execute("ALTER TABLE tables ADD COLUMN sede TEXT DEFAULT 'Centro'")
        print("[v] Columna 'sede' agregada a tabla 'tables'")
    except sqlite3.OperationalError:
        print("[i] Columna 'sede' ya existe en tabla 'tables'")

    # Asignar sede Centro a mesas existentes sin sede
    cursor.execute("UPDATE tables SET sede='Centro' WHERE sede IS NULL")

    # ── 4. Agregar columna 'sede' a reservations si no existe ─────
    try:
        cursor.execute("ALTER TABLE reservations ADD COLUMN sede TEXT DEFAULT 'Centro'")
        print("[v] Columna 'sede' agregada a tabla 'reservations'")
    except sqlite3.OperationalError:
        print("[i] Columna 'sede' ya existe en tabla 'reservations'")

    cursor.execute("UPDATE reservations SET sede='Centro' WHERE sede IS NULL")

    # ── 5. Agregar columna is_special_group si no existe ──────────
    try:
        cursor.execute("ALTER TABLE reservations ADD COLUMN is_special_group INTEGER DEFAULT 0")
        print("[v] Columna 'is_special_group' agregada")
    except sqlite3.OperationalError:
        print("[i] Columna 'is_special_group' ya existe")

    conn.commit()
    conn.close()
    print("\n[v] Migración completada exitosamente.")
    print("    Tablas: branches, daily_capacity")
    print("    Sedes insertadas: Centro, Usaquén, Chapinero")

if __name__ == '__main__':
    migrate()
