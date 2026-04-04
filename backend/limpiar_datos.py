import os
import sys
import psycopg2
from dotenv import load_dotenv

def clean_data(remove_db=False):
    base_dir = os.path.dirname(__file__)
    load_dotenv(os.path.join(base_dir, '.env'))
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_NAME = os.getenv('DB_NAME', 'tronquitos')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    conn_kwargs = {
        'host': DB_HOST,
        'port': DB_PORT,
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD
    }

    try:
        conn = psycopg2.connect(**conn_kwargs)
        conn.autocommit = True
        cursor = conn.cursor()
        
        if remove_db:
            # Eliminar la BD requeriría saltar a la db postgres, la forma fácil
            # es hacer DROP a las tablas
            tables = ['events', 'reservations', 'daily_capacity', 'tables', 'branches', 'contacts', 'opinions']
            for t in tables:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {t} CASCADE")
                except Exception as e:
                    pass
            print("[\u2713] Tablas eliminadas completamente. Deberás correr init_db.py de nuevo.")
        else:
            # Solo vaciar los datos transaccionales, dejando intactos tables y branches
            # Para vaciar todo TRUNCATE
            try:
                cursor.execute("TRUNCATE TABLE events, reservations, daily_capacity, contacts, opinions RESTART IDENTITY CASCADE")
                # Resetear el estado de las mesas a 'free'
                cursor.execute("UPDATE tables SET status = 'free'")
                print("[\u2713] Base de datos PostgreSQL limpiada con éxito (transacciones borradas).")
            except Exception as e:
                print(f"[!] Error al truncar datos: {e}")
                
        conn.close()
    except Exception as e:
        print(f"[!] Error conectando a PostgreSQL para limpieza: {e}")

    # 2. Clean CSVs
    csv_files = ['reservations.csv', 'contacts.csv']
    for file in csv_files:
        csv_path = os.path.join(base_dir, file)
        if os.path.exists(csv_path):
            try:
                os.remove(csv_path)
                print(f"[\u2713] Archivo {file} eliminado con éxito.")
            except Exception as e:
                print(f"[!] Error eliminando {file}: {e}")
        else:
            print(f"[-] Ignorado: {file} no existe aún.")
            
    print("\n¡Limpieza Completa! Todos los datos de prueba han sido eliminados.")

if __name__ == '__main__':
    # Aceptar parámetro --remove-db para eliminar completamente las tablas
    remove_db = '--remove-db' in sys.argv
    clean_data(remove_db=remove_db)
