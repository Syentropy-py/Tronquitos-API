import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from models import (
    BRANCHES_SCHEMA, DAILY_CAPACITY_SCHEMA, TABLES_SCHEMA, RESERVATIONS_SCHEMA, CONTACTS_SCHEMA, 
    OPINIONS_SCHEMA, EVENTS_SCHEMA, PRODUCTS_SCHEMA, PRODUCTS_TRIGGER_SCHEMA
)

load_dotenv()

# Configuración de conexión a PostgreSQL
DB_HOST = os.getenv('DB_HOST', 'aws-1-us-east-1.pooler.supabase.com')
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres.kzdlspaneugbymuzsber')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Tronquitos2026')

def init_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode='require'
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

        # Table for Products (Menú dinámico)
        cursor.execute(PRODUCTS_SCHEMA)
        print("[v] Tabla 'products' creada/verificada")

        # Trigger para updated_at en products
        cursor.execute(PRODUCTS_TRIGGER_SCHEMA)
        print("[v] Trigger 'set_product_timestamp' creado/verificado")

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
        
        # Poblar productos del menú si no existen
        cursor.execute('SELECT COUNT(*) as count FROM products')
        count_result = cursor.fetchone()
        count = count_result['count'] if count_result else 0
        
        if count == 0:
            print("[*] Creando productos del menú...")
            
            productos = [
                # Entradas
                ('ENT-001', 'Empanadas (3 und)', 12000, 'Entradas', 'Empanadas de carne criolla, servidas con ají casero'),
                ('ENT-002', 'Patacones con Hogao', 10000, 'Entradas', 'Patacones crocantes con hogao fresco'),
                ('ENT-003', 'Arepa de Choclo con Queso', 8000, 'Entradas', 'Arepa dulce de maíz tierno con queso derretido'),
                ('ENT-004', 'Morcilla Santandereana', 9000, 'Entradas', 'Morcilla artesanal al carbón'),
                ('ENT-005', 'Chorizo Criollo', 10000, 'Entradas', 'Chorizo a la parrilla con arepa y limón'),
                # Sopas
                ('SOP-001', 'Ajiaco Bogotano', 22000, 'Sopas', 'Ajiaco con pollo, papa criolla, mazorca, alcaparras y crema'),
                ('SOP-002', 'Sancocho de Gallina', 24000, 'Sopas', 'Sancocho tradicional con gallina campesina y plátano'),
                ('SOP-003', 'Sopa de Mondongo', 20000, 'Sopas', 'Mondongo en caldo con verduras y especias'),
                ('SOP-004', 'Caldo de Costilla', 15000, 'Sopas', 'Caldo reconfortante con costilla de res y papa'),
                # Especialidad
                ('ESP-001', 'Carne a la Llanera', 38000, 'Especialidad', 'Carne de res asada lentamente al carbón, corte premium de la casa'),
                ('ESP-002', 'Costilla BBQ', 35000, 'Especialidad', 'Costilla de cerdo marinada en salsa BBQ ahumada'),
                ('ESP-003', 'Churrasco', 36000, 'Especialidad', 'Churrasco de res a la parrilla con chimichurri'),
                ('ESP-004', 'Ternera a la Plancha', 34000, 'Especialidad', 'Corte de ternera tierna a la plancha con especias'),
                ('ESP-005', 'Chigüiro Asado', 42000, 'Especialidad', 'Chigüiro llanero asado al carbón, plato insignia'),
                ('ESP-006', 'Lomo de Cerdo', 32000, 'Especialidad', 'Lomo de cerdo marinado al carbón con salsa de la casa'),
                ('ESP-007', 'Pechuga a la Parrilla', 28000, 'Especialidad', 'Pechuga de pollo jugosa a la parrilla con hierbas'),
                ('ESP-008', 'Chunchullo', 18000, 'Especialidad', 'Chunchullo crocante asado al carbón'),
                ('ESP-009', 'Picada Los Tronquitos', 85000, 'Especialidad', 'Picada mixta para compartir: carne, costilla, chorizo, morcilla, chunchullo y arepa'),
                # Pescados
                ('PES-001', 'Mojarra Frita', 32000, 'Pescados', 'Mojarra roja frita entera con patacones y ensalada'),
                ('PES-002', 'Bagre en Salsa', 30000, 'Pescados', 'Bagre del río en salsa criolla con arroz'),
                ('PES-003', 'Trucha a la Plancha', 28000, 'Pescados', 'Trucha arcoíris a la plancha con mantequilla de hierbas'),
                # Infantil
                ('INF-001', 'Mini Hamburguesa', 15000, 'Infantil', 'Hamburguesa pequeña con papas a la francesa'),
                ('INF-002', 'Nuggets de Pollo', 14000, 'Infantil', 'Nuggets de pollo con papas y salsa'),
                ('INF-003', 'Deditos de Queso', 12000, 'Infantil', 'Deditos de queso crujientes con salsa rosada'),
                # Adiciones
                ('ADI-001', 'Arroz Blanco', 4000, 'Adiciones', 'Porción de arroz blanco'),
                ('ADI-002', 'Papa Salada', 3000, 'Adiciones', 'Papa criolla o papa salada'),
                ('ADI-003', 'Ensalada de la Casa', 6000, 'Adiciones', 'Ensalada fresca con vinagreta'),
                ('ADI-004', 'Arepa Asada', 3000, 'Adiciones', 'Arepa boyacense asada al carbón'),
                ('ADI-005', 'Guacamole', 8000, 'Adiciones', 'Guacamole fresco con totopos'),
                ('ADI-006', 'Papas a la Francesa', 7000, 'Adiciones', 'Papas fritas crocantes'),
                ('ADI-007', 'Plátano Maduro', 5000, 'Adiciones', 'Plátano maduro frito en tajadas'),
                # Bebidas
                ('BEB-001', 'Cerveza Nacional', 7000, 'Bebidas', 'Águila, Póker o Club Colombia'),
                ('BEB-002', 'Cerveza Artesanal', 12000, 'Bebidas', 'Cerveza artesanal de la casa'),
                ('BEB-003', 'Michelada', 14000, 'Bebidas', 'Michelada con salsa especial'),
                ('BEB-004', 'Gaseosa', 5000, 'Bebidas', 'Coca-Cola, Sprite o Colombiana'),
                ('BEB-005', 'Agua', 4000, 'Bebidas', 'Agua natural o con gas'),
                # Bebidas Naturales
                ('NAT-001', 'Limonada Natural', 6000, 'Bebidas Naturales', 'Limonada recién exprimida'),
                ('NAT-002', 'Limonada de Coco', 8000, 'Bebidas Naturales', 'Limonada con crema de coco'),
                ('NAT-003', 'Jugo de Maracuyá', 7000, 'Bebidas Naturales', 'Jugo natural de maracuyá'),
                ('NAT-004', 'Jugo de Lulo', 7000, 'Bebidas Naturales', 'Jugo natural de lulo'),
                ('NAT-005', 'Jugo de Mango', 7000, 'Bebidas Naturales', 'Jugo natural de mango'),
                ('NAT-006', 'Agua de Panela con Limón', 5000, 'Bebidas Naturales', 'Bebida tradicional colombiana'),
            ]
            
            for sku, nombre, precio, categoria, descripcion in productos:
                cursor.execute('''
                    INSERT INTO products (sku, nombre, precio, categoria, descripcion, disponible)
                    VALUES (%s, %s, %s, %s, %s, TRUE)
                ''', (sku, nombre, precio, categoria, descripcion))
            
            conn.commit()
            print(f"[v] {len(productos)} productos creados en el menú")
        
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
