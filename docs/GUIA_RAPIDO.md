# 🚀 Guia Rápido - Classificador de Documentos

## ⚡ Início Rápido (5 minutos)

### Passo 1: Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Classificar uma Imagem

```bash
# Classificação simples
python document_classifier.py path/to/image.png

# Classificação com detalhes
python document_classifier.py path/to/image.png --verbose
```

### Passo 3: Usar no Python

```python
from document_classifier import DocumentClassifier

# Criar classificador
classifier = DocumentClassifier()

# Classificar
result = classifier.classify('image.png')

# Ver resultado
print(result['classification'])  # 'advertisement' ou 'scientific_article'
print(f"Confiança: {result['confidence']:.2%}")
```

---

## 📊 Como Funciona?

O classificador analisa **6 características principais**:

### 1. 🎨 Cores
- **Alta saturação** → Advertisement
- **Baixa saturação** → Scientific Article

### 2. 🌈 Diversidade de Cores
- **Muitas cores diferentes** → Advertisement
- **Poucas cores** → Scientific Article

### 3. 📝 Densidade de Texto
- **Baixa densidade** → Advertisement
- **Alta densidade** → Scientific Article

### 4. 🎨 Cores Únicas
- **> 2000 cores** → Advertisement
- **≤ 2000 cores** → Scientific Article

### 5. 📐 Layout
- **Irregular** → Advertisement
- **Estruturado (colunas)** → Scientific Article

### 6. 🔲 Bordas/Linhas
- **Muitas bordas** → Advertisement (imagens/gráficos)
- **Poucas bordas** → Scientific Article (texto)

---

## 📦 Download do Dataset

### RVL-CDIP Dataset

1. **Acesse**: https://www.kaggle.com/datasets/pdavpoojan/the-rvlcdip-dataset-test

2. **Faça o download** (requer conta Kaggle)

3. **Extraia** o arquivo ZIP

4. **Estrutura esperada**:
   ```
   rvl-cdip-test/
   ├── advertisement/
   │   ├── img001.png
   │   ├── img002.png
   │   └── ...
   ├── scientific_publication/
   │   ├── img001.png
   │   ├── img002.png
   │   └── ...
   └── ...
   ```

---

## 💡 Exemplos Práticos

### Exemplo 1: Classificar 1 Imagem

```python
from document_classifier import DocumentClassifier

classifier = DocumentClassifier()
result = classifier.classify('anuncio.png')

print(f"Tipo: {result['classification']}")
print(f"Score: {result['score']}")
print(f"Confiança: {result['confidence']:.1%}")
```

**Saída:**
```
Tipo: advertisement
Score: 5
Confiança: 50.0%
```

---

### Exemplo 2: Classificar Pasta Inteira

```python
from document_classifier import DocumentClassifier
from pathlib import Path

classifier = DocumentClassifier()

# Processar todas as imagens PNG
for img_path in Path('minha_pasta/').glob('*.png'):
    result = classifier.classify(str(img_path))
    print(f"{img_path.name}: {result['classification']}")
```

**Saída:**
```
doc1.png: advertisement
doc2.png: scientific_article
doc3.png: advertisement
```

---

### Exemplo 3: Avaliar Acurácia

```python
from document_classifier import DocumentClassifier
from pathlib import Path

classifier = DocumentClassifier()

# Teste em advertisements conhecidos
correct = 0
total = 0

for img_path in Path('dataset/advertisement/').glob('*.png')[:20]:
    result = classifier.classify(str(img_path))
    if result['classification'] == 'advertisement':
        correct += 1
    total += 1

print(f"Acurácia: {correct/total:.1%}")
```

---

### Exemplo 4: Ver Características

```python
from document_classifier import DocumentFeatureExtractor

extractor = DocumentFeatureExtractor()
features = extractor.extract_all_features('image.png')

print(f"Saturação: {features['saturation_mean']:.1f}")
print(f"Entropia de Cores: {features['color_entropy']:.1f}")
print(f"Densidade de Texto: {features['text_density']:.3f}")
print(f"Cores Únicas: {features['unique_colors']}")
```

**Saída:**
```
Saturação: 45.2
Entropia de Cores: 6.3
Densidade de Texto: 0.087
Cores Únicas: 3247
```

---

## 🔧 Ajustando o Classificador

### Problema: Muitos Falsos Positivos

Se o classificador está marcando muitos scientific articles como advertisements:

```python
classifier = DocumentClassifier()

# Tornar mais conservador (aumentar thresholds)
classifier.thresholds['saturation_mean'] = 40  # Era 30
classifier.thresholds['color_entropy'] = 6.0   # Era 5.0

result = classifier.classify('image.png')
```

### Problema: Muitos Falsos Negativos

Se está marcando muitos advertisements como scientific articles:

```python
classifier = DocumentClassifier()

# Tornar mais sensível (diminuir thresholds)
classifier.thresholds['saturation_mean'] = 25  # Era 30
classifier.thresholds['text_density'] = 0.18   # Era 0.15

result = classifier.classify('image.png')
```

---

## 📈 Calibração Personalizada

Para encontrar os melhores thresholds para o SEU dataset:

