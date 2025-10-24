# 📄 Classificador de Documentos RVL-CDIP

Sistema de classificação de documentos baseado em visão computacional que diferencia **Advertisements** de **Scientific Articles** usando o dataset RVL-CDIP.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-red.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-82.3%25-brightgreen.svg)

## 🎯 Características

- **Classificação baseada em regras** usando extração de features visuais
- **API REST** em Flask para integração fácil
- **Interface web moderna** com drag & drop
- **Acurácia de 82.3%** no dataset completo RVL-CDIP
- **Processamento rápido**: ~44ms por imagem

## 📊 Performance

| Categoria | Acurácia | Amostras |
|-----------|----------|----------|
| Advertisements | 70.5% | 2,425 |
| Scientific Articles | 94.2% | 2,660 |
| **Geral** | **82.3%** | **5,085** |

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
git clone https://github.com/pfalconiere/visao-computacional.git
cd visao-computacional

# Instale as dependências
pip install -r requirements.txt
```

### Uso Rápido

```bash
# Inicie API e Frontend
./start.sh

# Acesse no navegador
open http://localhost:8080
```

A API estará rodando em `http://localhost:5000` e o frontend em `http://localhost:8080`.

## 📁 Estrutura do Projeto

```
visao-computacional/
├── api.py                      # API REST Flask
├── classificador_final.py      # Modelo treinado final
├── index.html                  # Interface web
├── servidor_web.py             # Servidor HTTP para frontend
├── start.sh                    # Script para iniciar tudo
├── stop.sh                     # Script para parar servidores
├── requirements.txt            # Dependências Python
├── training_data.pkl           # Dados de treinamento
└── docs/
    ├── API_README.md           # Documentação da API
    ├── COMO_TESTAR_API.md      # Guia de testes
    └── TECHNICAL_DETAILS.md    # Detalhes técnicos
```

## 🔧 Uso

### 1. Interface Web (Recomendado)

```bash
./start.sh
```

Abra http://localhost:8080 e faça upload de uma imagem `.tif`.

### 2. API REST

```bash
# Iniciar apenas a API
python3 api.py

# Classificar uma imagem
curl -X POST -F "image=@documento.tif" http://localhost:5000/classify
```

**Resposta:**
```json
{
  "success": true,
  "classification": "advertisement",
  "confidence": 0.876,
  "score": 3,
  "features": {
    "altura_media": 18.5,
    "desvio_altura": 45.2,
    "densidade_texto": 0.185,
    "num_componentes": 156
  }
}
```

### 3. Script Python

```python
from classificador_final import ClassificadorFinal

classifier = ClassificadorFinal()
result = classifier.classify("documento.tif")

print(f"Classificação: {result['classification']}")
print(f"Confiança: {result['confidence']:.1%}")
```

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Documentação da API |
| GET | `/health` | Status da API |
| GET | `/stats` | Estatísticas do modelo |
| POST | `/classify` | Classificar imagem |

## 🧪 Features Extraídas

O classificador analisa 8 features principais:

1. **Altura Média** - Tamanho médio dos componentes de texto
2. **Desvio de Altura** - Variação no tamanho do texto
3. **Densidade de Texto** - Proporção de pixels de texto
4. **Largura Média** - Largura média dos componentes
5. **Aspect Ratio** - Relação largura/altura
6. **Número de Componentes** - Quantidade de elementos de texto
7. **Transições de Layout** - Mudanças na distribuição do texto
8. **Colunas Detectadas** - Número de colunas identificadas

## 🎨 Interface Web

<img src="https://via.placeholder.com/800x500/667eea/ffffff?text=Screenshot+da+Interface" alt="Interface">

Características da interface:
- ✅ Upload via drag & drop
- ✅ Preview da imagem
- ✅ Resultado visual com cores
- ✅ Detalhes das features extraídas
- ✅ Indicador de confiança
- ✅ Design responsivo

## 📚 Dataset

**RVL-CDIP** (Ryerson Vision Lab Complex Document Information Processing)
- 320,000 documentos em escala de cinza
- 16 categorias diferentes
- Imagens em formato .tif
- [Download no Kaggle](https://www.kaggle.com/datasets/pdavpoojan/the-rvlcdip-dataset-test)

**Nota:** Este projeto foca em 2 categorias:
- `advertisement` - Anúncios de jornal antigos (P&B)
- `scientific_article` - Artigos científicos

## 🔬 Metodologia

### 1. Análise Exploratória
- Análise de ~5,000 imagens do dataset
- Identificação de features discriminativas
- Estudo de distribuições estatísticas

### 2. Extração de Features
- Processamento com OpenCV
- Detecção de componentes conectados
- Análise de layout e geometria

### 3. Classificação Baseada em Regras
- 6 regras principais otimizadas
- Thresholds ajustados empiricamente
- Sistema de pontuação ponderada

### 4. Validação
- Teste em dataset completo
- Análise de falsos positivos/negativos
- Ajuste fino dos parâmetros

## 🛠️ Tecnologias

- **Python 3.8+**
- **OpenCV** - Processamento de imagens
- **NumPy** - Operações numéricas
- **Flask** - API REST
- **Flask-CORS** - CORS para API
- **Pillow** - Manipulação de imagens

## 📦 Dependências

```txt
opencv-python-headless==4.8.1.78
numpy==1.24.3
Flask==2.3.3
flask-cors==4.0.0
Pillow==10.0.1
```

## 🚀 Deploy

### Desenvolvimento

```bash
./start.sh
```

### Produção

Para produção, use um servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

## 🧪 Testes

```bash
# Testar API
python3 testar_api.py

# Processar pasta de imagens
python3 processar_todas.py /caminho/para/pasta
```

## 📈 Melhorias Futuras

- [ ] Adicionar mais categorias de documentos
- [ ] Implementar machine learning (CNN)
- [ ] Suporte para outros formatos de imagem
- [ ] Cache de resultados
- [ ] Batch processing via API
- [ ] Docker containerization
- [ ] Métricas e monitoring

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

**Paulo Falconiere**
- GitHub: [@pfalconiere](https://github.com/pfalconiere)

## 🙏 Agradecimentos

- Dataset RVL-CDIP by Ryerson Vision Lab
- Comunidade OpenCV
- Flask framework

---

⭐ Se este projeto foi útil, considere dar uma estrela!
