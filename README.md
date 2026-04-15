# 🍽️ LOS TRONQUITOS - Sistema de Gestión de Reservas

**Plataforma inteligente y escalable para la automatización de reservas gastronómicas.**
Desplegado con arquitectura Serverless en **Vercel** y persistencia en **Supabase** (PostgreSQL).

---

## 🌟 Visión General

**Los Tronquitos** es un ecosistema digital diseñado para modernizar la operación de restaurantes con múltiples sedes. No es solo un formulario de reservas; es una arquitectura de datos que integra:

*   **Motor de Disponibilidad**: Control en tiempo real para evitar overbooking.
*   **Omnicanalidad**: Notificaciones automáticas vía **WhatsApp** y **Email**.
*   **Gestión Centralizada**: Dashboard administrativo para control total de mesas y sedes.
*   **Escalabilidad Cloud**: Operación 100% sobre tecnología Serverless (Cloud-First).

---

## ⚡ Inicio Rápido

### Requisitos Previos
*   **Python 3.10+**
*   **PostgreSQL** (Local o instancia en Supabase)
*   **Vercel CLI** (Opcional: `npm i -g vercel`)

### Instalación en 3 Pasos

```bash
# 1. Preparar el entorno
pip install -r requirements.txt

# 2. Configuración
# Crea un archivo .env basado en la sección "Variables de Entorno" de este README

# 3. Lanzamiento (Local)
python backend/app.py
```

---

## 📁 Arquitectura del Sistema

```text
TRONQUITOS/
├── 📗 README.md              # Documentación Maestra
├── 📋 requirements.txt       # Dependencias del servidor
├── ⚙️ vercel.json            # Orquestación Serverless
│
├── api/                      # 🎯 Gateway Vercel
│   └── index.py              # Puente de entrada a Python lambda
│
├── backend/                  # 🧠 Lógica Core
│   ├── app.py                # RESTful API Endpoints
│   ├── database.py           # Capa de Persistencia (PostgreSQL)
│   ├── models.py             # Definiciones de Entidades
│   ├── reservation_service.py# Lógica de negocio (Asignación de mesas)
│   └── init_db.py            # Script de inicialización
│
└── frontend/                 # 🎨 Capa de Presentación
    ├── index.html            # Reservas (Cliente)
    ├── gestor.html           # Dashboard (Admin)
    ├── styles.css            # Diseño Premium / Responsive
    └── scripts.js            # Lógica de Interfaz y API Fetching
```

---

## 🔌 API Reference

### Reservas y Disponibilidad
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/reservation` | Crear reserva (Valida capacidad y asigna mesa) |
| `GET` | `/api/availability` | Consulta cupos libres por fecha/sede |
| `GET` | `/api/calendar` | Resumen mensual de capacidad |
| `POST` | `/api/cancel-reservation` | Cancelación lógica de reserva |
| `POST` | `/api/delete-reservation` | Eliminación física (Admin) |

### Administración y Sedes
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/branches` | Listado dinámico de sedes activas |
| `GET` | `/api/schedule` | Horarios y slots disponibles (30 min) |
| `POST` | `/api/capacity` | Sobrescribir capacidad para un día específico |
| `POST` | `/api/block-day` | Bloqueo estratégico de días (Festivos/Eventos) |
| `GET` | `/api/tables` | Estado actual de todas las mesas |
| `POST` | `/api/free-table` | Liberar mesa manualmente |

### Auditoría y Comunicación
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/events` | Histórico de acciones y logs del sistema |
| `POST` | `/api/contacts` | Recepción de mensajes de contacto |

---

## 🔐 Variables de Entorno

Para una operación exitosa en Vercel, configurar las siguientes variables:

> [!TIP]
> Use contraseñas de aplicación para Gmail para evitar bloqueos por seguridad.

```env
# Database (Supabase / PostgreSQL)
DB_HOST=aws-0-xxxx.pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.xxxx
DB_PASSWORD=xxxxxxxx

# Email (SMTP)
SMTP_EMAIL=tu.correo@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx

# Notificaciones (N8N)
N8N_WEBHOOK_URL=https://n8n.tu-instancia.cloud/webhook/...
WHATSAPP_NUMBER=57312...
```

---

## 🚀 Despliegue Automático (CI/CD)

El sistema utiliza **Vercel Zero-Config**. Cualquier cambio en la rama `main` dispara:
1.  **Build Phase**: Aislamiento de dependencias (`requirements.txt`).
2.  **Asset Optimization**: Compresión de archivos estáticos en `/frontend`.
3.  **Lambda Deployment**: Publicación de las Python Functions bajo la ruta `/api/`.

---

## 🛠️ Tecnologías

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![N8N](https://img.shields.io/badge/n8n-FF6C37?style=for-the-badge&logo=n8n&logoColor=white)

---

**Última actualización:** Abril 2026  
**Versión:** 3.1 (Cloud Unified)  
**Autor:** Nicolás Martínez Pineda  
**CEO & Founder @ Syentropy**
