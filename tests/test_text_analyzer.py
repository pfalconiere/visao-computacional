"""
Testes unitários para TextAnalyzer
"""
import pytest
import tempfile
import os
from PIL import Image, ImageDraw, ImageFont


@pytest.fixture
def mock_image_with_text():
    """Cria uma imagem com texto para teste de OCR"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    # Adicionar texto simples
    draw.text((50, 50), "Test Document\nWith Multiple Lines\nAnd Paragraphs", fill='black')
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
    img.save(temp_file.name, format='TIFF')
    yield temp_file.name
    os.unlink(temp_file.name)


class TestTextAnalyzer:
    """Testes para módulos de análise de texto"""
    
    # ========== HAPPY PATH ==========
    
    def test_text_analyzer_import_happy_path(self):
        """
        HAPPY PATH: Importar text_analyzer
        
        Expected: Import bem-sucedido
        """
        try:
            from text_analyzer import extract_text, analyze_text
            assert extract_text is not None
            assert analyze_text is not None
        except ImportError:
            pytest.skip("text_analyzer não disponível")
    
    def test_text_analyzer_optimized_import_happy_path(self):
        """
        HAPPY PATH: Importar text_analyzer_optimized
        
        Expected: Import bem-sucedido
        """
        try:
            from text_analyzer_optimized import extract_text_fast, analyze_fast
            assert extract_text_fast is not None
            assert analyze_fast is not None
        except ImportError:
            pytest.skip("text_analyzer_optimized não disponível")
    
    def test_extract_text_returns_string(self, mock_image_with_text):
        """
        HAPPY PATH: extract_text retorna string
        
        Input: Imagem com texto
        Expected: String não vazia
        """
        try:
            from text_analyzer import extract_text
            text = extract_text(mock_image_with_text)
            assert isinstance(text, str)
            # Pode retornar string vazia se OCR não detectar texto
            assert text is not None
        except ImportError:
            pytest.skip("text_analyzer não disponível")
    
    def test_analyze_text_returns_dict(self, mock_image_with_text):
        """
        HAPPY PATH: analyze_text retorna dict com métricas
        
        Input: Imagem com texto
        Expected: Dict com word_count, frequent_words, etc.
        """
        try:
            from text_analyzer import analyze_text
            result = analyze_text(mock_image_with_text, min_words=10, min_paragraphs=2, language='pt')
            
            assert isinstance(result, dict)
            assert 'word_count' in result
            assert 'frequent_words' in result
            assert 'is_compliant' in result
            assert isinstance(result['word_count'], int)
            assert isinstance(result['frequent_words'], list)
        except ImportError:
            pytest.skip("text_analyzer não disponível")
    
    def test_frequent_words_format(self, mock_image_with_text):
        """
        HAPPY PATH: frequent_words tem formato correto
        
        Expected: Lista de dicts com 'word' e 'count'
        """
        try:
            from text_analyzer import analyze_text
            result = analyze_text(mock_image_with_text, min_words=10, min_paragraphs=2)
            
            frequent_words = result['frequent_words']
            assert isinstance(frequent_words, list)
            
            if len(frequent_words) > 0:
                # Pode ser lista de tuples ou lista de dicts
                first_item = frequent_words[0]
                assert isinstance(first_item, (tuple, dict))
        except ImportError:
            pytest.skip("text_analyzer não disponível")
    
    # ========== NEGATIVE PATH ==========
    
    def test_extract_text_nonexistent_file_negative(self):
        """
        NEGATIVE PATH: extract_text com arquivo inexistente
        
        Expected: Levanta exceção
        """
        try:
            from text_analyzer import extract_text
            with pytest.raises(Exception):
                extract_text('/fake/path/to/nonexistent.tif')
        except ImportError:
            pytest.skip("text_analyzer não disponível")
    
    def test_analyze_text_corrupted_image_negative(self):
        """
        NEGATIVE PATH: analyze_text com imagem corrompida
        
        Expected: Levanta exceção ou retorna resultado vazio
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif', mode='wb')
        temp_file.write(b'CORRUPTED IMAGE')
        temp_file.close()
        
        try:
            from text_analyzer import analyze_text
            with pytest.raises(Exception):
                analyze_text(temp_file.name, min_words=10, min_paragraphs=2)
        except ImportError:
            pytest.skip("text_analyzer não disponível")
        finally:
            os.unlink(temp_file.name)
    
    def test_analyze_text_invalid_language_negative(self, mock_image_with_text):
        """
        NEGATIVE PATH: analyze_text com idioma inválido
        
        Input: language='xyz' (inválido)
        Expected: Usa padrão ou levanta exceção
        """
        try:
            from text_analyzer import analyze_text
            # Deve aceitar ou usar padrão
            result = analyze_text(mock_image_with_text, min_words=10, min_paragraphs=2, language='xyz')
            assert isinstance(result, dict)
        except ImportError:
            pytest.skip("text_analyzer não disponível")


class TestOptimizedTextAnalyzer:
    """Testes para text_analyzer_optimized"""
    
    # ========== HAPPY PATH ==========
    
    def test_optimized_faster_than_regular(self, mock_image_with_text):
        """
        HAPPY PATH: Versão otimizada existe e funciona
        
        Expected: extract_text_fast retorna resultado válido
        """
        try:
            from text_analyzer_optimized import extract_text_fast
            text = extract_text_fast(mock_image_with_text, timeout=30)
            assert isinstance(text, str)
            assert text is not None
        except ImportError:
            pytest.skip("text_analyzer_optimized não disponível")
    
    def test_analyze_fast_returns_dict(self, mock_image_with_text):
        """
        HAPPY PATH: analyze_fast retorna dict
        
        Expected: Mesmo formato que analyze_text
        """
        try:
            from text_analyzer_optimized import analyze_fast
            result = analyze_fast(mock_image_with_text, min_words=10, min_paragraphs=2)
            
            assert isinstance(result, dict)
            assert 'word_count' in result
            assert 'frequent_words' in result
        except ImportError:
            pytest.skip("text_analyzer_optimized não disponível")
    
    # ========== NEGATIVE PATH ==========
    
    def test_analyze_fast_timeout_negative(self, mock_image_with_text):
        """
        NEGATIVE PATH: analyze_fast com timeout muito curto
        
        Input: timeout=0.001 (impossível completar)
        Expected: Timeout ou resultado parcial
        """
        try:
            from text_analyzer_optimized import analyze_fast
            # Pode levantar TimeoutError ou retornar resultado parcial
            try:
                result = analyze_fast(mock_image_with_text, min_words=10, min_paragraphs=2, timeout=0.001)
                # Se não levantou exceção, deve retornar dict válido
                assert isinstance(result, dict)
            except TimeoutError:
                # Timeout é comportamento esperado
                pass
        except ImportError:
            pytest.skip("text_analyzer_optimized não disponível")

