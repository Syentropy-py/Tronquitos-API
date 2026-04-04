"""
🚀 N8N SETUP - QUICK START

Archivo índice con todos los pasos y referencias para configurar
n8n con los prompts e integraciones en 1 hora
"""

# ============================================================
# QUICK START - 3 PASOS
# ============================================================

QUICK_START_3_PASOS = """

⚡ SETUP RÁPIDO EN 3 PASOS

Si ya conoces n8n, hazlo así:

PASO 1: VERIFICAR INFRAESTRUCTURA (5 min)
└─ Backend corre: python app.py (puerto 5000)
└─ n8n corre: npm start (puerto 5678)
└─ BD existe: backend/database.db
└─ Test: curl http://localhost:5000/api/tables

PASO 2: CREAR WORKFLOW (10 min)
└─ En http://localhost:5678
└─ New Workflow
└─ Nombre: LOS_TRONQUITOS_RESERVAS
└─ Agregar 9 nodos (ver checklist)

PASO 3: CONFIGURAR PROMPTS (15 min)
└─ Copiar prompts de N8N_PROMPTS_READY_TO_USE.md
└─ Pegar en nodos LLM
└─ Configurar credenciales OpenAI/Claude
└─ Test

✅ ¡Listo en 30 minutos!

═══════════════════════════════════════════════════════════

Si necesitas paso a paso detallado:
→ Ver N8N_IMPLEMENTATION_CHECKLIST.md (11 pasos completos)

"""

# ============================================================
# ARCHIVOS PRINCIPALES
# ============================================================

FILES_INDEX = """

📚 ARCHIVOS DE REFERENCIA

Para entender la estructura completa:

1️⃣ ESTE ARCHIVO (N8N_SETUP.md)
   ├─ Resumen rápido
   ├─ Links a otros archivos
   └─ Troubleshooting rápido

2️⃣ N8N_PROMPTS_READY_TO_USE.md ⭐ ESENCIAL
   ├─ 10 prompts copiar/pegar
   ├─ Uno para cada situación
   ├─ Variables automáticas
   └─ Quick reference table
   
   USO: Copiar exacto en nodo LLM

3️⃣ N8N_NODES_CONFIG_VISUAL.md ⭐ ESENCIAL
   ├─ Cada nodo paso por paso
   ├─ Configuraciones exactas
   ├─ URLs, headers, body JSON
   └─ Test esperado para cada
   
   USO: Referencia mientras se arma workflow

4️⃣ N8N_IMPLEMENTATION_CHECKLIST.md ⭐ ESENCIAL
   ├─ 11 pasos secuenciales
   ├─ Preflight check
   ├─ Timeline + timeline
   ├─ Troubleshooting
   └─ Quick help section
   
   USO: Seguir paso por paso todo el setup

5️⃣ API_DOCUMENTATION.md (Ya existe)
   ├─ Endpoints disponibles
   ├─ Request/response examples
   └─ Para troubleshooting
   
   USO: Ver si endpoint está bien

6️⃣ INSTALLATION_GUIDE.md (Ya existe)
   ├─ Setup backend
   ├─ Setup base de datos
   └─ Debugging
   
   USO: Si algo del backend falla

7️⃣ N8N_AI_INSTRUCTIONS.md (Ya existe)
   ├─ AI completo para mesa control
   ├─ State machine
   ├─ Ejemplos ejecutables
   └─ Diseño completo del sistema
   
   USO: Entender lógica global

═══════════════════════════════════════════════════════════

ORDEN RECOMENDADO DE LECTURA:

1. Este archivo (5 min) ← Estás aquí
2. N8N_IMPLEMENTATION_CHECKLIST.md (15 min) ← Cómo hacerlo
3. N8N_PROMPTS_READY_TO_USE.md (10 min) ← Qué copiar
4. N8N_NODES_CONFIG_VISUAL.md (consulta) ← Ref mientras trabajas
5. Implementar (45 min)
6. Troubleshooting si necesario

"""

# ============================================================
# QUICK START PATHS
# ============================================================

