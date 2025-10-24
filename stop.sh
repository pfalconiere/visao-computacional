#!/bin/bash

echo "🛑 Parando servidores..."
pkill -f "api.py"
pkill -f "servidor_web.py"
sleep 1
echo "✅ Servidores parados!"
