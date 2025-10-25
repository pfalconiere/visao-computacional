#!/usr/bin/env python3
"""Calibra thresholds do detector de parágrafos"""
import sys
sys.path.append('/Users/test/document_classifier_project')
import numpy as np

# Dados de calibração
samples = [
    ('/Users/test/Downloads/test/scientific_publication/50731065-1080.tif', 6),
    ('/Users/test/Downloads/test/scientific_publication/50723582-3589.tif', 4),
    ('/Users/test/Downloads/test/scientific_publication/50697313-7317.tif', 9),
    ('/Users/test/Downloads/test/scientific_publication/50575885-5885.tif', 7),
    ('/Users/test/Downloads/test/scientific_publication/87613430_87613442.tif', 1),
]

print("🔧 Calibrando detector de parágrafos...\n")

best_error = float('inf')
best_indent = 0
best_space = 0

# Testar combinações de thresholds
for indent_px in range(20, 60, 5):
    for space_ratio in [1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5]:
        
        # Criar detector com esses parâmetros
        import cv2
        
        total_error = 0
        results = []
        
        for img_path, expected in samples:
            # Simular detecção
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Detectar linhas
            height, width = binary.shape
            h_proj = np.sum(binary > 0, axis=1)
            if h_proj.max() > 0:
                h_proj = h_proj / h_proj.max()
            
            lines = []
            in_line = False
            line_start = 0
            
            for y in range(height):
                if h_proj[y] > 0.03 and not in_line:
                    line_start = y
                    in_line = True
                elif h_proj[y] <= 0.03 and in_line:
                    if (y - line_start) >= 5:
                        line_region = binary[line_start:y, :]
                        left = width
                        for x in range(width):
                            if np.sum(line_region[:, x]) > 0:
                                left = x
                                break
                        lines.append({'y_start': line_start, 'y_end': y, 'left': left, 'height': y - line_start})
                    in_line = False
            
            if len(lines) == 0:
                detected = 0
            else:
                # Detectar parágrafos
                typical_left = np.median([l['left'] for l in lines])
                avg_height = np.mean([l['height'] for l in lines])
                
                paras = 1
                for i in range(1, len(lines)):
                    v_space = lines[i]['y_start'] - lines[i-1]['y_end']
                    indent = lines[i]['left'] - typical_left
                    
                    if indent > indent_px or v_space > (avg_height * space_ratio):
                        paras += 1
                
                detected = paras
            
            error = abs(detected - expected)
            total_error += error
            results.append((detected, expected))
        
        if total_error < best_error:
            best_error = total_error
            best_indent = indent_px
            best_space = space_ratio
            print(f"✨ Melhor: indent={indent_px}px, space={space_ratio}x → Erro total: {total_error}")
            for i, (det, exp) in enumerate(results):
                status = "✅" if det == exp else "❌"
                print(f"   {status} Amostra {i+1}: {det} vs {exp}")

print(f"\n🎯 MELHOR CONFIGURAÇÃO:")
print(f"   indent_threshold_px = {best_indent}")
print(f"   vertical_space_ratio = {best_space}")
print(f"   Erro total: {best_error}")
