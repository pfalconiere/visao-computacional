# 🖼️ Imagens de Teste

Este diretório deve conter imagens de teste para os testes unitários e de API.

## 📁 Estrutura Esperada

```
test_images/
├── advertisement.tif      # 1 imagem de advertisement/anúncio
├── scientific.tif         # 1 imagem de artigo científico
├── invalid.jpg           # 1 arquivo .jpg (para teste negativo)
└── README.md             # Este arquivo
```

## 🎯 Como Obter as Imagens

### **Opção 1: Dataset RVL-CDIP**

Se você tem acesso ao dataset RVL-CDIP:

1. **Advertisement:**
   ```bash
   cp /path/to/rvl-cdip/advertisement/000001.tif test_images/advertisement.tif
   ```

2. **Scientific Article:**
   ```bash
   cp /path/to/rvl-cdip/scientific_publication/000001.tif test_images/scientific.tif
   ```

3. **Invalid (qualquer .jpg):**
   ```bash
   cp /path/to/any/image.jpg test_images/invalid.jpg
   ```

### **Opção 2: Criar Imagens Sintéticas**

Use Python + PIL para criar imagens de teste:

```python
from PIL import Image, ImageDraw, ImageFont

# Advertisement (simples, pouco texto)
img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)
draw.text((50, 50), "SALE 50% OFF", fill='red')
draw.rectangle([100, 200, 700, 500], outline='black', width=3)
img.save('test_images/advertisement.tif', format='TIFF')

# Scientific Article (muito texto)
img = Image.new('RGB', (800, 1200), color='white')
draw = ImageDraw.Draw(img)
y = 50
for i in range(20):
    draw.text((50, y), f"Paragraph {i+1}: Lorem ipsum dolor sit amet...", fill='black')
    y += 50
img.save('test_images/scientific.tif', format='TIFF')

# Invalid (qualquer imagem em .jpg)
img = Image.new('RGB', (100, 100), color='blue')
img.save('test_images/invalid.jpg', format='JPEG')
```

### **Opção 3: Download de Exemplos**

Se você tem exemplos de documentos reais (PDFs, etc.), converta-os para .tif:

```bash
# ImageMagick
convert documento.pdf -density 300 test_images/advertisement.tif
convert artigo.pdf -density 300 test_images/scientific.tif
```

## ⚠️ Importante

- **NÃO** commitar imagens grandes no Git (use `.gitignore`)
- As imagens devem ser **reais ou sintéticas**, mas com características distintas:
  - **Advertisement:** Pouco texto, layout simples, elementos visuais
  - **Scientific:** Muito texto, múltiplos parágrafos, estrutura complexa
- O arquivo `invalid.jpg` é apenas para testar rejeição de formato incorreto

## 🧪 Testar se as Imagens Funcionam

```bash
python -c "
from PIL import Image
import os

for f in ['advertisement.tif', 'scientific.tif', 'invalid.jpg']:
    path = f'test_images/{f}'
    if os.path.exists(path):
        img = Image.open(path)
        print(f'✅ {f}: {img.size} - {img.format}')
    else:
        print(f'❌ {f}: NÃO ENCONTRADO')
"
```

## 📝 Uso nos Testes

- **Pytest:** Usa fixtures que criam imagens sintéticas (não precisa de arquivos reais)
- **Newman/Postman:** Precisa de arquivos reais em `test_images/`

Se você não adicionar as imagens:
- ✅ Testes unitários (pytest) funcionarão normalmente
- ❌ Testes de API (Newman) falharão nos testes de classificação

## 🔒 Segurança

Se usar imagens reais:
- Verifique se não contêm informações confidenciais
- Não commite imagens proprietárias/licenciadas
- Adicione `test_images/*.tif` ao `.gitignore`

