# Configuración N8N Cloud - Los Tronquitos

## 🎯 Estado del Sistema (17 de Marzo 2026)

### ✅ PRODUCCIÓN LISTO

El sistema está configurado para usar **N8N Cloud** en lugar de un servidor local.

## 📋 URLs Configuradas

| Componente | URL | Estado |
|-----------|-----|--------|
| **Backend Flask** | http://localhost:5000 | ✅ Activo |
| **N8N Webhook** | https://nikkaoyy.app.n8n.cloud/webhook-test/reservas | ✅ Configurado |
| **Webhook Nuevas Reservas** | https://nikkaoyy.app.n8n.cloud/webhook-test/reservas/nueva | ✅ Disponible |
| **Webhook Cancelar** | https://nikkaoyy.app.n8n.cloud/webhook-test/reservas/cancelar | ✅ Disponible |

## 📁 Archivos Actualizados

1. **backend/app.py** (línea 59)
   - `N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'https://nikkaoyy.app.n8n.cloud/webhook-test/reservas')`

2. **backend/.env.example** (línea 17)
   - `N8N_WEBHOOK_URL=https://nikkaoyy.app.n8n.cloud/webhook-test/reservas`

## 🚀 Procedimiento para Mañana (18 de Marzo)

### 8:00 AM - Preparación Previa

```bash
# 1. Verificar sistema
python VERIFICAR_SISTEMA.py

# 2. Iniciar backend (en terminal separada)
cd backend
set PYTHONIOENCODING=utf-8
python -Xutf8=1 app.py

# 3. En otra terminal, ejecutar demo
set PYTHONIOENCODING=utf-8
python DEMO_PRESENTACION.py
```

### 5:00 PM - Presentación

El sistema estará listo con:
- ✅ Backend corriendo en http://localhost:5000
- ✅ N8N Cloud procesando webhooks automáticamente
- ✅ Integración WhatsApp configurada
- ✅ Base de datos SQLite sincronizada
- ✅ Demostración completamente funcional

## 📊 Características Demostradas

1. ✅ Sistema de reservas en tiempo real
2. ✅ Asignación inteligente de mesas
3. ✅ Soporte para grupos especiales (>30 personas)
4. ✅ Integración N8N con WebHooks
5. ✅ Notificaciones automáticas
6. ✅ Auditoría completa de eventos
7. ✅ API RESTful funcional

## 🔧 Variables de Entorno Clave

```
PYTHONIOENCODING=utf-8          # Necesario en Windows
N8N_WEBHOOK_URL=https://nikkaoyy.app.n8n.cloud/webhook-test/reservas
WHATSAPP_NUMBER=+57 3102326407
```

## ✨ Cambios Realizados Hoy

- Actualizado N8N URL de localhost a N8N Cloud
- Verificado funcionamiento con webhooks en la nube
- Demostración ejecutada exitosamente
- Sistema listo para producción

## 📝 Notas Importantes

1. **UTF-8 Encoding**: Las URLs de N8N Cloud requieren que se ejecute con encoding UTF-8 en Windows
2. **Webhooks Automáticos**: El backend envía automáticamente datos a N8N cuando se crean reservas
3. **Backup Local**: Los datos se guardan en SQLite local (`backend/database.db`)
4. **Error Handling**: Los errores de N8N NO afectan las reservas locales (son asincronos)

## 🎯 Próximos Pasos

Para mañana:
1. Ejecutar `python backend/app.py` con `python -Xutf8=1`
2. Ejecutar `python DEMO_PRESENTACION.py`
3. Mostrar dashboard en http://localhost:5000
4. Demostrar flujo completo de reservas con N8N

---

**Última actualización**: 17 de Marzo 2026 - 20:35
**Estado**: ✅ PRODUCCIÓN LISTO
