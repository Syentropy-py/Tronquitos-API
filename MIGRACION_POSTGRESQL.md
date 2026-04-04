# 🗄️ MIGRACIÓN DE SQLITE A POSTGRESQL - GUÍA DE CONFIGURACIÓN

## ✅ Cambios Realizados

Hemos migrado completamente tu proyecto de SQLite a PostgreSQL. Aquí está lo que se cambió:

### Archivos Modificados:
- ✓ `backend/requirements.txt` - Agregadas dependencias: `psycopg2-binary`, `python-dotenv`, `gunicorn`
- ✓ `backend/models.py` - Esquemas SQL convertidos a sintaxis PostgreSQL
- ✓ `backend/database.py` - Completamente reescrito para usar `psycopg2`
- ✓ `backend/init_db.py` - Adaptado para PostgreSQL
- ✓ `backend/app.py` - Removidas referencias a SQLite, añadida carga de variables de entorno
- ✓ `backend/.env` - Archivo de configuración con variables de conexión

---

## 🚀 INSTALACIÓN DE POSTGRESQL

### Opción 1: Windows (Más Fácil) 
Descargar e instalar desde: https://www.postgresql.org/download/windows/
- Instalar con password: `postgres` (o el que prefieras)
- Puerto: `5432` (default)
- Crear base de datos: `tronquitos`

### Opción 2: Docker (Si tienes Docker instalado)
```bash
docker run --name postgres-tronquitos -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=tronquitos -p 5432:5432 -d postgres:latest
```

### Opción 3: WSL (Windows Subsystem for Linux)
```bash
sudo apt update && sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

---

## ⚙️ CONFIGURACIÓN LOCAL

### 1. Instalar dependencias Python
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar conexión a PostgreSQL

Editar `backend/.env` con tus credenciales:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tronquitos
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui
```

### 3. Inicializar base de datos
```bash
python backend/init_db.py
```

Deberías ver:
```
[v] Tabla 'branches' creada/verificada
[v] Tabla 'daily_capacity' creada/verificada
[v] Tabla 'tables' creada/verificada
[v] Tabla 'reservations' creada/verificada
[v] Tabla 'contacts' creada/verificada
[v] Tabla 'opinions' creada/verificada
[v] Tabla 'events' creada/verificada
[v] 6 sedes creadas
[v] 60 mesas creadas (10 por sede)
[✓] Base de datos inicializada exitosamente en localhost:5432/tronquitos
```

### 4. Iniciar el servidor
```bash
python backend/app.py
```

Deberías ver:
```
Running on http://127.0.0.1:5000
```

---

## 🌐 DESPLIEGUE EN PRODUCTION

### Con Railway.app (RECOMENDADO)

1. **Crear instancia PostgreSQL en Railway**
   - Sign up en https://railway.app
   - Crear nuevo proyecto
   - Agregar servicio PostgreSQL
   - Copiar las variables de conexión

2. **Configurar variables en Railway**
   ```
   DB_HOST=tuhost.railway.app
   DB_PORT=5432
   DB_NAME=railway
   DB_USER=postgres
   DB_PASSWORD=tu_contraseña_generada
   N8N_WEBHOOK_URL=tu_webhook
   WHATSAPP_NUMBER=tu_numero
   ```

3. **Crear Procfile en raíz del proyecto**
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
   ```

4. **Deploy desde GitHub**
   - Conectar repositorio GitHub
   - Railway deployará automáticamente

---

## 🔒 DIFERENCIAS IMPORTANTES

### SQLite → PostgreSQL

| Aspecto | SQLite | PostgreSQL |
|--------|--------|-----------|
| **Instalación** | Automática en Python | Requiere servidor |
| **Archivos** | 1 archivo `.db` | Base de datos centralizada |
| **Escala** | Hasta ~10K usuarios | Millones de usuarios |
| **Concurrencia** | Limitada | Excelente |
| **Backup** | Copiar archivo | `pg_dump` / herramientas |
| **Costo** | Gratis | Gratis (self-hosted) o $$ (cloud) |

---

## 📋 CHECKLIST PRE-PRODUCCIÓN

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `tronquitos` creada
- [ ] Variables `.env` configuradas
- [ ] `python backend/init_db.py` ejecutado sin errores
- [ ] `python backend/app.py` inicia correctamente
- [ ] Frontend accesible en http://localhost:5000
- [ ] Pruebas de reserva funcionan
- [ ] N8N webhook configurado (si aplica)

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Error: `psycopg2.OperationalError: could not connect to server`
→ PostgreSQL no está corriendo o credenciales incorrectas en `.env`

### Error: `database "tronquitos" does not exist`
→ Crear la BD: `createdb -U postgres tronquitos`

### Error: `relation "branches" does not exist`
→ Ejecutar: `python backend/init_db.py`

### Error: `import psycopg2`
→ Instalar: `pip install psycopg2-binary`

---

## 📚 REFERENCIAS

- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Psycopg2 Docs**: https://www.psycopg.org/
- **Railway.app Docs**: https://docs.railway.app/
- **Gunicorn Docs**: https://gunicorn.org/

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Migración completada: SQLite → PostgreSQL
2. ⏭️ **Instalar PostgreSQL y ejecutar init_db.py**
3. ⏭️ **Testear localmente**
4. ⏭️ **Deploy en Railway.app o tu hosting favorito**

¿Necesitas ayuda con algún paso?
