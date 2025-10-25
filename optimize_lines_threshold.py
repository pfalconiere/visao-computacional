#!/usr/bin/env python3
"""Otimiza threshold de linhas"""

import sys
sys.path.append('/Users/test/document_classifier_project')

from paragraph_detector import ParagraphDetector
import glob
import numpy as np

detector = ParagraphDetector()

print("📊 Coletando dados...")

# Coletar num_lines de todas as amostras
ads = glob.glob('/Users/test/Downloads/test/advertisement/*.tif')[:200]
ad_lines = []
for img in ads:
    try:
        stats = detector.analyze(img)
        ad_lines.append(stats['num_lines'])
    except:
        pass

articles = glob.glob('/Users/test/Downloads/test/scientific_publication/*.tif')[:200]
article_lines = []
for img in articles:
    try:
        stats = detector.analyze(img)
        article_lines.append(stats['num_lines'])
    except:
        pass

print(f"\nAds: {len(ad_lines)} amostras")
print(f"   Média: {np.mean(ad_lines):.1f} linhas")
print(f"   Mediana: {np.median(ad_lines):.1f} linhas")
print(f"   Min/Max: {min(ad_lines)}/{max(ad_lines)} linhas")

print(f"\nArticles: {len(article_lines)} amostras")
print(f"   Média: {np.mean(article_lines):.1f} linhas")
print(f"   Mediana: {np.median(article_lines):.1f} linhas")
print(f"   Min/Max: {min(article_lines)}/{max(article_lines)} linhas")

# Encontrar melhor threshold
print("\n🎯 Testando thresholds...")
best_threshold = 0
best_accuracy = 0

for threshold in range(5, 50, 2):
    ads_correct = sum(1 for x in ad_lines if x < threshold)
    articles_correct = sum(1 for x in article_lines if x >= threshold)
    accuracy = (ads_correct + articles_correct) / (len(ad_lines) + len(article_lines))
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_threshold = threshold

print(f"\n✅ Melhor threshold: {best_threshold} linhas")
print(f"   Acurácia: {best_accuracy*100:.2f}%")
print(f"   Ads < {best_threshold}: {sum(1 for x in ad_lines if x < best_threshold)}/{len(ad_lines)}")
print(f"   Articles >= {best_threshold}: {sum(1 for x in article_lines if x >= best_threshold)}/{len(article_lines)}")
