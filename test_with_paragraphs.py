#!/usr/bin/env python3
"""Testa classificador com feature de parágrafos"""

import sys
sys.path.append('/Users/test/document_classifier_project')

from classificador_final import ClassificadorFinal
from paragraph_detector import ParagraphDetector
import glob

class ClassificadorComParagrafos(ClassificadorFinal):
    """Adiciona feature de parágrafos ao classificador existente"""
    
    def __init__(self):
        super().__init__()
        self.paragraph_detector = ParagraphDetector()
        # Threshold baseado na análise: ads=8.4, articles=31.5, meio=~20
        self.threshold_linhas = 20
        self.peso_linhas = 1.5  # Peso da nova regra
    
    def classify_with_paragraphs(self, image_path):
        """Classifica usando features originais + parágrafos"""
        # Classificação original
        result = self.classify(image_path)
        score_original = result['score']
        
        # Adicionar feature de parágrafos
        try:
            para_stats = self.paragraph_detector.analyze(image_path)
            num_lines = para_stats['num_lines']
            
            # REGRA NOVA: Menos linhas = Advertisement, Mais linhas = Article
            if num_lines < self.threshold_linhas:
                score_original += self.peso_linhas  # Advertisement
            else:
                score_original -= self.peso_linhas  # Scientific Article
            
            # Reclassificar com novo score
            classification = 'advertisement' if score_original > 0 else 'scientific_article'
            
            result['score'] = score_original
            result['classification'] = classification
            result['num_lines'] = num_lines
            result['num_paragraphs'] = para_stats['num_paragraphs']
        except:
            pass
        
        return result

# Testar
print("🧪 Testando CLASSIFICADOR COM PARÁGRAFOS...\n")

clf = ClassificadorComParagrafos()

print("📊 ADVERTISEMENTS:")
ads = glob.glob('/Users/test/Downloads/test/advertisement/*.tif')[:100]
ads_correct = 0
for img_path in ads:
    try:
        result = clf.classify_with_paragraphs(img_path)
        if result['classification'] == 'advertisement':
            ads_correct += 1
    except:
        pass

ads_accuracy = (ads_correct / len(ads)) * 100
print(f"   Corretos: {ads_correct}/{len(ads)}")
print(f"   Acurácia: {ads_accuracy:.2f}%")

print("\n📊 SCIENTIFIC ARTICLES:")
articles = glob.glob('/Users/test/Downloads/test/scientific_publication/*.tif')[:100]
articles_correct = 0
for img_path in articles:
    try:
        result = clf.classify_with_paragraphs(img_path)
        if result['classification'] == 'scientific_article':
            articles_correct += 1
    except:
        pass

articles_accuracy = (articles_correct / len(articles)) * 100
print(f"   Corretos: {articles_correct}/{len(articles)}")
print(f"   Acurácia: {articles_accuracy:.2f}%")

overall_accuracy = ((ads_correct + articles_correct) / (len(ads) + len(articles))) * 100
print(f"\n🎯 ACURÁCIA GERAL: {overall_accuracy:.2f}%")
print(f"   Anterior: 89.87%")
print(f"   Melhoria: {overall_accuracy - 89.87:+.2f}%")
