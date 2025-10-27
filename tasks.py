#!/usr/bin/env python3
"""
Tarefas Assíncronas do Celery para Classificação de Documentos
"""

from celery_config import celery_app
from classificador_final import ClassificadorFinal
import os
import time

# Instância global do classificador (carregada uma vez por worker)
classifier = None

def get_classifier():
    """Lazy loading do classificador"""
    global classifier
    if classifier is None:
        print("🔄 Inicializando classificador no worker...")
        classifier = ClassificadorFinal()
        print("✅ Classificador pronto!")
    return classifier


@celery_app.task(bind=True, name='tasks.classify_document')
def classify_document(self, file_base64, filename, min_words=2000, min_paragraphs=8, language='pt'):
    """
    Tarefa assíncrona para classificar documento
    
    Args:
        self: Task instance (para atualizar progresso)
        file_base64: Arquivo em base64 (bytes)
        filename: Nome do arquivo original
        min_words: Mínimo de palavras para conformidade
        min_paragraphs: Mínimo de parágrafos para conformidade
        language: Idioma ('pt' ou 'en')
    
    Returns:
        dict: Resultado da classificação
    """
    import base64
    import tempfile
    
    temp_path = None
    
    try:
        # Atualizar progresso: Iniciando
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Iniciando classificação...', 'progress': 10}
        )
        
        # Decodificar arquivo base64 e salvar temporariamente
        file_bytes = base64.b64decode(file_base64)
        
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"worker_{os.getpid()}_{int(time.time())}_{filename}")
        
        with open(temp_path, 'wb') as f:
            f.write(file_bytes)
        
        print(f"📥 Arquivo recebido e salvo: {temp_path} ({len(file_bytes)} bytes)")
        
        # Obter classificador
        clf = get_classifier()
        
        # Atualizar progresso: Classificando
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Classificando documento...', 'progress': 30}
        )
        
        # Classificar (método completo que faz tudo)
        result = clf.classify(temp_path, min_words=min_words, min_paragraphs=min_paragraphs, language=language)
        
        # Atualizar progresso: Finalizando
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Finalizando análise...', 'progress': 90}
        )
        
        # Limpar arquivo temporário
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"🗑️  Arquivo temporário removido: {temp_path}")
        except Exception as cleanup_error:
            print(f"⚠️  Erro ao limpar arquivo: {cleanup_error}")
        
        return result
        
    except Exception as e:
        # Erro na tarefa
        print(f"❌ Erro na classificação: {e}")
        import traceback
        traceback.print_exc()
        
        # Limpar arquivo temporário em caso de erro
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass
        
        raise


@celery_app.task(name='tasks.cleanup_old_files')
def cleanup_old_files():
    """
    Tarefa periódica para limpar arquivos temporários antigos
    """
    import glob
    import time
    
    temp_files = glob.glob('/tmp/classify_*.tif*')
    cleaned = 0
    
    for filepath in temp_files:
        try:
            # Remover arquivos com mais de 1 hora
            if time.time() - os.path.getmtime(filepath) > 3600:
                os.remove(filepath)
                cleaned += 1
        except:
            pass
    
    return f"Limpeza concluída: {cleaned} arquivos removidos"

