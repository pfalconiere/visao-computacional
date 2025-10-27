#!/usr/bin/env python3
"""Detector de Parágrafos - Calibrado com dados reais"""
import cv2
import numpy as np

class ParagraphDetector:
    def __init__(self):
        self.min_line_height = 5
        self.indent_threshold_px = 20  # Calibrado: 20px
        self.vertical_space_ratio = 3.0  # Calibrado: 3.0x
        
    def detect_text_lines_with_margins(self, binary_img):
        height, width = binary_img.shape
        h_projection = np.sum(binary_img > 0, axis=1)
        
        if h_projection.max() > 0:
            h_projection = h_projection / h_projection.max()
        
        threshold = 0.03
        lines = []
        in_line = False
        line_start = 0
        
        for y in range(height):
            density = h_projection[y]
            if density > threshold and not in_line:
                line_start = y
                in_line = True
            elif density <= threshold and in_line:
                line_end = y
                line_height = line_end - line_start
                
                if line_height >= self.min_line_height:
                    line_region = binary_img[line_start:line_end, :]
                    left_margin = width
                    for x in range(width):
                        if np.sum(line_region[:, x]) > 0:
                            left_margin = x
                            break
                    
                    lines.append({
                        'y_start': line_start,
                        'y_end': line_end,
                        'height': line_height,
                        'left': left_margin
                    })
                
                in_line = False
        
        if in_line and (height - line_start) >= self.min_line_height:
            line_region = binary_img[line_start:height, :]
            left_margin = width
            for x in range(width):
                if np.sum(line_region[:, x]) > 0:
                    left_margin = x
                    break
            lines.append({
                'y_start': line_start,
                'y_end': height,
                'height': height - line_start,
                'left': left_margin
            })
        
        return lines
    
    def detect_paragraphs(self, lines):
        if len(lines) <= 1:
            return len(lines), [[l] for l in lines]
        
        left_margins = [l['left'] for l in lines]
        typical_left = np.median(left_margins)
        
        heights = [l['height'] for l in lines]
        avg_height = np.mean(heights)
        
        paragraphs = []
        current_paragraph = [lines[0]]
        
        for i in range(1, len(lines)):
            prev = lines[i-1]
            curr = lines[i]
            
            v_space = curr['y_start'] - prev['y_end']
            indent_diff = curr['left'] - typical_left
            
            has_indent = indent_diff > self.indent_threshold_px
            has_large_space = v_space > (avg_height * self.vertical_space_ratio)
            
            if has_indent or has_large_space:
                paragraphs.append(current_paragraph)
                current_paragraph = [curr]
            else:
                current_paragraph.append(curr)
        
        if current_paragraph:
            paragraphs.append(current_paragraph)
        
        return len(paragraphs), paragraphs
    
    def analyze(self, image_path):
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Não foi possível carregar: {image_path}")
        
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        lines = self.detect_text_lines_with_margins(binary)
        num_paragraphs, paragraphs = self.detect_paragraphs(lines)
        
        return {'num_lines': len(lines), 'num_paragraphs': num_paragraphs}


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 paragraph_detector.py <imagem>")
        sys.exit(1)
    
    detector = ParagraphDetector()
    stats = detector.analyze(sys.argv[1])
    print(f"\n📄 Análise de Parágrafos:")
    print(f"   Linhas: {stats['num_lines']}")
    print(f"   Parágrafos: {stats['num_paragraphs']}")
