@echo off
REM ============================================================
REM LOS TRONQUITOS - Script de Inicio Rápido para Demo
REM ============================================================
REM Ejecutar este archivo para iniciar el sistema completo
REM ============================================================

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║        LOS TRONQUITOS - INICIO RÁPIDO                ║
echo ║        Sistema de Gestión de Reservas v1.0            ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Configurar encoding UTF-8
set PYTHONIOENCODING=utf-8

REM Cambiar a directorio del proyecto
cd /d "%~dp0"

echo [1/3] Verificando sistema...
python VERIFICAR_SISTEMA.py
if errorlevel 1 (
    echo.
    echo ⚠️  Error en verificación. Abortando...
    pause
    exit /b 1
)

echo.
echo [2/3] Iniciando backend Flask...
echo.
echo ℹ️  Frontend disponible en: http://localhost:5000
echo ℹ️  N8N Cloud Webhooks: https://nikkaoyy.app.n8n.cloud/webhook-test/reservas
echo ℹ️  Presiona CTRL+C para detener el servidor
echo.

start cmd /k "cd backend && python -Xutf8=1 app.py"

timeout /t 3

echo.
echo [3/3] Iniciando demostración automática...
echo.

python DEMO_PRESENTACION.py

echo.
echo ============================================================
echo ✅ Demostración completada
echo ============================================================
echo.
pause
