#!/usr/bin/env python3
"""
Classificador Final - Standalone
Baseado no treinamento completo do RVL-CDIP
Acurácia: 82.3% (Ads: 70.5%, Articles: 94.2%)
"""

import cv2
import numpy as np

class ClassificadorFinal:
    """
    Classificador de documentos RVL-CDIP
    Diferencia Advertisements de Scientific Articles
    """
    
    def __init__(self):
        # Thresholds otimizados baseados em 5,085 imagens
        self.thresholds = {
            'desvio_altura': 42.51,
            'altura_media': 16.34,
            'densidade_texto': 0.18,
            'largura_media': 17.30,
            'num_componentes': 181.92,
            'num_colunas': 1.51
        }
    
    def extract_features(self, image_path):
        """Extrai features da imagem"""
        # Carregar imagem
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
        
        # Normalizar tamanho (para consistência)
        height, width = img.shape
        if height > 2000 or width > 2000:
            scale = min(2000/height, 2000/width)
            img = cv2.resize(img, None, fx=scale, fy=scale)
        
        # Binarização
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Densidade de texto
        text_density = np.sum(binary > 0) / binary.size
        
        # Componentes conectados
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
        
        # Filtrar componentes pequenos (ruído)
        min_area = 20
        valid_components = stats[1:, cv2.CC_STAT_AREA] > min_area
        stats = stats[1:][valid_components]
        
        num_components = len(stats)
        
        if num_components == 0:
            # Imagem vazia ou muito pouco texto
            return {
                'text_density': text_density,
                'num_text_components': 0,
                'layout_transitions': 0
            }, {
                'avg_component_height': 0,
                'avg_component_width': 0,
                'height_std': 0,
                'avg_aspect_ratio': 0,
                'num_columns_detected': 0
            }
        
        # Estatísticas dos componentes
        heights = stats[:, cv2.CC_STAT_HEIGHT]
        widths = stats[:, cv2.CC_STAT_WIDTH]
        aspect_ratios = widths / (heights + 1e-6)
        
        avg_height = np.mean(heights)
        avg_width = np.mean(widths)
        height_std = np.std(heights)
        avg_aspect_ratio = np.mean(aspect_ratios)
        
        # Detectar colunas (projeção horizontal)
        h_projection = np.sum(binary, axis=0)
        h_projection_smooth = cv2.GaussianBlur(h_projection.astype(float).reshape(1, -1), (1, 51), 0).flatten()
        threshold = np.mean(h_projection_smooth) * 0.3
        columns = h_projection_smooth > threshold
        num_columns = np.sum(np.diff(columns.astype(int)) > 0)
        
        # Transições de layout (mudanças na projeção vertical)
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
            'avg_component_width': float(avg_width),
            'height_std': float(height_std),
            'avg_aspect_ratio': float(avg_aspect_ratio),
            'num_columns_detected': int(num_columns)
        }
        
        return features, extra_features
    
    def calculate_score(self, features, extra_features):
        """
        Calcula score de classificação
        Score positivo = Advertisement
        Score negativo = Scientific Article
        """
        score = 0
        
        # REGRA 1: Desvio de Altura (peso 4)
        if extra_features['height_std'] > self.thresholds['desvio_altura']:
            score += 4  # Alta variação = Advertisement
        else:
            score -= 4  # Baixa variação = Scientific Article
        
        # REGRA 2: Altura Média (peso 3)
        if extra_features['avg_component_height'] > self.thresholds['altura_media']:
            score += 3  # Letras grandes = Advertisement
        else:
            score -= 3  # Letras pequenas = Scientific Article
        
        # REGRA 3: Densidade (peso 3)
        if features['text_density'] > self.thresholds['densidade_texto']:
            score += 3  # Mais denso = Advertisement
        else:
            score -= 3  # Menos denso = Scientific Article
        
        # REGRA 4: Largura Média (peso 3)
        if extra_features['avg_component_width'] > self.thresholds['largura_media']:
            score += 3  # Componentes largos = Advertisement
        else:
            score -= 3  # Componentes estreitos = Scientific Article
        
        # REGRA 5: Número de Componentes (peso 2)
        if features['num_text_components'] < self.thresholds['num_componentes']:
            score += 2  # Poucos componentes = Advertisement
        else:
            score -= 2  # Muitos componentes = Scientific Article
        
        # REGRA 6: Número de Colunas (peso 1)
        if extra_features['num_columns_detected'] > self.thresholds['num_colunas']:
            score += 1  # Mais colunas = Advertisement
        else:
            score -= 1  # Menos colunas = Scientific Article
        
        return score
    
    def classify(self, image_path):
        """Classifica uma imagem"""
        # Extrair features
        features, extra_features = self.extract_features(image_path)
        
        # Calcular score
        score = self.calculate_score(features, extra_features)
        
        # Classificação baseada no score
        if score > 0:
            classification = 'advertisement'
        else:
            classification = 'scientific_article'
        
        # Confiança baseada na magnitude do score
        max_score = 16  # Soma dos pesos
        confidence = abs(score) / max_score
        confidence = min(confidence, 1.0)  # Cap em 1.0
        
        return {
            'classification': classification,
            'score': int(score),
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
    
    print(f"Classificação: {result['classification']}")
    print(f"Score: {result['score']}")
    print(f"Confiança: {result['confidence']:.1%}")
    print(f"\nDetalhes:")
    print(f"  Altura: {result['extra_features']['avg_component_height']:.1f}px")
    print(f"  Desvio altura: {result['extra_features']['height_std']:.1f}")
    print(f"  Densidade: {result['features']['text_density']:.3f}")
