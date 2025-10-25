#!/usr/bin/env python3
"""
API REST para Classificação de Documentos - COM FEEDBACK
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
import csv
import time

app = Flask(__name__)
CORS(app)

# Inicializar classificador
print("🔄 Carregando classificador...")
classifier = ClassificadorFinal()
print("✅ Classificador carregado!")

# Configurações
ALLOWED_EXTENSIONS = {'tif', 'tiff'}  # Apenas TIF
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
FEEDBACK_FILE = 'feedback_data.csv'

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
        'version': '2.0',
        'model': 'Classificador Final RVL-CDIP',
        'accuracy': '89.87%',
        'endpoints': {
            'GET /health': 'Verifica status',
            'GET /stats': 'Estatísticas do modelo',
            'POST /classify': 'Classifica imagem (apenas .tif/.tiff)',
            'POST /feedback': 'Envia feedback sobre classificação',
            'GET /feedback/stats': 'Estatísticas de feedback'
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
            'advertisements': '90.46%',
            'scientific_articles': '89.30%',
            'overall': '89.87%'
        },
        'features_used': [
            'avg_component_height',
            'height_std',
            'text_density',
            'num_text_components',
            'avg_component_width',
            'avg_aspect_ratio',
            'num_columns_detected'
        ],
        'processing_time': '~44ms por imagem',
        'supported_formats': ['tif', 'tiff'],
        'training_iterations': '12M+'
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
                'text_density': float(round(result['features']['text_density'], 3)),
                'num_text_components': int(result['features']['num_text_components']),
                'layout_transitions': int(result['features']['layout_transitions'])
            },
            'extra_features': {
                'avg_component_height': float(round(result['extra_features']['avg_component_height'], 2)),
                'avg_component_width': float(round(result['extra_features']['avg_component_width'], 2)),
                'height_std': float(round(result['extra_features']['height_std'], 2)),
                'avg_aspect_ratio': float(round(result['extra_features']['avg_aspect_ratio'], 2)),
                'num_columns_detected': int(result['extra_features']['num_columns_detected'])
            }
        }
        
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

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Endpoint para receber feedback do usuário sobre a classificação
    
    Parâmetros:
        - image_name: nome do arquivo
        - predicted_class: classe predita (advertisement/scientific_article)
        - is_correct: true/false
        - correct_class: se incorreto, qual a classe correta (opcional)
    """
    try:
        data = request.get_json()
        
        image_name = data.get('image_name', 'unknown')
        predicted_class = data.get('predicted_class', '')
        is_correct = data.get('is_correct', '')
        correct_class = data.get('correct_class', predicted_class)
        
        # Timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Create file with headers if doesn't exist
        file_exists = os.path.isfile(FEEDBACK_FILE)
        
        with open(FEEDBACK_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['timestamp', 'image_name', 'predicted_class', 'is_correct', 'correct_class'])
            
            writer.writerow([timestamp, image_name, predicted_class, is_correct, correct_class])
        
        print(f"📝 Feedback salvo: {image_name} - {'✅ Correto' if is_correct == 'true' else '❌ Incorreto'}")
        
        # Count total feedbacks
        feedback_count = 0
        if file_exists:
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                feedback_count = sum(1 for line in f) - 1  # -1 for header
        
        return jsonify({
            'success': True,
            'message': 'Feedback recebido com sucesso!',
            'total_feedbacks': feedback_count + 1
        })
        
    except Exception as e:
        print(f"❌ Erro ao salvar feedback: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/feedback/stats', methods=['GET'])
def feedback_stats():
    """
    Retorna estatísticas dos feedbacks coletados
    """
    try:
        if not os.path.isfile(FEEDBACK_FILE):
            return jsonify({
                'success': True,
                'total': 0,
                'correct': 0,
                'incorrect': 0,
                'accuracy': 0,
                'ready_for_retraining': False,
                'message': 'Nenhum feedback coletado ainda'
            })
        
        total = 0
        correct = 0
        incorrect = 0
        by_class = {
            'advertisement': {'correct': 0, 'incorrect': 0},
            'scientific_article': {'correct': 0, 'incorrect': 0}
        }
        
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                predicted = row['predicted_class']
                
                if row['is_correct'] == 'true':
                    correct += 1
                    if predicted in by_class:
                        by_class[predicted]['correct'] += 1
                else:
                    incorrect += 1
                    if predicted in by_class:
                        by_class[predicted]['incorrect'] += 1
        
        accuracy = (correct / total * 100) if total > 0 else 0
        
        # Calcular acurácia por classe
        class_accuracy = {}
        for cls, counts in by_class.items():
            cls_total = counts['correct'] + counts['incorrect']
            if cls_total > 0:
                class_accuracy[cls] = round(counts['correct'] / cls_total * 100, 2)
            else:
                class_accuracy[cls] = 0
        
        return jsonify({
            'success': True,
            'total': total,
            'correct': correct,
            'incorrect': incorrect,
            'accuracy': round(accuracy, 2),
            'by_class': {
                'advertisement': {
                    'correct': by_class['advertisement']['correct'],
                    'incorrect': by_class['advertisement']['incorrect'],
                    'accuracy': class_accuracy.get('advertisement', 0)
                },
                'scientific_article': {
                    'correct': by_class['scientific_article']['correct'],
                    'incorrect': by_class['scientific_article']['incorrect'],
                    'accuracy': class_accuracy.get('scientific_article', 0)
                }
            },
            'ready_for_retraining': total >= 100,
            'retraining_recommendation': get_retraining_recommendation(total, accuracy)
        })
        
    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_retraining_recommendation(total, accuracy):
    """Recomenda quando retreinar"""
    if total < 50:
        return f"Colete mais {50 - total} feedbacks antes de considerar retreino"
    elif total < 100:
        return f"Considere retreinar após coletar mais {100 - total} feedbacks"
    elif accuracy < 80:
        return "⚠️ RECOMENDADO: Acurácia baixa, considere retreinar o modelo"
    elif total >= 500:
        return "✅ RECOMENDADO: Grande volume de dados, retreino pode melhorar o modelo"
    else:
        return "Modelo funcionando bem, retreino opcional"

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 INICIANDO API DE CLASSIFICAÇÃO DE DOCUMENTOS")
    print("=" * 80)
    print("\n📡 Servidor: http://localhost:5000")
    print("\n📍 Endpoints disponíveis:")
    print("   GET  /                  - Documentação")
    print("   GET  /health            - Status da API")
    print("   GET  /stats             - Estatísticas do modelo")
    print("   POST /classify          - Classificar imagem (apenas .tif/.tiff)")
    print("   POST /feedback          - Enviar feedback sobre classificação")
    print("   GET  /feedback/stats    - Estatísticas de feedback")
    print("\n💡 Exemplo de uso:")
    print('   curl -X POST -F "image=@documento.tif" http://localhost:5000/classify')
    print("\n🛑 Pressione Ctrl+C para parar o servidor")
    print("=" * 80 + "\n")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
