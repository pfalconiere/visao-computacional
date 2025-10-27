#!/usr/bin/env python3
"""
Configuração do Celery para Processamento Assíncrono
"""

from celery import Celery
import os

# URL do Redis (variável de ambiente ou local)
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Criar instância do Celery
celery_app = Celery(
    'document_classifier',
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
    
    # Timeout das tarefas
    task_time_limit=300,  # 5 minutos máximo
    task_soft_time_limit=240,  # 4 minutos soft limit
    
    # Retry
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Resultados
    result_expires=3600,  # Resultados expiram em 1 hora
    result_backend_transport_options={'master_name': 'mymaster'},
    
    # Workers
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    
    # Monitoramento
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Importar tasks explicitamente para registrá-las
# IMPORTANTE: Isso deve ser feito DEPOIS de criar celery_app
try:
    import tasks  # Isso registra as tasks via decorador @celery_app.task
    print(f"✅ Tasks importadas: {list(celery_app.tasks.keys())}")
except ImportError as e:
    print(f"⚠️ Erro ao importar tasks: {e}")

if __name__ == '__main__':
    celery_app.start()

