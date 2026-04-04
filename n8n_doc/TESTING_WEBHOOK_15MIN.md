# ⚡ GUÍA RÁPIDA: TESTING CON WEBHOOKS EN 15 MINUTOS
## De cero a GPT-4 respondiendo mensajes

---

## ⏱️ TIEMPO ESTIMADO
- Configuración N8N: 5 min
- Agregar credenciales: 3 min
- Test webhook: 2 min  
- Ajustes: 5 min
- **TOTAL: 15 minutos**

---

## 📋 CHECKLIST PRE-REQUISITOS

Antes de empezar, asegúrate de tener:

```
✅ N8N corriendo en http://localhost:5678
   Verificar: Abre navegador y ve a http://localhost:5678
   Si no está corriendo:
   > npm start (en la carpeta de n8n)

✅ OpenAI API Key
   Obtener en: https://platform.openai.com/account/api-keys
   Confirmar que cuenta tiene acceso a GPT-4

✅ Backend API corriendo en http://localhost:5000
   Verificar: curl http://localhost:5000/api/health
   Si no: python backend/app.py

✅ WhatsApp Access Token configurado (si quieres enviar mensajes)
   De: https://developers.facebook.com
   
✅ Este archivo abierto (para copiar/pegar fácil)
```

Si alguno falta, detente y configúralo primero.

---

## 🎯 PASO 0: PREPARAR ARCHIVOS

Copia esto a una carpeta en tu escritorio para tener handy:

**archivo: `test_webhook.json`**
```json
{
  "from": "+573127923219",
  "message": "Hola, ¿tienen mesas para 4 personas el viernes a las 7 de la noche?",
  "name": "Juan de Prueba"
}
```

**archivo: `test_webhook_simple.json`**
```json
{
  "from": "+573127923219",
  "message": "¿Cuál es el horario?",
  "name": "María"
}
```

Los vas a usar para testear.

---

## 🔑 PASO 1: AGREGAR CREDENCIAL OPENAI EN N8N (3 MIN)

1. Abre N8N: http://localhost:5678
2. Haz login
3. Click en tu usuario (arriba a la derecha)
4. Click en **"Credentials"** (o "Credenciales")
5. Click en **"Create New"** (botón azul)
6. Busca y selecciona **"OpenAI"** en la lista
7. Llena así:

```
Credential Name: Mi OpenAI Key
API Key: [Pega tu clave de OpenAI aquí]
```

8. Click **"Create Credential"**

**✅ Listo, ya tienes OpenAI registrado en N8N**

---

## 🛠️ PASO 2: CREAR WORKFLOW (2 MIN)

En N8N:

1. Click en **"New Workflow"** (botón azul grande)
2. Dale un nombre: `Testing_GPT4_Tronquitos`
3. Descripción: `Webhook + GPT-4 + WhatsApp`
4. Click **"Create"**

**✅ Workflow creado, ahora agreguemos nodos**

---

## 🔗 PASO 3: AGREGAR NODO WEBHOOK (1 MIN)

1. En el workflow vacío, haz click en **"Add first step"** o **click en el "+""**
2. Busca **"Webhook"** en la lista
3. Selecciona **"Webhook"**
4. En la configuración que aparece, busca:
   - **Path**: Escribe `tronquitos-gpt4-test`
   - Deja todo lo demás igual
5. Click **Save node**

Notarás que aparece una URL:
```
http://localhost:5678/webhook/[id]/tronquitos-gpt4-test
```

⚠️ **COPIA Y GUARDA ESTA URL, LA NECESITARÁS**

---

## 🤖 PASO 4: AGREGAR NODO GPT-4 (3 MIN)

1. Click en el **"+"** (nodo Webhook) para agregar siguiente nodo
2. Busca **"OpenAI"** (o "Chat GPT")
3. Selecciona **"OpenAI > Chat"**
4. Aparecerá formulario. Llena así:

```
🔐 Credenciales:
  Authentication: Selecciona "Mi OpenAI Key" (la que creaste)

⚙️ Parámetros:
  Model: gpt-4 (o gpt-4-turbo si te pide)
  Temperature: 0.7
  Max Tokens: 500
```

5. **IMPORTANTE: Scroll down y busca "System Instructions"**
6. En el campo "System Instructions" copia/pega esto:

