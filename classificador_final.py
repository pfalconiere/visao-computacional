#!/usr/bin/env python3
"""
Classificador Final - Otimizado com Detecção de Parágrafos e Análise de Texto
Baseado no treinamento completo do RVL-CDIP
Acurácia: 90.00% (Otimizado com 50k iterações)
Otimizado com 50,000 iterações (90% acurácia)
"""

import cv2
import numpy as np
import os
import sys

# Importar detector de parágrafos
try:
    from paragraph_detector import ParagraphDetector
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from paragraph_detector import ParagraphDetector
    except:
        ParagraphDetector = None

# Importar analisador de texto (versão otimizada se disponível)
TextAnalyzer = None
try:
    # Tentar versão otimizada primeiro (5-10x mais rápida)
    from text_analyzer_optimized import TextAnalyzerOptimized as TextAnalyzer
    print("⚡ Usando Text Analyzer OTIMIZADO (5-10x mais rápido)")
except ImportError:
    try:
        # Fallback para versão original
        from text_analyzer import TextAnalyzer
        print("⚠️  Usando Text Analyzer ORIGINAL (mais lento)")
    except ImportError:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            from text_analyzer import TextAnalyzer
        except:
            TextAnalyzer = None

class ClassificadorFinal:
    """
    Classificador de documentos RVL-CDIP
    Diferencia Advertisements de Scientific Articles
    """
    
    def __init__(self):
        # Thresholds otimizados (12M+ iterações)
        self.thresholds = {
            'altura_min': 14.994531075828482,
            'altura_max': 12.770242544237275,
            'desvio_altura': 13.683751059379327,
            'densidade_texto': 0.4033884980057474,
            'num_componentes': 492.9498641142961,
            'num_linhas': 26.515364506408773
        }
        
        # Pesos otimizados das regras
        self.pesos = {
            'p1': 3.0802891803113677,
            'p2': 1.6107505780934257,
            'p3': 0.7447718755081227,
            'p4': 0.6455914619059228,
            'p5': 2.42
        }
        
        # Detector de parágrafos
        if ParagraphDetector:
            self.paragraph_detector = ParagraphDetector()
        else:
            self.paragraph_detector = None
        
        # Analisador de texto (OCR)
        if TextAnalyzer:
            self.text_analyzer = TextAnalyzer()
        else:
            self.text_analyzer = None
        
        # Estatísticas do modelo
        self.accuracy = 0.9000
        self.advertisement_accuracy = 0.9046
        self.scientific_article_accuracy = 0.8930
        self.total_samples = 5085
    
    def extract_features(self, image_path):
        """Extrai features da imagem"""
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        
        # Fallback: tentar com PIL se OpenCV falhar
        if img is None:
            print(f"⚠️ OpenCV falhou ao ler {image_path}, tentando PIL...")
            try:
                from PIL import Image
                pil_img = Image.open(image_path)
                # Converter para grayscale
                if pil_img.mode != 'L':
                    pil_img = pil_img.convert('L')
                img = np.array(pil_img)
                print(f"✅ PIL conseguiu ler: {img.shape}")
            except Exception as e:
                print(f"❌ PIL também falhou: {e}")
                raise ValueError(f"Não foi possível carregar: {image_path}")
        
        # Binarização
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Componentes conectados
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
        
        # Filtrar ruído
        min_area = 10
        valid_components = []
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= min_area:
                valid_components.append(i)
        
        if len(valid_components) == 0:
            return {
                'text_density': 0,
                'num_text_components': 0,
                'layout_transitions': 0
            }, {
                'avg_component_height': 0,
                'height_std': 0,
                'avg_component_width': 0,
                'avg_aspect_ratio': 0,
                'num_columns_detected': 0
            }
        
        # Estatísticas
        heights = [stats[i, cv2.CC_STAT_HEIGHT] for i in valid_components]
        widths = [stats[i, cv2.CC_STAT_WIDTH] for i in valid_components]
        areas = [stats[i, cv2.CC_STAT_AREA] for i in valid_components]
        
        avg_height = np.mean(heights)
        height_std = np.std(heights)
        avg_width = np.mean(widths)
        avg_aspect_ratio = np.mean([h/w if w > 0 else 0 for h, w in zip(heights, widths)])
        
        # Densidade
        total_text_area = sum(areas)
        image_area = img.shape[0] * img.shape[1]
        text_density = total_text_area / image_area if image_area > 0 else 0
        
        num_components = len(valid_components)
        
        # Transições de layout
        v_projection = np.sum(binary, axis=1)
        v_projection_norm = v_projection / (np.max(v_projection) + 1e-6)
        layout_transitions = np.sum(np.abs(np.diff(v_projection_norm)) > 0.1)
        
        features = {
            'text_density': float(text_density),
            'num_text_components': int(num_components),
            'layout_transitions': int(layout_transitions)
        }
        
        extra_features = {
            'avg_component_height': float(avg_height),
            'height_std': float(height_std),
            'avg_component_width': float(avg_width),
            'avg_aspect_ratio': float(avg_aspect_ratio),
            'num_columns_detected': 0
        }
        
        return features, extra_features
    
    def calculate_score(self, features, extra_features):
        """
        Calcula score otimizado
        Score positivo = Advertisement
        Score negativo = Scientific Article
        """
        score = 0
        
        altura_media = extra_features['avg_component_height']
        desvio_altura = extra_features['height_std']
        densidade = features['text_density']
        num_componentes = features['num_text_components']
        
        # Regra 1: Altura média
        if altura_media > self.thresholds['altura_max']:
            score += self.pesos['p1']
        elif altura_media < self.thresholds['altura_min']:
            score -= self.pesos['p1']
        
        # Regra 2: Desvio padrão da altura
        if desvio_altura > self.thresholds['desvio_altura']:
            score += self.pesos['p2']
        
        # Regra 3: Densidade de texto
        if densidade > self.thresholds['densidade_texto']:
            score += self.pesos['p3']
        else:
            score -= self.pesos['p3']
        
        # Regra 4: Número de componentes
        if num_componentes < self.thresholds['num_componentes']:
            score += self.pesos['p4']
        
        return score
    
    def generate_explanation(self, classification, features, extra_features, num_lines, num_paragraphs, text_analysis=None, min_words=2000, min_paragraphs=8, language="pt"):
        """Gera explicação textual sobre a classificação"""
        
        is_english = language == "en"
        
        if classification == 'advertisement':
            reasons = []
            
            if extra_features['avg_component_height'] > self.thresholds['altura_max']:
                reasons.append("larger letters than scientific article standard" if is_english else "letras maiores que o padrão de artigos científicos")
            elif extra_features['avg_component_height'] < self.thresholds['altura_min']:
                reasons.append("smaller and more varied letters" if is_english else "letras menores e mais variadas")
            
            if extra_features['height_std'] > self.thresholds['desvio_altura']:
                reasons.append("large variation in text element sizes" if is_english else "grande variação no tamanho dos elementos de texto")
            
            if features['text_density'] < self.thresholds['densidade_texto']:
                reasons.append("low text density" if is_english else "baixa densidade de texto")
            
            if features['num_text_components'] < self.thresholds['num_componentes']:
                reasons.append("few text components" if is_english else "poucos componentes de texto")
            
            if num_lines < self.thresholds['num_linhas']:
                reasons.append(f"only {num_lines} lines of text" if is_english else f"apenas {num_lines} linhas de texto")
            
            if len(reasons) == 0:
                return "Classified as advertisement based on general document pattern." if is_english else "Classificado como advertisement baseado no padrão geral do documento."
            
            if is_english:
                explanation = "Classified as advertisement due to " + ", ".join(reasons[:3])
                explanation += ". Typical characteristics of advertising."
            else:
                explanation = "Classificado como advertisement devido a " + ", ".join(reasons[:3])
                explanation += ". Características típicas de anúncios publicitários."
            return explanation
            
        else:  # scientific_article
            reasons = []
            
            altura = extra_features['avg_component_height']
            if self.thresholds['altura_min'] <= altura <= self.thresholds['altura_max']:
                reasons.append("uniform and academic text height" if is_english else "altura de texto uniforme e acadêmica")
            
            if features['text_density'] > self.thresholds['densidade_texto']:
                reasons.append("high text density" if is_english else "alta densidade de texto")
            
            if features['num_text_components'] >= self.thresholds['num_componentes']:
                reasons.append("large amount of textual components" if is_english else "grande quantidade de componentes textuais")
            
            if num_lines >= self.thresholds['num_linhas']:
                reasons.append(f"{num_lines} lines of continuous text" if is_english else f"{num_lines} linhas de texto contínuo")
            
            if num_paragraphs > 1:
                reasons.append(f"structured organization in {num_paragraphs} paragraphs" if is_english else f"estrutura organizada em {num_paragraphs} parágrafos")
            
            if len(reasons) == 0:
                explanation = "Classified as scientific article based on general document pattern." if is_english else "Classificado como artigo científico baseado no padrão geral do documento."
            else:
                if is_english:
                    explanation = "Classified as scientific article due to " + ", ".join(reasons[:3])
                    explanation += ". Typical characteristics of academic publications."
                else:
                    explanation = "Classificado como artigo científico devido a " + ", ".join(reasons[:3])
                    explanation += ". Características típicas de publicações acadêmicas."
            
            # Adicionar análise de conformidade se houver
            if text_analysis:
                word_count = text_analysis['word_count']
                is_compliant, issues = self.text_analyzer.check_compliance(word_count, num_paragraphs, min_words=min_words, min_paragraphs=min_paragraphs, language=language)
                
                if is_english:
                    if is_compliant:
                        explanation += f" Document COMPLIANT with standards (>{min_words} words and ≥{min_paragraphs} paragraphs): {word_count} words, {num_paragraphs} paragraphs."
                    else:
                        explanation += f" Document NOT COMPLIANT with standards: {', '.join(issues)}."
                else:
                    if is_compliant:
                        explanation += f" Documento CONFORME às normas (>{min_words} palavras e ≥{min_paragraphs} parágrafos): {word_count} palavras, {num_paragraphs} parágrafos."
                    else:
                        explanation += f" Documento NÃO CONFORME às normas: {', '.join(issues)}."
            
            return explanation

    def classify(self, image_path, min_words=2000, min_paragraphs=8, language="pt"):
        """Classifica uma imagem"""
        features, extra_features = self.extract_features(image_path)
        score = self.calculate_score(features, extra_features)
        
        # Detectar parágrafos e linhas (nova feature)
        num_lines = 0
        num_paragraphs = 0
        if self.paragraph_detector:
            try:
                para_stats = self.paragraph_detector.analyze(image_path)
                num_lines = para_stats['num_lines']
                num_paragraphs = para_stats['num_paragraphs']
                
                # Regra 5: Número de linhas
                if num_lines < self.thresholds['num_linhas']:
                    score += self.pesos['p5']  # Advertisement
                else:
                    score -= self.pesos['p5']  # Scientific Article
            except:
                pass
        
        classification = 'advertisement' if score > 0 else 'scientific_article'
        confidence = min(abs(score) / 10.0, 1.0)
        
        result = {
            'classification': classification,
            'score': float(score),
            'confidence': float(confidence),
            'features': features,
            'extra_features': extra_features
        }
        
        # Adicionar número de linhas e parágrafos ao resultado
        if num_lines > 0:
            result['num_lines'] = num_lines
        if num_paragraphs > 0:
            result['num_paragraphs'] = num_paragraphs
        
        # Se for artigo científico, fazer análise de texto via OCR
        text_analysis = None
        print(f"🔍 DEBUG: classification = {classification}, has text_analyzer = {self.text_analyzer is not None}")
        
        if classification == 'scientific_article' and self.text_analyzer:
            print("🔍 Iniciando análise de texto para artigo científico...")
            try:
                import time
                start_ocr = time.time()
                print("🔍 Extraindo texto do artigo científico (OCR otimizado)...")
                
                # Usar método otimizado se disponível, senão fallback para original
                has_fast = hasattr(self.text_analyzer, 'analyze_fast')
                print(f"🔍 DEBUG: text_analyzer tem analyze_fast? {has_fast}")
                
                if has_fast:
                    # Versão OTIMIZADA (5-10x mais rápida) com timeout de 30s
                    print("⚡ Usando analyze_fast...")
                    text_analysis = self.text_analyzer.analyze_fast(image_path, timeout=30)
                else:
                    # Fallback para versão original
                    print("⚠️ Usando analyze (versão original)...")
                    text_analysis = self.text_analyzer.analyze(image_path)
                
                elapsed_ocr = time.time() - start_ocr
                
                print(f"🔍 DEBUG: text_analysis = {text_analysis is not None}")
                print(f"🔍 DEBUG: word_count = {text_analysis.get('word_count', 'N/A')}")
                print(f"🔍 DEBUG: frequent_words length = {len(text_analysis.get('frequent_words', []))}")
                
                result['word_count'] = text_analysis['word_count']
                
                # Converter tuplas (palavra, count) para dicionários {word: ..., count: ...}
                frequent_words_list = text_analysis['frequent_words']
                if frequent_words_list and len(frequent_words_list) > 0:
                    # Se for tupla, converter para dict
                    if isinstance(frequent_words_list[0], tuple):
                        result['frequent_words'] = [
                            {'word': word, 'count': count} 
                            for word, count in frequent_words_list
                        ]
                    else:
                        # Já é dict, manter
                        result['frequent_words'] = frequent_words_list
                else:
                    result['frequent_words'] = []
                
                # Verificar conformidade
                is_compliant, issues = self.text_analyzer.check_compliance(
                    text_analysis['word_count'], 
                    num_paragraphs,
                    min_words=min_words,
                    min_paragraphs=min_paragraphs
                )
                result['is_compliant'] = is_compliant
                
                print(f"✅ Análise de texto completa: {text_analysis['word_count']} palavras, {len(text_analysis['frequent_words'])} palavras frequentes, conforme={is_compliant} ({elapsed_ocr:.2f}s)")
            except TimeoutError as e:
                print(f"⚠️ OCR timeout (>30s) - Documento muito grande ou ilegível: {e}")
                result['word_count'] = 0
                result['frequent_words'] = []
                result['is_compliant'] = False
            except Exception as e:
                print(f"⚠️ Erro na análise de texto: {e}")
                import traceback
                traceback.print_exc()
                result['word_count'] = 0
                result['frequent_words'] = []
                result['is_compliant'] = False
        else:
            if classification == 'scientific_article':
                print(f"⚠️ Artigo científico MAS sem text_analyzer disponível!")
        
        # Gerar explicação (incluindo conformidade se houver)
        result['explanation'] = self.generate_explanation(
            classification, features, extra_features, num_lines, num_paragraphs, text_analysis, min_words=min_words, min_paragraphs=min_paragraphs, language=language
        )
        
        return result

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3 classificador_final.py <imagem>")
        sys.exit(1)
    
    classifier = ClassificadorFinal()
    result = classifier.classify(sys.argv[1])
    
    print(f"\nClassificação: {result['classification']}")
    print(f"Score: {result['score']:.2f}")
    print(f"Confiança: {result['confidence']:.1%}")
    print(f"\nFeatures:")
    print(f"  Altura média: {result['extra_features']['avg_component_height']:.2f}px")
    print(f"  Desvio altura: {result['extra_features']['height_std']:.2f}")
    print(f"  Densidade: {result['features']['text_density']:.3f}")
    print(f"  Componentes: {result['features']['num_text_components']}")
    if 'num_lines' in result:
        print(f"  Linhas: {result['num_lines']}")
    if 'num_paragraphs' in result:
        print(f"  Parágrafos: {result['num_paragraphs']}")
    if 'word_count' in result:
        print(f"\n📊 Análise de Texto:")
        print(f"  Palavras: {result['word_count']}")
        print(f"  Conforme normas: {'✅ SIM' if result['is_compliant'] else '❌ NÃO'}")
        print(f"\n  Top 10 palavras mais frequentes:")
        for item in result['frequent_words']:
            if isinstance(item, dict):
                print(f"    {item['word']}: {item['count']}")
            else:
                # Tupla (backward compatibility)
                print(f"    {item[0]}: {item[1]}")
    print(f"\n💬 Explicação:")
    print(f"  {result['explanation']}")
