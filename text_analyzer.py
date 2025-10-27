#!/usr/bin/env python3
"""
Analisador de Texto para Artigos Científicos
Extrai texto via OCR e analisa palavras frequentes
"""

import cv2
from collections import Counter
import re

class TextAnalyzer:
    def __init__(self):
        self.stopwords = set([
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das',
            'em', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'sem', 'sob',
            'e', 'ou', 'mas', 'se', 'que', 'qual', 'quando', 'onde', 'como',
            'the', 'a', 'an', 'and', 'or', 'but', 'if', 'of', 'at', 'by', 'for',
            'with', 'about', 'as', 'into', 'through', 'to', 'from', 'in', 'on'
        ])
        self._pytesseract = None
        
    def _get_pytesseract(self):
        """Lazy import pytesseract to avoid dependency issues"""
        if self._pytesseract is None:
            try:
                import pytesseract
                self._pytesseract = pytesseract
            except ImportError:
                raise ImportError("pytesseract not installed. Run: pip install pytesseract")
        return self._pytesseract
        
    def extract_text(self, image_path):
        """Extrai texto da imagem usando OCR"""
        try:
            pytesseract = self._get_pytesseract()
            
            img = cv2.imread(str(image_path))
            if img is None:
                return ""
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Aplicar threshold para melhorar OCR
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extrair texto
            text = pytesseract.image_to_string(thresh, lang='eng')
            return text
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")
            return ""
    
    def count_words(self, text):
        """Conta total de palavras no texto"""
        # Remover pontuação e números
        words = re.findall(r'\b[a-zA-ZáéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇ]+\b', text.lower())
        return len(words)
    
    def get_most_frequent_words(self, text, top_n=10):
        """Retorna as palavras mais frequentes"""
        # Extrair palavras
        words = re.findall(r'\b[a-zA-ZáéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇ]{3,}\b', text.lower())
        
        # Filtrar stopwords
        filtered_words = [w for w in words if w not in self.stopwords]
        
        # Contar frequências
        word_counts = Counter(filtered_words)
        
        return word_counts.most_common(top_n)
    
    def analyze(self, image_path):
        """Análise completa do texto"""
        text = self.extract_text(image_path)
        word_count = self.count_words(text)
        frequent_words = self.get_most_frequent_words(text, top_n=10)
        
        return {
            'text': text,
            'word_count': word_count,
            'frequent_words': frequent_words
        }
    
    def check_compliance(self, word_count, num_paragraphs, min_words=2000, min_paragraphs=8, language="pt"):
        """Verifica se está conforme regras: >min_words palavras E >=min_paragraphs parágrafos"""
        is_compliant = word_count > min_words and num_paragraphs >= min_paragraphs
        
        is_english = language == "en"
        issues = []
        if word_count <= min_words:
            if is_english:
                issues.append(f"only {word_count} words (minimum: {min_words})")
            else:
                issues.append(f"apenas {word_count} palavras (mínimo: {min_words})")
        if num_paragraphs < min_paragraphs:
            if is_english:
                issues.append(f"only {num_paragraphs} paragraphs (minimum: {min_paragraphs})")
            else:
                issues.append(f"apenas {num_paragraphs} parágrafos (mínimo: {min_paragraphs})")
        
        return is_compliant, issues


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3 text_analyzer.py <imagem>")
        sys.exit(1)
    
    analyzer = TextAnalyzer()
    result = analyzer.analyze(sys.argv[1])
    
    print(f"\n📄 Análise de Texto:")
    print(f"   Palavras: {result['word_count']}")
    print(f"\n   Top 10 palavras mais frequentes:")
    for word, count in result['frequent_words']:
        print(f"      {word}: {count}")
