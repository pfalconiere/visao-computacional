# 📊 Guia de Configuração do Google Analytics 4

Este projeto está configurado com **Google Analytics 4 (GA4)** para rastreamento de métricas de uso.

---

## 🚀 **Como Configurar (5 minutos)**

### **PASSO 1: Criar conta no Google Analytics**

1. Acesse: **https://analytics.google.com**
2. Clique em **"Começar a medir"** (ou "Start measuring")
3. Crie uma **Conta**:
   - Nome da conta: `Document Classifier` (ou qualquer nome)
   - Configure compartilhamento de dados (padrão está OK)

### **PASSO 2: Criar uma Propriedade**

1. Nome da propriedade: `Document Classifier - Produção`
2. Fuso horário: `(GMT-03:00) Brasília`
3. Moeda: `Real brasileiro (R$)`

### **PASSO 3: Configurar Fluxo de Dados**

1. Escolha plataforma: **"Web"**
2. Preencha:
   - **URL do website**: `https://pfalconiere.github.io`
   - **Nome do stream**: `Document Classifier Web`
3. Clique em **"Criar stream"**

### **PASSO 4: Copiar o Measurement ID**

Após criar o stream, você verá:

```
Measurement ID: G-XXXXXXXXXX
```

**Este é o ID que você precisa!** ✅

---

## 🔧 **Integrar no Projeto**

### **1. Abrir o arquivo `index.html`**

Procure por estas linhas (próximo ao início do arquivo):

```html
<!-- Google Analytics 4 -->
<!-- INSTRUÇÕES: Substitua 'G-XXXXXXXXXX' pelo seu Measurement ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    
    gtag('config', 'G-XXXXXXXXXX', {
        'anonymize_ip': true,
        'cookie_flags': 'SameSite=None;Secure',
        'send_page_view': true
    });
```

### **2. Substituir `G-XXXXXXXXXX` pelo seu ID real**

Substitua **todas as 2 ocorrências** de `G-XXXXXXXXXX` pelo seu Measurement ID:

```html
<!-- ANTES -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
gtag('config', 'G-XXXXXXXXXX', {

<!-- DEPOIS (exemplo com ID G-ABC123DEF4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ABC123DEF4"></script>
gtag('config', 'G-ABC123DEF4', {
```

### **3. Salvar e fazer commit**

```bash
git add index.html
git commit -m "feat: Configura Google Analytics 4 com Measurement ID"
git push origin main
```

### **4. Aguardar deploy (GitHub Pages)**

O GitHub Pages atualiza automaticamente em ~2-5 minutos.

---

## 📊 **Eventos Rastreados Automaticamente**

O projeto está configurado para rastrear:

### **1. Classificações:**
- **`classification_started`**: Quando usuário faz upload e inicia classificação
  - Dados: tamanho do arquivo, tipo do arquivo
- **`classification_completed`**: Quando classificação é concluída
  - Dados: tipo (advertisement/scientific), confiança, contagem de palavras, conformidade

### **2. Feedbacks:**
- **`feedback_submitted`**: Quando usuário marca classificação como correta/incorreta
  - Dados: correto/incorreto, tipo de classificação

### **3. Navegação:**
- **`page_view`**: Quando usuário acessa página do Time
  - Dados: página visualizada

### **4. Métricas Padrão do GA4:**
- ✅ **Origem do tráfego**: De onde os usuários vieram (Google, link direto, redes sociais)
- ✅ **Tempo no site**: Quanto tempo cada usuário passou
- ✅ **Páginas visitadas**: Navegação completa
- ✅ **Dispositivo**: Desktop, mobile, tablet
- ✅ **Localização**: País, cidade
- ✅ **Taxa de rejeição**: Porcentagem de usuários que saíram imediatamente
- ✅ **Sessões**: Número de visitas

---

## 🔍 **Visualizar Dados no Google Analytics**

### **Em Tempo Real:**

1. Acesse o GA4
2. Menu lateral → **"Relatórios"** → **"Tempo real"**
3. Você verá:
   - Usuários ativos agora
   - Páginas sendo visualizadas
   - Eventos acontecendo em tempo real

