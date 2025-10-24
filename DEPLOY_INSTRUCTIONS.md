# 🚀 Instruções de Deploy

## ✅ Status Atual

- ✅ Código enviado para GitHub
- ✅ Branch `main` com código completo
- ✅ Branch `gh-pages` com landing page
- ⏳ Aguardando ativação do GitHub Pages

## 🌐 Ativar GitHub Pages

### Passo 1: Acessar Configurações

Acesse: https://github.com/pfalconiere/visao-computacional/settings/pages

### Passo 2: Configurar Source

Em **"Build and deployment"**, configure:

- **Source**: Deploy from a branch
- **Branch**: `gh-pages`
- **Folder**: `/ (root)`

### Passo 3: Salvar

Clique em **"Save"**

### Passo 4: Aguardar

O GitHub levará 1-2 minutos para fazer o deploy.

### Passo 5: Acessar

Seu site estará disponível em:

🔗 **https://pfalconiere.github.io/visao-computacional/**

---

## 📱 Links do Projeto

- **Repositório**: https://github.com/pfalconiere/visao-computacional
- **GitHub Pages**: https://pfalconiere.github.io/visao-computacional/
- **Issues**: https://github.com/pfalconiere/visao-computacional/issues

---

## 🔧 Deploy da API (Produção)

O GitHub Pages só serve arquivos estáticos. Para a API Flask funcionar em produção, você precisa de um servidor.

### Opções de Deploy da API:

#### 1. Heroku (Grátis)

```bash
# Criar Procfile
echo "web: gunicorn api:app" > Procfile

# Adicionar ao requirements.txt
echo "gunicorn" >> requirements.txt

# Deploy
heroku create seu-app-classifier
git push heroku main
```

#### 2. Railway

1. Acesse: https://railway.app
2. Conecte com GitHub
3. Selecione o repositório
4. Railway detecta Python automaticamente
5. Adicione variáveis de ambiente se necessário

#### 3. Render

1. Acesse: https://render.com
2. New > Web Service
3. Conecte repositório GitHub
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn api:app`

#### 4. Google Cloud Run

```bash
# Criar Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8080", "api:app"]
EOF

# Deploy
gcloud run deploy classifier-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🔄 Atualizar o Projeto

### Atualizar código (branch main):

```bash
cd ~/document_classifier_project
git add .
git commit -m "Descrição das mudanças"
git push origin main
```

### Atualizar GitHub Pages (branch gh-pages):

```bash
git checkout gh-pages
# Faça suas alterações no index.html
git add index.html
git commit -m "Atualiza landing page"
git push origin gh-pages
git checkout main
```

---

## 📊 Adicionar Badge no README

Adicione ao README.md:

```markdown
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fpfalconiere.github.io%2Fvisao-computacional%2F)](https://pfalconiere.github.io/visao-computacional/)
```

---

## 🎉 Checklist Final

- [ ] GitHub Pages ativado
- [ ] Site acessível em pfalconiere.github.io/visao-computacional
- [ ] README.md atualizado
- [ ] Imagens/screenshots adicionados
- [ ] API rodando localmente
- [ ] Testes realizados
- [ ] Documentação completa
- [ ] Compartilhado nas redes sociais

---

**🎊 Parabéns! Seu projeto está no ar!**
