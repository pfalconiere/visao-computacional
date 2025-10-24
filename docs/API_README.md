# 🚀 API de Classificação de Documentos

API REST para classificar documentos como **Advertisement** ou **Scientific Article** usando o modelo treinado com o dataset RVL-CDIP.

## ⚡ Início Rápido

### 1. Iniciar a API

```bash
cd ~/document_classifier_project
python3 api.py
```

A API estará disponível em: **http://localhost:5000**

### 2. Testar a API

Em outro terminal:

```bash
cd ~/document_classifier_project
python3 testar_api.py
```

## 📡 Endpoints

### `GET /` - Documentação
Retorna informações sobre a API e como usá-la.

```bash
curl http://localhost:5000/
```

### `GET /health` - Status
Verifica se a API está funcionando.

```bash
curl http://localhost:5000/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "message": "API está funcionando corretamente"
}
```

### `GET /stats` - Estatísticas
Retorna estatísticas do modelo treinado.

```bash
curl http://localhost:5000/stats
```

**Resposta:**
```json
{
  "model": "Classificador Final RVL-CDIP",
  "training_samples": 5085,
  "accuracy": {
    "advertisements": "70.5%",
    "scientific_articles": "94.2%",
    "overall": "82.3%"
  },
  "features_used": [
    "desvio_altura",
    "altura_media",
    "densidade_texto",
    "largura_media",
    "num_componentes",
    "colunas_detectadas"
  ]
}
```

### `POST /classify` - Classificar Imagem 🎯

Classifica uma imagem enviada.

**Usando cURL:**
```bash
curl -X POST -F "image=@documento.tif" http://localhost:5000/classify
```

**Usando Python:**
```python
import requests

with open('documento.tif', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/classify', files=files)
    result = response.json()
    
print(f"Tipo: {result['classification']}")
print(f"Confiança: {result['confidence']}")
```

**Usando JavaScript (Fetch):**
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('http://localhost:5000/classify', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log('Classificação:', data.classification);
    console.log('Confiança:', data.confidence);
});
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "filename": "documento.tif",
  "classification": "scientific_article",
  "score": -12,
  "confidence": 0.857,
  "features": {
    "altura_media": 9.68,
    "largura_media": 12.4,
    "desvio_altura": 17.21,
    "aspect_ratio": 1.75,
    "colunas_detectadas": 1,
    "densidade_texto": 0.110,
    "num_componentes": 260,
    "transicoes_layout": 17
  },
  "interpretation": {
    "type": "📚 Scientific Article",
    "confidence_level": "Alta",
    "characteristics": [
      "Texto uniforme",
      "Letras menores",
      "Muitos componentes de texto"
    ]
  }
}
```

**Resposta de Erro:**
```json
{
  "error": "Formato de arquivo não suportado",
  "supported_formats": ["png", "jpg", "jpeg", "tif", "tiff", "bmp"]
}
```

## 🧪 Exemplos de Uso

### Exemplo 1: Classificar uma imagem

```bash
cd ~/document_classifier_project
python3 testar_api.py /Users/test/Downloads/test/advertisement/imagem.tif
```

### Exemplo 2: Classificar múltiplas imagens

```python
import requests
from pathlib import Path

API_URL = "http://localhost:5000/classify"

for img_path in Path('/Users/test/Downloads/test/advertisement').glob('*.tif')[:10]:
    with open(img_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"{img_path.name}: {result['classification']} ({result['confidence']:.1%})")
```

### Exemplo 3: Integração com aplicação web

```html
<!DOCTYPE html>
<html>
<head>
    <title>Classificador de Documentos</title>
</head>
<body>
    <h1>📄 Classificador de Documentos</h1>
    
    <input type="file" id="imageInput" accept="image/*">
    <button onclick="classificar()">Classificar</button>
    
    <div id="resultado"></div>
    
    <script>
        async function classificar() {
            const fileInput = document.getElementById('imageInput');
            const resultDiv = document.getElementById('resultado');
            
            if (!fileInput.files[0]) {
                alert('Selecione uma imagem');
                return;
            }
            
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            
            resultDiv.innerHTML = 'Processando...';
            
            try {
                const response = await fetch('http://localhost:5000/classify', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = `
                        <h2>${data.interpretation.type}</h2>
                        <p><strong>Confiança:</strong> ${(data.confidence * 100).toFixed(1)}%</p>
                        <p><strong>Score:</strong> ${data.score}</p>
                        <h3>Características:</h3>
                        <ul>
                            ${data.interpretation.characteristics.map(c => `<li>${c}</li>`).join('')}
                        </ul>
                    `;
                } else {
                    resultDiv.innerHTML = `<p>Erro: ${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<p>Erro ao conectar com a API: ${error}</p>`;
            }
        }
    </script>
</body>
</html>
```

## 🔒 Segurança

⚠️ **Importante:** Esta é uma API de desenvolvimento. Para produção, considere:

- Adicionar autenticação (API keys, JWT)
- Limitar taxa de requisições (rate limiting)
- Validar e sanitizar inputs
- Usar HTTPS
- Configurar CORS apropriadamente
- Adicionar logs de auditoria

## 🐛 Solução de Problemas

### Erro: "Connection refused"
```bash
# Verifique se a API está rodando
ps aux | grep api.py

# Inicie a API
python3 api.py
```

### Erro: "ModuleNotFoundError: No module named 'flask'"
```bash
pip3 install --user flask flask-cors
```

### Erro: "Address already in use"
```bash
# Encontre o processo usando a porta 5000
lsof -i :5000

# Mate o processo
kill -9 <PID>

# Ou use outra porta
# Edite api.py e mude: app.run(port=5001)
```

## 📊 Performance

- **Tempo de resposta**: ~50ms por imagem
- **Throughput**: ~20 requisições/segundo
- **Tamanho máximo**: 16MB por imagem
- **Formatos suportados**: PNG, JPG, JPEG, TIF, TIFF, BMP

## 🚀 Deploy em Produção

### Usando Gunicorn (recomendado)

```bash
# Instalar Gunicorn
pip3 install gunicorn

# Rodar com 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

### Usando Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

```bash
# Build
docker build -t document-classifier-api .

# Run
docker run -p 5000:5000 document-classifier-api
```

## 📝 Licença

Este projeto é para fins educacionais e de pesquisa.

---

**Desenvolvido com 💙 usando Flask e o modelo treinado RVL-CDIP**
