"""
Documentação Swagger para Document Classifier API

Define as especificações de cada endpoint para documentação interativa.
"""

# ============================================
# HOME / ROOT
# ============================================
home_docs = {
    "tags": ["Health"],
    "summary": "Página inicial / Informações da API",
    "description": "Retorna informações gerais sobre a API e seus endpoints disponíveis",
    "responses": {
        "200": {
            "description": "Informações da API",
            "examples": {
                "application/json": {
                    "api": "Document Classifier API",
                    "version": "2.0",
                    "model": "Classificador Final RVL-CDIP",
                    "accuracy": "89.87%",
                    "endpoints": {
                        "GET /health": "Verifica status",
                        "GET /stats": "Estatísticas do modelo",
                        "POST /classify": "Classifica imagem",
                        "POST /classify/async": "Classifica assincronamente",
                        "GET /task/<task_id>": "Status da tarefa assíncrona",
                        "POST /feedback": "Envia feedback",
                        "GET /feedback/stats": "Estatísticas de feedback"
                    }
                }
            }
        }
    }
}

# ============================================
# HEALTH CHECK
# ============================================
health_docs = {
    "tags": ["Health"],
    "summary": "Health check da API",
    "description": "Verifica se a API está funcionando corretamente",
    "responses": {
        "200": {
            "description": "API está saudável",
            "examples": {
                "application/json": {
                    "status": "healthy",
                    "message": "API está funcionando corretamente"
                }
            }
        }
    }
}

# ============================================
# STATISTICS
# ============================================
stats_docs = {
    "tags": ["Statistics"],
    "summary": "Estatísticas do modelo",
    "description": "Retorna estatísticas de performance do modelo de classificação",
    "responses": {
        "200": {
            "description": "Estatísticas do modelo",
            "examples": {
                "application/json": {
                    "model": "Classificador Final RVL-CDIP",
                    "training_samples": 5085,
                    "accuracy": {
                        "overall": "89.87%",
                        "advertisement": "94.23%",
                        "scientific_article": "85.51%"
                    },
                    "features": 9,
                    "processing_time": "~44ms por imagem",
                    "supported_formats": ["tif", "tiff"],
                    "training_iterations": "12M+"
                }
            }
        }
    }
}

# ============================================
# CLASSIFY (SÍNCRONO)
# ============================================
classify_docs = {
    "tags": ["Classification"],
    "summary": "Classificar documento (síncrono)",
    "description": """
    Classifica uma imagem de documento como Advertisement ou Scientific Article.
    
    **Processamento síncrono:** A requisição aguarda o processamento completo (pode demorar 10-30s).
    
    **Para documentos grandes, use `/classify/async` para processamento assíncrono.**
    
    O endpoint realiza:
    1. Extração de features visuais (layout, densidade de texto, componentes)
    2. Classificação baseada em modelo treinado
    3. OCR para artigos científicos (extração de texto)
    4. Detecção de parágrafos
    5. Análise de palavras frequentes
    6. Verificação de conformidade com regras acadêmicas
    """,
    "consumes": ["multipart/form-data"],
    "produces": ["application/json"],
    "parameters": [
        {
            "name": "file",
            "in": "formData",
            "type": "file",
            "required": True,
            "description": "Arquivo de imagem (.tif ou .tiff)"
        },
        {
            "name": "min_words",
            "in": "formData",
            "type": "integer",
            "required": False,
            "default": 2000,
            "description": "Mínimo de palavras para conformidade (artigos científicos)"
        },
        {
            "name": "min_paragraphs",
            "in": "formData",
            "type": "integer",
            "required": False,
            "default": 8,
            "description": "Mínimo de parágrafos para conformidade (artigos científicos)"
        },
        {
            "name": "language",
            "in": "formData",
            "type": "string",
            "required": False,
            "default": "pt",
            "enum": ["pt", "en"],
            "description": "Idioma das mensagens de retorno (pt ou en)"
        }
    ],
    "responses": {
        "200": {
            "description": "Classificação bem-sucedida",
            "examples": {
                "application/json": {
                    "success": True,
                    "classification": "scientific_article",
                    "confidence": 0.89,
                    "filename": "document.tif",
                    "explanation": "Classificado como artigo científico devido a alta densidade de texto...",
                    "word_count": 3500,
                    "num_paragraphs": 12,
                    "frequent_words": [
                        {"word": "research", "count": 45},
                        {"word": "analysis", "count": 32},
                        {"word": "method", "count": 28}
                    ],
                    "is_compliant": True,
                    "features": {
                        "num_text_components": 1245,
                        "text_density": 0.78,
                        "layout_transitions": 45
                    },
                    "score": 2.45,
                    "processing_time": "12.34s"
                }
            }
        },
        "400": {
            "description": "Erro de validação",
            "examples": {
                "application/json": {
                    "error": "Nenhum arquivo enviado"
                }
            }
        },
        "500": {
            "description": "Erro no processamento",
            "examples": {
                "application/json": {
                    "success": False,
                    "error": "Erro ao processar imagem",
                    "message": "Detalhes do erro..."
                }
            }
        }
    }
}

