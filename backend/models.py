"""
Modelos de Base de Datos para Sistema de Gestión de Reservas
Define las tablas y esquemas para mesas y reservas (PostgreSQL)
"""

# Esquema SQL para tabla de branches/sedes
BRANCHES_SCHEMA = '''
CREATE TABLE IF NOT EXISTS branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    location VARCHAR(255),
    phone VARCHAR(20),
    open_time VARCHAR(5) DEFAULT '11:30',
    close_time VARCHAR(5) DEFAULT '18:00',
    default_capacity INTEGER DEFAULT 80,
    active SMALLINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
'''

# Esquema SQL para tabla de capacidad diaria
DAILY_CAPACITY_SCHEMA = '''
CREATE TABLE IF NOT EXISTS daily_capacity (
    id SERIAL PRIMARY KEY,
    branch_id INTEGER NOT NULL,
    date DATE NOT NULL,
    capacity_limit INTEGER NOT NULL,
    blocked SMALLINT DEFAULT 0,
    note VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES branches(id),
    UNIQUE(branch_id, date)
)
'''

# Esquema SQL para tabla de mesas (con columna sede)
TABLES_SCHEMA = '''
CREATE TABLE IF NOT EXISTS tables (
    id SERIAL PRIMARY KEY,
    table_number INTEGER NOT NULL,
    sede VARCHAR(255) NOT NULL DEFAULT 'Centro',
    capacity INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'free' CHECK (status IN ('free', 'reserved', 'occupied')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(table_number, sede)
)
'''

# Esquema SQL para tabla de reservas mejorada (con columna sede y groups especiales)
RESERVATIONS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS reservations (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    personas INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    sede VARCHAR(255) NOT NULL DEFAULT 'Centro',
    mensaje TEXT,
    table_id INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'cancelled', 'completed', 'no_show')),
    is_special_group SMALLINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reservation_time TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES tables(id)
)
'''

# Esquema SQL para tabla de contactos
CONTACTS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    mensaje TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
'''

# Esquema SQL para tabla de opiniones
OPINIONS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS opinions (
    id SERIAL PRIMARY KEY,
    autor VARCHAR(255) NOT NULL,
    rating INTEGER NOT NULL,
    comentario TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
'''

# Esquema SQL para tabla de eventos (para auditoría)
EVENTS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    reservation_id INTEGER,
    table_id INTEGER,
    description TEXT,
    n8n_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id),
    FOREIGN KEY (table_id) REFERENCES tables(id)
)
'''

# Esquema SQL para tabla de productos (menú dinámico)
PRODUCTS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    precio INTEGER NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen_url TEXT,
    disponible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
'''

# Trigger para actualizar updated_at automáticamente en products
PRODUCTS_TRIGGER_SCHEMA = '''
CREATE OR REPLACE FUNCTION update_product_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'set_product_timestamp'
    ) THEN
        CREATE TRIGGER set_product_timestamp
        BEFORE UPDATE ON products
        FOR EACH ROW
        EXECUTE FUNCTION update_product_timestamp();
    END IF;
END;
$$;
'''

# Constantes para estados
class TableStatus:
    FREE = 'free'
    RESERVED = 'reserved'
    OCCUPIED = 'occupied'

class ReservationStatus:
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    NO_SHOW = 'no_show'

class EventType:
    RESERVATION_CREATED = 'reservation'
    RESERVATION_CANCELLED = 'cancellation'
    TABLE_FREED = 'table_freed'
    NO_SHOW = 'no_show'
