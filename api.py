#!/usr/bin/env python3
"""
API REST para Classificação de Documentos - VERSÃO CORRIGIDA
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from classificador_final import ClassificadorFinal
from pathlib import Path
import tempfile
import os
import traceback
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
CORS(app)

# Inicializar classificador
print("🔄 Carregando classificador...")
classifier = ClassificadorFinal()
print("✅ Classificador carregado!")

# Configurações
ALLOWED_EXTENSIONS = {'tif', 'tiff'}  # Apenas TIF
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def convert_numpy_types(obj):
    """Converte tipos numpy para tipos nativos do Python"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    """Página inicial com documentação"""
    return jsonify({
        'api': 'Document Classifier API',
        'version': '1.0',
        'model': 'Classificador Final RVL-CDIP',
        'accuracy': '82.3%',
        'endpoints': {
            'GET /health': 'Verifica status',
            'GET /stats': 'Estatísticas do modelo',
            'POST /classify': 'Classifica imagem (apenas .tif/.tiff)'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Verifica se a API está funcionando"""
    return jsonify({
        'status': 'healthy',
        'message': 'API está funcionando corretamente'
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Retorna estatísticas do modelo"""
    return jsonify({
        'model': 'Classificador Final RVL-CDIP',
        'training_samples': 5085,
        'accuracy': {
            'advertisements': '70.5%',
            'scientific_articles': '94.2%',
            'overall': '82.3%'
        },
        'features_used': [
            'desvio_altura',
            'altura_media',
            'densidade_texto',
            'largura_media',
            'num_componentes',
            'colunas_detectadas'
        ],
        'processing_time': '~44ms por imagem',
        'supported_formats': ['tif', 'tiff']
    })

@app.route('/classify', methods=['POST'])
def classify():
    """Classifica uma imagem"""
    
    temp_path = None
    
    try:
        # Verificar se há arquivo na requisição
        if 'image' not in request.files:
            return jsonify({
                'error': 'Nenhuma imagem foi enviada',
                'message': 'Use o campo "image" para enviar a imagem'
            }), 400
        
        file = request.files['image']
        
        # Verificar se arquivo foi selecionado
        if file.filename == '':
            return jsonify({
                'error': 'Nenhum arquivo selecionado'
            }), 400
        
        # Verificar extensão
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Formato não suportado',
                'message': 'Apenas arquivos .tif e .tiff são aceitos',
                'supported_formats': ['tif', 'tiff']
            }), 400
        
        # Salvar arquivo temporariamente
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"classify_{os.getpid()}_{filename}")
        
        print(f"📥 Salvando arquivo: {temp_path}")
        file.save(temp_path)
        
        # Verificar se arquivo foi salvo
        if not os.path.exists(temp_path):
            return jsonify({
                'error': 'Erro ao salvar arquivo temporário'
            }), 500
        
        print(f"🔍 Classificando: {filename}")
        
        # Classificar imagem
        result = classifier.classify(temp_path)
        
        print(f"✅ Classificado como: {result['classification']}")
        
        # Remover arquivo temporário
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Preparar resposta (convertendo tipos numpy)
        response = {
            'success': True,
            'filename': filename,
            'classification': str(result['classification']),
            'score': float(result['score']),
            'confidence': float(round(result['confidence'], 3)),
            'features': {
                'altura_media': float(round(result['extra_features']['avg_component_height'], 2)),
                'largura_media': float(round(result['extra_features']['avg_component_width'], 2)),
                'desvio_altura': float(round(result['extra_features']['height_std'], 2)),
                'aspect_ratio': float(round(result['extra_features']['avg_aspect_ratio'], 2)),
                'colunas_detectadas': int(result['extra_features']['num_columns_detected']),
                'densidade_texto': float(round(result['features']['text_density'], 3)),
                'num_componentes': int(result['features']['num_text_components']),
                'transicoes_layout': int(result['features']['layout_transitions'])
            },
            'interpretation': {
                'type': '📰 Advertisement' if result['classification'] == 'advertisement' else '📚 Scientific Article',
                'confidence_level': 'Alta' if result['confidence'] > 0.7 else 'Média' if result['confidence'] > 0.4 else 'Baixa',
                'characteristics': []
            }
        }
        
        # Adicionar interpretações
        if result['classification'] == 'advertisement':
            if result['extra_features']['height_std'] > 42.51:
                response['interpretation']['characteristics'].append('Muita variação de tamanho de texto')
            if result['extra_features']['avg_component_height'] > 16.34:
                response['interpretation']['characteristics'].append('Letras maiores')
            if result['features']['text_density'] > 0.18:
                response['interpretation']['characteristics'].append('Texto mais denso')
        else:
            if result['extra_features']['height_std'] <= 42.51:
                response['interpretation']['characteristics'].append('Texto uniforme')
            if result['extra_features']['avg_component_height'] <= 16.34:
                response['interpretation']['characteristics'].append('Letras menores')
            if result['features']['num_text_components'] > 181:
                response['interpretation']['characteristics'].append('Muitos componentes de texto')
        
        # Garantir que tudo é serializável
        response = convert_numpy_types(response)
        
        return jsonify(response), 200
        
    except Exception as e:
        # Limpar arquivo temporário em caso de erro
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Log detalhado do erro
        error_details = traceback.format_exc()
        print(f"❌ ERRO: {error_details}")
        
        return jsonify({
            'error': 'Erro ao processar imagem',
            'message': str(e),
            'details': error_details if app.debug else 'Veja os logs do servidor'
        }), 500

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 INICIANDO API DE CLASSIFICAÇÃO DE DOCUMENTOS")
    print("=" * 80)
    print("\n📡 Servidor: http://localhost:5000")
    print("\n📍 Endpoints disponíveis:")
    print("   GET  /          - Documentação")
    print("   GET  /health    - Status da API")
    print("   GET  /stats     - Estatísticas do modelo")
    print("   POST /classify  - Classificar imagem (apenas .tif/.tiff)")
    print("\n💡 Exemplo de uso:")
    print('   curl -X POST -F "image=@documento.tif" http://localhost:5000/classify')
    print("\n🛑 Pressione Ctrl+C para parar o servidor")
    print("=" * 80 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