START_PATHS = """

🎯 ELIGE TU CAMINO

¿Cuál ES TU SITUACIÓN?

OPCIÓN A: "Soy principiante en n8n"
└─ Seguir N8N_IMPLEMENTATION_CHECKLIST.md
└─ 11 pasos desde 0
└─ Tiempo: 1 hora
└─ Recomendado para entender

OPCIÓN B: "Ya usado n8n antes"
└─ Leer este archivo (5 min)
└─ Consultar N8N_NODES_CONFIG_VISUAL.md
└─ Copiar configs de nodos
└─ Tiempo: 30 min

OPCIÓN C: "Solo dame el código"
└─ Ir directo a N8N_PROMPTS_READY_TO_USE.md
└─ Copiar/pegar prompts
└─ Conectar nodos
└─ Tiempo: 15 min (si sabes n8n)

OPCIÓN D: "Necesito entender la lógica"
└─ Leer N8N_AI_INSTRUCTIONS.md primero
└─ Entender state machine
└─ Luego implementar N8N_IMPLEMENTATION_CHECKLIST.md
└─ Tiempo: 1.5 horas

OPCIÓN E: "Necesito ayuda"
└─ Skip to "TROUBLESHOOTING" abajo ↓

"""

# ============================================================
# ESTRUCTURA VISUAL DEL WORKFLOW
# ============================================================

WORKFLOW_STRUCTURE = """

🔴 ESTRUCTURA DEL WORKFLOW

Así se ve armado:

    WhatsApp Meta
         ↓
    [Webhook] → Recibe mensaje
         ↓
    [Parse] → Extrae datos
         ↓
    [IF] → Distribuye por tipo mensaje
    ├─ new_reservation
    ├─ availability  
    ├─ modify/cancel
    └─ general
         ↓
    [HTTP Get Tables] → Consulta BD
         ↓
    [LLM] → Genera respuesta inteligente
         ↓
    [HTTP Create/Cancel] → Modifica BD
         ↓
    [HTTP Send WhatsApp] → Envía respuesta
         ↓
    [HTTP Log Event] → Registra en BD
         ↓
    [Respond] → Contesta a webhook
         ↓
    Registrado en database.db

═══════════════════════════════════════════════════════════

DATOS FLUYEN COMO:

Input:
  WhatsApp → JSON → n8n → parse → classify

Processing:
  tipo → HTTP a BD → respuesta de BD
  → LLM + contexto → respuesta inteligente

Output:
  LLM → HTTP a BD → HTTP a WhatsApp
  → HTTP a eventos → respuesta webhook

═══════════════════════════════════════════════════════════

NODOS NECESARIOS: 9

1. Webhook (entrada)
2. Parse (extraer data)
3. IF (distribuir)
4. HTTP - Get Tables (BD)
5. LLM (IA)
6. HTTP - Create/Modify (BD)
7. HTTP - Send WhatsApp (Meta)
8. HTTP - Log Events (BD)
9. Respond (salida)

Tiempo armado: ~45 minutos

"""

# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================

INITIAL_CONFIG = """

⚙️ ANTES DE EMPEZAR - CONFIGURAR

1️⃣ CREDENCIALES NECESARIAS

Ir a n8n → Credentials (lado izquierdo)

Agregar:
[✓] OpenAI (o Claude/HuggingFace)
[✓] Meta WhatsApp (si usas HTTP directo)

OpenAI:
- https://platform.openai.com/api-keys
- Crear "New secret key"
- Copiar en n8n Credentials → OpenAI → Paste

Claude:
- https://console.anthropic.com/
- API Keys → Create Key
- Copiar en n8n Credentials → Anthropic

2️⃣ CREDENCIALES WHATSAPP

De Meta Business Manager:
- Ir a https://developers.facebook.com/
- Apps → Tu app → WhatsApp
- Configuration
- Copiar:
  * Phone Number ID
  * Access Token (validad 24h)

En n8n:
- Nodo HTTP SendWhatsApp
- Headers → Authorization: Bearer [TOKEN]

3️⃣ BACKEND CORRIENDO

Terminal 1:
cd backend
python app.py

Output esperado:
WARNING in app.py line 30: CORS enabled
* Running on http://localhost:5000

Para verificar:
curl http://localhost:5000/api/tables

4️⃣ DATABASE INICIALIZADO

Si no existe database.db:
python backend/init_db.py

Output:
✅ Database initialized
✅ 10 tables created
✅ Events table created

Para verificar:
sqlite3 backend/database.db
sqlite> .tables
tables reservations events contacts opinions

═══════════════════════════════════════════════════════════

✅ Checklist:
□ OpenAI/Claude credential configurado
□ WhatsApp token copiado
□ Backend corre en :5000
□ Database existe

Si todo ✓ → Listo para n8n

"""

# ============================================================
# COMANDOS ÚTILES
# ============================================================

