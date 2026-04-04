# 🍽️ LOS TRONQUITOS - Sistema de Gestión de Reservas

**Sistema inteligente de reservas de restaurante con notificaciones por WhatsApp via N8N**

---

## ⚡ INICIO RÁPIDO (3 minutos)

### Requisitos
- Python 3.8+
- pip
- Base de datos SQLite (automática)

### Instalación
```bash
# 1. Instalar dependencias
pip install -r backend/requirements.txt

# 2. Inicializar base de datos
python backend/init_db.py

# 3. Iniciar servidor
python backend/app.py
```

### Verificar que funciona
```bash
# Ejecutar en otra terminal
curl http://localhost:5000/api/tables
```

---

## 📖 DOCUMENTACIÓN ESENCIAL

| Documento | Para | Leer si |
|-----------|------|--------|
| [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) | Instalación completa | Tienes problemas de setup |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Referencia de endpoints | Necesitas usar la API |
| [N8N_QUICK_START.md](n8n_doc/N8N_QUICK_START.md) | Configurar WhatsApp | Quieres notificaciones SMS/WhatsApp |
| [WHATSAPP_INTEGRATION.md](WHATSAPP_INTEGRATION.md) | Integración WhatsApp | Necesitas detalles de WhatsApp |

---

## 🎯 FUNCIONALIDADES

✅ **Control de Mesas**
- Gestión automática de mesas
- Búsqueda de disponibilidad en tiempo real
- Soporte multi-sede (Centro, Usaquén, Chapinero)

✅ **Reservas**
- Creación de reservas validadas
- Prevención de overbooking
- Cancelación con liberación de mesa
- Historial completo

✅ **Autopilot (N8N + WhatsApp)**
- Notificaciones automáticas de reservas
- Confirmaciones por WhatsApp
- Recordatorios antes de la fecha
- Manejo de cancelaciones

---

## 🔗 ENDPOINTS API

```
POST   /api/reservation          - Crear reserva
GET    /api/availability         - Ver disponibilidad
POST   /api/cancel-reservation   - Cancelar reserva
GET    /api/tables               - Listar mesas
POST   /api/contacts             - Mensaje de contacto
```

Ver documentación completa en [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🛠️ VERIFICACIÓN PRE-PRESENTACIÓN

Antes de presentar, ejecutar:

```bash
python VERIFICAR_SISTEMA.py
```

Esto verifica:
- ✓ Todos los archivos necesarios
- ✓ Número WhatsApp: +57 3102326407
- ✓ Dependencias instaladas
- ✓ Base de datos inicializada

---

## 📁 ESTRUCTURA

```
TRONQUITOS/
├── backend/
│   ├── app.py                      # Servidor Flask + endpoints
│   ├── database.py                 # Operaciones con BD
│   ├── models.py                   # Esquemas de datos
│   ├── reservation_service.py      # Lógica de negocio
│   ├── init_db.py                  # Inicialización BD
│   ├── database.db                 # Base de datos SQLite
│   └── requirements.txt            # Dependencias Python
│
├── frontend/
│   ├── index.html                  # Página principal
│   ├── styles.css                  # Estilos
│   └── scripts.js                  # JavaScript
│
├── n8n_doc/
│   ├── N8N_QUICK_START.md         # Inicio rápido N8N
│   ├── N8N_SETUP_GUIDE.md         # Configuración completa
│   ├── N8N_PROMPTS_READY_TO_USE.md # Prompts para IA
│   └── n8n_workflow.json          # Workflow importable
│
└── docs/
    └── slides/                     # Presentación
```

---

## 🚀 PRESENTACIÓN MAÑANA

**Checklist de últimos minutos:**

- [ ] Ejecutar `python backend/app.py` (backend)
- [ ] Ejecutar `python VERIFICAR_SISTEMA.py` (verificación)
- [ ] Abrir http://localhost:5000 en navegador
- [ ] Probar crear una reserva
- [ ] Verificar /api/tables endpoint
- [ ] Si presentas con N8N: verificar webhook conectado

**Número WhatsApp:** `+57 3102326407`

---

## 📞 SOPORTE RÁPIDO

**El sistema no inicia:**
```bash
python VERIFICAR_SISTEMA.py
# Ver qué falta, luego:
pip install -r backend/requirements.txt
python backend/init_db.py
```

**Errores en terminal:**
- Ver logs en la terminal del servidor
- Revisar [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

**N8N no se conecta:**
- Ver [N8N_QUICK_START.md](n8n_doc/N8N_QUICK_START.md)
- Verificar que N8N corre en puerto 5678
- Revisar el webhook URL en app.py

---

## ✨ Listo para Demostración

El sistema está optimizado para presentación mañana:
- ✅ Código limpio y funcional
- ✅ Documentación esencial incluida
- ✅ Scripts de verificación automática
- ✅ WhatsApp configurado (+57 3102326407)
- ✅ Multi-sede soportado
- ✅ Errores corregidos

**¡A presentar! 🎉**