```
Eres un asistente amable para ASADERO LOS TRONQUITOS.

RESTAURANTE INFO:
- Horarios: 12 PM - 6 PM todos los días
- Ubicación: Av. Calle 3 #53-07, Bogotá
- Teléfono: 414 68 70
- Especialidad: Carnes a la llanera desde 1971

Cuando el cliente pregunta sobre mesas/fechas/horas:
1. Di amablemente que confirmen fecha, hora y cantidad personas
2. Responde en máximo 2-3 líneas
3. Incluye emojis ocasionales: 🍽️ 📅 ✅ 😊

Cuando pregunta horarios/ubicación:
- Responde directo: "Abierto 12 PM - 6 PM, ubicación Av. Calle 3 #53-07"

Cuando pregunta por menú:
- "Tenemos especialidades en carnes a la llanera. Puedes descargar el PDF en nuestro sitio"

Siempre sé profesional pero amable.
```

7. Scroll down más, busca **"Input Message Format"**
8. En el campo "Messages": 
   - Tipo: String
   - Valor: `{{$json.message}}`
   
9. Click **Save node**

**✅ Ahora GPT-4 procesa el mensaje del cliente**

---

## 📤 PASO 5: AGREGAR NODO DE OUTPUT (Optional pero útil)

1. Click en **"+"** del nodo GPT-4
2. Busca y selecciona **"Set"** (no HTTPRequest, es el Set Node)
3. En el formulario que aparece, busca **"Set values"** o **"Assignments"**
4. Agrega un parámetro nuevo:
```
Name: response
Type: String
Value: {{$json.choices[0].message.content}}
```

5. Click **Save node**

Esto extrae solo la respuesta de texto de GPT-4.

---

## 🧪 PASO 6: TEST (ANTES DE ENVIAR A WHATSAPP) (2 MIN)

Ahora comes y testas sin enviar a WhatsApp.

**Opción A: Test desde N8N UI (Recomendado)**

1. En el workflow, arriba de todo, haz click en **"Listen for Test Events"** (botón verde/azul)
2. El workflow entra en "escucha"
3. Abre **Terminal/PowerShell**
4. Ejecuta esto (Windows PowerShell):

```powershell
$body = @{
    from = "+573127923219"
    message = "Hola, ¿tienes disponibilidad para 4 personas el viernes a las 7 PM?"
    name = "Juan"
} | ConvertTo-Json

$url = "http://localhost:5678/webhook/tronquitos-gpt4-test"

Invoke-WebRequest -Uri $url `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

5. Si todo va bien, verás en N8N la ejecución en VERDE ✅
6. Haz click en la ejecución para ver el detalle
7. Verifica que GPT-4 respondió algo coherente

**Opción B: Test desde Postman**

1. Abre Postman
2. Nueva request
3. Método: POST
4. URL: `http://localhost:5678/webhook/tronquitos-gpt4-test`
5. Body (JSON):
```json
{
  "from": "+573127923219",
  "message": "¿Cuál es tu horario de atención?",
  "name": "María"
}
```
6. Click Send
7. Verifica respuesta en la sección Response

**✅ Si ves respuesta de GPT-4, funciona!**

---

## 📞 PASO 7: OPCIONAL - ENVIAR A WHATSAPP (SOLO SI QUIERES)

Si ya tienes WhatsApp configurado:

1. Después del nodo "Set", agrega un nodo **"HTTP Request"**
2. Configuración:

```
Method: POST
URL: https://graph.facebook.com/v18.0/{TU_PHONE_ID}/messages

Headers:
  Authorization: Bearer {TU_ACCESS_TOKEN}
  Content-Type: application/json

Body (JSON):
{
  "messaging_product": "whatsapp",
  "to": "{{$json.from}}",
  "type": "text",
  "text": {
    "body": "{{$json.response}}"
  }
}
```

3. Reemplaza:
   - `{TU_PHONE_ID}`: Tu Phone Number ID de WhatsApp
   - `{TU_ACCESS_TOKEN}`: Tu Access Token de Meta

4. Haz un test y verifica que el mensaje llega a tu teléfono ✅

---

## 🔄 PASO 8: TEST FULL END-TO-END (2-3 MIN)

Ahora testa el **flujo completo**:

