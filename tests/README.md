# 🧪 Testes Unitários - Document Classifier

Suite completa de testes unitários para o Document Classifier.

## 📁 Estrutura

```
tests/
├── __init__.py                    # Inicializador
├── test_classificador.py          # Testes do ClassificadorFinal
├── test_api.py                    # Testes dos endpoints da API
├── test_text_analyzer.py          # Testes do análise de texto/OCR
├── test_paragraph_detector.py     # Testes do detector de parágrafos
└── README.md                      # Este arquivo
```

## 🚀 Como Rodar

### **Instalação de Dependências:**
```bash
pip install -r requirements-dev.txt
```

### **Rodar todos os testes:**
```bash
pytest tests/ -v
```

### **Rodar um arquivo específico:**
```bash
pytest tests/test_api.py -v
```

### **Rodar um teste específico:**
```bash
pytest tests/test_api.py::TestHealthEndpoints::test_health_endpoint_happy_path -v
```

### **Rodar com coverage:**
```bash
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html  # Abrir relatório
```

### **Rodar apenas Happy Path:**
```bash
pytest tests/ -v -k "happy_path"
```

### **Rodar apenas Negative Path:**
```bash
pytest tests/ -v -k "negative"
```

## 📊 Métricas

Cada módulo de teste cobre:
- ✅ **Happy Path** (fluxos positivos esperados)
- ❌ **Negative Path** (erros, validações, edge cases)

### **Coverage Esperado:**
- `classificador_final.py`: **80%+**
- `api.py`: **70%+**
- `text_analyzer*.py`: **60%+**
- `paragraph_detector.py`: **60%+**

## 🎯 Testes por Módulo

### **1. test_classificador.py**

Testa `ClassificadorFinal`:

**Happy Path:**
- ✅ Classificação de advertisement
- ✅ Classificação de artigo científico
- ✅ Extração de features visuais
- ✅ Verificação de conformidade (conforme)

**Negative Path:**
- ❌ Arquivo inexistente
- ❌ Formato inválido (.txt)
- ❌ Imagem corrompida
- ❌ Documento não conforme (poucas palavras)
- ❌ Documento não conforme (poucos parágrafos)
- ❌ Parâmetros inválidos

### **2. test_api.py**

Testa endpoints da API Flask:

**Happy Path:**
- ✅ GET / (root)
- ✅ GET /health
- ✅ GET /stats
- ✅ GET /api-info
- ✅ POST /classify (com .tif válido)
- ✅ POST /classify/async
- ✅ GET /task/{task_id}
- ✅ POST /feedback (correto e incorreto)
- ✅ GET /feedback/stats

**Negative Path:**
- ❌ GET /nonexistent (404)
- ❌ POST /classify (sem arquivo)
- ❌ POST /classify (extensão inválida)
- ❌ GET /classify (método errado)
- ❌ POST /classify (parâmetros inválidos)
- ❌ POST /feedback (campos faltando)
- ❌ POST /feedback (JSON inválido)

### **3. test_text_analyzer.py**

Testa análise de texto e OCR:

**Happy Path:**
- ✅ Import text_analyzer
- ✅ Import text_analyzer_optimized
- ✅ extract_text retorna string
- ✅ analyze_text retorna dict
- ✅ frequent_words tem formato correto

**Negative Path:**
- ❌ extract_text (arquivo inexistente)
- ❌ analyze_text (imagem corrompida)
- ❌ analyze_text (idioma inválido)
- ❌ analyze_fast (timeout)

### **4. test_paragraph_detector.py**

Testa detecção de parágrafos:

**Happy Path:**
- ✅ Import paragraph_detector
- ✅ detect_paragraphs retorna número
- ✅ Diferentes estratégias funcionam
- ✅ Imagem vazia retorna 0

**Negative Path:**
- ❌ detect_paragraphs (arquivo inexistente)
- ❌ detect_paragraphs (imagem corrompida)
- ❌ detect_paragraphs (arquivo não-imagem)

## 🔧 Fixtures

Fixtures disponíveis (criadas automaticamente):

- `client` - Cliente de teste da API Flask
- `mock_tif_file` - Arquivo .tif sintético
- `mock_image_advertisement` - Imagem sintética de advertisement
- `mock_image_scientific` - Imagem sintética de artigo científico
- `mock_image_with_text` - Imagem com texto para OCR
- `mock_image_with_paragraphs` - Imagem com múltiplos parágrafos

## 📝 Convenções

### **Nomenclatura:**
```python
def test_<funcao>_<cenario>_<tipo>():
    """
    HAPPY/NEGATIVE PATH: Descrição do teste
    
    Input: Descrição do input
    Expected: Resultado esperado
    """
    # Arrange
    # Act
    # Assert
```

### **Tipos:**
- `_happy_path` - Teste de fluxo positivo
- `_negative` - Teste de erro/validação

### **Assertions:**
- Use `assert` para validações simples
- Use `pytest.raises()` para exceções esperadas
- Use `pm.test()` no Postman/Newman

## 🐛 Debugging

### **Rodar em modo verboso:**
```bash
pytest tests/ -vv -s
```

### **Rodar com pdb (debugger):**
```bash
pytest tests/test_api.py --pdb
```

### **Ver print statements:**
```bash
pytest tests/ -s
```

### **Rodar apenas testes que falharam:**
```bash
pytest tests/ --lf
```

## 🚫 Ignorar Testes

### **Skip temporário:**
```python
@pytest.mark.skip(reason="WIP")
def test_something():
    pass
```

### **Skip condicional:**
```python
@pytest.mark.skipif(condition, reason="...")
def test_something():
    pass
```

## 🎨 Code Coverage

Após rodar os testes com coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

Abra `htmlcov/index.html` para ver:
- Linhas cobertas vs não cobertas
- Branches não testados
- Arquivos com baixa coverage

## ⚙️ Configuração

Ver `pytest.ini` para configurações globais:
- Timeouts
- Markers customizados
- Paths
- Coverage settings

## 🔗 Integração CI/CD

Estes testes rodam automaticamente em:
- **Pre-commit:** Antes de cada commit (local)
- **GitHub Actions:** Em cada push/PR
- **Deploy:** Bloqueiam deploy se falharem

Ver `.github/workflows/ci.yml` para detalhes.

