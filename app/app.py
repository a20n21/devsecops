from flask import Flask, render_template_string
import os
import socket
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matias IT Consulting | Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col">

    <!-- Navbar -->
    <nav class="border-b border-slate-800 p-4 bg-slate-900/50 backdrop-blur-md sticky top-0">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <div class="bg-blue-600 p-2 rounded-lg">
                    <i class="fas fa-terminal text-white"></i>
                </div>
                <span class="text-xl font-bold tracking-tight">Matias <span class="text-blue-500">IT Consulting</span></span>
            </div>
            <div class="hidden md:flex space-x-6 text-sm font-medium text-slate-400">
                <a href="#" class="hover:text-blue-400 transition">Dashboard</a>
                <a href="#" class="hover:text-blue-400 transition">Security Analysis</a>
                <a href="#" class="hover:text-blue-400 transition">Cloud Status</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto flex-grow p-6">
        <div class="max-w-4xl mx-auto">
            
            <!-- Header Section -->
            <div class="mb-10 text-center md:text-left">
                <h1 class="text-3xl font-extrabold mb-2">DevSecOps Pipeline Status</h1>
                <p class="text-slate-400">Monitoramento em tempo real da infraestrutura e aplicações.</p>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <div class="bg-slate-800/50 border border-slate-700 p-6 rounded-2xl">
                    <p class="text-slate-400 text-sm mb-1">Hostname</p>
                    <p class="text-xl font-mono text-blue-400">{{ hostname }}</p>
                </div>
                <div class="bg-slate-800/50 border border-slate-700 p-6 rounded-2xl">
                    <p class="text-slate-400 text-sm mb-1">Ambiente</p>
                    <p class="text-xl font-semibold text-emerald-400">Produção</p>
                </div>
                <div class="bg-slate-800/50 border border-slate-700 p-6 rounded-2xl">
                    <p class="text-slate-400 text-sm mb-1">Última Varredura</p>
                    <p class="text-xl font-semibold">{{ time }}</p>
                </div>
            </div>

            <!-- Deployment Card -->
            <div class="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-3xl p-8 shadow-2xl">
                <div class="flex flex-col md:flex-row items-center justify-between">
                    <div>
                        <h2 class="text-2xl font-bold mb-2">Aplicação Ativa</h2>
                        <p class="text-slate-400 mb-6 md:mb-0">Pipeline executado via Jenkins com sucesso.</p>
                    </div>
                    <div class="flex -space-x-2">
                        <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center border-4 border-slate-800 shadow-xl" title="Docker">
                            <i class="fab fa-docker text-xl"></i>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center border-4 border-slate-800 shadow-xl" title="AWS">
                            <i class="fab fa-aws text-xl"></i>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-red-500 flex items-center justify-center border-4 border-slate-800 shadow-xl" title="Security">
                            <i class="fas fa-shield-alt text-xl"></i>
                        </div>
                    </div>
                </div>
                
                <hr class="my-8 border-slate-700">

                <div class="flex items-center text-sm text-slate-500">
                    <span class="flex h-3 w-3 rounded-full bg-emerald-500 mr-3 animate-pulse"></span>
                    Sistemas operacionais e estáveis.
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="p-8 text-center text-slate-500 text-xs border-t border-slate-800">
        <p>&copy; 2026 Matias IT Consulting. All rights reserved.</p>
    </footer>

</body>
</html>
"""

@app.route('/')
def home():
    hostname = socket.gethostname()
    now = datetime.now().strftime("%H:%M:%S")
    return render_template_string(HTML_TEMPLATE, hostname=hostname, time=now)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000)