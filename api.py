#!/usr/bin/env python3
"""
API REST para Classificação de Documentos - COM FEEDBACK
"""

import sys
sys.stdout = sys.stderr  # Força prints irem para stderr (que o Flask mostra)

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flasgger import Swagger, swag_from
from swagger_docs import *
from classificador_final import ClassificadorFinal
from pathlib import Path
import tempfile
import os
import traceback
from werkzeug.utils import secure_filename
import numpy as np
import csv
import time

# Celery (opcional - funciona sem Redis também)
CELERY_AVAILABLE = False
try:
    from celery_config import celery_app
    from tasks import classify_document
    
    # Verificar se tem workers ativos
    try:
        inspect = celery_app.control.inspect(timeout=2.0)
        active_workers = inspect.active()
        if active_workers and len(active_workers) > 0:
            CELERY_AVAILABLE = True
            print(f"✅ Celery disponível - {len(active_workers)} worker(s) ativo(s) - modo assíncrono ativado")
        else:
            print("⚠️ Celery instalado mas SEM WORKERS ativos - usando modo síncrono")
            print("   (Para ativar async: inicie um worker ou use Render Standard plan)")
    except Exception as e:
        print(f"⚠️ Celery instalado mas não conectável: {e} - usando modo síncrono")
except ImportError:
    print("⚠️ Celery não disponível - usando modo síncrono")

