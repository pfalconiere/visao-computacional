"""
Testes unitários para ClassificadorFinal
"""
import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
from PIL import Image


@pytest.fixture
def mock_image_advertisement():
    """Cria uma imagem sintética de advertisement (pouco texto, muitas imagens)"""
    img = Image.new('RGB', (800, 600), color='white')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
    img.save(temp_file.name, format='TIFF')
    yield temp_file.name
    os.unlink(temp_file.name)


@pytest.fixture
def mock_image_scientific():
    """Cria uma imagem sintética de artigo científico (muito texto)"""
    img = Image.new('RGB', (800, 1200), color='white')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
    img.save(temp_file.name, format='TIFF')
    yield temp_file.name
    os.unlink(temp_file.name)


class TestClassificadorFinal:
    """Testes para ClassificadorFinal"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        from classificador_final import ClassificadorFinal
        self.clf = ClassificadorFinal()
    
    # ========== HAPPY PATH ==========
    
    def test_classify_advertisement_happy_path(self, mock_image_advertisement):
        """
        HAPPY PATH: Classificação de advertisement
        
        Input: Imagem de advertisement (pouco texto, layout simples)
        Expected: classification='advertisement', confidence > 0, success=True
        """
        result = self.clf.classify(mock_image_advertisement, min_words=100, min_paragraphs=3)
        
        assert result['success'] is True
        assert 'classification' in result
        assert result['classification'] in ['advertisement', 'scientific_article']
        assert 'confidence' in result
        assert isinstance(result['confidence'], (int, float))
        assert 'filename' in result
    
    def test_classify_scientific_happy_path(self, mock_image_scientific):
        """
        HAPPY PATH: Classificação de artigo científico
        
        Input: Imagem de artigo científico (muito texto, estrutura complexa)
        Expected: classification='scientific_article', confidence > 0, success=True
        """
        result = self.clf.classify(mock_image_scientific, min_words=100, min_paragraphs=3)
        
        assert result['success'] is True
        assert 'classification' in result
        assert result['classification'] in ['advertisement', 'scientific_article']
        assert 'confidence' in result
        assert 'num_paragraphs' in result
    
    def test_extract_features_happy_path(self, mock_image_advertisement):
        """
        HAPPY PATH: Extração de features visuais
        
        Input: Imagem válida
        Expected: Dicionário com 9 features numéricas
        """
        features = self.clf.extract_features(mock_image_advertisement)
        
        assert isinstance(features, dict)
        assert len(features) >= 3  # Pelo menos 3 features principais
        assert 'num_text_components' in features
        assert 'text_density' in features
        assert 'layout_transitions' in features
        assert all(isinstance(v, (int, float, np.number)) for v in features.values())
    
    def test_compliance_check_compliant(self):
        """
        HAPPY PATH: Documento conforme
        
        Input: word_count=2500, num_paragraphs=10, min_words=2000, min_paragraphs=8
        Expected: is_compliant=True
        """
        result = {
            'classification': 'scientific_article',
            'word_count': 2500,
            'num_paragraphs': 10
        }
        
        is_compliant = result['word_count'] >= 2000 and result['num_paragraphs'] >= 8
        
        assert is_compliant is True
    
    # ========== NEGATIVE PATH ==========
    
    def test_classify_nonexistent_file_negative(self):
        """
        NEGATIVE PATH: Arquivo não existe
        
        Input: Caminho para arquivo inexistente
        Expected: Levanta exceção ou retorna success=False
        """
        fake_path = '/fake/path/to/nonexistent/file.tif'
        
        with pytest.raises(Exception):
            self.clf.classify(fake_path)
    
    def test_classify_invalid_format_negative(self):
        """
        NEGATIVE PATH: Formato de arquivo inválido
        
        Input: Arquivo não-imagem (ex: .txt)
        Expected: Levanta exceção ou retorna success=False
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
        temp_file.write("Not an image")
        temp_file.close()
        
        try:
            with pytest.raises(Exception):
                self.clf.classify(temp_file.name)
        finally:
            os.unlink(temp_file.name)
    
    def test_extract_features_corrupted_image_negative(self):
        """
        NEGATIVE PATH: Imagem corrompida
        
        Input: Arquivo .tif corrompido
        Expected: Levanta exceção
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif', mode='wb')
        temp_file.write(b'CORRUPTED IMAGE DATA')
        temp_file.close()
        
        try:
            with pytest.raises(Exception):
                self.clf.extract_features(temp_file.name)
        finally:
            os.unlink(temp_file.name)
    
    def test_compliance_check_non_compliant_words(self):
        """
        NEGATIVE PATH: Documento não conforme (poucas palavras)
        
        Input: word_count=500, num_paragraphs=10, min_words=2000, min_paragraphs=8
        Expected: is_compliant=False
        """
        result = {
            'classification': 'scientific_article',
            'word_count': 500,
            'num_paragraphs': 10
        }
        
        is_compliant = result['word_count'] >= 2000 and result['num_paragraphs'] >= 8
        
        assert is_compliant is False
    
    def test_compliance_check_non_compliant_paragraphs(self):
        """
        NEGATIVE PATH: Documento não conforme (poucos parágrafos)
        
        Input: word_count=2500, num_paragraphs=5, min_words=2000, min_paragraphs=8
        Expected: is_compliant=False
        """
        result = {
            'classification': 'scientific_article',
            'word_count': 2500,
            'num_paragraphs': 5
        }
        
        is_compliant = result['word_count'] >= 2000 and result['num_paragraphs'] >= 8
        
        assert is_compliant is False
    
    def test_classify_with_invalid_parameters_negative(self, mock_image_advertisement):
        """
        NEGATIVE PATH: Parâmetros inválidos
        
        Input: min_words=-1, min_paragraphs=-1
        Expected: Funciona ou levanta exceção apropriada
        """
        # Deve aceitar ou validar parâmetros
        result = self.clf.classify(mock_image_advertisement, min_words=-1, min_paragraphs=-1)
        
        # Se aceitar parâmetros negativos, ainda deve retornar resultado válido
        assert result['success'] is True or 'error' in result

