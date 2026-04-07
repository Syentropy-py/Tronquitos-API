# 🍽️ LOS TRONQUITOS - Sistema de Gestión de Reservas

**Sistema inteligente de gestión de reservas multi-sede con notificaciones automáticas vía WhatsApp + N8N.**
Desplegado en arquitectura Serverless usando **Vercel** y **Supabase** (PostgreSQL).

---

## ⚡ INICIO RÁPIDO (5 minutos)

### Requisitos Previos (Desarrollo Local)
- **Python** 3.8+
- **pip**
- **Vercel CLI** (Opcional para pruebas locales: `npm i -g vercel`)
- **Base de datos PostgreSQL** (o conexión a Supabase)

### Instalación Rápida

```bash
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env asegurándote de incluir el DB_HOST de Supabase y credenciales PostgreSQL

# 3. Inicializar base de datos PostgreSQL
python backend/init_db.py

# 4. (Opcional) Cargar datos iniciales de sedes
python backend/setup_system.py

# 5. Iniciar servidor localmente (Flask tradicional)
python backend/app.py
```

---

## 📖 DOCUMENTACIÓN

### Endpoints Principales

Todos los llamados a la API del cliente web pasan por `/api/*` y Vercel se encarga de enviarlos a la instancia de Python en la nube.

```
POST   /api/reservation           - Crear nueva reserva
GET    /api/availability          - Consultar disponibilidad
POST   /api/cancel-reservation    - Cancelar una reserva
GET    /api/tables                - Listar todas las mesas
GET    /api/schedule              - Obtener horarios y slots
POST   /api/contacts              - Enviar mensaje de contacto
GET    /api/opinions              - Obtener opiniones/reseñas
```

---

## 🎯 FUNCIONALIDADES PRINCIPALES

✅ **Gestión Multi-Sede**
- 6 sedes independientes: Principal, Terraza, Restrepo, Nieves, 7ma con 22, Av Rojas.
- Control de horarios y capacidad por sede.

✅ **Sistema de Mesas Inteligente**
- Disponibilidad en tiempo real para evitar Overbooking.
- Asignación automática o manual desde el módulo Gestor.

✅ **Notificaciones (Integración N8N)**
- Webhook integrado para disparar flujos en N8N.
- Mensajes automáticos y de seguimiento vía WhatsApp (Cita, Cancelación, Bienvenida).

✅ **Frontend + Backend Serverless**
- Frontend desplegado gratis vía Vercel CDN (Red de contenidos ultrarrápida).
- Backend de Python operando al instante mediante Vercel Serverless Functions (`api/index.py`).

---

## 📁 ESTRUCTURA DEL PROYECTO ACTUAL

```
TRONQUITOS/
│
├── 📗 README.md                    # Etse archivo
├── 📋 requirements.txt             # Dependencias estrictas del servidor Python en Vercel
├── ⚙️ vercel.json                  # Configuración oficial de Serverless y Mapeos
│
├── api/                            # 🎯 ENTRADA DEL SERVIDOR SERVERLESS (VERCEL)
│   └── index.py                    # Puente encargado de instanciar Flask para Vercel
│
├── backend/                        # 🧠 LÓGICA CORE DE PYTHON CLÁSICA
│   ├── app.py                      # Rutas (Endpoints) de API y lógica de App
│   ├── database.py                 # Conexión remota a PostgreSQL (Supabase)
│   ├── models.py                   # Esquemas SQL de tablas
│   ├── reservation_service.py      # Lógica de asignación y cruces de reservas
│   ├── init_db.py                  # Setup de esquema inicial DB
│   └── .env                        # Variables transitorias de desarrollo (NO versionar)
│
├── frontend/                       # 🎨 UI (INTERFAZ DE USUARIO ESTATICAMENTE DESPLEGADA)
│   ├── index.html                  # Cliente Clientes
│   ├── gestor.html                 # Cliente Administradores ⚠️ (Oculto)
│   ├── galeria.html                # Galería promocional
│   ├── nosotros.html               # About 
│   ├── styles.css                  # Hoja de vida gráfica (Aesthetics)
│   ├── scripts.js                  # Peticiones Fetch a URLs Relativas /api/*
│   ├── sedes-config.js             # Info de sedes JS paramétrica
│   └── assets/                     # Imágenes y catálogos PDF HD (+200mb CDN)
```

---

## ⚙️ CONFIGURACIÓN VERCEL (PRODUCCIÓN)

En la plataforma web de Vercel, en la sección de **Settings > Environment Variables**, es **OBLIGATORIO** cargar las siguientes claves secretas para que el backend reconozca al Gestor de PostgreSQL (Supabase) y el motor de flujos (N8N):

```env
# Conexión Base de Datos Supabase (PostgreSQL)
DB_HOST=aws-0-....pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.xxxxxxxxxx
DB_PASSWORD=tu_contraseña

# Notificaciones y Motores
EMAIL_ADDRESS=tu_correo@gmail.com
EMAIL_PASSWORD=tu_app_password
N8N_WEBHOOK_URL=https://tu-instancia-n8n.com/webhook/123
WHATSAPP_NUMBER=573000000000
```

---

## 🚀 DESPLIEGUE A PRODUCCIÓN

El sistema está configurado de manera especial para aprovechar la arquitectura "Zero Config / Builds" de **Vercel** usando Serverless Functions.

1. **Haz cualquier iteración en local.**
2. Realiza el guardado: `git add .` seguido de `git commit -m "Descripción"`.
3. Empuja los cambios `git push origin main`.
4. Vercel detectará el archivo de compilación **vercel.json** y levantará instántaneamente su respectivo *pipeline*: 
   - Aislará la carpeta `/frontend` y la servirá mediante Fast CDN global.
   - Creará un entorno micro-python leyendo `requirements.txt` exclusivamente para la carpeta lógica e ignorará las imágenes para no romper el límite de peso (250MB Limit Lambda Fix).
   - Proyectará los EndPoints bajo `/api/(.*)`.

Para consultar el panel de control administrativo ir a:
`https://url-app-vercel.com/gestor.html`

---

**Última actualización:** Abril 2026  
**Estado:** Producción Total Web (Vercel Serverless + Supabase PostgreSQL)
**Versión:** 3.0 (Cloud-First)

---

## ⚒️ HECHO POR:

**Nicolás Martínez Pineda (Syentropy's CEO & Head)**
