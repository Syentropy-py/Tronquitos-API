import urllib.request
import json

data = {
    "Nombre": "Test API",
    "Teléfono": "555-0000",
    "Email": "test@test.com",
    "Personas": 4,
    "Fecha": "2026-06-04",
    "Hora": "15:00",
    "Sede": "Principal",
    "Mensaje": ""
}
req = urllib.request.Request(
    'http://localhost:5000/api/reservation',
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req) as res:
        print("SUCCESS:", res.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code, e.read().decode())
except Exception as e:
    print("OTHER ERROR:", getattr(e, 'read', lambda: str(e))())
