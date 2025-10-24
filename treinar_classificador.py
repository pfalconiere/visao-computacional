#!/usr/bin/env python3
"""
Treina classificador analisando toda a base de dados
"""

from classificador_melhorado import ClassificadorMelhorado
from pathlib import Path
import numpy as np
import pickle
import time

def extrair_features_dataset(pasta, label):
    """Extrai features de todas as imagens de uma pasta"""
    print(f"\nProcessando {label}...")
    
    classifier = ClassificadorMelhorado()
    features_list = []
    
    imagens = list(Path(pasta).glob('*.tif'))
    total = len(imagens)
    
    for idx, img_path in enumerate(imagens, 1):
        if idx % 100 == 0:
            print(f"  Progresso: {idx}/{total} ({idx/total*100:.1f}%)")
        
        try:
            result = classifier.classify(str(img_path))
            features_list.append({
                'altura': result['extra_features']['avg_component_height'],
                'largura': result['extra_features']['avg_component_width'],
                'aspect': result['extra_features']['avg_aspect_ratio'],
                'desvio_altura': result['extra_features']['height_std'],
                'densidade': result['features']['text_density'],
                'transicoes': result['features']['layout_transitions'],
                'colunas': result['extra_features']['num_columns_detected'],
                'num_componentes': result['features']['num_text_components'],
                'edge_density': result['features']['edge_density'],
                'num_lines': result['features']['num_lines']
            })
        except Exception as e:
            pass
    
    print(f"  ✅ {len(features_list)} imagens processadas")
    return features_list

def calcular_thresholds(ad_features, article_features):
    """Calcula thresholds ótimos baseados nas distribuições"""
    print("\n" + "=" * 80)
    print("ANÁLISE ESTATÍSTICA E CÁLCULO DE THRESHOLDS")
    print("=" * 80)
    
    thresholds = {}
    metrics = list(ad_features[0].keys())
    
    for metric in metrics:
        ad_values = np.array([f[metric] for f in ad_features])
        article_values = np.array([f[metric] for f in article_features])
        
        ad_mean = np.mean(ad_values)
        ad_std = np.std(ad_values)
        article_mean = np.mean(article_values)
        article_std = np.std(article_values)
        
        # Threshold ótimo é o ponto médio entre as médias
        threshold = (ad_mean + article_mean) / 2
        
        # Calcular separabilidade (Cohen's d)
        pooled_std = np.sqrt((ad_std**2 + article_std**2) / 2)
        separability = abs(ad_mean - article_mean) / pooled_std if pooled_std > 0 else 0
        
        thresholds[metric] = {
            'threshold': threshold,
            'ad_mean': ad_mean,
            'ad_std': ad_std,
            'article_mean': article_mean,
            'article_std': article_std,
            'separability': separability
        }
        
        stars = "⭐" * min(int(separability), 5)
        direction = ">" if ad_mean > article_mean else "<"
        
        print(f"\n{metric.upper()}:")
        print(f"  📰 Ads:      {ad_mean:7.2f} ± {ad_std:6.2f}")
        print(f"  📚 Articles: {article_mean:7.2f} ± {article_std:6.2f}")
        print(f"  🎯 Threshold: {threshold:7.2f}")
        print(f"  📊 Separabilidade: {separability:.2f} {stars}")
        print(f"  💡 Regra: Se {metric} {direction} {threshold:.2f} → {'Ad' if direction == '>' else 'Article'}")
    
    return thresholds