COMMANDS = """

⌨️ COMANDOS ÚTILES (terminal)

Iniciar Backend:
$ cd backend
$ python app.py

Iniciar n8n:
$ npm start -g n8n

Iniciar Base de Datos (si no existe):
$ python backend/init_db.py

Verificar Backend:
$ curl http://localhost:5000/api/tables

Verificar BD desde terminal:
$ sqlite3 backend/database.db
sqlite> SELECT * FROM tables LIMIT 1;
sqlite> SELECT * FROM events LIMIT 5;
sqlite> .exit

Importar workflow (si tienes JSON):
En n8n → File → Import workflow → Paste JSON

Exportar workflow:
En n8n → File → Export workflow

Limpiar n8n (resetear):
$ npm run reset -g n8n

URLs principales:
- n8n: http://localhost:5678
- Backend: http://localhost:5000
- BD: backend/database.db
- WhatsApp API: https://graph.instagram.com/v18.0/

"""

# ============================================================
# MAPA DE PROMPTS
# ============================================================

PROMPTS_MAP = """

🎤 MAPA DE PROMPTS

Cada PROMPT en N8N_PROMPTS_READY_TO_USE.md:

PARA USAR        USE PROMPT
─────────────────────────────────────────────
Nueva reserva   → PROMPT_NEW_RESERVATION
Disponibilidad  → PROMPT_CHECK_AVAILABILITY
Cambiar reserva → PROMPT_MODIFY_RESERVATION
Cancelar        → PROMPT_CANCEL_RESERVATION
No-show detect  → PROMPT_NO_SHOW_DETECTION
Preguntas gral  → PROMPT_GENERAL_QUESTIONS
Confirmar final → PROMPT_CONFIRM_RESERVATION
Horarios alt.   → PROMPT_ALTERNATIVE_TIMES
Errores         → PROMPT_ERROR_RESPONSE
Sistema global  → SYSTEM_PROMPT_GENERAL

─────────────────────────────────────────────

Para cada nodo LLM en n8n:

1. Click en nodo LLM
2. Field "System Message"
3. Ir a N8N_PROMPTS_READY_TO_USE.md
4. Buscar PROMPT_*
5. Copiar exacto el texto
6. Pegar en "System Message"
7. Click Save

Variables ({{...}}) se reemplazan automáticamente

"""

# ============================================================
# TROUBLESHOOTING RÁPIDO
# ============================================================

TROUBLESHOOTING = """

🆘 TROUBLESHOOTING RÁPIDO

PROBLEMA: "Connection refused :5000"
SOLUCIÓN:
  1. Terminal: cd backend && python app.py
  2. Esperar "Running on http://localhost:5000"
  3. Reintentar

PROBLEMA: "LLM returns error 401"
SOLUCIÓN:
  1. Verificar credential OpenAI válida
  2. api.openai.com sin estar bloqueado
  3. Token no expirado

PROBLEMA: "WhatsApp Authentication failed"
SOLUCIÓN:
  1. Verificar Phone ID correcto
  2. Verificar Token válido (caducan)
  3. Ir a console.developers.facebook.com
  4. Generar nuevo token si es necesario

PROBLEMA: "Message not received"
SOLUCIÓN:
  1. Teléfono debe estar en recuento blancura en Meta
  2. Esperar 5-10s (delay de Meta)
  3. Ver logs en n8n → Logs tab

PROBLEMA: "Reservation not saved"
SOLUCIÓN:
  1. Verificar endpoint URL: http://localhost:5000/api/reservation
  2. Verificar JSON correcto en HTTP body
  3. En terminal Backend: ver error si aparece
  4. Verificar BD no está locked

PROBLEMA: "Variables {{}} no se reemplazan"
SOLUCIÓN:
  1. Verificar nombre nodo exacto en {{ }}
  2. Nombre es caso sensitivo
  3. Ejemplo: $node["Parse Message"].json.phone
  4. Verificar nodo anterior ejecutó sin error

PROBLEMA: "LLM responde genérico sin mesa info"
SOLUCIÓN:
  1. Prompt no accede a Get Tables
  2. En SYSTEM_PROMPT verificar:
     {{$node["Get Available Tables"].json.xxx}}
  3. Nombre de nodo debe coincidir

PROBLEMA: "Workflow ejecuta pero no entra en IF"
SOLUCIÓN:
  1. Verificar campo en IF coincide con Parse output
  2. Nombre campo: message_type
  3. En IF → Field: $node["Parse Message"].json.message_type

PROBLEMA: "Ngrok URL no funciona"
SOLUCIÓN:
  1. URL ngrok expira cada 2 horas
  2. Necesitas versión pagada para permanente
  3. O usar servidor en la nube (Heroku, Render)

PROBLEMA: "BD locked o corrupta"
SOLUCIÓN:
  1. Cerrar n8n: Ctrl+C en terminal
  2. Cerrar Backend: Ctrl+C en terminal
  3. rm backend/database.db (elimina)
  4. python backend/init_db.py (recrear)
  5. Reiniciar

═══════════════════════════════════════════════════════════

No está en la lista?
→ Ver logs en n8n (cada nodo tiene tab "Logs")
→ Ver terminal Backend para errores Python
→ Consultar API_DOCUMENTATION.md para endpoints

"""

