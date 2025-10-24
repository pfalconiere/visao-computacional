#!/usr/bin/env python3
"""
Script de teste para a API de classificação
"""

import requests
import sys
from pathlib import Path

API_URL = "http://localhost:5000"

def testar_api():
    """Testa todos os endpoints da API"""
    
    print("=" * 80)
    print("🧪 TESTANDO API DE CLASSIFICAÇÃO")
    print("=" * 80)
    
    # Teste 1: Health check
    print("\n1️⃣  Testando /health...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        print("   💡 Certifique-se que a API está rodando: python3 api.py")
        return
    
    # Teste 2: Stats
    print("\n2️⃣  Testando /stats...")
    try:
        response = requests.get(f"{API_URL}/stats")
        print(f"   Status: {response.status_code}")
        stats = response.json()
        print(f"   Acurácia Geral: {stats['accuracy']['overall']}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Classificar imagem
    print("\n3️⃣  Testando /classify...")
    
    # Procurar uma imagem de teste
    test_folders = [
        '/Users/test/Downloads/test/advertisement',
        '/Users/test/Downloads/test/scientific_publication'
    ]
    
    test_image = None
    for folder in test_folders:
        images = list(Path(folder).glob('*.tif'))[:1]
        if images:
            test_image = images[0]
            break
    
    if not test_image:
        print("   ⚠️  Nenhuma imagem de teste encontrada")
        return
    
    print(f"   Enviando: {test_image.name}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{API_URL}/classify", files=files)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n   ✅ Classificação bem-sucedida!")
            print(f"   📄 Arquivo: {result['filename']}")
            print(f"   🏷️  Tipo: {result['interpretation']['type']}")
            print(f"   📊 Score: {result['score']}")
            print(f"   🎯 Confiança: {result['confidence']*100:.1f}%")
            print(f"   📏 Altura média: {result['features']['altura_media']:.1f}px")
            print(f"   📐 Desvio altura: {result['features']['desvio_altura']:.1f}")
        else:
            print(f"   ❌ Erro: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("\n" + "=" * 80)
    print("✅ Testes concluídos!")
    print("=" * 80)

def classificar_imagem(imagem_path):
    """Classifica uma imagem específica"""
    
    if not Path(imagem_path).exists():
        print(f"❌ Imagem não encontrada: {imagem_path}")
        return
    
    print(f"📤 Enviando imagem: {Path(imagem_path).name}")
    
    try:
        with open(imagem_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{API_URL}/classify", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "=" * 80)
            print("RESULTADO DA CLASSIFICAÇÃO")
            print("=" * 80)
            print(f"🏷️  Tipo: {result['interpretation']['type']}")
            print(f"📊 Score: {result['score']}")
            print(f"🎯 Confiança: {result['confidence']*100:.1f}% ({result['interpretation']['confidence_level']})")
            print(f"\n📐 Características:")
            print(f"   • Altura média: {result['features']['altura_media']:.1f}px")
            print(f"   • Desvio altura: {result['features']['desvio_altura']:.1f}")
            print(f"   • Densidade texto: {result['features']['densidade_texto']:.3f}")
            print(f"   • Num. componentes: {result['features']['num_componentes']}")
            print(f"   • Colunas: {result['features']['colunas_detectadas']}")
            
            if result['interpretation']['characteristics']:
                print(f"\n💡 Características identificadas:")
                for char in result['interpretation']['characteristics']:
                    print(f"   • {char}")
            
            print("=" * 80)
        else:
            print(f"❌ Erro: {response.json()}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Certifique-se que a API está rodando: python3 api.py")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Classificar imagem específica
        classificar_imagem(sys.argv[1])
    else:
        # Rodar testes
        testar_api()
