#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║      🚀 INICIANDO CLASSIFICADOR DE DOCUMENTOS                    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

cd ~/document_classifier_project

# Parar processos antigos
echo "🧹 Limpando processos antigos..."
pkill -f "api.py" 2>/dev/null
pkill -f "servidor_web.py" 2>/dev/null
sleep 2

# Iniciar API
echo ""
echo -e "${BLUE}🔧 Iniciando API (porta 5000)...${NC}"
nohup python3 api.py > api.log 2>&1 &
API_PID=$!
sleep 3

# Verificar se API está rodando
if curl -s http://localhost:5000/health > /dev/null; then
    echo -e "${GREEN}✅ API iniciada com sucesso! (PID: $API_PID)${NC}"
else
    echo -e "${YELLOW}⚠️  API pode não estar pronta ainda...${NC}"
fi

# Iniciar Frontend
echo ""
echo -e "${BLUE}🌐 Iniciando Frontend (porta 8080)...${NC}"
nohup python3 servidor_web.py > frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 2

echo -e "${GREEN}✅ Frontend iniciado! (PID: $FRONTEND_PID)${NC}"

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SISTEMA INICIADO!                          ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}📡 API:${NC}      http://localhost:5000"
echo -e "${GREEN}🌐 Frontend:${NC} http://localhost:8080"
echo ""
echo "📋 Logs:"
echo "   API:      tail -f ~/document_classifier_project/api.log"
echo "   Frontend: tail -f ~/document_classifier_project/frontend.log"
echo ""
echo "🛑 Para parar:"
echo "   kill $API_PID $FRONTEND_PID"
echo "   ou execute: pkill -f api.py && pkill -f servidor_web.py"
echo ""
echo -e "${YELLOW}💡 Abrindo navegador...${NC}"
echo ""

sleep 2
open http://localhost:8080

echo "✅ Pronto! Use Ctrl+C para sair (os servidores continuarão rodando)"
echo ""
