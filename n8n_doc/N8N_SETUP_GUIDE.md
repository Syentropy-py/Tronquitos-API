"""
Configuración de N8N para Automatización de Reservas
Incluye instrucciones paso a paso para crear el workflow
"""

# INSTRUCCIONES PASO A PASO PARA N8N

## 1. OBTENER CREDENCIALES

### WhatsApp Cloud API (Meta)
1. Ir a https://developers.facebook.com/
2. Crear una app de tipo "WhatsApp Business"
3. Obtener:
   - PHONE_NUMBER_ID: el ID del número de teléfono de WhatsApp
   - WHATSAPP_ACCESS_TOKEN: token de acceso de Meta

### Variables de Ambiente en Backend
```
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/tronquitos"
WHATSAPP_NUMBER = "573127923219"  # Número del cliente en formato E.164
```

---

## 2. ESTRUCTURA DEL WORKFLOW EN N8N

```
┌─────────────────────┐
│  Webhook Trigger    │
│ (POST /tronquitos)  │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────┐
│   Switch Node        │
│  (según json.type)   │
└──┬──────┬───────┬────┘
   │      │       │
   ▼      ▼       ▼
 RES    CANCEL  FREED
  │        │       │
  ▼        ▼       ▼
 SET     SET     SET
  │        │       │
  ▼        ▼       ▼
 HTTP    HTTP    HTTP
  │        │       │
  └────┬───┴───┬───┘
       ▼       ▼
    Respond
    (webhook)
```

---

## 3. NODOS DETALLADOS

### 3.1 WEBHOOK TRIGGER
- **Tipo**: Webhook
- **Método**: POST
- **URL**: /tronquitos
- **Opciones**: 
  - Only Data: ON
  - Authentication: Basic Auth (opcional)

---

### 3.2 SWITCH NODE (Decisión por tipo)
- **Tipo**: Switch
- **Entrada**: Evaluar expresión
- **Condición**: `{{$json.type}}`

**Rutas**:
1. `== "reservation"` → Proceso de Reserva
2. `== "cancellation"` → Proceso de Cancelación
3. `== "table_freed"` → Proceso de Mesa Liberada
4. Default → Respuesta genérica

---

### 3.3 SET NODE - RESERVA (primera rama)

**Nombre**: Set Message - Reservation

**Parámetros a establecer**:

```javascript
// message (tipo: string)
🍽️ NUEVA RESERVA\n\n
Nombre: {{$json.data.Nombre}}\n
Teléfono: {{$json.data.Teléfono}}\n
Email: {{$json.data.Email}}\n
Fecha: {{$json.data.Fecha}}\n
Hora: {{$json.data.Hora}}\n
Personas: {{$json.data.Personas}}\n
\n
Mesa asignada: {{$json.data.table_number}}\n
\n
¡Gracias por tu reserva!
```

---

### 3.4 SET NODE - CANCELACIÓN (segunda rama)

**Nombre**: Set Message - Cancellation

```javascript
// message
❌ RESERVA CANCELADA\n\n
Nombre: {{$json.data.Nombre}}\n
Fecha: {{$json.data.Fecha}}\n
Hora: {{$json.data.Hora}}\n
\n
Tu reserva ha sido cancelada.
```

---

### 3.5 SET NODE - MESA LIBERADA (tercera rama)

**Nombre**: Set Message - Table Freed

```javascript
// message
🪑 MESA DISPONIBLE\n\n
Una mesa ha sido liberada y vuelve a estar disponible.
```

---

### 3.6 HTTP REQUEST NODE (3 instancias)

**Nombre**: Send WhatsApp - Reservation (y similares)

**Configuración**:
- **Método**: POST
- **URL**: https://graph.facebook.com/v18.0/{{PHONE_NUMBER_ID}}/messages
  - Reemplazar {{PHONE_NUMBER_ID}} con el ID real
  
**Headers**:
```
Authorization: Bearer {{WHATSAPP_ACCESS_TOKEN}}
Content-Type: application/json
```

**Body** (JSON):
```json
{
  "messaging_product": "whatsapp",
  "to": "{{$json.whatsapp_number}}",
  "type": "text",
  "text": {
    "body": "{{$prevNode.data.message}}"
  }
}
```

**Error Handling**:
- Retry: 3 veces
- Wait Between Attempts: 2 segundos

---

### 3.7 RESPOND NODE
- **Tipo**: Respond to Webhook
- **Status Code**: 200
- **Body**:
```json
{
  "success": true,
  "message": "Evento procesado por n8n"
}
```

---

## 4. PRUEBAS DEL WEBHOOK

**Test Request desde Backend** (curl):
```bash
curl -X POST http://localhost:5678/webhook/tronquitos \
  -H "Content-Type: application/json" \
  -d '{
    "type": "reservation",
    "timestamp": "2026-03-14T20:30:00",
    "whatsapp_number": "573127923219",
    "data": {
      "Nombre": "Juan Pérez",
      "Teléfono": "+573001234567",
      "Email": "juan@example.com",
      "Fecha": "2026-03-20",
      "Hora": "20:00",
      "Personas": 4,
      "Mensaje": "Sin gluten",
      "table_number": 3
    }
  }'
```

---

## 5. VARIABLES GLOBALES EN N8N

Crear variables de ambiente en n8n:
1. Ir a **Settings > Variables**
2. Crear:
   - `PHONE_NUMBER_ID`: "xxxxxxxxxxxx"
   - `WHATSAPP_ACCESS_TOKEN`: "EAAx...xxx"
   - `WHATSAPP_API_URL`: "https://graph.facebook.com/v18.0"

Luego usarlas en las URLs:
```
{{$env.WHATSAPP_API_URL}}/{{$env.PHONE_NUMBER_ID}}/messages
```

---

## 6. MANEJO DE ERRORES

### En HTTP Request Node:
```
Expresión de error:
{{$error}}

Guardar error en log:
1. Agregar nodo "Merge" después de HTTP
2. Agregar rama de error
3. Guardar en base de datos o archivo
```

### Notification en caso de fallo:
```
Agregar nodo "Email" o "Slack" para alertar
si el envío a WhatsApp falla
```

---

## 7. WEBHOOK SIGNATURE VERIFICATION (Seguridad)

**En Webhook Node - Auth**:
```javascript
// Usar Basic Auth o similar
// O implementar verificación de JWT si lo requiere
```

---

## 8. LOGGING Y MONITOREO

N8N proporciona:
- **Execution History**: Guardar todos los eventos
- **Logs**: Ver detalles de cada ejecución
- **Alerts**: Configurar notificaciones por errores

**Recomendaciones**:
1. Habilitar "Wait for webhook to complete execution"
2. Guardar un log en base de datos de cada evento
3. Configurar alertas por tasa de errores

---

## 9. ESCALABILIDAD

### Para manejar muchas reservas:
1. Agregar un **Queue** node después de Switch
2. Usar base de datos para guardar eventos
3. Procesar en lotes

---

## 10. VARIABLES DINÁMICAS

En los SET nodes, acceder a:
- `$json.data`: Datos de la reserva
- `$json.timestamp`: Timestamp del evento
- `$json.whatsapp_number`: Número a enviar
- `$json.type`: Tipo de evento

---

## 11. IMPORTAR EL WORKFLOW

1. En n8n, click en **Import Workflow**
2. Pegar el contenido de `n8n_workflow.json`
3. Reemplazar IDs y tokens
4. Click en **Save and Active**

