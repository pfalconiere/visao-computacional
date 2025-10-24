# 🚀 Deploy Completo - API + Frontend Funcionando

## ✅ Status Atual

- ✅ Código no GitHub
- ✅ Frontend no GitHub Pages
- ⏳ Aguardando deploy da API no Render

## 🎯 O Que Você Vai Ter

Depois deste deploy, você terá:

1. **Frontend funcionando** em `https://pfalconiere.github.io/visao-computacional/`
2. **API funcionando** em `https://visao-computacional-api.onrender.com` (ou similar)
3. **Usuários poderão** acessar o site, fazer upload de imagem `.tif` e receber classificação!

---

## 📋 Passo a Passo Completo

### PARTE 1: Deploy da API no Render (5 minutos)

#### 1. Criar conta no Render

Acesse: https://render.com/register

- Faça login com sua conta GitHub
- Autorize o Render a acessar seus repositórios

#### 2. Criar Web Service

1. No dashboard do Render, clique em **"New +"** > **"Web Service"**

2. Conecte seu repositório:
   - Selecione: **"visao-computacional"**
   - Clique em **"Connect"**

3. Configure o serviço:
   
   ```
   Name: visao-computacional-api
   Region: Oregon (US West) [ou qualquer]
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT api:app
   ```

4. Escolha o plano:
   - Selecione: **"Free"** (grátis!)
   
5. Clique em **"Create Web Service"**

#### 3. Aguardar Deploy (2-5 minutos)

O Render vai:
- ✅ Instalar dependências
- ✅ Iniciar a API
- ✅ Gerar uma URL pública

Você verá: **"Your service is live 🎉"**

#### 4. Copiar URL da API

Você receberá uma URL tipo:
```
https://visao-computacional-api.onrender.com
```

**COPIE ESSA URL!**

---

### PARTE 2: Atualizar Frontend com URL da API (2 minutos)

#### 1. Editar index.html

No seu computador:

```bash
cd ~/document_classifier_project
```

Abra `index.html` e procure por (linha ~278):

```javascript
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000'
    : 'https://visao-computacional-api.onrender.com'; // VOCÊ VAI ATUALIZAR ESSA URL!
```

**Substitua** `https://visao-computacional-api.onrender.com` pela sua URL do Render!

#### 2. Fazer Commit e Push

```bash
git add index.html
git commit -m "✅ Update API URL to Render deployment"
git push origin main

# Atualizar GitHub Pages
git checkout gh-pages
git checkout main -- index.html
git add index.html
git commit -m "✅ Update GitHub Pages with Render API URL"
git push origin gh-pages
git checkout main
```

---

### PARTE 3: Ativar GitHub Pages (1 minuto)

1. Acesse: https://github.com/pfalconiere/visao-computacional/settings/pages

2. Configure:
   - Source: **Deploy from a branch**
   - Branch: **gh-pages**
   - Folder: **/ (root)**

3. Clique em **"Save"**

4. Aguarde 1-2 minutos

---

## 🎉 PRONTO! Acesse Seu Site

Depois de 1-2 minutos, acesse:

🔗 **https://pfalconiere.github.io/visao-computacional/**

O que funcionará:
- ✅ Upload de imagens .tif
- ✅ Preview da imagem
- ✅ Classificação em tempo real
- ✅ Resultado visual
- ✅ Features extraídas

---

## 🧪 Testar o Sistema

### 1. Verificar API

Abra: `https://sua-url.onrender.com/health`

Deve retornar:
```json
{
  "status": "healthy",
  "message": "API está funcionando corretamente"
}
```

### 2. Testar Frontend

1. Acesse: https://pfalconiere.github.io/visao-computacional/
2. Você deve ver: **"✅ API Online e funcionando!"**
3. Faça upload de uma imagem .tif
4. Clique em "Classificar Documento"
5. Veja o resultado!

---

## ⚠️ Importante sobre o Plano Free do Render

O plano gratuito do Render tem algumas limitações:

- **Sleep após inatividade**: A API "dorme" após 15 minutos sem uso
- **Primeira requisição lenta**: Pode demorar 30-60 segundos para "acordar"
- **Solução**: A primeira pessoa que acessar precisa esperar um pouco

**Dica**: O frontend mostra "API offline" enquanto ela está "dormindo". É normal!

---

## 🚀 Melhorias Futuras (Opcional)

### 1. Remover Limitação de Sleep

**Opção 1**: Upgrade para plano pago ($7/mês)
- API sempre online
- Mais CPU e RAM

**Opção 2**: Usar serviço sempre-on
- Railway: https://railway.app
- Vercel (para API): https://vercel.com
- AWS Lambda

### 2. Adicionar Mais Formatos de Imagem

Edite `api.py` linha 26:

```python
ALLOWED_EXTENSIONS = {'tif', 'tiff', 'png', 'jpg', 'jpeg'}
```

### 3. Adicionar Analytics

Adicione Google Analytics ao `index.html` para ver quantas pessoas usam.

---

## 📊 Monitoramento

### Ver Logs da API

1. No dashboard do Render
2. Clique no seu serviço
3. Vá em **"Logs"**
4. Veja requisições em tempo real

### Ver Tráfego do GitHub Pages

1. Acesse: https://github.com/pfalconiere/visao-computacional
2. Clique em **"Insights"** > **"Traffic"**

---

## 🐛 Troubleshooting

### Erro: "API offline"

**Causa**: API está dormindo (plano free)

**Solução**: 
- Aguarde 30-60 segundos
- A API vai acordar automaticamente
- Tente classificar novamente

### Erro: "CORS"

**Causa**: URL da API não foi atualizada no frontend

**Solução**:
- Verifique se atualizou o `index.html` com a URL correta
- Faça push para gh-pages novamente

### Erro: "Module not found"

**Causa**: Falta dependência no `requirements.txt`

**Solução**:
- Adicione a dependência em `requirements.txt`
- Faça commit e push
- Render vai fazer redeploy automaticamente

---

## ✅ Checklist Final

- [ ] API deployada no Render
- [ ] URL da API copiada
- [ ] `index.html` atualizado com URL da API
- [ ] Push feito para main e gh-pages
- [ ] GitHub Pages ativado
- [ ] Site acessível
- [ ] API respondendo
- [ ] Upload de imagem funcionando
- [ ] Classificação funcionando

---

## 🎊 Parabéns!

Você agora tem um sistema completo de classificação de documentos funcionando online!

**Compartilhe**: https://pfalconiere.github.io/visao-computacional/

---

## 📱 Próximos Passos

1. ⭐ Compartilhe nas redes sociais
2. 📸 Tire screenshots para o portfólio
3. 📝 Escreva um artigo sobre o projeto
4. 🎬 Grave um vídeo demonstração
5. 💼 Adicione ao LinkedIn/CV

---

**Dúvidas?** Abra uma issue no GitHub!
