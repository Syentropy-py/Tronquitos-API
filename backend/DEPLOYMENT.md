# Guía de Despliegue en Producción (Producción Web)

Esta guía documenta todo lo que tienes que cambiar y dónde subir tu aplicación para publicarla en vivo en una URL pública.

## 1. Dónde hacer Host (Alojar tu App)
Dado que tu aplicación cuenta con 3 componentes (Interfaz Web, Servidor Python, Base de Datos), necesitas alojarlas de la siguiente manera:

* **Base de Datos (PostgreSQL)**: 
  Puedes utilizar **Supabase** (Recomendado, gratuito) o **Render Postgres** para crear una base de datos PostgreSQL pública. Te darán tus credenciales (`Host, Port, User, Pass, y Name`).
* **Backend (Python)**:
  La mejor plataforma para subir un servidor Flask gratuitamente desde Git es **Render.com** o **Railway.app**. Estas plataformas soportan Python nativamente.
* **Frontend (HTML/CSS/JS)**:
  Puedes alojar tu carpeta `frontend/` de forma gratuita y ultra rápida en **Vercel**, **Netlify**, o **GitHub Pages**.

---

## 2. Cambios en el Código para Producción

### En el Frontend
Tienes que cambiar la dirección con la que el frontend se comunica con el servidor.

1. Abre `frontend/gestor.html`, `frontend/index.html` y `frontend/scripts.js` (u otros donde uses tu API).
2. Cambia la variable:
   ```javascript
   const BACKEND = 'http://localhost:5000';
   ```
   Por el nuevo dominio de tu backend subido a Render/Railway (ejemplo):
   ```javascript
   const BACKEND = 'https://tronquitos-backend.onrender.com';
   ```

### En el Backend

1. **Uso del Servidor Gunicorn (Obligatorio en Prod)**
   En lugar de ejecutar `python app.py` (lo cual usa el servidor de depuración de Flask), el servicio de Cloud (Render) te va a pedir un *Command de arranque*.
   Tu comando en el host debe ser: 
   ```bash
   gunicorn app:app
   ```
   (Asegúrate de que `gunicorn` esté en tu `requirements.txt`).

2. **Variables de Entorno en el Cloud**
   No subas el archivo `.env` a GitHub. Debes configurar estas variables de forma manual en el panel de control (Dashboard) de Render o Railway bajo la pestaña "Environment Variables":
   - `DB_HOST` = (Tu nuevo host de Supabase/Render Postgres)
   - `DB_PORT` = 5432
   - `DB_NAME` = tronquitos
   - `DB_USER` = (tu usuario db)
   - `DB_PASSWORD` = (tu password db)

3. **CORS (Crucial)**
   Actualmente tu `app.py` tiene `CORS(app)`. Esto está bien para pruebas, pero en producción deberías limitarlo al dominio de tu Vercel (ej. `tronquitos.vercel.app`) para que no cualquier página web pueda consumir tu base de datos:
   ```python
   # en app.py
   CORS(app, resources={r"/api/*": {"origins": ["https://tu-dominio-frontend.com"]}})
   ```

---

## 3. Flujo Correcto con Git y GitHub

Ya he inicializado tu repositorio Git locálmente y he creado un archivo `.gitignore` para ignorar secretos (`.env`) o archivos temporales.

1. Entra a github.com y crea un nuevo repositorio (vacío) llamado `tronquitos-app`.
2. En tu terminal de VSCode (estando en la carpeta `TRONQUITOS`), pega estos comandos para linkear tu carpeta subida:
   ```bash
   git branch -M main
   git remote add origin https://github.com/tu_usuario/tronquitos-app.git
   git push -u origin main
   ```
3. Luego de este `push`, Render y Vercel te permitirán hacer "Deploy from Github" detectando tus ramas automáticamente en sus páginas.
