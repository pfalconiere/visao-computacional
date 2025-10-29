#!/bin/bash

# ============================================
# 🧪 Script de Testes - Document Classifier
# ============================================

set -e  # Exit on error

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}   🧪 DOCUMENT CLASSIFIER - TESTES     ${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

# Verificar se dependências estão instaladas
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest não encontrado!${NC}"
    echo -e "${YELLOW}Instalando dependências...${NC}"
    python3 -m pip install -r requirements-dev.txt --quiet || {
        echo -e "${RED}❌ Falha ao instalar dependências!${NC}"
        echo -e "${YELLOW}Execute manualmente: python3 -m pip install -r requirements-dev.txt${NC}"
        exit 1
    }
fi

# Modo de teste (default: all)
MODE=${1:-all}

case "$MODE" in
    "unit"|"units"|"unittest")
        echo -e "${BLUE}🧪 Rodando TESTES UNITÁRIOS...${NC}"
        echo ""
        pytest tests/ \
            -v \
            --tb=short \
            --cov=. \
            --cov-report=term-missing \
            --cov-report=html \
            --junitxml=junit/test-results.xml
        ;;
    
    "api"|"newman")
        echo -e "${BLUE}🔬 Rodando TESTES DE API (Newman)...${NC}"
        echo ""
        
        # Verificar se Newman está instalado
        if ! command -v newman &> /dev/null; then
            echo -e "${RED}❌ Newman não encontrado!${NC}"
            echo -e "${YELLOW}Instale com: npm install -g newman newman-reporter-htmlextra${NC}"
            exit 1
        fi
        
        # Verificar se API está rodando
        if ! curl -s http://localhost:5000/health > /dev/null; then
            echo -e "${YELLOW}⚠️  API não está rodando em http://localhost:5000${NC}"
            echo -e "${YELLOW}   Inicie a API com: python api.py${NC}"
            exit 1
        fi
        
        # Criar diretório newman se não existir
        mkdir -p newman
        
        # Rodar Newman
        newman run postman/document-classifier-api.postman_collection.json \
            -e postman/document-classifier.postman_environment.json \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export newman/report.html \
            --timeout-request 60000
        
        echo ""
        echo -e "${GREEN}✅ Relatório salvo em: newman/report.html${NC}"
        ;;
    
    "happy")
        echo -e "${BLUE}✅ Rodando apenas HAPPY PATH...${NC}"
        echo ""
        pytest tests/ -v -k "happy_path"
        ;;
    
    "negative")
        echo -e "${BLUE}❌ Rodando apenas NEGATIVE PATH...${NC}"
        echo ""
        pytest tests/ -v -k "negative"
        ;;
    
    "quick"|"fast")
        echo -e "${BLUE}⚡ Rodando testes RÁPIDOS...${NC}"
        echo ""
        pytest tests/ -v --tb=short -x -q
        ;;
    
    "coverage"|"cov")
        echo -e "${BLUE}📊 Gerando relatório de COVERAGE...${NC}"
        echo ""
        pytest tests/ --cov=. --cov-report=html --cov-report=term
        echo ""
        echo -e "${GREEN}✅ Relatório salvo em: htmlcov/index.html${NC}"
        
        # Abrir relatório no navegador (MacOS/Linux)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open htmlcov/index.html
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            xdg-open htmlcov/index.html 2>/dev/null || echo "Abra: htmlcov/index.html"
        fi
        ;;
    
    "all"|"full")
        echo -e "${BLUE}🎯 Rodando TODOS OS TESTES...${NC}"
        echo ""
        
        # 1. Testes unitários
        echo -e "${YELLOW}[1/2] Testes Unitários...${NC}"
        pytest tests/ \
            -v \
            --tb=short \
            --cov=. \
            --cov-report=html \
            --junitxml=junit/test-results.xml
        
        echo ""
        echo -e "${GREEN}✅ Testes unitários concluídos!${NC}"
        echo ""
        
        # 2. Testes de API (se API estiver rodando)
        if curl -s http://localhost:5000/health > /dev/null; then
            echo -e "${YELLOW}[2/2] Testes de API (Newman)...${NC}"
            
            if command -v newman &> /dev/null; then
                mkdir -p newman
                newman run postman/document-classifier-api.postman_collection.json \
                    -e postman/document-classifier.postman_environment.json \
                    --reporters cli,htmlextra \
                    --reporter-htmlextra-export newman/report.html \
                    --timeout-request 60000
                
                echo ""
                echo -e "${GREEN}✅ Testes de API concluídos!${NC}"
            else
                echo -e "${YELLOW}⚠️  Newman não instalado, pulando testes de API${NC}"
            fi
        else
            echo -e "${YELLOW}[2/2] Pulando testes de API (API não está rodando)${NC}"
        fi
        ;;
    
    "clean")
        echo -e "${YELLOW}🧹 Limpando arquivos de teste...${NC}"
        rm -rf htmlcov/
        rm -rf .pytest_cache/
        rm -rf junit/
        rm -rf newman/
        rm -f coverage.xml
        rm -f .coverage
        echo -e "${GREEN}✅ Limpeza concluída!${NC}"
        exit 0
        ;;
    
    "help"|"-h"|"--help")
        echo "Uso: ./run_tests.sh [MODO]"
        echo ""
        echo "Modos disponíveis:"
        echo "  unit, unittest     - Rodar apenas testes unitários (pytest)"
        echo "  api, newman        - Rodar apenas testes de API (Newman)"
        echo "  happy              - Rodar apenas happy path"
        echo "  negative           - Rodar apenas negative path"
        echo "  quick, fast        - Rodar testes rápidos"
        echo "  coverage, cov      - Gerar relatório de coverage"
        echo "  all, full          - Rodar todos os testes (default)"
        echo "  clean              - Limpar arquivos de teste"
        echo "  help               - Mostrar esta ajuda"
        echo ""
        echo "Exemplos:"
        echo "  ./run_tests.sh              # Rodar tudo"
        echo "  ./run_tests.sh unit         # Apenas testes unitários"
        echo "  ./run_tests.sh api          # Apenas testes de API"
        echo "  ./run_tests.sh coverage     # Relatório de coverage"
        exit 0
        ;;
    
    *)
        echo -e "${RED}❌ Modo inválido: $MODE${NC}"
        echo "Use './run_tests.sh help' para ver os modos disponíveis."
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ TESTES CONCLUÍDOS!               ${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"

