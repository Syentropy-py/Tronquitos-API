# 🍽️ LOS TRONQUITOS - Sistema de Gestión de Reservas

**Sistema inteligente de gestión de reservas multi-sede con notificaciones automáticas vía WhatsApp + N8N**

---

## ⚡ INICIO RÁPIDO (5 minutos)

### Requisitos Previos
- **Python** 3.8+
- **pip**
- **PostgreSQL** 12+ ejecutándose localmente
- **Base de datos PostgreSQL** llamada `tronquitos`

### Instalación Rápida

```bash
# 1. Instalar dependencias Python
pip install -r backend/requirements.txt

# 2. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con credenciales PostgreSQL

# 3. Inicializar base de datos PostgreSQL
python backend/init_db.py

# 4. (Opcional) Cargar datos iniciales de sedes
python backend/setup_system.py

# 5. Iniciar servidor
python backend/app.py
```

### Verificación de Funcionamiento

```bash
# En otra terminal, listar todas las mesas:
curl http://localhost:5000/api/tables

# Ver disponibilidad para una fecha específica:
curl "http://localhost:5000/api/availability?fecha=2026-04-15&sede=Principal"
```

---

## 📖 DOCUMENTACIÓN

| Documento | Para | Ubicación |
|-----------|------|-----------|
| [DEPLOYMENT.md](backend/DEPLOYMENT.md) | Desplegar en producción | `backend/` |
| [SCHEMA.md](docs/) | Schema de BD PostgreSQL | `docs/` |
| Código inline | Endpoints y lógica | `backend/app.py` |

### Endpoints Principales

```
POST   /api/reservation           - Crear nueva reserva
GET    /api/availability          - Consultar disponibilidad
POST   /api/cancel-reservation    - Cancelar una reserva
GET    /api/tables                - Listar todas las mesas
GET    /api/schedule              - Obtener horarios y slots
POST   /api/contacts              - Enviar mensaje de contacto
GET    /api/opinions              - Obtener opiniones/reseñas
```

**Documentación detallada:** Ver `app.py` en sección de rutas (routes).

---

## 🎯 FUNCIONALIDADES PRINCIPALES

✅ **Gestión Multi-Sede**
- 6 sedes independientes: Principal, Terraza, Restrepo, Nieves, 7ma con 22, Av Rojas
- Control de horarios y capacidad por sede
- Capacidad diaria personalizable

✅ **Sistema de Mesas Inteligente**
- Disponibilidad en tiempo real
- Asignación automática de mesas por capacidad
- Estados: libre, reservada, ocupada
- Control preventivo de overbooking

✅ **Gestión de Reservas**
- Creación y validación de reservas
- Soporte para grupos especiales (>30 personas)
- Historial completo de transacciones
- Estados: confirmada, cancelada, completada, no-show

✅ **Notificaciones (Integración N8N)**
- Webhook integrado para N8N
- Envío automático de datos de reservas/cancelaciones
- Notificaciones por WhatsApp (configurable en N8N)
- Información de cliente y detalles de reserva

✅ **Contacto y Opiniones**
- Formulario de contacto con notificación SMTP
- Sistema de opiniones/reseñas
- Envío a Gmail vía SMTP

---

## 🔧 VERIFICACIÓN PRE-PRODUCTIVO

```bash
# Script de verificación del sistema
python VERIFICAR_SISTEMA.py
```

Este verificará:
- ✓ Estructura de archivos críticos
- ✓ Dependencias Python instaladas
- ✓ Conexión a PostgreSQL
- ✓ Tablas de BD creadas
- ✓ Variables de entorno configuradas

---

## 📁 ESTRUCTURA DEL PROYECTO

