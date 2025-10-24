#!/usr/bin/env python3
"""
Servidor web para o frontend
"""
import http.server
import socketserver
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Adicionar headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

os.chdir('/Users/test/document_classifier_project')

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("=" * 80)
    print("🌐 SERVIDOR WEB INICIADO")
    print("=" * 80)
    print(f"\n📡 Frontend disponível em: http://localhost:{PORT}")
    print(f"📄 Arquivo: index.html")
    print("\n💡 Abra no navegador: http://localhost:8080")
    print("\n⚠️  IMPORTANTE: Certifique-se que a API está rodando em http://localhost:5000")
    print("   Para iniciar a API: python3 api.py")
    print("\n🛑 Pressione Ctrl+C para parar o servidor")
    print("=" * 80 + "\n")
    
    httpd.serve_forever()
