import urllib.request
try:
    with urllib.request.urlopen("http://localhost:5000/api/reservations") as res:
        print("SUCCESS:", res.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code, e.read().decode())
