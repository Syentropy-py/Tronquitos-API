-- ============================================================
-- MIGRACIÓN: Tabla de Productos (Menú Dinámico)
-- Base de datos: PostgreSQL (Supabase)
-- Proyecto: Los Tronquitos
-- 
-- USO: Copiar y pegar en Supabase > SQL Editor > New Query > Run
-- ============================================================

-- 1. CREAR TABLA PRODUCTS
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
);

-- 2. TRIGGER PARA AUTO-ACTUALIZAR updated_at
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

-- 3. SEED DATA — 42 productos del menú
-- (Solo se insertan si la tabla está vacía)
INSERT INTO products (sku, nombre, precio, categoria, descripcion, disponible)
SELECT * FROM (VALUES
    -- ═══ ENTRADAS ═══
    ('ENT-001', 'Empanadas (3 und)', 12000, 'Entradas', 'Empanadas de carne criolla, servidas con ají casero', TRUE),
    ('ENT-002', 'Patacones con Hogao', 10000, 'Entradas', 'Patacones crocantes con hogao fresco', TRUE),
    ('ENT-003', 'Arepa de Choclo con Queso', 8000, 'Entradas', 'Arepa dulce de maíz tierno con queso derretido', TRUE),
    ('ENT-004', 'Morcilla Santandereana', 9000, 'Entradas', 'Morcilla artesanal al carbón', TRUE),
    ('ENT-005', 'Chorizo Criollo', 10000, 'Entradas', 'Chorizo a la parrilla con arepa y limón', TRUE),

    -- ═══ SOPAS ═══
    ('SOP-001', 'Ajiaco Bogotano', 22000, 'Sopas', 'Ajiaco con pollo, papa criolla, mazorca, alcaparras y crema', TRUE),
    ('SOP-002', 'Sancocho de Gallina', 24000, 'Sopas', 'Sancocho tradicional con gallina campesina y plátano', TRUE),
    ('SOP-003', 'Sopa de Mondongo', 20000, 'Sopas', 'Mondongo en caldo con verduras y especias', TRUE),
    ('SOP-004', 'Caldo de Costilla', 15000, 'Sopas', 'Caldo reconfortante con costilla de res y papa', TRUE),

    -- ═══ ESPECIALIDAD ═══
    ('ESP-001', 'Carne a la Llanera', 38000, 'Especialidad', 'Carne de res asada lentamente al carbón, corte premium de la casa', TRUE),
    ('ESP-002', 'Costilla BBQ', 35000, 'Especialidad', 'Costilla de cerdo marinada en salsa BBQ ahumada', TRUE),
    ('ESP-003', 'Churrasco', 36000, 'Especialidad', 'Churrasco de res a la parrilla con chimichurri', TRUE),
    ('ESP-004', 'Ternera a la Plancha', 34000, 'Especialidad', 'Corte de ternera tierna a la plancha con especias', TRUE),
    ('ESP-005', 'Chigüiro Asado', 42000, 'Especialidad', 'Chigüiro llanero asado al carbón, plato insignia', TRUE),
    ('ESP-006', 'Lomo de Cerdo', 32000, 'Especialidad', 'Lomo de cerdo marinado al carbón con salsa de la casa', TRUE),
    ('ESP-007', 'Pechuga a la Parrilla', 28000, 'Especialidad', 'Pechuga de pollo jugosa a la parrilla con hierbas', TRUE),
    ('ESP-008', 'Chunchullo', 18000, 'Especialidad', 'Chunchullo crocante asado al carbón', TRUE),
    ('ESP-009', 'Picada Los Tronquitos', 85000, 'Especialidad', 'Picada mixta para compartir: carne, costilla, chorizo, morcilla, chunchullo y arepa', TRUE),

    -- ═══ PESCADOS ═══
    ('PES-001', 'Mojarra Frita', 32000, 'Pescados', 'Mojarra roja frita entera con patacones y ensalada', TRUE),
    ('PES-002', 'Bagre en Salsa', 30000, 'Pescados', 'Bagre del río en salsa criolla con arroz', TRUE),
    ('PES-003', 'Trucha a la Plancha', 28000, 'Pescados', 'Trucha arcoíris a la plancha con mantequilla de hierbas', TRUE),

    -- ═══ INFANTIL ═══
    ('INF-001', 'Mini Hamburguesa', 15000, 'Infantil', 'Hamburguesa pequeña con papas a la francesa', TRUE),
    ('INF-002', 'Nuggets de Pollo', 14000, 'Infantil', 'Nuggets de pollo con papas y salsa', TRUE),
    ('INF-003', 'Deditos de Queso', 12000, 'Infantil', 'Deditos de queso crujientes con salsa rosada', TRUE),

    -- ═══ ADICIONES ═══
    ('ADI-001', 'Arroz Blanco', 4000, 'Adiciones', 'Porción de arroz blanco', TRUE),
    ('ADI-002', 'Papa Salada', 3000, 'Adiciones', 'Papa criolla o papa salada', TRUE),
    ('ADI-003', 'Ensalada de la Casa', 6000, 'Adiciones', 'Ensalada fresca con vinagreta', TRUE),
    ('ADI-004', 'Arepa Asada', 3000, 'Adiciones', 'Arepa boyacense asada al carbón', TRUE),
    ('ADI-005', 'Guacamole', 8000, 'Adiciones', 'Guacamole fresco con totopos', TRUE),
    ('ADI-006', 'Papas a la Francesa', 7000, 'Adiciones', 'Papas fritas crocantes', TRUE),
    ('ADI-007', 'Plátano Maduro', 5000, 'Adiciones', 'Plátano maduro frito en tajadas', TRUE),

    -- ═══ BEBIDAS ═══
    ('BEB-001', 'Cerveza Nacional', 7000, 'Bebidas', 'Águila, Póker o Club Colombia', TRUE),
    ('BEB-002', 'Cerveza Artesanal', 12000, 'Bebidas', 'Cerveza artesanal de la casa', TRUE),
    ('BEB-003', 'Michelada', 14000, 'Bebidas', 'Michelada con salsa especial', TRUE),
    ('BEB-004', 'Gaseosa', 5000, 'Bebidas', 'Coca-Cola, Sprite o Colombiana', TRUE),
    ('BEB-005', 'Agua', 4000, 'Bebidas', 'Agua natural o con gas', TRUE),

    -- ═══ BEBIDAS NATURALES ═══
    ('NAT-001', 'Limonada Natural', 6000, 'Bebidas Naturales', 'Limonada recién exprimida', TRUE),
    ('NAT-002', 'Limonada de Coco', 8000, 'Bebidas Naturales', 'Limonada con crema de coco', TRUE),
    ('NAT-003', 'Jugo de Maracuyá', 7000, 'Bebidas Naturales', 'Jugo natural de maracuyá', TRUE),
    ('NAT-004', 'Jugo de Lulo', 7000, 'Bebidas Naturales', 'Jugo natural de lulo', TRUE),
    ('NAT-005', 'Jugo de Mango', 7000, 'Bebidas Naturales', 'Jugo natural de mango', TRUE),
    ('NAT-006', 'Agua de Panela con Limón', 5000, 'Bebidas Naturales', 'Bebida tradicional colombiana', TRUE)
) AS v(sku, nombre, precio, categoria, descripcion, disponible)
WHERE NOT EXISTS (SELECT 1 FROM products LIMIT 1);

-- 4. VERIFICAR
SELECT categoria, COUNT(*) as total FROM products GROUP BY categoria ORDER BY categoria;
