#!/usr/bin/env python3
"""
Classificador Final - Otimizado
Baseado no treinamento completo do RVL-CDIP
Acurácia: 89.87% (Ads: 90.46%, Articles: 89.30%)
Otimizado com 12+ milhões de iterações
"""

import cv2
import numpy as np

class ClassificadorFinal:
    """
    Classificador de documentos RVL-CDIP
    Diferencia Advertisements de Scientific Articles
    """
    
    def __init__(self):
        # Thresholds otimizados (12M+ iterações)
        self.thresholds = {
            'altura_min': 11.237462286915132,
            'altura_max': 13.412157638433888,
            'desvio_altura': 12.445331918061154,
            'densidade_texto': 0.4033884980057474,
            'num_componentes': 454
        }
        
        # Pesos otimizados das regras
        self.pesos = {
            'p1': 2.577449845562375,
            'p2': 1.6107505780934257,
            'p3': 0.7373781260674225,
            'p4': 0.6455914619059228
        }
        
        # Estatísticas do modelo
        self.accuracy = 0.8987
        self.advertisement_accuracy = 0.9046
        self.scientific_article_accuracy = 0.8930
        self.total_samples = 5085
    
    def extract_features(self, image_path):
        """Extrai features da imagem"""
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
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
    
    def classify(self, image_path):
        """Classifica uma imagem"""
        features, extra_features = self.extract_features(image_path)
        score = self.calculate_score(features, extra_features)
        
        classification = 'advertisement' if score > 0 else 'scientific_article'
        confidence = min(abs(score) / 10.0, 1.0)
        
        return {
            'classification': classification,
            'score': float(score),
            'confidence': float(confidence),
            'features': features,
            'extra_features': extra_features
        }

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