```
Cliente envía mensaje
  ↓
Webhook recibe
  ↓
GPT-4 procesa
  ↓
Responde al cliente (si lo conectaste)
```

**Abre terminal y ejecuta varias llamadas:**

```powershell
# Test 1: Pregunta sobre horarios
$test1 = @{
    from = "+573127923219"
    message = "¿A qué hora abren?"
    name = "Test1"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5678/webhook/tronquitos-gpt4-test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $test1

# Test 2: Pregunta sobre reserva
$test2 = @{
    from = "+573127923219"
    message = "Necesito una mesa para 6 personas el sábado"
    name = "Test2"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5678/webhook/tronquitos-gpt4-test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $test2

# Test 3: Pregunta sobre menú
$test3 = @{
    from = "+573127923219"
    message = "¿Cuáles son los platos más populares?"
    name = "Test3"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5678/webhook/tronquitos-gpt4-test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $test3
```

Verifica en N8N que todas las ejecuciones sean ✅ verde.

---

## ⚙️ PASO 9: TROUBLESHOOTING RÁPIDO

| Problema | Causa | Solución |
|----------|-------|----------|
| "401" en HTTP | API Key inválida | Verifica clave OpenAI en https://platform.openai.com/account/api-keys |
| GPT-4 no responde | Credencial no conectada | En nodo GPT-4, selecciona "Mi OpenAI Key" en Authentication |
| Webhook no recibe | N8N no está corriendo | Abre http://localhost:5678 en navegador |
| "Connection refused" | Puerto 5678 ocupado | `netstat -ano \| grep 5678` y mata el proceso |
| Respuesta genérica | Prompt muy simple | Reemplaza System Instructions con uno de [GPT4_PROMPTS_COPY_PASTE.md](GPT4_PROMPTS_COPY_PASTE.md) |

---

## ✅ CHECKLIST TESTING

- [ ] N8N corriendo en http://localhost:5678
- [ ] Credencial OpenAI creada
- [ ] Webhook nodo configurado con path correcto
- [ ] GPT-4 nodo conectado con credencial
- [ ] System Instructions tiene un prompt claro
- [ ] Test desde PowerShell/Postman funciona ✅
- [ ] GPT-4 responde en español amablemente
- [ ] Respuestas son cortas (2-3 líneas)
- [ ] Emojis aparecen en respuestas (opcional)
- [ ] [ ] **TESTING COMPLETO: GREEN LIGHT PARA PRODUCCIÓN** ✅

---

## 🚀 SIGUIENTE PASO: CONECTAR CON TU BACKEND

Una vez tengas el webhook testeado, conecta con tu app:

**En `backend/app.py`:**

```python
import requests
import json

N8N_WEBHOOK = "http://localhost:5678/webhook/tronquitos-gpt4-test"

@app.route('/api/send-to-gpt4', methods=['POST'])
def send_to_gpt4():
    data = request.json
    
    payload = {
        "from": data.get("phone"),
        "message": data.get("message"),
        "name": data.get("name")
    }
    
    try:
        response = requests.post(N8N_WEBHOOK, json=payload, timeout=15)
        return jsonify({"status": "ok", "response": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

Luego desde tu frontend o app, llama:

```python
requests.post(
    "http://localhost:5000/api/send-to-gpt4",
    json={
        "phone": "+573127923219",
        "message": "Quiero reservar para 5",
        "name": "Juan"
    }
)
```

---

## 🎓 RECURSOS ADICIONALES

📖 Guía completa: [GPT4_N8N_WEBHOOK_SETUP.md](GPT4_N8N_WEBHOOK_SETUP.md)
🎯 Más prompts: [GPT4_PROMPTS_COPY_PASTE.md](GPT4_PROMPTS_COPY_PASTE.md)
⚡ Config N8N: [N8N_SETUP_GUIDE.md](N8N_SETUP_GUIDE.md)

---

## 💬 ¿PREGUNTAS?

Si algo no funciona:
1. Revisa que N8N esté corriendo: http://localhost:5678
2. Verifica credencial OpenAI: Settings → Credentials
3. Mira los logs del workflow: Click en ejecución roja
4. Compara tu setup con esta guía paso a paso

---

**Última actualización:** Marzo 2026
**Versión:** 1.0 (Testing Rápido)
