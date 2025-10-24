#!/usr/bin/env python3
"""
Classificador Final - Corrigido com lógica correta
Baseado no treinamento completo do RVL-CDIP
"""

from classificador_melhorado import ClassificadorMelhorado

class ClassificadorFinal(ClassificadorMelhorado):
    """
    Classificador com regras corretamente aplicadas
    
    Descobertas do treinamento:
    - Advertisements têm: letras MAIORES, MAIS variação de altura, MAIS densidade
    - Scientific Articles têm: letras MENORES, menos variação, MAIS componentes
    """
    
    def calculate_score(self, features, extra_features):
        """Score com lógica corrigida"""
        score = 0
        
        # REGRA 1: Desvio de Altura (separabilidade: 1.47 - MELHOR!)
        # Ads=67.8, Articles=17.2, threshold=42.51
        desvio = extra_features['height_std']
        if desvio > 42.51:
            score += 4  # ALTA variação = Advertisement
        else:
            score -= 4  # BAIXA variação = Scientific Article
        
        # REGRA 2: Altura Média (separabilidade: 1.09)
        # Ads=23.0, Articles=9.7, threshold=16.34
        altura = extra_features['avg_component_height']
        if altura > 16.34:
            score += 3  # Letras GRANDES = Advertisement
        else:
            score -= 3  # Letras PEQUENAS = Scientific Article
        
        # REGRA 3: Densidade (separabilidade: 0.97)
        # Ads=0.25, Articles=0.11, threshold=0.18
        densidade = features['text_density']
        if densidade > 0.18:
            score += 3  # MAIS denso = Advertisement
        else:
            score -= 3  # MENOS denso = Scientific Article
        
        # REGRA 4: Largura Média (separabilidade: 0.95)
        # Ads=22.2, Articles=12.4, threshold=17.30
        largura = extra_features['avg_component_width']
        if largura > 17.30:
            score += 3  # Componentes LARGOS = Advertisement
        else:
            score -= 3  # Componentes ESTREITOS = Scientific Article
        
        # REGRA 5: Número de Componentes (separabilidade: 0.91)
        # Ads=103, Articles=260, threshold=181
        num_comp = features['num_text_components']
        if num_comp < 181.92:
            score += 2  # POUCOS componentes = Advertisement
        else:
            score -= 2  # MUITOS componentes = Scientific Article
        
        # REGRA 6: Número de Colunas (separabilidade: 0.71)
        # Ads=1.82, Articles=1.19, threshold=1.51
        colunas = extra_features['num_columns_detected']
        if colunas > 1.51:
            score += 1  # Mais colunas = Advertisement (inesperado mas é o que os dados mostram)
        else:
            score -= 1
        
        return score

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