# ============================================
# CLASSIFY ASYNC
# ============================================
classify_async_docs = {
    "tags": ["Classification"],
    "summary": "Classificar documento (assíncrono)",
    "description": """
    Submete uma imagem para classificação assíncrona via Celery + Redis.
    
    **Processamento assíncrono:** A requisição retorna imediatamente com um `task_id`.
    Use o endpoint `/task/<task_id>` para consultar o status e resultado.
    
    **Recomendado para:**
    - Documentos grandes (artigos científicos)
    - Múltiplas classificações simultâneas
    - Evitar timeouts
    
    **Fluxo:**
    1. POST /classify/async → Retorna `task_id`
    2. GET /task/<task_id> (polling a cada 2s) → Retorna status
    3. Quando `state='SUCCESS'` → Resultado disponível
    """,
    "consumes": ["multipart/form-data"],
    "produces": ["application/json"],
    "parameters": [
        {
            "name": "file",
            "in": "formData",
            "type": "file",
            "required": True,
            "description": "Arquivo de imagem (.tif ou .tiff)"
        },
        {
            "name": "min_words",
            "in": "formData",
            "type": "integer",
            "required": False,
            "default": 2000,
            "description": "Mínimo de palavras para conformidade"
        },
        {
            "name": "min_paragraphs",
            "in": "formData",
            "type": "integer",
            "required": False,
            "default": 8,
            "description": "Mínimo de parágrafos para conformidade"
        },
        {
            "name": "language",
            "in": "formData",
            "type": "string",
            "required": False,
            "default": "pt",
            "enum": ["pt", "en"],
            "description": "Idioma das mensagens"
        }
    ],
    "responses": {
        "200": {
            "description": "Tarefa submetida com sucesso",
            "examples": {
                "application/json": {
                    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "status": "Tarefa submetida para processamento",
                    "check_status_url": "/task/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                }
            }
        },
        "503": {
            "description": "Processamento assíncrono indisponível",
            "examples": {
                "application/json": {
                    "error": "Processamento assíncrono não disponível",
                    "message": "Use /classify para processamento síncrono"
                }
            }
        }
    }
}

# ============================================
# TASK STATUS
# ============================================
task_status_docs = {
    "tags": ["Classification"],
    "summary": "Consultar status de tarefa assíncrona",
    "description": """
    Consulta o status de uma tarefa de classificação assíncrona.
    
    **Estados possíveis:**
    - `PENDING`: Tarefa aguardando processamento
    - `PROGRESS`: Em processamento (com % de progresso)
    - `SUCCESS`: Concluída com sucesso (resultado disponível)
    - `FAILURE`: Falhou (erro disponível)
    
    **Polling recomendado:** A cada 2 segundos até `state='SUCCESS'` ou `'FAILURE'`.
    """,
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa retornado por /classify/async"
        }
    ],
    "responses": {
        "200": {
            "description": "Status da tarefa",
            "examples": {
                "application/json": {
                    "state": "SUCCESS",
                    "status": "Classificação concluída",
                    "progress": 100,
                    "result": {
                        "success": True,
                        "classification": "scientific_article",
                        "confidence": 0.89,
                        "word_count": 3500
                    }
                }
            }
        },
        "404": {
            "description": "Tarefa não encontrada",
            "examples": {
                "application/json": {
                    "error": "Tarefa não encontrada",
                    "task_id": "invalid-id"
                }
            }
        },
        "503": {
            "description": "Celery indisponível"
        }
    }
}

# ============================================
# FEEDBACK (POST)
# ============================================
feedback_post_docs = {
    "tags": ["Feedback"],
    "summary": "Enviar feedback sobre classificação",
    "description": """
    Permite ao usuário informar se a classificação estava correta ou não.
    
    **Uso para retreinamento:**
    Os feedbacks são salvos em `feedback_data.csv` e podem ser usados para:
    - Retreinar o modelo
    - Identificar padrões de erro
    - Melhorar a acurácia
    
    **Campos obrigatórios:**
    - `image_name`: Nome do arquivo classificado
    - `is_correct`: True (correto) ou False (incorreto)
    - `predicted_class`: O que o modelo previu
    - `actual_class`: A classe correta (informada pelo usuário)
    """,
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["image_name", "is_correct", "predicted_class", "actual_class"],
                "properties": {
                    "image_name": {
                        "type": "string",
                        "example": "document_001.tif",
                        "description": "Nome do arquivo classificado"
                    },
                    "is_correct": {
                        "type": "boolean",
                        "example": False,
                        "description": "Se a classificação estava correta"
                    },
                    "predicted_class": {
                        "type": "string",
                        "enum": ["advertisement", "scientific_article"],
                        "example": "advertisement",
                        "description": "Classe prevista pelo modelo"
                    },
                    "actual_class": {
                        "type": "string",
                        "enum": ["advertisement", "scientific_article"],
                        "example": "scientific_article",
                        "description": "Classe correta informada pelo usuário"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Feedback salvo com sucesso",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Feedback salvo com sucesso"
                }
            }
        },
        "400": {
            "description": "Dados inválidos",
            "examples": {
                "application/json": {
                    "success": False,
                    "error": "Campos obrigatórios faltando"
                }
            }
        }
    }
}

# ============================================
# FEEDBACK STATS (GET)
# ============================================
feedback_stats_docs = {
    "tags": ["Feedback"],
    "summary": "Estatísticas de feedback",
    "description": """
    Retorna estatísticas agregadas dos feedbacks recebidos.
    
    **Métricas incluídas:**
    - Total de feedbacks
    - % de classificações corretas
    - % de classificações incorretas
    - Erros por classe
    - Matriz de confusão
    """,
    "responses": {
        "200": {
            "description": "Estatísticas de feedback",
            "examples": {
                "application/json": {
                    "total_feedbacks": 150,
                    "correct_count": 135,
                    "incorrect_count": 15,
                    "accuracy_rate": "90.00%",
                    "errors_by_class": {
                        "advertisement": 5,
                        "scientific_article": 10
                    },
                    "confusion_matrix": {
                        "advertisement_as_scientific": 3,
                        "scientific_as_advertisement": 12
                    }
                }
            }
        },
        "200 (sem feedbacks)": {
            "description": "Nenhum feedback disponível",
            "examples": {
                "application/json": {
                    "message": "Nenhum feedback disponível ainda"
                }
            }
        }
    }
}

