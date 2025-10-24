#!/usr/bin/env python3
"""
Script para processar todas as imagens de uma pasta com classificador_final
"""

from pathlib import Path
from classificador_final import ClassificadorFinal
import time
import csv

def processar_pasta(pasta_path, salvar_csv=True):
    """
    Processa todas as imagens de uma pasta
    
    Args:
        pasta_path: Caminho da pasta
        salvar_csv: Se True, salva resultados em CSV
    """
    print("=" * 80)
    print("PROCESSAMENTO EM LOTE - CLASSIFICADOR FINAL")
    print("=" * 80)
    
    classifier = ClassificadorFinal()
    pasta = Path(pasta_path)
    
    # Buscar todas as imagens
    extensoes = ['*.png', '*.jpg', '*.jpeg', '*.tif', '*.tiff', '*.bmp']
    imagens = []
    for ext in extensoes:
        imagens.extend(pasta.glob(ext))
    
    if not imagens:
        print(f"❌ Nenhuma imagem encontrada em: {pasta_path}")
        return
    
    total = len(imagens)
    print(f"📁 Pasta: {pasta_path}")
    print(f"📊 Total de imagens: {total}")
    print("=" * 80)
    print()
    
    # Processar cada imagem
    resultados = []
    stats = {'advertisement': 0, 'scientific_article': 0, 'erros': 0}
    inicio = time.time()
    
    for idx, img_path in enumerate(imagens, 1):
        try:
            result = classifier.classify(str(img_path))
            
            stats[result['classification']] += 1
            
            # Salvar resultado
            resultados.append({
                'arquivo': img_path.name,
                'classificacao': result['classification'],
                'score': result['score'],
                'confianca': result['confidence'],
                'altura_media': result['extra_features']['avg_component_height'],
                'desvio_altura': result['extra_features']['height_std'],
                'densidade': result['features']['text_density'],
                'num_componentes': result['features']['num_text_components']
            })
            
            # Mostrar progresso a cada 100 imagens
            if idx % 100 == 0:
                pct = (idx / total) * 100
                emoji = "📰" if result['classification'] == 'advertisement' else "📚"
                print(f"[{idx:4d}/{total}] {pct:5.1f}% {emoji} {img_path.name[:40]:42s} "
                      f"→ {result['classification']:20s} (score: {result['score']:+3d})")
            
        except Exception as e:
            stats['erros'] += 1
            resultados.append({
                'arquivo': img_path.name,
                'classificacao': 'ERRO',
                'score': 0,
                'confianca': 0,
                'altura_media': 0,
                'desvio_altura': 0,
                'densidade': 0,
                'num_componentes': 0
            })
            print(f"[{idx:4d}/{total}] ❌ Erro: {img_path.name}")
    
    tempo_total = time.time() - inicio
    
    # Mostrar resultados
    print("\n" + "=" * 80)
    print("RESULTADOS FINAIS")
    print("=" * 80)
    print(f"📰 Advertisements:      {stats['advertisement']:4d} ({stats['advertisement']/total*100:.1f}%)")
    print(f"📚 Scientific Articles: {stats['scientific_article']:4d} ({stats['scientific_article']/total*100:.1f}%)")
    print(f"❌ Erros:              {stats['erros']:4d} ({stats['erros']/total*100:.1f}%)")
    print(f"\n⏱️  Tempo total: {tempo_total:.1f}s ({tempo_total/60:.1f} minutos)")
    print(f"⏱️  Tempo por imagem: {tempo_total/total*1000:.0f}ms")
    print(f"🚀 Velocidade: {total/tempo_total:.1f} imagens/segundo")
    print("=" * 80)
    
    # Salvar em CSV
    if salvar_csv:
        nome_pasta = Path(pasta_path).name
        arquivo_csv = f"resultados_{nome_pasta}.csv"
        
        with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)
        
        print(f"\n💾 Resultados salvos em: {arquivo_csv}")
        print(f"   Total de linhas: {len(resultados)}")
    
    return resultados

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3 processar_todas.py <pasta>")
        print("\nExemplo:")
        print("  python3 processar_todas.py /Users/test/Downloads/test/scientific_publication")
        sys.exit(1)
    
    pasta = sys.argv[1]
    
    if not Path(pasta).exists():
        print(f"❌ Pasta não encontrada: {pasta}")
        sys.exit(1)
    
    processar_pasta(pasta)
