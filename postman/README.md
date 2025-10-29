# 🧪 Postman + Newman API Tests

Coleção completa de testes para a Document Classifier API.

## 📦 Arquivos

- `document-classifier-api.postman_collection.json` - Collection com todos os testes
- `document-classifier.postman_environment.json` - Environment para testes locais
- `document-classifier-production.postman_environment.json` - Environment para produção (Render)

## 🚀 Como Usar

### **Opção 1: Postman GUI**

1. Abra o Postman
2. Importe a collection:
   - `File` → `Import` → Selecione `document-classifier-api.postman_collection.json`
3. Importe o environment:
   - `File` → `Import` → Selecione `document-classifier.postman_environment.json`
4. Selecione o environment no dropdown (canto superior direito)
5. Execute os testes:
   - Individual: Clique em um request e clique em `Send`
   - Toda a collection: Clique em `...` → `Run collection`

### **Opção 2: Newman (CLI)**

#### **Instalar Newman:**
```bash
npm install -g newman
npm install -g newman-reporter-htmlextra
```

#### **Rodar testes localmente:**
```bash
# Todos os testes
newman run postman/document-classifier-api.postman_collection.json \
  -e postman/document-classifier.postman_environment.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export newman/report.html

# Apenas uma pasta (ex: Health Checks)
newman run postman/document-classifier-api.postman_collection.json \
  -e postman/document-classifier.postman_environment.json \
  --folder "Health Checks"
```

#### **Rodar testes em produção:**
```bash
newman run postman/document-classifier-api.postman_collection.json \
  -e postman/document-classifier-production.postman_environment.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export newman/report-production.html
```

## 📊 Estrutura dos Testes

### **1. Health Checks**
- ✅ `GET /health` - Verifica se API está online
- ✅ `GET /stats` - Estatísticas do modelo
- ❌ `GET /nonexistent` - Endpoint inexistente (404)

### **2. Classification**
- ✅ `POST /classify` - Advertisement (happy path)
- ✅ `POST /classify` - Scientific Article (happy path)
- ❌ `POST /classify` - Sem arquivo (400)
- ❌ `POST /classify` - Extensão inválida (400)
- ❌ `GET /classify` - Método errado (405)

### **3. Async Classification**
- ✅ `POST /classify/async` - Submissão assíncrona
- ✅ `GET /task/{task_id}` - Status da tarefa

### **4. Feedback**
- ✅ `POST /feedback` - Feedback correto
- ✅ `POST /feedback` - Feedback incorreto
- ✅ `GET /feedback/stats` - Estatísticas de feedback
- ❌ `POST /feedback` - Campos faltando (400)
- ❌ `POST /feedback` - JSON inválido (400)

## 🖼️ Imagens de Teste

**IMPORTANTE:** Antes de rodar os testes, você precisa adicionar imagens de teste ao diretório `test_images/`:

```
test_images/
├── advertisement.tif      # 1 imagem de advertisement
├── scientific.tif         # 1 imagem de artigo científico
└── invalid.jpg           # 1 arquivo .jpg (para teste negativo)
```

### **Como obter as imagens:**

1. **Advertisement:** Use qualquer .tif de propaganda/anúncio
2. **Scientific Article:** Use qualquer .tif de artigo científico
3. **Invalid:** Renomeie qualquer .jpg para `invalid.jpg`

**OU** use as imagens do dataset RVL-CDIP (se disponível).

## 🎯 Métricas dos Testes

Cada teste verifica:
- ✅ Status code correto
- ✅ Estrutura da resposta (campos obrigatórios)
- ✅ Tipos de dados corretos
- ✅ Tempo de resposta (< 30s para classificação)
- ✅ Validações de negócio

## 📈 Relatórios

Newman gera relatórios em:
- **CLI:** Output no terminal
- **HTML:** `newman/report.html` (com `newman-reporter-htmlextra`)

## 🔧 Troubleshooting

### **Erro: "Could not read file"**
- Verifique se as imagens de teste existem em `test_images/`
- Verifique os caminhos no environment

### **Erro: "ECONNREFUSED"**
- Certifique-se de que a API está rodando
- Verifique a URL no environment (`base_url`)

### **Timeout nos testes de classificação:**
- Aumente o timeout no Newman: `--timeout-request 60000` (60s)
- Verifique se o OCR está funcionando

## 🚀 CI/CD Integration

Estes testes são executados automaticamente no GitHub Actions:
- ✅ PR aberto → Testes rodam
- ✅ Push para `main` → Testes rodam → Deploy

Ver `.github/workflows/ci.yml` para configuração.

