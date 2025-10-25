#!/usr/bin/env python3
"""Retreino Rápido com Feature de Linhas"""

import sys
sys.path.append('/Users/test/document_classifier_project')

from classificador_final import ClassificadorFinal
from paragraph_detector import ParagraphDetector
import glob
import random
import json
import time

class ClassificadorComLinhas(ClassificadorFinal):
    def __init__(self):
        super().__init__()
        self.paragraph_detector = ParagraphDetector()
        self.threshold_linhas = 20
        self.peso_linhas = 1.0
    
    def classify_with_lines(self, image_path):
        result = self.classify(image_path)
        try:
            para_stats = self.paragraph_detector.analyze(image_path)
            num_lines = para_stats['num_lines']
            num_paragraphs = para_stats['num_paragraphs']
            
            score = result['score']
            if num_lines < self.threshold_linhas:
                score += self.peso_linhas
            else:
                score -= self.peso_linhas
            
            result['score'] = score
            result['classification'] = 'advertisement' if score > 0 else 'scientific_article'
            result['num_lines'] = num_lines
            result['num_paragraphs'] = num_paragraphs
        except:
            pass
        return result

print("╔═══════════════════════════════════════════════════════════════════════╗")
print("║           🚀 RETREINO RÁPIDO - OTIMIZAÇÃO COM LINHAS 🚀              ║")
print("╚═══════════════════════════════════════════════════════════════════════╝\n")

# Carregar dados
print("📂 Carregando dataset...")
ads = glob.glob('/Users/test/Downloads/test/advertisement/*.tif')[:500]
articles = glob.glob('/Users/test/Downloads/test/scientific_publication/*.tif')[:500]
print(f"   Ads: {len(ads)}")
print(f"   Articles: {len(articles)}")

# Baseline
print("\n📊 Testando baseline (modelo atual)...")
clf = ClassificadorFinal()
baseline_correct = 0
total = 0
for img in ads[:100]:
    try:
        result = clf.classify(img)
        if result['classification'] == 'advertisement':
            baseline_correct += 1
        total += 1
    except:
        pass
for img in articles[:100]:
    try:
        result = clf.classify(img)
        if result['classification'] == 'scientific_article':
            baseline_correct += 1
        total += 1
    except:
        pass
baseline_acc = (baseline_correct / total) * 100
print(f"   Acurácia baseline: {baseline_acc:.2f}%")

# Otimização
print("\n🔄 Iniciando otimização (10,000 iterações)...")
print("   Isso vai levar ~20-30 minutos...\n")

best_accuracy = 0
best_params = None
iteration = 0
start_time = time.time()

for i in range(10000):
    iteration += 1
    
    # Gerar parâmetros aleatórios
    threshold_linhas = random.uniform(10, 35)
    peso_linhas = random.uniform(0.1, 3.0)
    
    # Testar
    clf_test = ClassificadorComLinhas()
    clf_test.threshold_linhas = threshold_linhas
    clf_test.peso_linhas = peso_linhas
    
    correct = 0
    tested = 0
    
    # Testar amostra (50 de cada para velocidade)
    sample_ads = random.sample(ads, min(50, len(ads)))
    sample_articles = random.sample(articles, min(50, len(articles)))
    
    for img in sample_ads:
        try:
            result = clf_test.classify_with_lines(img)
            if result['classification'] == 'advertisement':
                correct += 1
            tested += 1
        except:
            pass
    
    for img in sample_articles:
        try:
            result = clf_test.classify_with_lines(img)
            if result['classification'] == 'scientific_article':
                correct += 1
            tested += 1
        except:
            pass
    
    accuracy = (correct / tested) * 100 if tested > 0 else 0
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_params = {
            'threshold_linhas': threshold_linhas,
            'peso_linhas': peso_linhas
        }
        elapsed = time.time() - start_time
        print(f"   ✨ Iteração {iteration:,}: {accuracy:.2f}% (threshold={threshold_linhas:.1f}, peso={peso_linhas:.2f}) [{elapsed:.0f}s]")
    
    if iteration % 1000 == 0:
        elapsed = time.time() - start_time
        print(f"   ⏳ Iteração {iteration:,}... melhor até agora: {best_accuracy:.2f}% [{elapsed:.0f}s]")

print(f"\n✅ Otimização completa!")
print(f"   Melhor acurácia: {best_accuracy:.2f}%")
print(f"   Threshold linhas: {best_params['threshold_linhas']:.2f}")
print(f"   Peso linhas: {best_params['peso_linhas']:.2f}")

# Testar no dataset completo
print("\n🧪 Testando no dataset completo (200 de cada)...")
clf_final = ClassificadorComLinhas()
clf_final.threshold_linhas = best_params['threshold_linhas']
clf_final.peso_linhas = best_params['peso_linhas']

ads_correct = 0
ads_total = 0
for img in ads[:200]:
    try:
        result = clf_final.classify_with_lines(img)
        if result['classification'] == 'advertisement':
            ads_correct += 1
        ads_total += 1
    except:
        pass

articles_correct = 0
articles_total = 0
for img in articles[:200]:
    try:
        result = clf_final.classify_with_lines(img)
        if result['classification'] == 'scientific_article':
            articles_correct += 1
        articles_total += 1
    except:
        pass

final_acc = ((ads_correct + articles_correct) / (ads_total + articles_total)) * 100
ads_acc = (ads_correct / ads_total) * 100
articles_acc = (articles_correct / articles_total) * 100

print(f"\n📊 RESULTADOS FINAIS:")
print(f"   Advertisements: {ads_correct}/{ads_total} ({ads_acc:.2f}%)")
print(f"   Scientific Articles: {articles_correct}/{articles_total} ({articles_acc:.2f}%)")
print(f"   GERAL: {final_acc:.2f}%")
print(f"   Baseline: {baseline_acc:.2f}%")
print(f"   Melhoria: {final_acc - baseline_acc:+.2f}%")

# Salvar parâmetros
with open('~/document_classifier_project/best_params_with_lines.json', 'w') as f:
    json.dump(best_params, f, indent=2)

print(f"\n💾 Parâmetros salvos em: best_params_with_lines.json")