```
TRONQUITOS/
│
├── 📗 README.md                    # Este archivo
├── 📋 requirements.txt             # Dependencias Python
├── 📄 LICENSE                      # Licencia del proyecto
│
├── 🔧 SCRIPTS DE UTILIDAD (Desarrollo/Admin)
│   ├── VERIFICAR_SISTEMA.py        # Verifica que todo funcione correctamente
│   ├── setup_system.py             # Configura sistema con 6 sedes
│   ├── limpiar_datos.py            # Limpia datos transaccionales o BD completa
│   ├── check_db.py                 # Verifica existencia de BD PostgreSQL
│   └── INICIAR_DEMO.bat            # Script Windows para iniciar demo
│
├── backend/                        # 🎯 CÓDIGO PRINCIPAL DE LA API
│   ├── app.py                      # ⭐ Aplicación Flask (endpoints)
│   ├── database.py                 # Conexión y operaciones CRUD en PostgreSQL
│   ├── models.py                   # Esquemas SQL de tablas
│   ├── reservation_service.py      # Lógica de negocio de reservas
│   ├── init_db.py                  # Inicializa tablas en PostgreSQL (ejecutar 1 vez)
│   │
│   ├── .env                        # Variables de entorno (NO versionar)
│   ├── DEPLOYMENT.md               # Guía de despliegue a producción
│   └── SCHEMA.sql                  # [OBSOLETO] Schema SQLite (solo referencia)
│
├── frontend/                       # 🎨 INTERFAZ WEB
│   ├── index.html                  # Página principal
│   ├── gestor.html                 # Panel de gestión de reservas
│   ├── galeria.html                # Galería de imágenes
│   ├── nosotros.html               # Información de la empresa
│   ├── styles.css                  # Estilos CSS
│   ├── scripts.js                  # Lógica frontend
│   ├── sedes-config.js             # Configuración de 6 sedes
│   └── assets/
│       ├── images/                 # Imágenes del sitio
│       └── src/                    # Recursos estáticos
│
└── docs/                           # 📚 Documentación
    └── slides/                     # Presentaciones/diapositivas
```

### Archivos Críticos para la API

| Archivo | Propósito | Debe editarse |
|---------|-----------|----------------|
| `app.py` | Endpoints y lógica principal | Sí (agregar/cambiar endpoints) |
| `database.py` | CRUD y conexión PostgreSQL | Solo si cambias la BD |
| `models.py` | Esquemas SQL | Solo si cambias las tablas |
| `reservation_service.py` | Lógica de negocio | Sí (mejorar validaciones) |
| `init_db.py` | Inicialización | No (ejecutar 1 sola vez) |

---

## ⚙️ CONFIGURACIÓN (Variables de Entorno)

Crear archivo `backend/.env`:

```env
# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tronquitos
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aquí

# SMTP para correos
EMAIL_ADDRESS=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_app

# N8N Webhook para WhatsApp
N8N_WEBHOOK_URL=https://tu-instancia-n8n.com/webhook-test/tu-id
WHATSAPP_NUMBER=573127923219
```

---

## 📊 BASES DE DATOS

### PostgreSQL (Actual - Producción)
- **Host:** localhost
- **Puerto:** 5432
- **Usuario:** postgres
- **Base de datos:** tronquitos

**Tablas:**
- `branches` - Sedes del restaurante
- `tables` - Mesas disponibles
- `reservations` - Historial de reservas
- `daily_capacity` - Capacidad por día y sede
- `events` - Auditoría de cambios
- `contacts` - Mensajes de contacto
- `opinions` - Reseñas y opiniones

### Crear/Resetear Base de Datos

```bash
# Inicializar BD (crear tablas)
python backend/init_db.py

# Limpiar datos transaccionales (mantener estructura)
python backend/limpiar_datos.py

# Limpiar completamente incluyendo tablas
python backend/limpiar_datos.py --remove-db
python backend/init_db.py
```

---

## 🚀 DESPLIEGUE A PRODUCCIÓN

Ver [DEPLOYMENT.md](backend/DEPLOYMENT.md) para instrucciones completas.

**Resumen:**
1. Usar **Gunicorn** en lugar de Flask dev server
2. Configurar **Nginx** como proxy reverso
3. SSL/HTTPS obligatorio
4. Variables de entorno en servidor
5. Backups automáticos de PostgreSQL

---

## 🔍 TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: No module named 'psycopg2'` | `pip install -r backend/requirements.txt` |
| `Connection refused (PostgreSQL)` | Verifica que PostgreSQL esté corriendo: `pg_isready` |
| `Database 'tronquitos' does not exist` | Ejecuta: `python backend/check_db.py` |
| Frontend no carga estilos | Reinicia servidor Flask |
| N8N no recibe datos | Verifica URL del webhook en `.env` |

---

## 📝 NOTAS PARA EL EQUIPO

- El proyecto pasó de **SQLite a PostgreSQL**, algunos archivos antiguos (SCHEMA.sql) son obsoletos
- Siempre usar **variables de entorno** para credenciales (**NO** en el código)
- Los endpoints están documentados en **docstrings** de `app.py`
- Para cambios de esquema: modificar `models.py` + ejecutar `init_db.py` en BD limpia

---

**Última actualización:** Abril 2026  
**Estado:** Producción (PostgreSQL)  
**Versión:** 2.0 (Multi-sede + N8N)
