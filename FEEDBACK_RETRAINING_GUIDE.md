# 🔄 Sistema de Feedback e Retreino

## 📊 **Visão Geral**

Este sistema coleta feedback dos usuários sobre classificações e permite retreinar o modelo periodicamente para melhorar sua acurácia.

---

## 🎯 **Estratégia de Retreino (RECOMENDADA)**

### ✅ **Batch Learning** (Implementado)

- **Acumular**: 100-500 feedbacks antes de retreinar
- **Validar**: Testar nova acurácia antes de deploy
- **Periodicidade**: Semanal/Mensal
- **Estável**: Evita overfitting e manipulação

### ❌ **Online Learning** (NÃO Recomendado)

- Retreina a cada feedback
- Instável, manipulável, overfitting
- Não use em produção!

---

## 📁 **Arquivos do Sistema**

### 1. **`feedback_data.csv`**
Armazena todos os feedbacks:

```csv
timestamp,image_name,predicted_class,is_correct,correct_class
2025-10-25 10:30:15,doc1.tif,advertisement,true,advertisement
2025-10-25 10:31:22,doc2.tif,scientific_article,false,advertisement
```

### 2. **Endpoints da API**

#### POST `/feedback`
Envia feedback sobre uma classificação:

```bash
curl -X POST http://localhost:5000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "image_name": "document.tif",
    "predicted_class": "advertisement",
    "is_correct": "true",
    "correct_class": "advertisement"
  }'
```

#### GET `/feedback/stats`
Retorna estatísticas dos feedbacks:

```bash
curl http://localhost:5000/feedback/stats
```

Resposta:
```json
{
  "success": true,
  "total": 150,
  "correct": 135,
  "incorrect": 15,
  "accuracy": 90.0,
  "by_class": {
    "advertisement": {
      "correct": 70,
      "incorrect": 8,
      "accuracy": 89.74
    },
    "scientific_article": {
      "correct": 65,
      "incorrect": 7,
      "accuracy": 90.28
    }
  },
  "ready_for_retraining": true,
  "retraining_recommendation": "✅ RECOMENDADO: Grande volume de dados, retreino pode melhorar o modelo"
}
```

---

## 🔁 **Processo de Retreino**

### **Quando Retreinar?**

1. **✅ 100+ feedbacks** coletados
2. **⚠️ Acurácia < 80%** (modelo degradando)
3. **📅 Periodicidade** (mensal recomendado)
4. **📊 500+ feedbacks** (grande volume)

### **Como Retreinar?**

#### **Opção 1: Manual (Recomendado)**

1. **Verificar estatísticas:**
   ```bash
   curl http://localhost:5000/feedback/stats
   ```

2. **Baixar feedbacks:**
   ```bash
   # Copiar feedback_data.csv do servidor
   scp user@server:/path/feedback_data.csv ./
   ```

3. **Analisar dados:**
   - Ver distribuição de erros
   - Identificar padrões problemáticos
   - Decidir se vale a pena retreinar

4. **Retreinar modelo:**
   ```bash
   python3 retrain_from_feedback.py
   ```

5. **Validar nova acurácia:**
   ```bash
   python3 validate_new_model.py
   ```

6. **Deploy se melhorou:**
   ```bash
   git add classificador_final.py
   git commit -m "Atualizar modelo com feedback (acurácia: 92.5%)"
   git push origin main
   ```

#### **Opção 2: Automático (Cuidado!)**

```bash
# Apenas para ambientes controlados
python3 auto_retrain.py --min-feedbacks 100 --min-accuracy 85
```

---

## 🛠️ **Scripts de Retreino**

### **1. Verificar Status**

```bash
# Ver estatísticas de feedback
python3 check_feedback_stats.py
```

### **2. Retreinar Modelo**

```bash
# Retreinar com feedbacks coletados
python3 retrain_from_feedback.py --validate
```

### **3. Validar Modelo**

```bash
# Testar novo modelo antes de deploy
python3 validate_new_model.py --old-model classificador_final.py --new-model classificador_retrained.py
```

---

