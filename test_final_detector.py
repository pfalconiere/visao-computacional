#!/usr/bin/env python3
import sys
sys.path.append('/Users/test/document_classifier_project')
from paragraph_detector import ParagraphDetector
import glob
import numpy as np

detector = ParagraphDetector()

print("📊 ADVERTISEMENTS (100 amostras):")
ads = glob.glob('/Users/test/Downloads/test/advertisement/*.tif')[:100]
ad_paras = []
for img in ads:
    try:
        stats = detector.analyze(img)
        ad_paras.append(stats['num_paragraphs'])
    except:
        pass
print(f"   Média: {np.mean(ad_paras):.1f} parágrafos")
print(f"   Range: {min(ad_paras)}-{max(ad_paras)}")

print("\n📊 SCIENTIFIC ARTICLES (100 amostras):")
articles = glob.glob('/Users/test/Downloads/test/scientific_publication/*.tif')[:100]
art_paras = []
for img in articles:
    try:
        stats = detector.analyze(img)
        art_paras.append(stats['num_paragraphs'])
    except:
        pass
print(f"   Média: {np.mean(art_paras):.1f} parágrafos")
print(f"   Range: {min(art_paras)}-{max(art_paras)}")

print(f"\n✅ Articles têm {np.mean(art_paras) - np.mean(ad_paras):.1f} parágrafos A MAIS!")