```python
from document_classifier import DocumentFeatureExtractor
from pathlib import Path
import numpy as np

extractor = DocumentFeatureExtractor()

# Coletar features de advertisements
ad_saturations = []
for img in Path('dataset/advertisement/').glob('*.png')[:50]:
    features = extractor.extract_all_features(str(img))
    ad_saturations.append(features['saturation_mean'])

# Coletar features de scientific articles  
article_saturations = []
for img in Path('dataset/scientific_publication/').glob('*.png')[:50]:
    features = extractor.extract_all_features(str(img))
    article_saturations.append(features['saturation_mean'])

# Calcular threshold ideal (ponto médio)
ad_mean = np.mean(ad_saturations)
article_mean = np.mean(article_saturations)
optimal_threshold = (ad_mean + article_mean) / 2

print(f"Advertisement média: {ad_mean:.1f}")
print(f"Scientific Article média: {article_mean:.1f}")
print(f"Threshold ideal: {optimal_threshold:.1f}")
```

---

## 🎯 Interpretando Resultados

### Score

- **Score > 0**: Advertisement
- **Score < 0**: Scientific Article
- **Score = 0**: Incerto

**Magnitude do score indica confiança:**
- Score = ±8: Muito confiante
- Score = ±4: Moderadamente confiante  
- Score = ±1: Pouco confiante

### Confidence

- **> 0.7**: Alta confiança
- **0.4 - 0.7**: Média confiança
- **< 0.4**: Baixa confiança (pode precisar revisão manual)

---

## 🐛 Solução de Problemas

### Erro: "Não foi possível carregar a imagem"

**Causa**: Caminho incorreto ou formato não suportado

**Solução**:
```python
from pathlib import Path

# Verificar se arquivo existe
img_path = 'image.png'
if Path(img_path).exists():
    print("Arquivo encontrado!")
else:
    print("Arquivo não existe. Verifique o caminho.")

# Formatos suportados: .png, .jpg, .jpeg, .bmp, .tiff
```

### Erro: "module 'cv2' has no attribute..."

**Causa**: OpenCV não instalado corretamente

**Solução**:
```bash
pip uninstall opencv-python opencv-python-headless
pip install opencv-python-headless
```

### Classificação Incorreta

**Causa**: Imagem com características atípicas

**Solução**:
1. Verifique as características extraídas
2. Ajuste os thresholds
3. Adicione regras customizadas

```python
# Ver características
result = classifier.classify('image.png')
print(result['features'])

# Identificar qual regra está falhando
features = result['features']
print(f"Saturação: {features['saturation_mean']} (threshold: 30)")
print(f"Entropia: {features['color_entropy']} (threshold: 5.0)")
print(f"Densidade texto: {features['text_density']} (threshold: 0.15)")
```

---

## 📚 Uso Avançado

### Processamento em Lote

```python
from document_classifier import DocumentClassifier
from pathlib import Path
import json

classifier = DocumentClassifier()

# Classificar e salvar resultados
results = []
for img_path in Path('dataset/').rglob('*.png'):
    result = classifier.classify(str(img_path))
    results.append({
        'file': str(img_path),
        'classification': result['classification'],
        'confidence': result['confidence']
    })

# Salvar em JSON
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Integração com Pandas

```python
import pandas as pd
from document_classifier import DocumentClassifier
from pathlib import Path

classifier = DocumentClassifier()

# Criar DataFrame com resultados
data = []
for img_path in Path('dataset/').glob('*.png'):
    result = classifier.classify(str(img_path))
    data.append({
        'filename': img_path.name,
        'classification': result['classification'],
        'score': result['score'],
        'confidence': result['confidence'],
        'saturation': result['features']['saturation_mean'],
        'text_density': result['features']['text_density']
    })

df = pd.DataFrame(data)
print(df)

# Análise estatística
print(df.groupby('classification').mean())

# Salvar em CSV
df.to_csv('results.csv', index=False)
```

---

## 🎓 Aprendizado de Máquina (Próximo Passo)

Para melhor performance, considere treinar um modelo ML:

```python
from sklearn.ensemble import RandomForestClassifier
from document_classifier import DocumentFeatureExtractor
import numpy as np

# 1. Extrair features de imagens conhecidas
extractor = DocumentFeatureExtractor()

X = []  # Features
y = []  # Labels (0=ad, 1=article)

# Coletar features
for img in Path('dataset/advertisement/').glob('*.png'):
    features = extractor.extract_all_features(str(img))
    X.append(list(features.values()))
    y.append(0)

for img in Path('dataset/scientific_publication/').glob('*.png'):
    features = extractor.extract_all_features(str(img))
    X.append(list(features.values()))
    y.append(1)

# 2. Treinar modelo
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# 3. Avaliar
from sklearn.model_selection import cross_val_score
scores = cross_val_score(clf, X, y, cv=5)
print(f"Acurácia média: {scores.mean():.2%}")

# 4. Usar modelo
new_features = extractor.extract_all_features('new_image.png')
prediction = clf.predict([list(new_features.values())])
print("Advertisement" if prediction[0] == 0 else "Scientific Article")
```

---

## 📞 Suporte

### Problemas Comuns

1. **Dependências**: `pip install -r requirements.txt`
2. **Dataset**: Baixar do Kaggle (link acima)
3. **Imagens**: Usar formatos PNG, JPG, ou TIFF
4. **Performance**: Ajustar thresholds conforme seu dataset

### Recursos Adicionais

- `README.md` - Documentação completa
- `document_classifier.py` - Código fonte
- `document_classifier.ipynb` - Notebook interativo
- `example_usage.py` - Exemplos de uso

---

## ✅ Checklist de Implementação

- [ ] Instalar dependências (`pip install -r requirements.txt`)
- [ ] Baixar dataset RVL-CDIP do Kaggle
- [ ] Testar classificação em uma imagem
- [ ] Avaliar acurácia no seu dataset
- [ ] Ajustar thresholds se necessário
- [ ] Implementar no seu pipeline

---

**Pronto para começar! 🎉**

Execute: `python example_usage.py` para ver exemplos interativos!

