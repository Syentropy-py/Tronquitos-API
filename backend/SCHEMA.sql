-- SQL Schema para Los Tronquitos Restaurant Management System
-- Base de datos SQLite

-- ============================================================
-- 1. TABLA DE MESAS
-- ============================================================
CREATE TABLE IF NOT EXISTS tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER UNIQUE NOT NULL,
    capacity INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'free',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('free', 'reserved', 'occupied'))
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_tables_status ON tables(status);
CREATE INDEX idx_tables_capacity ON tables(capacity);

-- ============================================================
-- 2. TABLA DE RESERVAS (MEJORADA)
-- ============================================================
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT,
    personas INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    mensaje TEXT,
    table_id INTEGER,
    status TEXT NOT NULL DEFAULT 'confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reservation_time DATETIME,
    FOREIGN KEY (table_id) REFERENCES tables(id),
    CHECK (status IN ('confirmed', 'cancelled', 'completed', 'no_show'))
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_reservations_date ON reservations(fecha);
CREATE INDEX idx_reservations_status ON reservations(status);
CREATE INDEX idx_reservations_table ON reservations(table_id);

-- ============================================================
-- 3. TABLA DE CONTACTOS
-- ============================================================
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT,
    mensaje TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_contacts_email ON contacts(email);

-- ============================================================
-- 4. TABLA DE OPINIONES
-- ============================================================
CREATE TABLE IF NOT EXISTS opinions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor TEXT NOT NULL,
    rating INTEGER NOT NULL,
    comentario TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (rating >= 1 AND rating <= 5)
);

-- Índices
CREATE INDEX idx_opinions_rating ON opinions(rating);

-- ============================================================
-- 5. TABLA DE EVENTOS (AUDITORÍA)
-- ============================================================
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    reservation_id INTEGER,
    table_id INTEGER,
    description TEXT,
    n8n_sent BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id),
    FOREIGN KEY (table_id) REFERENCES tables(id)
);

-- Índices
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_created ON events(created_at);
CREATE INDEX idx_events_reservation ON events(reservation_id);

-- ============================================================
-- DATOS DE EJEMPLO - MESAS
-- ============================================================

-- Insertar mesas por defecto
INSERT INTO tables (table_number, capacity) VALUES
    (1, 2),   -- Mesa pequeña para 2 personas
    (2, 2),   -- Mesa pequeña para 2 personas
    (3, 4),   -- Mesa mediana para 4 personas
    (4, 4),   -- Mesa mediana para 4 personas
    (5, 4),   -- Mesa mediana para 4 personas
    (6, 6),   -- Mesa grande para 6 personas
    (7, 6),   -- Mesa grande para 6 personas
    (8, 8),   -- Mesa muy grande para 8 personas
    (9, 8),   -- Mesa muy grande para 8 personas
    (10, 10); -- Mesa de grupo para 10 personas

-- ============================================================
-- DATOS DE EJEMPLO - RESERVAS
-- ============================================================

-- Reserva futura confirmada
INSERT INTO reservations (nombre, telefono, email, personas, fecha, hora, table_id, status, mensaje)
VALUES (
    'Juan Pérez García',
    '+573001234567',
    'juan@example.com',
    4,
    date('2026-03-20'),
    '20:00',
    3,
    'confirmed',
    'Sin gluten, vegetariano uno de los comensales'
);

-- Reserva futura confirmada
INSERT INTO reservations (nombre, telefono, email, personas, fecha, hora, table_id, status)
VALUES (
    'María García López',
    '+573009876543',
    'maria@example.com',
    2,
    date('2026-03-20'),
    '19:30',
    1,
    'confirmed'
);

-- Reserva cancelada
INSERT INTO reservations (nombre, telefono, email, personas, fecha, hora, table_id, status, mensaje)
VALUES (
    'Carlos Rodríguez',
    '+573015551234',
    'carlos@example.com',
    6,
    date('2026-03-18'),
    '21:00',
    6,
    'cancelled',
    'Fue cancelada por el cliente'
);

-- ============================================================
-- DATOS DE EJEMPLO - CONTACTOS
-- ============================================================

INSERT INTO contacts (nombre, telefono, email, mensaje)
VALUES (
    'Pedro Martínez',
    '+573021112222',
    'pedro@example.com',
    '¿Tienen opciones sin lactosa?'
);

-- ============================================================
-- DATOS DE EJEMPLO - OPINIONES
-- ============================================================

INSERT INTO opinions (autor, rating, comentario)
VALUES (
    'Juan Pérez',
    5,
    'Excelente comida y muy buen servicio. Volveré pronto.'
);

INSERT INTO opinions (autor, rating, comentario)
VALUES (
    'María López',
    4,
    'Muy buena experiencia, el ambiente es perfecto.'
);

-- ============================================================
-- DATOS DE EJEMPLO - EVENTOS
-- ============================================================

INSERT INTO events (event_type, reservation_id, table_id, description, n8n_sent)
VALUES (
    'reservation',
    1,
    3,
    'Reserva creada para 4 personas',
    1
);

INSERT INTO events (event_type, reservation_id, table_id, description, n8n_sent)
VALUES (
    'table_freed',
    1,
    3,
    'Mesa 3 liberada después de la comida',
    0
);

INSERT INTO events (event_type, reservation_id, table_id, description, n8n_sent)
VALUES (
    'cancellation',
    3,
    6,
    'Reserva cancelada por el cliente',
    1
);

-- ============================================================
-- QUERIES ÚTILES PARA ANÁLISIS
-- ============================================================

-- Ver todas las reservas confirmadas para una fecha
-- SELECT r.*, t.table_number 
-- FROM reservations r
-- LEFT JOIN tables t ON r.table_id = t.id
-- WHERE r.fecha = '2026-03-20' AND r.status = 'confirmed'
-- ORDER BY r.hora;

-- Ver disponibilidad en tiempo real
-- SELECT 
--     t.table_number,
--     t.capacity,
--     t.status,
--     COUNT(r.id) as reservations_today
-- FROM tables t
-- LEFT JOIN reservations r ON t.id = r.table_id AND r.fecha = date('now')
-- GROUP BY t.id
-- ORDER BY t.table_number;

-- Ver estadísticas de ocupación
-- SELECT 
--     COUNT(CASE WHEN status = 'free' THEN 1 END) as mesas_libres,
--     COUNT(CASE WHEN status = 'reserved' THEN 1 END) as mesas_reservadas,
--     COUNT(CASE WHEN status = 'occupied' THEN 1 END) as mesas_ocupadas
-- FROM tables;

-- Ver eventos en las últimas 24 horas
-- SELECT * FROM events
-- WHERE created_at >= datetime('now', '-1 day')
-- ORDER BY created_at DESC;

-- Ver reservas sin asignar de mesa (si las hay)
-- SELECT * FROM reservations
-- WHERE table_id IS NULL AND status = 'confirmed'
-- ORDER BY reservation_time DESC;
