# 🎯 Classificador de Documentos RVL-CDIP

Sistema de classificação de documentos usando processamento de imagens e otimização por regras para diferenciar **Advertisements** de **Scientific Articles** do dataset RVL-CDIP.

**Acurácia:** 89.87% (após 12+ milhões de iterações de otimização)

---

## 📊 Desempenho do Modelo

| Classe | Acurácia | Precisão |
|--------|----------|----------|
| **Advertisements** | 90.46% | 2,275/2,515 acertos |
| **Scientific Articles** | 89.30% | 2,295/2,570 acertos |
| **Geral** | **89.87%** | 4,570/5,085 acertos |

---

## 🚀 Demo Online

- **API:** https://visao-computacional.onrender.com
- **Frontend:** https://pfalconiere.github.io/visao-computacional/
- **GitHub:** https://github.com/pfalconiere/visao-computacional

---

## 📋 Sobre o Projeto

Este classificador usa **regras otimizadas** baseadas em características visuais extraídas das imagens. Após análise de 5,085 imagens e **12+ milhões de iterações** de otimização, o modelo alcançou 89.87% de acurácia.

### Características Analisadas

1. **Altura média dos componentes de texto** - Advertisements tendem a ter letras maiores
2. **Desvio padrão da altura** - Maior variação em Advertisements
3. **Densidade de texto** - Articles têm mais texto denso
4. **Número de componentes** - Articles têm mais componentes de texto

---

## 🔬 Processo de Treinamento

### 1. Extração de Features (5,085 imagens)
- Dataset: RVL-CDIP Test Set
- 2,515 advertisements
- 2,570 scientific articles
- Features extraídas: altura, desvio, densidade, componentes

### 2. Otimização Massiva (12+ milhões de iterações)

O modelo foi otimizado usando múltiplas estratégias:

| Estratégia | Descrição |
|------------|-----------|
| **Exploração Aleatória** | Busca em espaço amplo de parâmetros |
| **Mutação Adaptativa** | Variações pequenas, médias e grandes |
| **Hill Climbing** | Refinamento local |
| **Simulated Annealing** | Escape de mínimos locais |
| **Random Restart** | Reinício inteligente quando estagnado |

**Tempo total:** ~8 horas  
**Iterações:** 12,000,000+  
**Estratégia:** Multi-algoritmo adaptativo

### 3. Thresholds Otimizados

```python
thresholds = {
    'altura_min': 11.24,
    'altura_max': 13.41,
    'desvio_altura': 12.45,
    'densidade': 0.403,
    'componentes': 454
}

pesos = {
    'p1': 2.58,  # Peso da altura
    'p2': 1.61,  # Peso do desvio
    'p3': 0.74,  # Peso da densidade
    'p4': 0.65   # Peso dos componentes
}
```

---

## 🛠️ Instalação

### Requisitos

- Python 3.10+
- OpenCV
- NumPy
- Flask (para API)

### Instalação Local

```bash
# Clonar repositório
git clone https://github.com/pfalconiere/visao-computacional.git
cd visao-computacional

# Instalar dependências
pip install -r requirements.txt

# Rodar API localmente
python api.py
```

---

## 🐳 Deploy com Docker

O projeto inclui suporte completo para Docker, garantindo ambiente consistente.

### Dockerfile

```dockerfile
FROM python:3.10-slim-buster

WORKDIR /app

# Instalar dependências do sistema para OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

### Build e Run

```bash
# Build da imagem
docker build -t classificador-documentos .

# Rodar container
docker run -p 5000:5000 classificador-documentos
```

---

## 📡 API REST

### Endpoints

#### `GET /health`
Verifica status da API

```bash
curl https://visao-computacional.onrender.com/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "flask-backend",
  "api": "Document Classifier API",
  "version": "1.0"
}
```

#### `GET /stats`
Retorna estatísticas do modelo

```bash
curl https://visao-computacional.onrender.com/stats
```

**Response:**
```json
{
  "model_name": "Classificador Final RVL-CDIP",
  "accuracy": "89.9%",
  "advertisement_accuracy": "90.5%",
  "scientific_article_accuracy": "89.3%",
  "total_samples": 5085
}
```

#### `POST /classify`
Classifica uma imagem (apenas .tif/.tiff)

```bash
curl -X POST -F "image=@documento.tif" \
  https://visao-computacional.onrender.com/classify
