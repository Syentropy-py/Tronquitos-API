# 🚀 GUÍA COMPLETA DE DEPLOYMENT PARA TRONQUITOS

## 📋 Resumen de Arquitectura

Tu aplicación tiene 3 componentes que deben desplegarse en diferentes plataformas:

| Componente | Tecnología | Plataforma | URL |
|-----------|-----------|-----------|-----|
| **Frontend** | HTML/CSS/JS | Vercel | `https://www.lostronquitos.com` |
| **Backend** | Python Flask | Render | `https://api.lostronquitos.com` |
| **Base de Datos** | PostgreSQL | Supabase | Privada |

---

## 1️⃣ PASO 1: Preparar GitHub

### 1.1 Crear Repositorio en GitHub
1. Ve a [github.com/new](https://github.com/new)
2. Nombre: `tronquitos-app`
3. Privado (opcional)
4. Click en "Create repository"

### 1.2 Pushear el código a GitHub
En tu terminal en VS Code:

```bash
git branch -M main
git remote add origin https://github.com/tu_usuario/tronquitos-app.git
git push -u origin main
```

---

## 2️⃣ PASO 2: Deploy Frontend en Vercel

### 2.1 Importar en Vercel
1. Ve a [vercel.com/new](https://vercel.com/new)
2. Conecta tu repositorio GitHub `tronquitos-app`
3. **IMPORTANTE**: En "Root Directory", selecciona `frontend/`
4. Click en Deploy

### 2.2 Configurar Dominio Personalizado
1. En tu panel Vercel → Settings → Domains
2. Agrega `www.lostronquitos.com` y `lostronquitos.com`
3. Sigue las instrucciones para configurar DNS en tu registrador

### 2.3 Variables de Entorno (Frontend)
En Vercel Settings → Environment Variables:
```
VITE_BACKEND_URL=https://api.lostronquitos.com
```

---

## 3️⃣ PASO 3: Deploy Backend en Render

### 3.1 Crear Proyecto en Render
1. Ve a [render.com](https://render.com)
2. Click en "New +" → Web Service
3. Conecta tu repositorio GitHub `tronquitos-app`

### 3.2 Configurar Build & Deploy
- **Name**: `tronquitos-backend`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app` (desde carpeta backend)

### 3.3 Variables de Entorno (Backend)
En Render Dashboard → Environment:
```
DB_HOST=tu-proyecto.postgresql.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña_supabase
N8N_WEBHOOK_URL=https://tu-n8n-url.app.n8n.cloud/webhook/...
WHATSAPP_NUMBER=+56XXXXXXXXX
```

### 3.4 Configurar Root Path
En Render → Settings → Build & Deploy → Root Directory: `backend`

### 3.5 Obtener URL del Backend
Después del deploy, Render te da una URL tipo:
```
https://tronquitos-backend.onrender.com
```

---

## 4️⃣ PASO 4: Base de Datos en Supabase

### 4.1 Crear Proyecto Supabase
1. Ve a [supabase.com](https://supabase.com)
2. New Project → Completa datos
3. Espera inicialización

### 4.2 Obtener Credenciales
En Settings → Database → Connection Info:
```
DB_HOST=xxxx.postgresql.supabase.co
DB_USER=postgres
DB_PASSWORD=xxxx
DB_NAME=postgres
DB_PORT=5432
```

### 4.3 Crear Tablas
En Supabase → SQL Editor, ejecuta el contenido de cada CREATE TABLE de [backend/models.py](../backend/models.py):
- branches
- tables
- daily_capacity
- reservations
- contacts
- opinions
- events

### 4.4 Migrar Datos Iniciales
En tu terminal local:
```bash
# Configurar .env
python migrate_csv_to_supabase.py
```

---

## 5️⃣ PASO 5: Actualizar Código para Producción

### 5.1 Frontend (scripts.js)
```javascript
// Cambiar de:
const BACKEND = 'http://localhost:5000';

// A:
const BACKEND = 'https://api.lostronquitos.com';
```

### 5.2 Backend (app.py)
```python
# Cambiar CORS de:
CORS(app)

# A:
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://www.lostronquitos.com",
            "https://lostronquitos.com"
        ]
    }
})
```

### 5.3 Variables de Entorno - NO subir .env a GitHub
Asegúrate que `.gitignore` contenga:
```
.env
__pycache__/
*.pyc
```

---

## 6️⃣ PASO 6: Configurar DNS

En tu registrador de dominios (Namecheap, GoDaddy, Cloudflare):

| Type | Name | Value |
|------|------|-------|
| CNAME | www | `cname.vercel-dns.com` |
| CNAME | @ | `cname.vercel-dns.com` |
| CNAME | api | `tronquitos-backend.onrender.com` |

**Espera 24-48 horas para propagación.**

---

## 7️⃣ PASO 7: Verificación Final

✅ Checklist:
- [ ] Backend deploy en Render (verde)
- [ ] Frontend deploy en Vercel (verde)
- [ ] Base de datos Supabase iniciada
- [ ] Dominio propagado (verifica en DNSChecker.org)
- [ ] Frontend conecta a `https://api.lostronquitos.com`
- [ ] Backend conecta a Supabase
- [ ] No hay secretos en GitHub (.env ignorado)

---

## 🔧 Solucionar Problemas

### Error: "CORS blocked"
→ Actualiza CORS en app.py con los dominios correctos

### Error: "Cannot connect to database"
→ Verifica variables de entorno en Render/Supabase

### Frontend no carga
→ Verifica que BACKEND URL tiene `https://` (no `http://`)

### Build failure en Vercel
→ Verifica que `vercel.json` está configurado correctamente

---

## 📞 Soporte
Para questions sobre:
- **Supabase**: docs.supabase.com
- **Vercel**: vercel.com/docs
- **Render**: render.com/docs