def criar_classificador_otimizado(thresholds):
    """Cria código do classificador otimizado"""
    
    # Ordenar métricas por separabilidade
    sorted_metrics = sorted(thresholds.items(), 
                           key=lambda x: x[1]['separability'], 
                           reverse=True)
    
    print("\n" + "=" * 80)
    print("MÉTRICAS MAIS IMPORTANTES (ordenadas por separabilidade):")
    print("=" * 80)
    for i, (metric, data) in enumerate(sorted_metrics[:10], 1):
        print(f"{i}. {metric:20s} - separabilidade: {data['separability']:.2f}")
    
    codigo = '''#!/usr/bin/env python3
"""
Classificador Otimizado - Treinado com toda a base RVL-CDIP
Gerado automaticamente em: ''' + time.strftime("%Y-%m-%d %H:%M:%S") + '''
"""

from classificador_melhorado import ClassificadorMelhorado

class ClassificadorOtimizado(ClassificadorMelhorado):
    """Classificador com thresholds otimizados baseados no dataset completo"""
    
    def __init__(self):
        super().__init__()
        
        # Thresholds calculados a partir de toda a base de dados
        self.thresholds = {
'''
    
    for metric, data in thresholds.items():
        codigo += f"            '{metric}': {data['threshold']:.4f},\n"
    
    codigo += '''        }
        
        # Estatísticas para referência
        self.stats = {
'''
    
    for metric, data in thresholds.items():
        codigo += f"            '{metric}': {{\n"
        codigo += f"                'ad_mean': {data['ad_mean']:.4f},\n"
        codigo += f"                'article_mean': {data['article_mean']:.4f},\n"
        codigo += f"                'separability': {data['separability']:.4f}\n"
        codigo += f"            }},\n"
    
    codigo += '''        }
    
    def calculate_score(self, features, extra_features):
        """Score otimizado baseado nas métricas mais separáveis"""
        score = 0
        
        # As 10 regras mais importantes (por separabilidade)
'''
    
    # Adicionar as top 10 regras
    for i, (metric, data) in enumerate(sorted_metrics[:10], 1):
        threshold = data['threshold']
        sep = data['separability']
        peso = min(int(sep) + 1, 4)  # Peso baseado na separabilidade
        
        # Determinar direção
        if data['ad_mean'] > data['article_mean']:
            codigo += f'''        
        # Regra {i}: {metric} (separabilidade: {sep:.2f})
        value = extra_features.get('{metric}', features.get('{metric}', 0))
        if value > {threshold:.4f}:
            score += {peso}  # Advertisement
        else:
            score -= {peso}  # Scientific Article
'''
        else:
            codigo += f'''        
        # Regra {i}: {metric} (separabilidade: {sep:.2f})
        value = extra_features.get('{metric}', features.get('{metric}', 0))
        if value < {threshold:.4f}:
            score += {peso}  # Advertisement
        else:
            score -= {peso}  # Scientific Article
'''
    
    codigo += '''        
        return score

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3 classificador_otimizado.py <imagem>")
        sys.exit(1)
    
    classifier = ClassificadorOtimizado()
    result = classifier.classify(sys.argv[1])
    
    print(f"Classificação: {result['classification']}")
    print(f"Score: {result['score']}")
    print(f"Confiança: {result['confidence']:.1%}")
'''
    
    return codigo

def main():
    print("=" * 80)
    print("TREINAMENTO DO CLASSIFICADOR - BASE COMPLETA RVL-CDIP")
    print("=" * 80)
    
    inicio = time.time()
    
    # Extrair features de advertisements
    ad_features = extrair_features_dataset(
        '/Users/test/Downloads/test/advertisement',
        'Advertisements'
    )
    
    # Extrair features de scientific publications
    article_features = extrair_features_dataset(
        '/Users/test/Downloads/test/scientific_publication',
        'Scientific Publications'
    )
    
    # Calcular thresholds ótimos
    thresholds = calcular_thresholds(ad_features, article_features)
    
    # Salvar dados
    with open('training_data.pkl', 'wb') as f:
        pickle.dump({
            'ad_features': ad_features,
            'article_features': article_features,
            'thresholds': thresholds
        }, f)
    print("\n✅ Dados salvos em: training_data.pkl")
    
    # Criar classificador otimizado
    codigo = criar_classificador_otimizado(thresholds)
    with open('classificador_otimizado.py', 'w') as f:
        f.write(codigo)
    print("✅ Classificador otimizado salvo em: classificador_otimizado.py")
    
    tempo_total = time.time() - inicio
    print(f"\n⏱️  Tempo total de treinamento: {tempo_total:.1f}s ({tempo_total/60:.1f} minutos)")
    print("\n" + "=" * 80)
    print("TREINAMENTO CONCLUÍDO!")
    print("=" * 80)
    print("\nPróximos passos:")
    print("  1. Teste o classificador otimizado:")
    print("     python3 processar_melhorado.py /path/to/folder tipo limite")
    print("  2. Use o classificador:")
    print("     python3 classificador_otimizado.py imagem.tif")

if __name__ == '__main__':
    main()