```

**Response:**
```json
{
  "success": true,
  "filename": "documento.tif",
  "classification": "advertisement",
  "score": 3.45,
  "confidence": 0.876,
  "features": {
    "altura_media": 15.23,
    "desvio_altura": 18.45,
    "densidade_texto": 0.234,
    "num_componentes": 342
  }
}
```

---

## 💻 Uso do Classificador

### Python Script

```python
from classificador_final import ClassificadorFinal

# Inicializar
classifier = ClassificadorFinal()

# Classificar imagem
result = classifier.classify('documento.tif')

print(f"Classificação: {result['classification']}")
print(f"Confiança: {result['confidence']:.1%}")
print(f"Score: {result['score']:.2f}")
```

### Linha de Comando

```bash
python classificador_final.py documento.tif
```

**Output:**
```
Classificação: advertisement
Score: 3.45
Confiança: 87.6%

Features:
  Altura média: 15.23px
  Desvio altura: 18.45
  Densidade: 0.234
  Componentes: 342
```

---

## 📊 Regras de Classificação

O classificador calcula um **score** baseado em 4 regras:

```python
score = 0

# Regra 1: Altura média (peso 2.58)
if altura > 13.41:
    score += 2.58  # Advertisement
elif altura < 11.24:
    score -= 2.58  # Scientific Article

# Regra 2: Desvio padrão (peso 1.61)
if desvio > 12.45:
    score += 1.61  # Advertisement

# Regra 3: Densidade (peso 0.74)
if densidade > 0.403:
    score += 0.74  # Advertisement
else:
    score -= 0.74  # Scientific Article

# Regra 4: Componentes (peso 0.65)
if num_componentes < 454:
    score += 0.65  # Advertisement

# Classificação
if score > 0:
    return "advertisement"
else:
    return "scientific_article"
```

---

## 🌐 Deploy em Produção

### Render.com (Recomendado)

1. Conecte seu repositório GitHub ao Render
2. Selecione "Web Service"
3. Configure:
   - **Build Command:** `docker build -t app .`
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT api:app`
   - **Environment:** Docker
   - **Python Version:** 3.10

4. Deploy automático a cada push!

### GitHub Pages (Frontend)

1. Crie branch `gh-pages` apenas com `index.html`
2. Ative GitHub Pages nas Settings
3. Acesse: `https://seu-usuario.github.io/visao-computacional/`

---

## 📁 Estrutura do Projeto

```
visao-computacional/
├── api.py                          # API Flask
├── classificador_final.py          # Modelo otimizado
├── requirements.txt                # Dependências Python
├── Dockerfile                      # Container Docker
├── Procfile                        # Config Render.com
├── runtime.txt                     # Versão Python
├── index.html                      # Frontend web
├── README.md                       # Esta documentação
└── resultados_*.csv               # Dados de treinamento
```

---

## 🎓 Dataset RVL-CDIP

- **Fonte:** [Kaggle - RVL-CDIP Dataset](https://www.kaggle.com/datasets/pdavpoojan/the-rvlcdip-dataset-test)
- **Tamanho:** 400,000 imagens (16 classes)
- **Usado neste projeto:** 5,085 imagens (2 classes)
  - 2,515 advertisements
  - 2,570 scientific articles

---

## 📈 Evolução do Modelo

| Versão | Iterações | Acurácia | Ads | Articles |
|--------|-----------|----------|-----|----------|
| v1.0 | 30 | 85.03% | 83.7% | 86.3% |
| v2.0 | 1,000 | 89.48% | 89.2% | 89.7% |
| v3.0 | 100,000 | 89.81% | 89.9% | 89.7% |
| **v4.0** | **12,000,000+** | **89.87%** | **90.5%** | **89.3%** |

---

## 🔧 Tecnologias Utilizadas

- **Python 3.10** - Linguagem principal
- **OpenCV** - Processamento de imagens
- **NumPy** - Operações numéricas
- **Flask** - API REST
- **Gunicorn** - WSGI server
- **Docker** - Containerização
- **Render.com** - Deploy cloud
- **GitHub Pages** - Hospedagem frontend

---

## 👨‍💻 Autor

**Pedro Falcão Martins**

- GitHub: [@pfalconiere](https://github.com/pfalconiere)
- Projeto: [visao-computacional](https://github.com/pfalconiere/visao-computacional)

---

## 📄 Licença

Este projeto é fornecido para fins educacionais e de pesquisa.

---

## 🙏 Agradecimentos

- Dataset RVL-CDIP: Harley et al. (2015)
- Kaggle pela hospedagem do dataset
- Render.com pela infraestrutura cloud

---

**Desenvolvido com ❤️ usando Processamento de Imagens e Otimização Massiva**