# ============================================================
# VALIDACIÓN FINAL
# ============================================================

FINAL_CHECKLIST = """

✅ VALIDACIÓN ANTES DE IR A PRODUCCIÓN

Sistema armado. Ahora verificar:

FUNCIONALIDAD:
□ Enviar mensaje WhatsApp de prueba
□ n8n recibe en webhook
□ n8n responde con mesa disponible
□ Respuesta llega en WhatsApp
□ database.db tiene nueva reserva registrada

DATOS:
□ Nombre cliente correcto en BD
□ Teléfono guardado
□ Fecha/hora correcta
□ N° mesa asignada válida
□ Event registrado en tabla eventos

ESTADOS:
□ Nueva reserva: mesa status = reserved
□ Cancelar: mesa status = free
□ No-show: mesa status = free + evento

PRUEBAS EXTREMAS:
□ 0 personas → error/rechazo
□ Pasado (fecha vieja) → error/rechazo
□ 100 personas → sugerir alternativas
□ Caracteres especiales en nombre → guardados correctamente

PERFORMANCE:
□ Respuesta <15 segundos
□ Sin timeouts
□ BD no se bloquea

LOGGING:
□ /api/events tiene todos los eventos
□ n8n_sent = true en eventos
□ Timestamps correctos

═══════════════════════════════════════════════════════════

Si TODO ✓ → LISTO PARA PRODUCCIÓN

Ir a N8N_IMPLEMENTATION_CHECKLIST.md PASO 11
Para conectar webhook permanente en Meta

"""

# ============================================================
# SIGUIENTE PASO
# ============================================================

NEXT_STEP = """

🎬 TÚ ESTÁS AQUÍ

Dos opciones:

OPCIÓN 1: "Entiendo n8n, quiero ser rápido"
→ 1. Leer QUICK_START_3_PASOS (arriba)
→ 2. Ir a N8N_NODES_CONFIG_VISUAL.md
→ 3. Copiar config de cada nodo
→ 4. Copiar prompts de N8N_PROMPTS_READY_TO_USE.md
→ 5. Ejecutar y test

OPCIÓN 2: "Prefiero paso seguro"
→ 1. Abrir N8N_IMPLEMENTATION_CHECKLIST.md
→ 2. Seguir PASO 1 a PASO 11
→ 3. Cada paso ~5-10 min
→ 4. Total 1 hora
→ 5. Entenderás todo el process

OPCIÓN 3: "Necesito entiender la lógica"
→ 1. Leer N8N_AI_INSTRUCTIONS.md (mesa state machine)
→ 2. Luego ejecutar OPCIÓN 2
→ 3. Total 1.5 horas

OPCIÓN 4: "Algo falla"
→ Ver TROUBLESHOOTING (arriba)
→ Si no está: Check INSTALLATION_GUIDE.md
→ Si sigue: Revisar logs de n8n

═══════════════════════════════════════════════════════════

👉 RECOMENDADO:
Seguir OPCIÓN 2 (paso a paso)
Aunque lleve 1 hora, será claro y seguro

Ahora abre:
N8N_IMPLEMENTATION_CHECKLIST.md
Y sigue PASO 1

═══════════════════════════════════════════════════════════

¿Preguntas? Consulta:
- N8N_PROMPTS_READY_TO_USE.md
- N8N_NODES_CONFIG_VISUAL.md
- N8N_IMPLEMENTATION_CHECKLIST.md
- API_DOCUMENTATION.md
- INSTALLATION_GUIDE.md

📧 Todos en la carpeta raíz del proyecto

"""

print(QUICK_START_3_PASOS)
print("\n" + "="*60 + "\n")
print(FILES_INDEX)
print("\n" + "="*60 + "\n")
print(WORKFLOW_STRUCTURE)
print("\n" + "="*60 + "\n")
print(NEXT_STEP)