### **Relatórios Principais:**

1. **Aquisição** → Veja de onde seus usuários vêm:
   - Pesquisa orgânica (Google)
   - Redes sociais
   - Links diretos
   - Referências (outros sites)

2. **Engajamento** → Veja como usuários interagem:
   - Eventos customizados (`classification_started`, `feedback_submitted`, etc.)
   - Páginas mais visitadas
   - Tempo médio no site

3. **Usuários** → Veja informações demográficas:
   - Países
   - Cidades
   - Idiomas
   - Dispositivos (desktop/mobile)

---

## 🛡️ **Conformidade LGPD**

O projeto está configurado para respeitar a LGPD:

- ✅ **`anonymize_ip: true`**: IPs dos usuários são anonimizados
- ✅ **Sem cookies de terceiros**: Configurado para minimizar rastreamento
- ✅ **Dados agregados**: GA4 não identifica usuários individualmente

### **Recomendação:**

Para total conformidade com LGPD, considere adicionar um **banner de cookies** informando sobre o uso do Google Analytics. Você pode usar:
- **Cookie Consent** (gratuito): https://cookieconsent.orestbida.com/
- **OneTrust** (pago, mais completo)

---

## 📈 **Exemplo de Relatório**

Após alguns dias de uso, você terá dados como:

```
📊 ÚLTIMOS 7 DIAS:

USUÁRIOS:
- Total de usuários: 142
- Novos usuários: 98 (69%)
- Usuários recorrentes: 44 (31%)

ORIGEM DO TRÁFEGO:
- Pesquisa orgânica: 56 (39%)
- Link direto: 48 (34%)
- Redes sociais: 38 (27%)

COMPORTAMENTO:
- Classificações iniciadas: 89
- Classificações concluídas: 76 (85% de conclusão)
- Feedbacks enviados: 42 (55% dos que classificaram)
- Tempo médio no site: 3min 24s

DISPOSITIVOS:
- Desktop: 98 (69%)
- Mobile: 44 (31%)
```

---

## 🎓 **Para Apresentação Acadêmica**

Use estes dados na sua apresentação:

1. **Demonstrar Uso Real:**
   - "O sistema teve X acessos em Y dias"
   - "Taxa de conclusão de classificação: Z%"

2. **Mostrar Engajamento:**
   - "Tempo médio de uso: X minutos"
   - "Taxa de feedback dos usuários: Y%"

3. **Dashboard Visual:**
   - Tire prints do GA4 para incluir nos slides
   - Mostre gráficos de origem de tráfego e dispositivos

---

## 🆘 **Troubleshooting**

### **"Não vejo dados no GA4"**

1. Verifique se substituiu `G-XXXXXXXXXX` pelo ID correto
2. Aguarde 24-48h (primeiros dados podem demorar)
3. Teste localmente:
   - Abra o site
   - Abra DevTools (F12) → Console
   - Procure por: `📊 GA Event: ...`
   - Se aparecer, está funcionando!

### **"GA4 diz que o código não foi detectado"**

1. Limpe o cache do navegador (Ctrl+Shift+Del)
2. Aguarde 30 minutos e tente novamente
3. Verifique se o site já foi deployado no GitHub Pages

---

## 📚 **Links Úteis**

- **Google Analytics**: https://analytics.google.com
- **Documentação GA4**: https://support.google.com/analytics
- **Google Tag Assistant**: https://tagassistant.google.com/ (para testar)
- **GA4 Query Explorer**: https://ga-dev-tools.google/ (para consultas avançadas)

---

## ✅ **Checklist de Configuração**

- [ ] Criar conta no Google Analytics
- [ ] Criar propriedade e fluxo de dados
- [ ] Copiar Measurement ID
- [ ] Substituir `G-XXXXXXXXXX` no `index.html`
- [ ] Fazer commit e push
- [ ] Aguardar deploy (2-5 min)
- [ ] Testar acessando o site
- [ ] Verificar dados em tempo real no GA4

---

**Precisa de ajuda?** Abra uma issue no GitHub! 🚀

