#!/usr/bin/env python3
"""Analisa parágrafos em todo o dataset"""

import sys
sys.path.append('/Users/test/document_classifier_project')

from paragraph_detector import ParagraphDetector
import glob
import numpy as np

detector = ParagraphDetector()

print("📊 Analisando ADVERTISEMENTS...")
ads = glob.glob('/Users/test/Downloads/test/advertisement/*.tif')[:50]
ad_stats = []
for img_path in ads:
    try:
        stats = detector.analyze(img_path)
        ad_stats.append(stats)
    except:
        pass

print(f"   Amostras: {len(ad_stats)}")
print(f"   Linhas (média): {np.mean([s['num_lines'] for s in ad_stats]):.1f}")
print(f"   Parágrafos (média): {np.mean([s['num_paragraphs'] for s in ad_stats]):.1f}")

print("\n📊 Analisando SCIENTIFIC ARTICLES...")
articles = glob.glob('/Users/test/Downloads/test/scientific_publication/*.tif')[:50]
article_stats = []
for img_path in articles:
    try:
        stats = detector.analyze(img_path)
        article_stats.append(stats)
    except:
        pass

print(f"   Amostras: {len(article_stats)}")
print(f"   Linhas (média): {np.mean([s['num_lines'] for s in article_stats]):.1f}")
print(f"   Parágrafos (média): {np.mean([s['num_paragraphs'] for s in article_stats]):.1f}")

print("\n📈 COMPARAÇÃO:")
ad_lines_avg = np.mean([s['num_lines'] for s in ad_stats])
article_lines_avg = np.mean([s['num_lines'] for s in article_stats])
diff = article_lines_avg - ad_lines_avg
diff_pct = (diff / ad_lines_avg) * 100

print(f"   Articles têm {diff:.1f} linhas a MAIS que Ads ({diff_pct:+.1f}%)")
print(f"   Diferença significativa: {'SIM ✅' if abs(diff) > 10 else 'NÃO ❌'}")
