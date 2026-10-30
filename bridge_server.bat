@echo off
title robloxstudio-mcp server (leave open)
:loop
echo [%date% %time%] starting server >> "C:\Users\Nitro\.kiro\crew\workspace\town\bridge_server_log.txt"
node "C:\Users\Nitro\AppData\Local\npm-cache\_npx\2dca8ffe7201fd5b\node_modules\robloxstudio-mcp\dist\index.js" 2>> "C:\Users\Nitro\.kiro\crew\workspace\town\bridge_server_log.txt"
echo [%date% %time%] server exited with code %errorlevel%, restarting in 5s >> "C:\Users\Nitro\.kiro\crew\workspace\town\bridge_server_log.txt"
timeout /t 5 /nobreak >nul
goto loop
