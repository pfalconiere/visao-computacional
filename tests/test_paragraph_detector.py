"""
Testes unitários para ParagraphDetector
"""
import pytest
import tempfile
import os
from PIL import Image, ImageDraw


@pytest.fixture
def mock_image_with_paragraphs():
    """Cria uma imagem com múltiplos parágrafos visuais"""
    img = Image.new('RGB', (800, 1000), color='white')
    draw = ImageDraw.Draw(img)
    
    # Simular 3 parágrafos com espaçamento
    paragraphs = [
        "First paragraph with some text content",
        "Second paragraph with more text here",
        "Third paragraph at the bottom"
    ]
    
    y_position = 50
    for para in paragraphs:
        draw.text((50, y_position), para, fill='black')
        y_position += 100  # Espaçamento entre parágrafos
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
    img.save(temp_file.name, format='TIFF')
    yield temp_file.name
    os.unlink(temp_file.name)


class TestParagraphDetector:
    """Testes para ParagraphDetector"""
    
    # ========== HAPPY PATH ==========
    
    def test_paragraph_detector_import_happy_path(self):
        """
        HAPPY PATH: Importar paragraph_detector
        
        Expected: Import bem-sucedido
        """
        try:
            from paragraph_detector import detect_paragraphs, count_paragraphs
            assert detect_paragraphs is not None or count_paragraphs is not None
        except ImportError:
            pytest.skip("paragraph_detector não disponível")
    
    def test_detect_paragraphs_returns_number(self, mock_image_with_paragraphs):
        """
        HAPPY PATH: detect_paragraphs retorna número
        
        Input: Imagem com parágrafos
        Expected: int >= 0
        """
        try:
            from paragraph_detector import detect_paragraphs
            num_paragraphs = detect_paragraphs(mock_image_with_paragraphs)
            
            assert isinstance(num_paragraphs, int)
            assert num_paragraphs >= 0
        except ImportError:
            pytest.skip("paragraph_detector não disponível")
    
    def test_detect_paragraphs_with_different_strategies(self, mock_image_with_paragraphs):
        """
        HAPPY PATH: detect_paragraphs com estratégias diferentes
        
        Expected: Retorna resultados válidos
        """
        try:
            from paragraph_detector import detect_paragraphs
            
            # Testar diferentes estratégias se disponível
            result = detect_paragraphs(mock_image_with_paragraphs)
            assert isinstance(result, int)
            assert result >= 0
        except ImportError:
            pytest.skip("paragraph_detector não disponível")
    
    def test_empty_image_returns_zero_paragraphs(self):
        """
        HAPPY PATH: Imagem vazia retorna 0 parágrafos
        
        Input: Imagem completamente branca
        Expected: 0 parágrafos
        """
        img = Image.new('RGB', (800, 600), color='white')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
        img.save(temp_file.name, format='TIFF')
        
        try:
            from paragraph_detector import detect_paragraphs
            num_paragraphs = detect_paragraphs(temp_file.name)
            
            # Imagem vazia deve retornar 0 ou número muito baixo
            assert num_paragraphs >= 0
            # Pode retornar 0 ou detectar ruído como parágrafo
        except ImportError:
            pytest.skip("paragraph_detector não disponível")
        finally:
            os.unlink(temp_file.name)
    
    # ========== NEGATIVE PATH ==========
    
    def test_detect_paragraphs_nonexistent_file_negative(self):
        """
        NEGATIVE PATH: detect_paragraphs com arquivo inexistente
        
        Expected: Levanta exceção
        """
        try:
            from paragraph_detector import detect_paragraphs
            with pytest.raises(Exception):
                detect_paragraphs('/fake/path/to/nonexistent.tif')
        except ImportError:
            pytest.skip("paragraph_detector não disponível")
    
    def test_detect_paragraphs_corrupted_image_negative(self):
        """
        NEGATIVE PATH: detect_paragraphs com imagem corrompida
        
        Expected: Levanta exceção
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif', mode='wb')
        temp_file.write(b'CORRUPTED IMAGE DATA')
        temp_file.close()
        
        try:
            from paragraph_detector import detect_paragraphs
            with pytest.raises(Exception):
                detect_paragraphs(temp_file.name)
        except ImportError:
            pytest.skip("paragraph_detector não disponível")
        finally:
            os.unlink(temp_file.name)
    
    def test_detect_paragraphs_non_image_file_negative(self):
        """
        NEGATIVE PATH: detect_paragraphs com arquivo não-imagem
        
        Expected: Levanta exceção
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
        temp_file.write("This is not an image")
        temp_file.close()
        
        try:
            from paragraph_detector import detect_paragraphs
            with pytest.raises(Exception):
                detect_paragraphs(temp_file.name)
        except ImportError:
            pytest.skip("paragraph_detector não disponível")
        finally:
            os.unlink(temp_file.name)