## 📊 **Métricas Importantes**

### **Mínimos Recomendados**

- **Feedbacks totais**: 100+
- **Acurácia mínima**: 80%
- **Feedbacks por classe**: 50+ cada
- **Proporção correto/incorreto**: 70/30

### **Alertas**

- ⚠️ **Acurácia < 75%**: Problema sério, retreinar urgente
- ⚠️ **Uma classe < 60%**: Desbalanceamento, coletar mais dados
- ⚠️ **Muito feedback incorreto**: Revisar features ou regras

---

## 🚀 **Melhorias Futuras**

### **Curto Prazo**
- [ ] Dashboard de feedback (Grafana/Streamlit)
- [ ] Alertas automáticos (Email/Slack)
- [ ] Exportar feedbacks para análise

### **Médio Prazo**
- [ ] A/B Testing (modelo antigo vs novo)
- [ ] Validação cruzada automática
- [ ] Backup automático de modelos

### **Longo Prazo**
- [ ] Active Learning (pedir feedback em casos duvidosos)
- [ ] Ensemble com feedback
- [ ] Migrar para ML real (CNN/Transformers)

---

## 📝 **Exemplo Completo**

### **1. Coletar 100 Feedbacks**

Usuários classificam documentos pelo frontend e enviam feedback (correto/incorreto).

### **2. Verificar Status**

```bash
$ curl http://localhost:5000/feedback/stats

{
  "total": 120,
  "correct": 98,
  "incorrect": 22,
  "accuracy": 81.67,
  "ready_for_retraining": true
}
```

### **3. Analisar Feedbacks Incorretos**

```bash
$ grep "false" feedback_data.csv | head -5

2025-10-25 10:35:22,doc5.tif,advertisement,false,scientific_article
2025-10-25 11:20:15,doc12.tif,scientific_article,false,advertisement
...
```

### **4. Retreinar Modelo**

```bash
$ python3 retrain_from_feedback.py

🔄 Retreinando modelo...
📊 Feedbacks: 120 (98 corretos, 22 incorretos)
✅ Novo modelo: 88.5% acurácia (+6.5%)
💾 Salvando classificador_final.py...
✅ Retreino concluído!
```

### **5. Deploy**

```bash
$ git add classificador_final.py
$ git commit -m "Retreinar modelo: 88.5% acurácia (120 feedbacks)"
$ git push origin main

# Render.com fará deploy automático
```

---

## ⚠️ **Avisos Importantes**

### **NÃO FAZER:**
- ❌ Retreinar com < 50 feedbacks
- ❌ Deploy sem validação
- ❌ Retreino automático em produção sem testes
- ❌ Ignorar feedback negativo sistemático

### **SEMPRE FAZER:**
- ✅ Validar nova acurácia
- ✅ Backup do modelo antigo
- ✅ Testar em dataset de validação
- ✅ Monitorar métricas pós-deploy
- ✅ Documentar mudanças

---

## 🎓 **Conceitos**

### **Overfitting**
Quando o modelo "decora" os dados de treino e perde generalização.

**Solução**: Acumular muitos feedbacks antes de retreinar (100+).

### **Data Poisoning**
Quando usuários maliciosos enviam feedbacks errados propositalmente.

**Solução**: Validação manual periódica dos feedbacks.

### **Concept Drift**
Quando o tipo de documento muda com o tempo.

**Solução**: Monitorar acurácia e retreinar periodicamente.

---

## 📚 **Referências**

- [Online vs Batch Learning](https://scikit-learn.org/stable/modules/scaling_strategies.html)
- [Active Learning](https://modal-python.readthedocs.io/en/latest/content/overview/active_learning.html)
- [Model Retraining Best Practices](https://ml-ops.org/content/phase-two)

---

## 💡 **Suporte**

Dúvidas? Entre em contato:
- **Email**: pedro@example.com
- **GitHub Issues**: https://github.com/pfalconiere/visao-computacional/issues

---

**Última atualização**: 2025-10-25
**Versão do Sistema**: 2.0
**Autor**: Pedro Falcão Martins
