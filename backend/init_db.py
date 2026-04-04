import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from models import (
    BRANCHES_SCHEMA, DAILY_CAPACITY_SCHEMA, TABLES_SCHEMA, RESERVATIONS_SCHEMA, CONTACTS_SCHEMA, 
    OPINIONS_SCHEMA, EVENTS_SCHEMA
)

load_dotenv()

# Configuración de conexión a PostgreSQL
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_NAME = os.getenv('DB_NAME', 'tronquitos')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

def init_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Table for Branches (Sedes)
        cursor.execute(BRANCHES_SCHEMA)
        print("[v] Tabla 'branches' creada/verificada")

        # Table for Daily Capacity
        cursor.execute(DAILY_CAPACITY_SCHEMA)
        print("[v] Tabla 'daily_capacity' creada/verificada")

        # Table for Mesas (Tables)
        cursor.execute(TABLES_SCHEMA)
        print("[v] Tabla 'tables' creada/verificada")

        # Table for Reservations (Mejorada con control de mesas)
        cursor.execute(RESERVATIONS_SCHEMA)
        print("[v] Tabla 'reservations' creada/verificada")

        # Table for Contacts
        cursor.execute(CONTACTS_SCHEMA)
        print("[v] Tabla 'contacts' creada/verificada")

        # Table for Opinions
        cursor.execute(OPINIONS_SCHEMA)
        print("[v] Tabla 'opinions' creada/verificada")
        
        # Table for Events (Auditoría)
        cursor.execute(EVENTS_SCHEMA)
        print("[v] Tabla 'events' creada/verificada")

        conn.commit()
        
        # Poblar branches (sedes)
        cursor.execute('SELECT COUNT(*) as count FROM branches')
        count_result = cursor.fetchone()
        count = count_result['count'] if count_result else 0
        
        if count == 0:
            print("[*] Creando sedes...")
            
            # Definir las 6 sedes con sus horarios
            sedes_data = [
                ('Principal', 'Av. Calle 3 #53-07, Bogotá', '414 68 70', '11:30', '18:00', 80),
                ('Terraza', 'Cra 7 #19-74, Bogotá', '414 68 70', '11:30', '18:00', 80),
                ('Restrepo', 'Cl 15 Sur #22-20, Bogotá', '414 68 70', '11:30', '18:00', 80),
                ('Nieves', 'Cra 7 #19-74, Bogotá', '414 68 70', '11:30', '18:00', 80),
                ('7ma con 22', 'Cra 7 #22-12, Bogotá', '414 68 70', '11:30', '19:00', 80),
                ('Av Rojas', 'Av. Rojas #3-08, Bogotá', '414 68 70', '11:30', '18:00', 80),
            ]
            
            for name, location, phone, open_time, close_time, capacity in sedes_data:
                cursor.execute('''
                    INSERT INTO branches (name, location, phone, open_time, close_time, default_capacity, active)
                    VALUES (%s, %s, %s, %s, %s, %s, 1)
                ''', (name, location, phone, open_time, close_time, capacity))
            
            conn.commit()
            print(f"[v] {len(sedes_data)} sedes creadas")
            print(f"[v] Sedes: {', '.join([s[0] for s in sedes_data])}")
        
        # Crear mesas por defecto si no existen
        cursor.execute('SELECT COUNT(*) as count FROM tables')
        count_result = cursor.fetchone()
        count = count_result['count'] if count_result else 0
        
        if count == 0:
            print("[*] Creando mesas por defecto para cada sede...")
            
            # Obtener las sedes creadas
            cursor.execute('SELECT name FROM branches ORDER BY name')
            sedes = [row['name'] for row in cursor.fetchall()]
            
            # Definir capacidades de mesas
            # Mesas con capacidades desde 2 hasta 50 personas
            default_table_configs = [
                (1, 2), (2, 2), (3, 4), (4, 4), (5, 4),
                (6, 6), (7, 6), (8, 8), (9, 15), (10, 50)
            ]
            
            # Crear mesas para cada sede
            total_tables = 0
            for sede in sedes:
                for table_num, capacity in default_table_configs:
                    cursor.execute(
                        'INSERT INTO tables (table_number, capacity, sede, status) VALUES (%s, %s, %s, %s)',
                        (table_num, capacity, sede, 'free')
                    )
                    total_tables += 1
            
            conn.commit()
            print(f"[v] {total_tables} mesas creadas ({len(default_table_configs)} por sede)")
            print(f"[v] Sedes: {', '.join(sedes)}")
            print(f"[v] Capacidad por sede: ~92 personas (hasta 50 en mesa de eventos)")
        
        
        conn.close()
        print(f"\n[✓] Base de datos inicializada exitosamente en {DB_HOST}:{DB_PORT}/{DB_NAME}")
        
    except psycopg2.Error as e:
        print(f"[!] Error al conectar a la base de datos: {e}")
        print("\n[NOTA] Asegúrate de que PostgreSQL está corriendo y los parámetros de conexión son correctos.")
        print("Variables de entorno requeridas:")
        print(f"  - DB_HOST={DB_HOST}")
        print(f"  - DB_PORT={DB_PORT}")
        print(f"  - DB_NAME={DB_NAME}")
        print(f"  - DB_USER={DB_USER}")
        raise

if __name__ == '__main__':
    init_db()
