# 📄 Document Classifier - RVL-CDIP

Sistema inteligente de classificação de documentos que diferencia **Advertisements** de **Scientific Articles**, com análise avançada de parágrafos, extração de texto via OCR e verificação de conformidade com regras acadêmicas.

![Accuracy](https://img.shields.io/badge/Accuracy-90.00%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Casos de Uso](#casos-de-uso)
  - [Caso de Uso 1: Classificação de Tipo de Documento](#caso-de-uso-1-classificação-de-tipo-de-documento)
  - [Caso de Uso 2: Detecção e Quantificação de Parágrafos](#caso-de-uso-2-detecção-e-quantificação-de-parágrafos)
  - [Caso de Uso 3: Extração de Texto e Palavras Frequentes](#caso-de-uso-3-extração-de-texto-e-palavras-frequentes)
  - [Caso de Uso 4: Verificação de Conformidade](#caso-de-uso-4-verificação-de-conformidade)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [API REST](#api-rest)
- [Performance](#performance)
- [Tecnologias](#tecnologias)

---

## 🎯 Visão Geral

Este projeto implementa um classificador de documentos treinado no dataset **RVL-CDIP** com **90% de acurácia**, capaz de diferenciar anúncios publicitários de artigos científicos. O sistema vai além da simples classificação, oferecendo análise estrutural e de conteúdo dos documentos.

### Principais Features

✅ Classificação binária de documentos (Advertisement vs Scientific Article)  
✅ Detecção automática de parágrafos com algoritmo calibrado  
✅ Extração de texto via OCR (Tesseract)  
✅ Análise de palavras mais frequentes  
✅ Verificação de conformidade com regras acadêmicas configuráveis  
✅ API REST completa com documentação Swagger  
✅ Interface web moderna e responsiva  
✅ Sistema de feedback para retreinamento  

---

## 📚 Casos de Uso

### Caso de Uso 1: Classificação de Tipo de Documento

#### 📝 Descrição
Classifica automaticamente um documento TIFF como **Advertisement** (anúncio publicitário) ou **Scientific Article** (artigo científico) com base em características visuais e estruturais.

#### 🔍 Como Funciona

O classificador analisa múltiplas features extraídas da imagem:

1. **Densidade de Texto**: Proporção de pixels de texto em relação à área total
2. **Número de Componentes**: Quantidade de elementos de texto detectados
3. **Altura Média dos Componentes**: Tamanho médio das linhas de texto
4. **Desvio Padrão da Altura**: Variação no tamanho das linhas
5. **Aspect Ratio**: Proporção entre largura e altura dos componentes

O modelo aplica **regras ponderadas otimizadas** através de 50.000 iterações de treinamento:

```python
# Pesos otimizados (classificador_final.py, linhas 52-58)
self.pesos = {
    'p1': 3.0802891803113677,  # Densidade de texto
    'p2': 1.6107505780934257,  # Número de componentes
    'p3': 0.7447718755081227,  # Altura média
    'p4': 0.6455914619059228,  # Desvio padrão
    'p5': 2.42                  # Transições de layout
}
```

#### 📂 Arquivos Envolvidos

**`classificador_final.py`** (Arquivo principal)
- **Linhas 34-77**: Classe `ClassificadorFinal` e inicialização de thresholds
- **Linhas 78-158**: Método `extract_features()` - Extração de características visuais
- **Linhas 160-236**: Método `classify()` - Lógica de classificação com regras ponderadas
- **Linhas 42-49**: Thresholds otimizados calibrados com dataset RVL-CDIP

**`api.py`** (Endpoint de classificação)
- **Linhas 70-179**: Endpoint `/classify` - Processa upload e retorna classificação
- **Linhas 111-116**: Extração de features da imagem
- **Linhas 118-123**: Aplicação do modelo de classificação

**`index.html`** (Interface Frontend)
- **Linhas 1107-1141**: Função `classifyImage()` - Envia imagem para API
- **Linhas 1144-1223**: Função `displayResult()` - Exibe resultado da classificação

#### 🎯 Acurácia do Modelo

- **Acurácia Geral**: 90.00%
- **Advertisement**: 90.46%
- **Scientific Article**: 89.30%
- **Total de Amostras**: 5,085 documentos

#### 💡 Exemplo de Uso

```python
from classificador_final import ClassificadorFinal

# Inicializar classificador
classifier = ClassificadorFinal()

# Classificar documento
result = classifier.classify("document.tif")

print(f"Tipo: {result['classification']}")
# Output: "Tipo: scientific_article" ou "Tipo: advertisement"
```

---

### Caso de Uso 2: Detecção e Quantificação de Parágrafos

#### 📝 Descrição
Detecta automaticamente parágrafos em artigos científicos através de análise de indentação, espaçamento vertical e estrutura de linhas.

#### 🔍 Como Funciona

O algoritmo implementa **3 estratégias de detecção calibradas**:

1. **Detecção por Indentação**
   - Identifica recuos no início de linhas (≥20px)
   - Diferencia primeira linha de continuações de parágrafo

2. **Detecção por Espaçamento Vertical**
   - Analisa espaços maiores entre linhas (≥3.0x a altura média)
   - Identifica quebras naturais de parágrafo

3. **Detecção por Análise de Fluxo**
   - Combina indentação + espaçamento
   - Identifica mudanças no fluxo de texto

#### 📂 Arquivos Envolvidos

**`paragraph_detector.py`** (Detector especializado)
- **Linhas 6-11**: Classe `ParagraphDetector` e parâmetros calibrados
  ```python
  self.min_line_height = 5
  self.indent_threshold_px = 20      # Calibrado: 20px
  self.vertical_space_ratio = 3.0    # Calibrado: 3.0x
  ```
- **Linhas 12-59**: Método `detect_text_lines_with_margins()` - Detecção de linhas com margens
- **Linhas 61-91**: Método `detect_by_indentation()` - Estratégia de indentação
- **Linhas 93-113**: Método `detect_by_vertical_space()` - Estratégia de espaçamento
- **Linhas 115-123**: Método `detect_paragraphs()` - Método principal unificado

**`classificador_final.py`** (Integração)
- **Linhas 14-22**: Importação do `ParagraphDetector`
- **Linhas 60-64**: Inicialização do detector
- **Linhas 201-206**: Chamada da detecção de parágrafos
  ```python
  if self.paragraph_detector:
      num_paragraphs = self.paragraph_detector.detect_paragraphs(img)
  ```

**`api.py`** (Resposta da API)
- **Linhas 126-130**: Retorno do número de parágrafos detectados
  ```python
  'num_paragraphs': result.get('num_paragraphs', 0)
  ```

**`index.html`** (Exibição no Frontend)
- **Linhas 1174-1189**: Exibição de parágrafos para artigos científicos
  ```javascript
  if (!isAd && data.num_paragraphs !== undefined) {
      const paragraphDiv = document.createElement('div');
      paragraphDiv.innerHTML = `<strong>${t.paragraphs}:</strong> ${data.num_paragraphs}`;
  }
  ```

#### 🎯 Parâmetros Calibrados

O detector foi calibrado com dados reais do RVL-CDIP:

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `min_line_height` | 5px | Altura mínima de uma linha válida |
| `indent_threshold_px` | 20px | Recuo mínimo para considerar indentação |
| `vertical_space_ratio` | 3.0x | Espaço vertical relativo à altura média |

#### 💡 Exemplo de Uso

```python
from paragraph_detector import ParagraphDetector
import cv2

detector = ParagraphDetector()
img = cv2.imread("scientific_article.tif", cv2.IMREAD_GRAYSCALE)

num_paragraphs = detector.detect_paragraphs(img)
print(f"Parágrafos detectados: {num_paragraphs}")
# Output: "Parágrafos detectados: 12"
```

---

### Caso de Uso 3: Extração de Texto e Palavras Frequentes

#### 📝 Descrição
Extrai o texto completo de artigos científicos via OCR (Tesseract) e identifica as **10 palavras mais frequentes**, excluindo stopwords.

#### 🔍 Como Funciona

O processo de análise de texto segue 4 etapas:

1. **OCR (Optical Character Recognition)**
   - Utiliza Tesseract OCR para extrair texto
   - Pré-processamento com threshold OTSU para melhor qualidade

2. **Limpeza e Normalização**
   - Remove pontuação e caracteres especiais
   - Converte para minúsculas

3. **Filtragem de Stopwords**
   - Remove palavras comuns sem valor semântico (PT e EN)
   - Exemplos: "o", "a", "de", "the", "and", "or"

4. **Contagem e Ranking**
   - Conta frequência de cada palavra
   - Retorna top 10 palavras mais relevantes

#### 📂 Arquivos Envolvidos

**`text_analyzer.py`** (Analisador de texto)
- **Linhas 11-19**: Classe `TextAnalyzer` e lista de stopwords
  ```python
  self.stopwords = set([
      'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da',
      'the', 'a', 'an', 'and', 'or', 'but', 'if', 'of', 'at'
  ])
  ```
- **Linhas 32-50**: Método `extract_text()` - Extração via OCR
  ```python
  def extract_text(self, image_path):
      img = cv2.imread(str(image_path))
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
      text = pytesseract.image_to_string(thresh, lang='eng')
      return text
  ```
- **Linhas 52-83**: Método `analyze_text()` - Análise e contagem de palavras
- **Linhas 85-120**: Método `get_word_count_and_frequent_words()` - Pipeline completo

**`classificador_final.py`** (Integração)
- **Linhas 24-32**: Importação do `TextAnalyzer`
- **Linhas 66-70**: Inicialização do analisador
- **Linhas 208-221**: Análise de texto para artigos científicos
  ```python
  if result['classification'] == 'scientific_article' and self.text_analyzer:
      word_count, frequent_words = self.text_analyzer.get_word_count_and_frequent_words(image_path)
      result['word_count'] = word_count
      result['frequent_words'] = frequent_words
  ```

**`api.py`** (Resposta da API)
- **Linhas 131-136**: Inclusão de dados de texto na resposta
  ```python
  'word_count': result.get('word_count', 0),
  'frequent_words': result.get('frequent_words', [])
  ```

**`index.html`** (Exibição no Frontend)
- **Linhas 1182-1188**: Exibição da contagem de palavras
- **Linhas 1193-1217**: Renderização da lista de palavras frequentes
  ```javascript
  data.frequent_words.slice(0, 10).forEach(item => {
      const li = document.createElement('li');
      li.innerHTML = `${item.word}: <strong>${item.count}</strong>`;
      wordsList.appendChild(li);
  });
  ```

#### 🎯 Stopwords Filtradas

O sistema filtra **42 stopwords** comuns em português e inglês:

**Português**: o, a, os, as, um, uma, de, do, da, dos, das, em, no, na, nos, nas, por, para, com, sem, sob, e, ou, mas, se, que, qual, quando, onde, como

**Inglês**: the, a, an, and, or, but, if, of, at, by, for, with, about, as, into, through, to, from, in, on

#### 💡 Exemplo de Saída

```json
{
  "word_count": 3247,
  "frequent_words": [
    {"word": "algorithm", "count": 42},
    {"word": "data", "count": 38},
    {"word": "results", "count": 31},
    {"word": "analysis", "count": 28},
    {"word": "method", "count": 25},
    {"word": "performance", "count": 22},
    {"word": "system", "count": 20},
    {"word": "model", "count": 18},
    {"word": "evaluation", "count": 16},
    {"word": "research", "count": 15}
  ]
}
```

---

### Caso de Uso 4: Verificação de Conformidade

#### 📝 Descrição
Verifica se artigos científicos estão **conformes** com regras acadêmicas configuráveis, considerando número mínimo de palavras e parágrafos.

#### 🔍 Como Funciona

O sistema avalia dois critérios principais:

1. **Contagem de Palavras**
   - Padrão: ≥ 2000 palavras
   - Configurável pelo usuário

2. **Número de Parágrafos**
   - Padrão: ≥ 8 parágrafos
   - Configurável pelo usuário

**Lógica de Conformidade:**
```
CONFORME ⟺ (palavra_count > min_words) AND (num_paragraphs ≥ min_paragraphs)
```

Se qualquer critério falhar, o documento é marcado como **NÃO CONFORME**.

#### 📂 Arquivos Envolvidos

**`api.py`** (Lógica de conformidade)
- **Linhas 87-93**: Recepção de parâmetros configuráveis
  ```python
  min_words = int(request.form.get('min_words', 2000))
  min_paragraphs = int(request.form.get('min_paragraphs', 8))
  ```
- **Linhas 138-157**: Verificação de conformidade para artigos científicos
  ```python
  if result['classification'] == 'scientific_article':
      word_count = result.get('word_count', 0)
      num_paragraphs = result.get('num_paragraphs', 0)
      
      # Verificar conformidade
      is_compliant = word_count > min_words and num_paragraphs >= min_paragraphs
      
      # Gerar explicação bilíngue
      if is_compliant:
          explanation_pt = f"Documento CONFORME..."
          explanation_en = f"Document COMPLIANT..."
      else:
          explanation_pt = f"Documento NÃO CONFORME..."
          explanation_en = f"Document NOT COMPLIANT..."
  ```
- **Linhas 166-172**: Resposta com status de conformidade
  ```python
  'is_compliant': is_compliant,
  'compliance_rules': {
      'min_words': min_words,
      'min_paragraphs': min_paragraphs
  }
  ```

**`index.html`** (Interface de Configuração)
- **Linhas 894-895**: Variáveis de regras (padrão)
  ```javascript
  let minWords = 2000;
  let minParagraphs = 8;
  ```
- **Linhas 1113-1118**: Envio de parâmetros para API
  ```javascript
  formData.append('min_words', minWords);
  formData.append('min_paragraphs', minParagraphs);
  ```
- **Linhas 1331-1393**: Função `translateExplanation()` - Gera resumo de conformidade
  ```javascript
  if (isCompliant) {
      explanation += ` Documento CONFORME às normas (>${minWords} palavras 
                       e ≥${minParagraphs} parágrafos): ${wordCount} palavras, 
                       ${numParagraphs} parágrafos.`;
  } else {
      explanation += ` Documento NÃO CONFORME às normas: `;
      // Lista problemas encontrados
  }
  ```
- **Linhas 1286-1303**: Modal de configuração de regras
  ```javascript
  function confirmRule() {
      minWords = parseInt(document.getElementById('modal-min-words').value) || 2000;
      minParagraphs = parseInt(document.getElementById('modal-min-paragraphs').value) || 8;
  }
  ```

**Componentes do Modal (HTML)**
- **Linhas 1444-1464**: Modal HTML para alterar regras
  ```html
  <div class="modal" id="rule-modal">
      <input type="number" id="modal-min-words" value="2000">
      <input type="number" id="modal-min-paragraphs" value="8">
  </div>
  ```

#### 🎯 Regras Padrão

| Critério | Valor Padrão | Configurável |
|----------|--------------|--------------|
| Mínimo de Palavras | 2000 | ✅ Sim |
| Mínimo de Parágrafos | 8 | ✅ Sim |

#### 💡 Exemplos de Resposta

**Documento CONFORME:**
```json
{
  "classification": "scientific_article",
  "word_count": 3247,
  "num_paragraphs": 12,
  "is_compliant": true,
  "explanation_pt": "Documento CONFORME às normas (>2000 palavras e ≥8 parágrafos): 3247 palavras, 12 parágrafos.",
  "explanation_en": "Document COMPLIANT with standards (>2000 words and ≥8 paragraphs): 3247 words, 12 paragraphs."
}
```

**Documento NÃO CONFORME:**
```json
{
  "classification": "scientific_article",
  "word_count": 1450,
  "num_paragraphs": 6,
  "is_compliant": false,
  "explanation_pt": "Documento NÃO CONFORME às normas: apenas 1450 palavras (mínimo: 2000), apenas 6 parágrafos (mínimo: 8).",
  "explanation_en": "Document NOT COMPLIANT with standards: only 1450 words (minimum: 2000), only 6 paragraphs (minimum: 8)."
}
```

#### 🎨 Interface de Configuração

O usuário pode **alterar as regras** através do botão "Alterar Regra" no header:

1. Clica no botão "Alterar Regra"
2. Modal aparece com inputs numéricos
3. Define novos valores para palavras e parágrafos
4. Confirma e as novas regras são aplicadas na próxima classificação

---

## 🏗️ Arquitetura

### Arquitetura Síncrona (Modo Fallback)

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (index.html)                    │
│  - Interface Web Responsiva                                  │
│  - Upload de arquivos TIFF                                   │
│  - Configuração de regras                                    │
│  - Exibição de resultados                                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP POST /classify
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     API REST (api.py)                        │
│  - Endpoint /classify                                        │
│  - Endpoint /feedback                                        │
│  - Documentação Swagger                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              CLASSIFICADOR (classificador_final.py)          │
│  - Extração de features visuais                              │
│  - Modelo de classificação (90% acc)                         │
│  - Integração com detectores                                 │
└─────────┬───────────────────────┬───────────────────────────┘
          │                       │
          ▼                       ▼
┌─────────────────────┐  ┌──────────────────────────────┐
│  PARAGRAPH DETECTOR │  │      TEXT ANALYZER           │
│  (paragraph_        │  │  (text_analyzer_optimized.py)│
│   detector.py)      │  │  - OCR (Tesseract)           │
│  - Detecção linhas  │  │  - Contagem palavras         │
│  - Análise indent   │  │  - Palavras frequentes       │
│  - Espaçamento      │  │  - Filtragem stopwords       │
└─────────────────────┘  └──────────────────────────────┘
```

### ⚡ Arquitetura Assíncrona (Modo de Produção)

O sistema implementa processamento assíncrono para lidar com documentos pesados (especialmente artigos científicos com OCR) sem causar timeouts.

```
┌────────────────────────────────────────────────────────────────┐
│                  FRONTEND (index.html)                         │
│  - Upload de arquivo                                           │
│  - Polling automático de progresso                             │
│  - Barra de progresso em tempo real                            │
└─────────────┬──────────────────────────────────────────────────┘
              │ 1. POST /classify/async (arquivo em base64)
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  WEB SERVICE (api.py)                           │
│  Container 1: Flask + Gunicorn                                  │
│  - Recebe arquivo como bytes                                    │
│  - Converte para base64                                         │
│  - Submete task ao Celery                                       │
│  - Retorna task_id imediatamente (202 Accepted)                │
└────────────┬────────────────────────────────────────────────────┘
             │ 2. Envia via Redis
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     REDIS (Message Broker)                      │
│  - Fila de tarefas (broker)                                     │
│  - Armazenamento de resultados (backend)                        │
│  - Máximo 30 conexões simultâneas (Free tier)                   │
└────────────┬────────────────────────────────────────────────────┘
             │ 3. Worker consome task
             ▼
┌─────────────────────────────────────────────────────────────────┐
│               CELERY WORKER (tasks.py)                          │
│  Container 2: Celery Process                                    │
│  - Recebe file_base64 + filename                                │
│  - Decodifica base64 → bytes                                    │
│  - Salva temporariamente no /tmp do worker                      │
│  - Atualiza progresso (10%, 30%, 90%)                           │
│  - Chama classificador                                          │
│  - Remove arquivo temporário                                    │
│  - Retorna resultado via Redis                                  │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CLASSIFICADOR (classificador_final.py)              │
│  - Extração de features                                          │
│  - Detecção de parágrafos                                        │
│  - OCR otimizado (text_analyzer_optimized.py)                    │
│  - Análise de conformidade                                       │
└──────────────────────────────────────────────────────────────────┘
```

#### 🔄 Fluxo de Processamento Assíncrono

**Passo 1: Submissão**
```javascript
// Frontend submete arquivo
POST /classify/async
→ Retorna: { task_id: "abc-123", status: "PENDING" }
```

**Passo 2: Polling**
```javascript
// Frontend faz polling a cada 2 segundos
GET /task/abc-123
→ Retorna: { 
    state: "PROGRESS", 
    progress: 30, 
    status: "Classificando documento..." 
}
```

**Passo 3: Conclusão**
```javascript
// Worker completa o processamento
GET /task/abc-123
→ Retorna: { 
    state: "SUCCESS", 
    result: { classification: "scientific_article", ... } 
}
```

#### 📦 Arquivos da Solução Assíncrona

**`celery_config.py`** - Configuração do Celery
```python
# Cria instância do Celery conectada ao Redis
celery_app = Celery(
    'document_classifier',
    broker=REDIS_URL,      # Fila de tarefas
    backend=REDIS_URL      # Armazenamento de resultados
)
```

**`tasks.py`** - Definição de Tarefas
```python
@celery_app.task(bind=True, name='tasks.classify_document')
def classify_document(self, file_base64, filename, ...):
    # 1. Decodifica base64 → bytes
    file_bytes = base64.b64decode(file_base64)
    
    # 2. Salva temporariamente
    with open(temp_path, 'wb') as f:
        f.write(file_bytes)
    
    # 3. Atualiza progresso
    self.update_state(state='PROGRESS', meta={...})
    
    # 4. Classifica
    result = classifier.classify(temp_path, ...)
    
    # 5. Remove arquivo
    os.remove(temp_path)
    
    return result
```

**`api.py`** - Endpoints Assíncronos
```python
# Endpoint para submeter tarefa
@app.route('/classify/async', methods=['POST'])
def classify_async():
    file_bytes = file.read()
    file_base64 = base64.b64encode(file_bytes).decode('utf-8')
    
    task = classify_document.apply_async(
        args=[file_base64, filename, ...]
    )
    
    return jsonify({'task_id': task.id})

# Endpoint para consultar status
@app.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = classify_document.AsyncResult(task_id)
    
    if task.state == 'PROGRESS':
        return jsonify({
            'state': task.state,
            'progress': task.info.get('progress', 0),
            'status': task.info.get('status', '')
        })
    elif task.state == 'SUCCESS':
        return jsonify({
            'state': task.state,
            'result': task.info
        })
```

**`index.html`** - Frontend com Polling
```javascript
// 1. Submete arquivo
const response = await fetch('/classify/async', {
    method: 'POST',
    body: formData
});
const data = await response.json();

// 2. Inicia polling
pollTaskStatus(data.task_id);

// 3. Polling a cada 2 segundos
async function pollTaskStatus(taskId) {
    const response = await fetch(`/task/${taskId}`);
    const data = await response.json();
    
    if (data.state === 'PROGRESS') {
        updateProgress(data.progress, data.status);
        setTimeout(() => pollTaskStatus(taskId), 2000);
    } else if (data.state === 'SUCCESS') {
        displayResult(data.result);
    }
}
```

#### 🐳 Deploy com Docker Compose (Local)

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn -w 1 -b 0.0.0.0:5000 --timeout 180 api:app
    ports:
      - "5000:5000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  worker:
    build: .
    command: celery -A celery_config.celery_app worker --loglevel=info --concurrency=1
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
```

#### 🚀 Deploy em Produção (Render)

**Render Standard Plan** ($25/mês por serviço):

1. **Redis** (Free tier): Message broker e result backend
2. **Web Service** (Standard): Flask API com 1 Gunicorn worker
3. **Background Worker** (Standard): Celery worker para processamento

**Procfile:**
```
web: gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 180 api:app
worker: celery -A celery_config.celery_app worker --loglevel=info --concurrency=1
```

#### ⚠️ Desafio Arquitetural Resolvido

**Problema:** Containers separados não compartilham filesystem
```
Web Container:  /tmp/arquivo.tif  ❌
Worker Container: /tmp/  (vazio)
```

**Solução:** Transferência via Redis
```
Web: arquivo → bytes → base64 → Redis
Worker: Redis → base64 → bytes → /tmp worker → processa
```

#### 🎯 Benefícios da Arquitetura Assíncrona

✅ **Sem timeouts**: Processamento em background independente do HTTP timeout  
✅ **Escalável**: Múltiplos workers podem processar tarefas em paralelo  
✅ **Feedback em tempo real**: Barra de progresso atualizada via polling  
✅ **Resiliente**: Retry automático em caso de falha  
✅ **Rastreável**: Task ID permite consultar status a qualquer momento

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8+
- Tesseract OCR

### Instalar Tesseract

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**Windows:**
Baixe o instalador em: https://github.com/UB-Mannheim/tesseract/wiki

### Instalar Dependências Python

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/document-classifier.git
cd document-classifier

# Instale as dependências
pip install -r requirements.txt
```

### Conteúdo do `requirements.txt`

```txt
flask==3.0.0
flask-cors==4.0.0
flasgger==0.9.7.1
opencv-python==4.8.1.78
numpy==1.24.3
pytesseract==0.3.10
Pillow==10.1.0
```

---

## 🚀 Como Usar

### 1. Iniciar o Sistema (Linux/macOS)

```bash
bash start.sh
```

Este comando:
- Inicia a API na porta 5000
- Inicia o frontend na porta 8080
- Abre o navegador automaticamente

### 2. Iniciar Manualmente

**API:**
```bash
python3 api.py
```

**Frontend:**
```bash
python3 servidor_web.py
```

### 3. Acessar a Aplicação

- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:5000/api/docs

### 4. Parar o Sistema

```bash
bash stop.sh
```

Ou manualmente:
```bash
pkill -f api.py
pkill -f servidor_web.py
```

---

## 🔌 API REST

### Endpoint: Classificar Documento

**POST** `/classify`

#### Request (multipart/form-data)

```bash
curl -X POST http://localhost:5000/classify \
  -F "image=@document.tif" \
  -F "min_words=2000" \
  -F "min_paragraphs=8" \
  -F "language=pt"
```

#### Response

```json
{
  "success": true,
  "classification": "scientific_article",
  "confidence": 0.95,
  "num_paragraphs": 12,
  "word_count": 3247,
  "frequent_words": [
    {"word": "algorithm", "count": 42},
    {"word": "data", "count": 38}
  ],
  "is_compliant": true,
  "explanation_pt": "Documento CONFORME às normas...",
  "explanation_en": "Document COMPLIANT with standards...",
  "features": {
    "text_density": 0.42,
    "num_text_components": 523,
    "avg_component_height": 15.3
  }
}
```

### Endpoint: Enviar Feedback

**POST** `/feedback`

```bash
curl -X POST http://localhost:5000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "image_name": "document.tif",
    "predicted_class": "scientific_article",
    "is_correct": "true",
    "correct_class": "scientific_article"
  }'
```

### Documentação Completa

Acesse a documentação interativa Swagger em: http://localhost:5000/api/docs

---

## 📊 Performance

### Métricas do Modelo

| Métrica | Valor |
|---------|-------|
| **Acurácia Geral** | 90.00% |
| **Precision (Advertisement)** | 90.46% |
| **Recall (Scientific Article)** | 89.30% |
| **Total de Amostras** | 5,085 |
| **Iterações de Treinamento** | 50,000 |

### Detecção de Parágrafos

- **Acurácia Média**: ~85%
- **Falsos Positivos**: <5%
- **Tempo de Processamento**: ~0.3s por imagem

### Extração de Texto (OCR)

- **Taxa de Sucesso**: ~92% (texto legível)
- **Tempo Médio**: ~2-3s por página
- **Idiomas Suportados**: Inglês (primary)

---

## 🛠️ Tecnologias

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **OpenCV** - Processamento de imagem
- **NumPy** - Computação numérica
- **Tesseract OCR** - Extração de texto
- **Flasgger** - Documentação Swagger

### Frontend
- **HTML5 / CSS3**
- **JavaScript (ES6+)**
- **Tiff.js** - Renderização de TIFF no navegador

### Machine Learning
- **Feature Engineering** - 9 features extraídas
- **Weighted Rule-Based Classifier** - Otimizado com 50k iterações
- **Calibrated Thresholds** - Ajustados no dataset RVL-CDIP

---

## 📁 Estrutura do Projeto

```
document_classifier_project/
├── api.py                      # API REST principal
├── classificador_final.py      # Modelo de classificação
├── paragraph_detector.py       # Detector de parágrafos
├── text_analyzer.py           # Analisador de texto (OCR)
├── swagger_docs.py            # Documentação Swagger
├── servidor_web.py            # Servidor frontend
├── index.html                 # Interface web
├── requirements.txt           # Dependências Python
├── start.sh                   # Script de inicialização
├── stop.sh                    # Script para parar servidores
├── training_data.pkl          # Dados de treinamento
├── feedback_data.csv          # Dados de feedback
└── docs/                      # Documentação adicional
    ├── API_README.md
    ├── COMO_TESTAR_API.md
    ├── GUIA_RAPIDO.md
    └── TECHNICAL_DETAILS.md
```

---

## 🧪 Testes

### Testar Classificação

```python
from classificador_final import ClassificadorFinal

classifier = ClassificadorFinal()

# Testar advertisement
result = classifier.classify("samples/advertisement.tif")
assert result['classification'] == 'advertisement'

# Testar scientific article
result = classifier.classify("samples/scientific_article.tif")
assert result['classification'] == 'scientific_article'
assert result['num_paragraphs'] > 0
assert result['word_count'] > 0
```

### Testar API

```bash
# Health check
curl http://localhost:5000/health

# Classificar documento
curl -X POST http://localhost:5000/classify \
  -F "image=@test_document.tif" \
  -F "min_words=2000" \
  -F "min_paragraphs=8"
```

---

## 📈 Roadmap

- [x] Classificação binária (Advertisement vs Scientific Article)
- [x] Detecção de parágrafos
- [x] Extração de texto via OCR
- [x] Análise de palavras frequentes
- [x] Verificação de conformidade
- [x] API REST com Swagger
- [x] Interface web responsiva
- [x] Sistema de feedback
- [ ] Suporte a múltiplos idiomas no OCR
- [ ] Retreinamento automático com feedback
- [ ] Classificação multi-classe (10 categorias RVL-CDIP)
- [ ] Deploy em Cloud (AWS/Azure/GCP)
- [ ] Batch processing de múltiplos documentos
- [ ] Exportação de relatórios em PDF

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é parte do trabalho do **Mestrado de Engenharia de Software 2025.1** do **C.E.S.A.R**.

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

**Projeto desenvolvido como parte do Mestrado de Engenharia de Software 2025.1**

🏢 **C.E.S.A.R - Centro de Estudos e Sistemas Avançados do Recife**

---

## 📞 Suporte

Para questões, bugs ou sugestões:

- 📧 Email: [seu-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/document-classifier/issues)
- 📚 Documentação: [Wiki](https://github.com/seu-usuario/document-classifier/wiki)

---

## 🙏 Agradecimentos

- **RVL-CDIP Dataset** - Dataset público de classificação de documentos
- **Tesseract OCR** - Engine de OCR open-source
- **OpenCV Community** - Biblioteca de visão computacional
- **Flask Team** - Framework web minimalista e poderoso

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub! ⭐**

Made with ❤️ by C.E.S.A.R Students

</div>
