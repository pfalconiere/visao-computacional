# 🧪 Como Testar a API

## 1️⃣ Verificar se a API está rodando

```bash
# Verificar processo
ps aux | grep api.py

# Verificar porta
lsof -i :5000
```

Se não estiver rodando, inicie:

```bash
cd ~/document_classifier_project
python3 api.py
```

**IMPORTANTE:** Deixe esse terminal aberto! A API precisa estar rodando.

---

## 2️⃣ Testar Endpoints (em OUTRO terminal)

### ✅ Teste 1: Health Check (GET)

```bash
curl http://localhost:5000/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "message": "API está funcionando corretamente"
}
```

---

### ✅ Teste 2: Documentação (GET)

```bash
curl http://localhost:5000/
```

Ou abra no navegador: http://localhost:5000/

---

### ✅ Teste 3: Estatísticas (GET)

```bash
curl http://localhost:5000/stats
```

---

### ✅ Teste 4: Classificar Imagem (POST) 🎯

**Opção A - Usando cURL:**

```bash
# Ajuste o caminho para uma imagem real
curl -X POST -F "image=@/Users/test/Downloads/test/advertisement/2070421639.tif" \
  http://localhost:5000/classify
```

**Opção B - Usando o script Python:**

```bash
cd ~/document_classifier_project

# Testar automaticamente
python3 testar_api.py

# Ou classificar uma imagem específica
python3 testar_api.py /Users/test/Downloads/test/advertisement/sua_imagem.tif
```

---

## 3️⃣ Erros Comuns e Soluções

### ❌ "Connection refused" ou "Failed to connect"

**Problema:** API não está rodando

**Solução:**
```bash
cd ~/document_classifier_project
python3 api.py
```

---

### ❌ "Method Not Allowed"

**Problema:** Você está usando GET em vez de POST no /classify

**Solução correta:**
```bash
# ❌ ERRADO (GET)
curl http://localhost:5000/classify

# ✅ CORRETO (POST com imagem)
curl -X POST -F "image=@documento.tif" http://localhost:5000/classify
```

---

### ❌ "Nenhuma imagem foi enviada"

**Problema:** Faltou enviar a imagem ou campo está errado

**Solução:**
```bash
# O campo deve se chamar "image"
curl -X POST -F "image=@/caminho/completo/para/imagem.tif" \
  http://localhost:5000/classify
```

---

### ❌ "Formato de arquivo não suportado"

**Problema:** Extensão não permitida

**Formatos suportados:** .png, .jpg, .jpeg, .tif, .tiff, .bmp

---

## 4️⃣ Exemplos Práticos

### Exemplo 1: Classificar uma imagem

```bash
cd ~/document_classifier_project

# Usar uma imagem do dataset
curl -X POST \
  -F "image=@/Users/test/Downloads/test/advertisement/2070421639.tif" \
  http://localhost:5000/classify | python3 -m json.tool
```

---

### Exemplo 2: Classificar várias imagens

Crie um arquivo `testar_multiplas.sh`:

```bash
#!/bin/bash
cd /Users/test/Downloads/test/advertisement

for img in *.tif | head -5; do
  echo "Testando: $img"
  curl -X POST -F "image=@$img" http://localhost:5000/classify | \
    python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"  → {data['classification']} ({data['confidence']:.1%})\")"
  echo ""
done
```

Execute:
```bash
chmod +x testar_multiplas.sh
./testar_multiplas.sh
```

---

### Exemplo 3: Python Script

```python
import requests
from pathlib import Path

# URL da API
API_URL = "http://localhost:5000/classify"

# Caminho da imagem
imagem_path = "/Users/test/Downloads/test/advertisement/2070421639.tif"

# Enviar imagem
with open(imagem_path, 'rb') as f:
    files = {'image': f}
    response = requests.post(API_URL, files=files)

# Ver resultado
if response.status_code == 200:
    result = response.json()
    print(f"✅ Classificação: {result['classification']}")
    print(f"📊 Score: {result['score']}")
    print(f"🎯 Confiança: {result['confidence']:.1%}")
else:
    print(f"❌ Erro: {response.json()}")
```

---

## 5️⃣ Teste Completo Passo a Passo

### Terminal 1: Iniciar API

```bash
cd ~/document_classifier_project
python3 api.py
```

Aguarde ver:
```
🚀 INICIANDO API DE CLASSIFICAÇÃO DE DOCUMENTOS
📡 Servidor: http://localhost:5000
```

### Terminal 2: Testar

```bash
# 1. Health check
curl http://localhost:5000/health

# 2. Stats
curl http://localhost:5000/stats

# 3. Classificar imagem
curl -X POST \
  -F "image=@/Users/test/Downloads/test/advertisement/2070421639.tif" \
  http://localhost:5000/classify | python3 -m json.tool
```

---

## 6️⃣ Parar a API

```bash
# Encontrar o processo
ps aux | grep api.py

# Matar o processo
kill -9 <PID>

# Ou se iniciou com Ctrl+C no terminal
```

---

## 7️⃣ Logs e Debug

Ver logs da API:

```bash
cd ~/document_classifier_project
tail -f api.log
```

---

## ✅ Checklist de Teste

- [ ] API está rodando (`ps aux | grep api.py`)
- [ ] `/health` retorna status healthy
- [ ] `/stats` retorna estatísticas
- [ ] `/classify` com POST funciona
- [ ] Imagem é classificada corretamente
- [ ] Resposta JSON está completa

---

**Dica:** Use o Postman ou Insomnia para testes mais visuais!
