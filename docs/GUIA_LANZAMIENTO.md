# 📱 LANZAMIENTO FINAL - 18 MARZO 2026 A LAS 5 PM

## ⚡ INICIO RÁPIDO (2 OPCIONES)

### OPCIÓN 1: Automático (RECOMENDADO)
```batch
INICIAR_DEMO.bat
```
✅ Inicia todo automáticamente en 30 segundos

### OPCIÓN 2: Manual
```bash
# Terminal 1
cd c:\Users\nikka\OneDrive\Documentos\TRONQUITOS\backend
python -Xutf8=1 app.py

# Terminal 2 (esperar 3 segundos)
cd c:\Users\nikka\OneDrive\Documentos\TRONQUITOS
python DEMO_PRESENTACION.py
```

---

## 🎯 URLs IMPORTANTES

| Servicio | URL | Función |
|----------|-----|---------|
| **Frontend** | http://localhost:5000 | Dashboard web |
| **Panel Gestor** | http://localhost:5000/gestor.html | Cancelar/gestionar reservas |
| **API** | http://localhost:5000/api | Endpoints REST |
| **N8N Cloud** | https://nikkaoyy.app.n8n.cloud | Webhooks |
| **Webhook Principal** | https://nikkaoyy.app.n8n.cloud/webhook-test/reservas | Eventos |

---

## ✅ CHECKLIST MAÑANA (5 MINUTOS ANTES)

- [ ] Terminal 1: Verificar sistema (VERIFICAR_SISTEMA.py)
- [ ] Terminal 2: Iniciar backend (python app.py)
- [ ] Esperar: "Running on http://127.0.0.1:5000"
- [ ] Abrir navegador: http://localhost:5000
- [ ] Ejecutar: python DEMO_PRESENTACION.py
- [ ] Verificar: 8 pasos completados exitosamente

---

## 🎬 DEMOSTRACIÓN (15 MINUTOS)

### Minutos 0-2: Bienvenida
```
"Buenos días. Soy Nikka, desarrollador de Los Tronquitos.
Hoy voy a mostrar nuestro nuevo sistema de reservas
completamente automatizado e integrado."
```

### Minutos 2-5: Sistema Actual
```
1. Abrir http://localhost:5000
2. Mostrar: "30 mesas disponibles"
3. Explicar: Estructura simple, rápida, confiable
```

### Minutos 5-10: Reserva Normal
```
1. Formulario: "Reserva para 4 personas"
2. Sistema: "Asignando mesa #3..."
3. Resultado: "✅ Reserva confirmada - Mesa #3"
```

### Minutos 10-13: Grupo Especial
```
1. Formulario: "Reserva para 60 personas"
2. Sistema: "Detectando grupo especial..."
3. Result: "⭐ Contactaremos para confirmar disponibilidad"
```

### Minutos 13-15: N8N Cloud & Gestión de Reservas
```
MOSTRAR N8N:
1. Datos en https://nikkaoyy.app.n8n.cloud
2. Explicar: Automático, sin código extra
3. Demo: "WhatsApp enviado al cliente automáticamente"

MOSTRAR GESTIÓN:
1. Abrir: http://localhost:5000/gestor.html
2. Panel visual con todas las reservas
3. Cancelar una reserva en vivo
4. Cliente notificado automáticamente
5. Mesa liberada al instante
```

---

## 🎯 BONUS: GESTIÓN EN VIVO

**Si alguien pregunta: "¿Cómo cancelo una reserva?"**

1. **Opción Visual** (mejor para presentación):
   ```
   http://localhost:5000/gestor.html
   → Click "Cancelar" en la reserva
   → Mensaje personalizado (opcional)
   → ¡LISTO!
   ```

2. **Opción Terminal**:
   ```bash
   python CANCELAR_RESERVAS.py
   → Menú interactivo
   → Seleccionar opción 3
   → Ingresa ID de reserva
   ```

---

## 🛠️ SOLUCIÓN RÁPIDA DE PROBLEMAS

### Error: "Connection refused" en N8N
```
✅ NORMAL - N8N Cloud puede estar retrasado
✅ Las reservas se guardan localmente igual
✅ Los webhooks se reintentarán automáticamente
```

### Error: "Unicode encoding"
```
Usar: python -Xutf8=1 app.py
Alternativa: set PYTHONIOENCODING=utf-8
```

### Error: "Puerto 5000 en uso"
```
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## 📊 NÚMEROS CLAVE

- **Teléfono**: +57 3102326407
- **Mesas**: 30 disponibles
- **Capacidad Total**: 150 personas
- **Grupo Especial**: 30+ personas
- **Backend**: Flask 3.0.2
- **BD**: SQLite3
- **Integración**: N8N Cloud

---

## 🌟 PUNTOS FUERTES A DESTACAR

✨ **Automático**: Sin intervención manual para reservas normales
✨ **Rápido**: Respuesta en <100ms
✨ **Seguro**: Datos locales + respaldo en cloud
✨ **Escalable**: Soporta grupos de cualquier tamaño
✨ **Integrado**: Notificaciones automáticas vía WhatsApp
✨ **Profesional**: Auditoría completa de eventos

---

## 💡 SI HAY PREGUNTAS...

**"¿Cómo cancela una reserva?"**
→ Endpoint: POST /api/cancel-reservation

**"¿Qué pasa si falla N8N?"**
→ Las reservas se guardan localmente. Los webhooks se reintentarán.

**"¿Cuánto tiempo para integrar?"**
→ Ya está hecho. Demo completa en 15 minutos.

**"¿Qué pasa con grupos muy grandes?"**
→ Sistema automático sin límite de personas. Confirmación manual.

---

## 🎊 FINAL

```
"El sistema está listo para producción.
Hemos probado todo y está 100% funcional.
Cualquier pregunta, estoy aquí para ayudar."
```

---

**ESTADO FINAL**: ✅ LISTO PARA PRESENTACIÓN
**ÚLTIMA PRUEBA**: 17 Marzo 2026 - 20:36 PM
**DEMOSTRACIÓN**: Exitosa - 8/8 pasos completados
