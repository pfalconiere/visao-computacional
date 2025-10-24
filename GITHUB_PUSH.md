# Como Fazer Push para o GitHub

## Status Atual

✅ Repositório inicializado  
✅ Arquivos commitados  
✅ Remote configurado  
⏳ Aguardando autenticação

## Métodos de Autenticação

### 1. Personal Access Token (PAT)

**Passo 1:** Gere um token
- Acesse: https://github.com/settings/tokens/new
- Dê um nome: "Document Classifier Project"
- Selecione: ✅ `repo` (full control)
- Clique em "Generate token"
- **Copie o token** (você só verá uma vez!)

**Passo 2:** Use o token para fazer push
```bash
cd ~/document_classifier_project
git push -u origin main

# Quando pedir credenciais:
Username: pfalconiere
Password: ghp_seuTokenAqui123456789
```

**Dica:** Salve o token no cache:
```bash
git config --global credential.helper cache
git push -u origin main
```

### 2. SSH (Recomendado para uso frequente)

**Passo 1:** Gere chave SSH
```bash
ssh-keygen -t ed25519 -C "seu_email@example.com"
# Pressione Enter 3 vezes
```

**Passo 2:** Copie a chave pública
```bash
cat ~/.ssh/id_ed25519.pub
```

**Passo 3:** Adicione no GitHub
- Acesse: https://github.com/settings/keys
- Clique em "New SSH key"
- Cole a chave
- Clique em "Add SSH key"

**Passo 4:** Mude para SSH e faça push
```bash
cd ~/document_classifier_project
git remote set-url origin git@github.com:pfalconiere/visao-computacional.git
git push -u origin main
```

### 3. GitHub CLI (gh)

```bash
# Instalar
brew install gh

# Autenticar
gh auth login

# Fazer push
cd ~/document_classifier_project
git push -u origin main
```

## Verificar Push

Depois do push, verifique:
- https://github.com/pfalconiere/visao-computacional

Você deverá ver:
- ✅ 21 arquivos
- ✅ README.md renderizado
- ✅ Documentação em `/docs`
- ✅ Interface web em `index.html`

## Troubleshooting

### Erro: "Permission denied"
- Verifique se está usando as credenciais corretas
- Se usar SSH, verifique se a chave está no GitHub

### Erro: "Authentication failed"
- Token expirado ou inválido
- Gere um novo token

### Erro: "Repository not found"
- Verifique se o repositório existe
- Verifique se o remote está correto: `git remote -v`

## Após o Push

Atualize o README com screenshot real:
1. Faça deploy do projeto
2. Tire um screenshot da interface
3. Suba para o repositório
4. Atualize o README.md
