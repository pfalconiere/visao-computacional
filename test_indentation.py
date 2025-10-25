#!/usr/bin/env python3
import sys
sys.path.append('/Users/test/document_classifier_project')
from paragraph_detector import ParagraphDetector
import glob
import numpy as np

detector = ParagraphDetector()

print("📊 Testando ADVERTISEMENTS (50 amostras):")
ads = glob.glob('/Users/test/Downloads/test/advertisement/*.tif')[:50]
ad_paragraphs = []
for img in ads:
    try:
        stats = detector.analyze(img)
        ad_paragraphs.append(stats['num_paragraphs'])
    except:
        pass
print(f"   Parágrafos (média): {np.mean(ad_paragraphs):.1f}")
print(f"   Range: {min(ad_paragraphs)}-{max(ad_paragraphs)}")

print("\n📊 Testando SCIENTIFIC ARTICLES (50 amostras):")
articles = glob.glob('/Users/test/Downloads/test/scientific_publication/*.tif')[:50]
article_paragraphs = []
for img in articles:
    try:
        stats = detector.analyze(img)
        article_paragraphs.append(stats['num_paragraphs'])
    except:
        pass
print(f"   Parágrafos (média): {np.mean(article_paragraphs):.1f}")
print(f"   Range: {min(article_paragraphs)}-{max(article_paragraphs)}")

print(f"\n✅ Diferença: Articles têm {np.mean(article_paragraphs) - np.mean(ad_paragraphs):.1f} parágrafos A MAIS!")
