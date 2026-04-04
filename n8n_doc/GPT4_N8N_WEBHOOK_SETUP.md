# 🤖 INTEGRACIÓN GPT-4 + N8N + WEBHOOKS
## Guía Completa para Testing y Producción

---

## 📋 TABLA DE CONTENIDOS
1. [Arquitectura General](#arquitectura)
2. [Paso 1: Obtener Credenciales](#paso1)
3. [Paso 2: Crear Workflow en N8N](#paso2)
4. [Paso 3: Configurar GPT-4](#paso3)
5. [Paso 4: Setup de Webhooks](#paso4)
6. [Paso 5: Testing](#paso5)
7. [Paso 6: Ir a Producción](#paso6)
8. [Troubleshooting](#troubleshooting)

---

## 🏗️ ARQUITECTURA GENERAL {#arquitectura}

```
┌──────────────┐
│   Cliente    │
│  (WhatsApp)  │
└────────┬─────┘
         │
         ▼
┌──────────────────┐      ┌─────────────────┐
│   Webhook N8N    │─────▶│   GPT-4 API     │
│   (Receptor)     │      │   (OpenAI)      │
└────────┬─────────┘      └─────────────────┘
         │
         ▼
    ┌─────────────┐
    │ Switch Node │ (Decide: nueva reserva / consulta / otra)
    └────┬─────┬──┘
    ┌────┘  ┌──┘
    │       │
    ▼       ▼
┌────────┐ ┌──────────┐
│ GPT-4  │ │ Backend  │
│ (Chat) │ │ (API)    │
└────┬───┘ └────┬─────┘
     │          │
     └────┬─────┘
          ▼
    ┌─────────────────┐
    │ WhatsApp Send   │
    │ (Meta API)      │
    └─────────────────┘
```

---

## 🔐 PASO 1: OBTENER CREDENCIALES {#paso1}

### 1.1 OpenAI (Para GPT-4)

**Obtener API Key:**
1. Ir a https://platform.openai.com/account/api-keys
2. Crear una nueva API Key
3. Copiar y guardar SEGURAMENTE (nunca en Git)
4. Asegurarse que la cuenta tenga acceso a GPT-4

**Variable de Ambiente:**
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
```

### 1.2 Meta WhatsApp (Para enviar mensajes)

**Ya tienes esto configurado, pero verifica:**
```env
WHATSAPP_PHONE_NUMBER_ID=1234567890123456
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_BUSINESS_ACCOUNT_ID=xxxxxxxxxxxxxx
```

### 1.3 N8N (Local o Cloud)

**Para Testing (Local):**
- Corre en: `http://localhost:5678`
- Usuario: el que configuraste
- Contraseña: la que configuraste

**Para Producción (Cloud):**
- Ir a https://n8n.cloud
- Crear cuenta pro
- Los datos de credenciales se guardan seguros en N8N

---

## 🛠️ PASO 2: CREAR WORKFLOW EN N8N {#paso2}

### 2.1 Crear nuevo workflow

**En http://localhost:5678:**
1. Click en "New Workflow"
2. Nombre: `Los_Tronquitos_GPT4_Reservas`
3. Descripción: "Sistema de reservas con IA (GPT-4)"

### 2.2 Agregar Nodos

**Nodo 1: Webhook Trigger (Entrada)**

```
Tipo: Webhook
Método: POST
Ruta: /tronquitos-gpt4
Autenticación: Basic Auth (opcional pero recomendado)

Nota: Este webhook recibirá:
{
  "from": "+573127923219",
  "message": "Quiero reservar para 5 personas mañana",
  "name": "Juan"
}
```

**Nodo 2: Fetch Database Status** (Opcional pero recomendado)

```
Tipo: HTTP Request
Método: GET
URL: http://localhost:5000/api/tables
Autenticación: None

Esto obtiene las mesas disponibles ACTUALES
```

**Nodo 3: GPT-4 Chat Node** ⭐ PRINCIPAL

```
Tipo: OpenAI > Chat
Modelo: gpt-4 (o gpt-4-turbo si necesitas)
Temperatura: 0.7 (para conversación natural)
```

Conectar:
- Webhook Trigger → GPT-4
- Database Status → GPT-4

**Nodo 4: Parse Response**

```
Tipo: Set
Salida: Parsear respuesta de GPT-4
```

**Nodo 5: Send WhatsApp**

```
Tipo: HTTP Request
Método: POST
URL: https://graph.facebook.com/v18.0/{PHONE_ID}/messages
Headers:
  Authorization: Bearer {ACCESS_TOKEN}
  Content-Type: application/json

Body JSON:
{
  "messaging_product": "whatsapp",
  "to": "{{$json.from}}",
  "type": "text",
  "text": {
    "body": "{{$json.response}}"
  }
}
```

---

## 🤖 PASO 3: CONFIGURAR GPT-4 {#paso3}

### 3.1 Agregar OpenAI Credential en N8N

En el Nodo GPT-4:
1. Click en "Create New Credential"
2. Seleccionar "OpenAI"
3. Pegar API Key que obtuviste
4. Click "Save Credential"

### 3.2 Configurar el Prompt (System Instructions)

Este es el CORAZÓN de la IA. En el Nodo GPT-4, en "System Instructions":

```
Eres un asistente amable y profesional para reservas de ASADERO LOS TRONQUITOS.

INFORMACIÓN DEL RESTAURANTE:
- Nombre: Asadero Los Tronquitos (Desde 1971)
- Especialidades: Carne a la llanera, costillas, chigüiro, pescados
- Horarios: Domingo a Domingo 12:00 PM - 6:00 PM
- Eventos: Disponibles 24 horas
- Dirección: Av. Calle 3 #53-07, Bogotá
- Teléfono: 414 68 70
- WhatsApp: +57 312 792 3219

MESAS DISPONIBLES AHORA:
- Total: 10 mesas
- Capacidades: 2, 4, 6, 8, 10 personas
- Estado actual: {{$json.tables}} (si tienes DB conectada)

TUS TAREAS:
1. Escuchar la solicitud del cliente
2. Si quiere reservar:
   - Confirmar: Número de personas, fecha, hora
   - Verificar disponibilidad en BD
   - Dar mesa específica si está disponible
   - Ofrecer alternativa si no hay espacio
3. Si solo pregunta precios/horarios: RESPONDER directamente
4. Si cancelar reserva: Confirmación y motivo
5. Siempre ser amable, profesional, eficiente

REGLAS IMPORTANTES:
- Máximo 2-3 líneas de WhatsApp por respuesta
- Usa emojis ocasionales: 🍽️ 📅 ✅ ❌ 😊
- Si no entiendes: pide aclaración amable
- Nunca hagas cambios sin confirmación del cliente
- Si reserva se confirma: incluye MESA NÚMERO y HORA

FORMATO DE RESPUESTA:
- Confirmación clara
- Detalles de la reserva (si aplica)
- Próximo paso (qué hacer)
```

### 3.3 Input Message (Lo que envía el cliente)

En el Nodo GPT-4, en "Messages":

```
Agregar parámetro "User Message":
{{$json.message}}

Esto toma el mensaje del cliente del webhook
```

---

## 🔗 PASO 4: SETUP DE WEBHOOKS {#paso4}

### 4.1 URL del Webhook (Para Testing)

```
Local (Development):
http://localhost:5678/webhook/tronquitos-gpt4

Con Basic Auth (agregar usuario:contraseña):
http://usuario:contraseña@localhost:5678/webhook/tronquitos-gpt4
```

### 4.2 URL del Webhook (Para Producción)

```
Cloud N8N:
https://[tu-instance].n8n.cloud/webhook/[unique-id]/tronquitos-gpt4

HTTPS está incluido y es obligatorio
```

### 4.3 Cómo conectar desde tu Backend

**En tu archivo `app.py` o donde manejes reservas:**

```python
import requests
import json

def notify_gpt4_for_reservation(customer_data):
    """Envía mensaje del cliente a N8N para que GPT-4 procese"""
    
    webhook_url = "http://localhost:5678/webhook/tronquitos-gpt4"
    
    payload = {
        "from": customer_data["whatsapp_number"],  # "+573127923219"
        "message": customer_data["message"],        # Mensaje del cliente
        "name": customer_data["name"],              # Nombre del cliente
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error enviando a N8N: {e}")
        return False

# Uso:
# notify_gpt4_for_reservation({
#     "whatsapp_number": "+573127923219",
#     "message": "Quiero reservar para 5 personas mañana",
#     "name": "Juan"
# })
```

### 4.4 Cómo disparar desde Frontend (JavaScript)

Si quieres enviar directamente desde website:

```javascript
async function sendToGPT4(message, phone, name) {
    const webhookUrl = "http://localhost:5678/webhook/tronquitos-gpt4";
    
    const payload = {
        from: phone,
        message: message,
        name: name
    };
    
    try {
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        console.log("Respuesta de GPT-4:", data);
        return data;
    } catch (error) {
        console.error("Error:", error);
    }
}

// Uso:
// sendToGPT4(
//     "Quiero una mesa para 4 personas mañana a las 7 PM",
//     "+573127923219",
//     "Juan"
// )
```

---

## ✅ PASO 5: TESTING {#paso5}

### 5.1 Test Manual desde N8N

1. Abre tu workflow en N8N
2. Click en "Listen for Test Events" (botón verde)
3. En otra pestaña, ejecuta esto en terminal:

```bash
# Windows PowerShell
$body = @{
    from = "+573127923219"
    message = "Quiero una mesa para 4 personas el sábado a las 8 PM"
    name = "Juan"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5678/webhook/tronquitos-gpt4" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

```bash
# Linux/Mac
curl -X POST http://localhost:5678/webhook/tronquitos-gpt4 \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+573127923219",
    "message": "Quiero una mesa para 4 personas el sábado a las 8 PM",
    "name": "Juan"
  }'
```

### 5.2 Verificar Response

En N8N, deberías ver:
- ✅ Webhook recibió datos
- ✅ GPT-4 procesó mensaje
- ✅ WhatsApp envió respuesta
- ✅ Sin errores en logs

### 5.3 Test con Postman

1. Abre Postman
2. New Request
3. Method: POST
4. URL: `http://localhost:5678/webhook/tronquitos-gpt4`
5. Body (JSON):
```json
{
  "from": "+573127923219",
  "message": "Hola, ¿tienen disponibilidad el viernes?",
  "name": "María"
}
```
6. Click Send
7. Verificar status 200

### 5.4 Test Real (WhatsApp)

Si quieres probar desde WhatsApp real:

1. Configura webhook en Meta Dashboard
2. En tu Backend, cuando recibas mensaje de WhatsApp:

```python
@app.route('/webhook/whatsapp', methods=['POST'])
def webhook_whatsapp():
    data = request.json
    
    # Enviar a N8N para procesamiento GPT-4
    send_to_gpt4(
        from=data['From'],
        message=data['Body'],
        name=data.get('From')
    )
    
    return jsonify({'status': 'ok'})
```

---

## 🚀 PASO 6: IR A PRODUCCIÓN {#paso6}

### 6.1 Cambios Necesarios

**6.1.1 Cambiar URLs**

En `GPT4_CONFIG.env`:
```env
# ANTES (Testing)
WEBHOOK_URL=http://localhost:5678/webhook/tronquitos-gpt4
BACKEND_URL=http://localhost:5000

# DESPUÉS (Producción)
WEBHOOK_URL=https://[instance].n8n.cloud/webhook/[id]/tronquitos-gpt4
BACKEND_URL=https://tu-dominio-produccion.com
```

**6.1.2 Actualizar app.py**

```python
import os

# Detectar entorno
ENV = os.getenv('ENVIRONMENT', 'development')

if ENV == 'production':
    N8N_WEBHOOK = "https://[instance].n8n.cloud/webhook/[id]/tronquitos-gpt4"
else:
    N8N_WEBHOOK = "http://localhost:5678/webhook/tronquitos-gpt4"

def notify_gpt4(data):
    response = requests.post(N8N_WEBHOOK, json=data)
    return response.status_code == 200
```

### 6.2 Deployment N8N Cloud

**Opción A: N8N Cloud Pro**

1. Ir a https://n8n.cloud
2. Crear cuenta / Login
3. Create New Workflow
4. Copiar y pegar tu workflow JSON
5. Configurar credenciales en N8N Cloud (no guardes en el archivo)
6. Deploy / Activar workflow

**Opción B: Self-Hosted en tu servidor**

```bash
# En tu servidor (Ubuntu/Debian)
sudo docker pull n8nio/n8n:latest

sudo docker run -d \
  -p 5678:5678 \
  -e N8N_HOST=tu-dominio.com \
  -e N8N_PROTOCOL=https \
  -e N8N_PORT=5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n:latest
```

### 6.3 URL Webhook Producción

Una vez desplegado:

```
ANTES:
http://localhost:5678/webhook/tronquitos-gpt4

DESPUÉS:
https://n8n-prod-123.example.com/webhook/xxx-yyy-zzz
o
https://instance.n8n.cloud/webhook/xxx-yyy-zzz
```

### 6.4 Checklist Pre-Producción

- [ ] API Key OpenAI está usando cuenta con GPT-4
- [ ] WhatsApp Token probado y activo
- [ ] Todas las URLs usan HTTPS
- [ ] Credenciales no están en código (usar variables .env)
- [ ] N8N workflow tiene error handling (onError: continue)
- [ ] Testing funciona end-to-end
- [ ] Logs están configurados
- [ ] Rate limits configurados (evitar spam)
- [ ] Backups de workflow JSON creados
- [ ] Documentación actualizada

---

## 🐛 TROUBLESHOOTING {#troubleshooting}

### Problema: "401 Unauthorized" en OpenAI

**Causa:** API Key inválida o sin permiso GPT-4

**Solución:**
1. Verificar key en https://platform.openai.com/account/api-keys
2. Confirmar que cuenta tiene acceso a GPT-4
3. Re-crear credencial en N8N

### Problema: Webhook no recibe datos

**Causa:** URL incorrecta o firewall bloqueando

**Solución:**
```bash
# Test si N8N está corriendo
curl http://localhost:5678/

# Si no responde:
# 1. Reiniciar N8N
# 2. Verificar puerto 5678 no está en uso
# 3. Verificar firewall Windows permite puerto 5678
```

### Problema: WhatsApp no envía mensajes

**Causa:** Token expirado o formato incorrecto

**Solución:**
1. Ir a https://developers.facebook.com/apps
2. Verificar que token es válido
3. Revisar que PHONE_NUMBER_ID es correcto
4. Verificar que número cliente está en formato E.164 (+573XX...)

### Problema: GPT-4 da respuestas genéricas

**Causa:** Prompt system instructions no está claro

**Solución:**
1. Click en nodo GPT-4
2. Editar "System Instructions"
3. Ser más específico: incluir contexto del restaurante
4. Test nuevamente

### Problema: N8N consume muchos recursos

**Causa:** Workflow ineficiente con demasiadas llamadas API

**Solución:**
1. Agregar caché de respuestas
2. Limitar frecuencia de webhook
3. Usar n8n triggers instead of polling
4. En producción: usar plan de pago que permita más recursos

### Problema: Errores de CORS (frontend → webhook)

**Causa:** Navegador bloquea llamada cross-domain

**Solución:**

En N8N Nodo Webhook, agregar:
```
Opciones avanzadas → Headers:
{
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
}
```

O mejor: usar backend como intermediario:

```python
@app.route('/api/gpt4', methods=['POST'])
def handle_gpt4_request():
    data = request.json
    # Backend→N8N (no browser→N8N)
    response = requests.post(N8N_WEBHOOK, json=data)
    return response.json()
```

---

## 📊 MONITORING & LOGS

### Ver Logs de N8N

```
Terminal donde corre n8n:
- Buscar errores en rojo
- Buscar "timestamp" para ver cuando se ejecutó
- Click en execution log en N8N UI
```

### Crear Log de Webhook Calls

Agregar nodo "Log" después del webhook:

```
N8N Node: Function
Code:
console.log("Webhook recibido:", $json);
```

### Alertas en Producción

En N8N Cloud, agregar notificación:

```
N8N Node: Slack / Email
Enviar alerta si:
- Webhook fail
- GPT-4 timeout
- WhatsApp error
```

---

## 🎓 PRÓXIMOS PASOS

1. ✅ Implementa webhook basic (sin GPT-4)
2. ✅ Agrega GPT-4 con prompt simple
3. ✅ Test en staging/QA
4. ✅ Itera prompt basado en feedback
5. ✅ Deploy a producción
6. ✅ Monitor y mejora

---

## 📞 CONTACTO & SOPORTE

- N8N Docs: https://docs.n8n.io
- OpenAI Docs: https://platform.openai.com/docs
- Meta WhatsApp: https://developers.facebook.com/docs/whatsapp

---

**Última actualización:** Marzo 2026
**Versión:** 2.0 (GPT-4 + Webhooks para Testing)
