@echo off
setlocal
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
 echo Instala Node.js LTS 22 o superior desde https://nodejs.org y vuelve a abrir este archivo.
 pause
 exit /b 1
)
node -e "if(Number(process.versions.node.split('.')[0])<22)process.exit(1)"
if errorlevel 1 (
 echo Se necesita Node.js 22 o superior. Actualiza Node.js desde https://nodejs.org
 pause
 exit /b 1
)
echo Abre http://127.0.0.1:8765 en Edge o Chrome.
echo Manten esta ventana abierta mientras trabajas. Para cerrar, pulsa Ctrl+C.
node server.js
pause