app = Flask(__name__)
# Configurar CORS para permitir GitHub Pages e localhost (todas as portas)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://pfalconiere.github.io",
            "http://localhost:8080",
            "http://localhost:8000",  # Porta alternativa
            "http://localhost:5000",
            "http://127.0.0.1:8080",
            "http://127.0.0.1:8000",  # Porta alternativa
            "http://127.0.0.1:5000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Document Classifier API",
        "description": "API REST para classificação de documentos RVL-CDIP (Advertisement vs Scientific Article) com OCR, análise de texto e processamento assíncrono",
        "version": "3.0.0",
        "contact": {
            "name": "Document Classifier Team",
            "url": "https://github.com/pfalconiere/visao-computacional"
        }
    },
    "host": "visao-computacional.onrender.com",
    "basePath": "/",
    "schemes": ["https", "http"],
    "tags": [
        {
            "name": "Health",
            "description": "Endpoints de status e saúde da API"
        },
        {
            "name": "Classification",
            "description": "Endpoints de classificação de documentos (síncrono e assíncrono)"
        },
        {
            "name": "Feedback",
            "description": "Endpoints de feedback do usuário para retreinamento"
        },
        {
            "name": "Statistics",
            "description": "Endpoints de estatísticas do modelo"
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

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
    """Página inicial - Interface Web"""
    try:
        return send_file('index.html')
    except:
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

@app.route('/favicon.svg', methods=['GET'])
def favicon():
    """Serve o favicon"""
    try:
        return send_file('favicon.svg', mimetype='image/svg+xml')
    except:
        return '', 404

@app.route('/api-info', methods=['GET'])
@swag_from(home_docs)
def api_info():
    """Informações da API"""
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
@swag_from(health_docs)
def health():
    """Verifica se a API está funcionando"""
    return jsonify({
        'status': 'healthy',
        'message': 'API está funcionando corretamente'
    })

@app.route('/stats', methods=['GET'])
@swag_from(stats_docs)
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
@swag_from(classify_docs)
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

        # Obter parâmetros de conformidade (opcionais)
        min_words = request.form.get('min_words', '2000')
        min_paragraphs = request.form.get('min_paragraphs', '8')
        try:
            min_words = int(min_words)
            min_paragraphs = int(min_paragraphs)
        except:
            min_words = 2000
            min_paragraphs = 8

        print(f"📊 Regras: >={min_words} palavras e >={min_paragraphs} parágrafos")

        # Obter idioma (opcional)
        language = request.form.get('language', 'pt')
        print(f"🌐 Idioma: {language}")
        
        # Classificar imagem
        result = classifier.classify(temp_path, min_words=min_words, min_paragraphs=min_paragraphs, language=language)
        
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
        
        # Adicionar número de linhas e parágrafos se disponível
        if 'num_lines' in result:
            response['num_lines'] = int(result['num_lines'])
        if 'num_paragraphs' in result:
            response['num_paragraphs'] = int(result['num_paragraphs'])
        
        # Adicionar explicação textual
        # Adicionar análise de texto (se artigo científico)
        if 'word_count' in result:
            response['word_count'] = int(result['word_count'])
        if 'is_compliant' in result:
            response['is_compliant'] = bool(result['is_compliant'])
        if 'frequent_words' in result:
            # frequent_words já vem como lista de dicionários do classificador
            freq_words = result['frequent_words']
            if freq_words and isinstance(freq_words[0], dict):
                # Já está no formato correto {'word': ..., 'count': ...}
                response['frequent_words'] = freq_words
            else:
                # Fallback: converter tuplas para dicionários
                response['frequent_words'] = [
                    {'word': word, 'count': int(count)} 
                    for word, count in freq_words
                ]
        
        # Adicionar explicação textual
        if 'explanation' in result:
            response['explanation'] = str(result['explanation'])
        
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

@app.route('/classify/async', methods=['POST'])
@swag_from(classify_async_docs)
def classify_async():
    """
    Endpoint ASSÍNCRONO para classificação de documentos
    Retorna task_id imediatamente, processa em background
    """
    if not CELERY_AVAILABLE:
        return jsonify({
            'error': 'Processamento assíncrono não disponível',
            'message': 'Use /classify para processamento síncrono'
        }), 503
    
    try:
        # Verificar se há arquivo na requisição
        if 'image' not in request.files:
            return jsonify({
                'error': 'Nenhuma imagem foi enviada',
                'message': 'Use o campo "image" para enviar a imagem'
            }), 400
        
        file = request.files['image']
        
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
        
        # Ler arquivo como bytes (Web e Worker são containers separados!)
        filename = secure_filename(file.filename)
        file_bytes = file.read()
        
        # Converter para base64 para enviar via Redis
        import base64
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')
        
        # Parâmetros opcionais
        min_words = int(request.form.get('min_words', '2000'))
        min_paragraphs = int(request.form.get('min_paragraphs', '8'))
        language = request.form.get('language', 'pt')
        
        # Submeter tarefa assíncrona (enviando bytes, não caminho!)
        task = classify_document.apply_async(
            args=[file_base64, filename, min_words, min_paragraphs, language]
        )
        
        return jsonify({
            'success': True,
            'task_id': task.id,
            'status': 'PENDING',
            'message': 'Tarefa submetida com sucesso',
            'check_status_url': f'/task/{task.id}',
            'filename': filename
        }), 202  # 202 Accepted
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ Erro ao submeter tarefa: {e}")
        print(error_details)
        
        return jsonify({
            'error': 'Erro ao submeter tarefa',
            'message': str(e)
        }), 500


@app.route('/task/<task_id>', methods=['GET'])
@swag_from(task_status_docs)
def get_task_status(task_id):
    """
    Consultar status de uma tarefa assíncrona
    """
    if not CELERY_AVAILABLE:
        return jsonify({
            'error': 'Processamento assíncrono não disponível'
        }), 503
    
    try:
        task = classify_document.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Tarefa aguardando processamento...',
                'progress': 0
            }
        elif task.state == 'PROGRESS':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': task.info.get('status', 'Processando...'),
                'progress': task.info.get('progress', 0)
            }
        elif task.state == 'SUCCESS':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Concluído',
                'progress': 100,
                'result': task.result
            }
        elif task.state == 'FAILURE':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Erro no processamento',
                'error': str(task.info)
            }
        else:
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Status desconhecido'
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao consultar tarefa',
            'message': str(e)
        }), 500


@app.route('/feedback', methods=['POST'])
@swag_from(feedback_post_docs)
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
@swag_from(feedback_stats_docs)
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
