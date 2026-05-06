from flask import Flask, render_template_string
import os
import socket
import random
import platform
from datetime import datetime

app = Flask(__name__)

# Design moderno com efeito Glassmorphism (vidro)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matias IT | Cloud Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body class="bg-[#050505] text-white font-sans min-h-screen overflow-x-hidden">

    <!-- Background decorativo (Blur) -->
    <div class="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-900/20 rounded-full blur-[120px] -z-10"></div>
    <div class="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-900/20 rounded-full blur-[120px] -z-10"></div>

    <nav class="p-6 border-b border-white/5 bg-black/40 backdrop-blur-md">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <span class="text-2xl font-black tracking-tighter italic">MATIAS<span class="text-blue-500">.IT</span></span>
            </div>
            <div class="flex items-center space-x-2 text-xs font-mono text-emerald-400 animate-pulse">
                <span class="h-2 w-2 rounded-full bg-emerald-500"></span>
                <span>SISTEMA ONLINE</span>
            </div>
        </div>
    </nav>

    <main class="container mx-auto p-6 mt-10">
        <div class="max-w-5xl mx-auto">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <!-- Card 1: Infra -->
                <div class="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-sm">
                    <p class="text-slate-500 text-xs font-bold uppercase mb-2">Provedor Cloud</p>
                    <div class="flex items-center justify-between">
                        <span class="text-2xl font-bold text-blue-400">AWS</span>
                        <i class="fab fa-aws text-3xl opacity-20"></i>
                    </div>
                </div>
                <!-- Card 2: Hostname -->
                <div class="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-sm">
                    <p class="text-slate-500 text-xs font-bold uppercase mb-2">ID da Instância</p>
                    <span class="text-xl font-mono">{{ hostname }}</span>
                </div>
                <!-- Card 3: Security -->
                <div class="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-sm border-l-emerald-500/50 border-l-4">
                    <p class="text-slate-500 text-xs font-bold uppercase mb-2">Segurança</p>
                    <span class="text-xl font-bold text-emerald-400 italic font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 underline underline-offset-4 decoration-emerald-500/30">SCAN OK</span>
                </div>
            </div>

            <!-- Seção de Métricas (Simuladas) -->
            <div class="bg-gradient-to-br from-white/10 to-transparent border border-white/10 rounded-[2rem] p-10 relative overflow-hidden">
                <div class="relative z-10">
                    <h2 class="text-4xl font-black mb-10 tracking-tight">Real-time <span class="text-blue-500 italic">Metrics.</span></h2>
                    
                    <div class="space-y-8">
                        <div>
                            <div class="flex justify-between mb-2 text-sm font-mono text-slate-300">
                                <span>CPU LOAD</span>
                                <span>{{ cpu }}%</span>
                            </div>
                            <div class="w-full bg-white/5 h-3 rounded-full overflow-hidden">
                                <div class="bg-gradient-to-r from-blue-600 to-cyan-400 h-full rounded-full transition-all duration-1000" style="width: {{ cpu }}%"></div>
                            </div>
                        </div>
                        
                        <div>
                            <div class="flex justify-between mb-2 text-sm font-mono text-slate-300">
                                <span>RAM ALLOCATION</span>
                                <span>{{ ram }}%</span>
                            </div>
                            <div class="w-full bg-white/5 h-3 rounded-full overflow-hidden">
                                <div class="bg-gradient-to-r from-purple-600 to-pink-500 h-full rounded-full transition-all duration-1000" style="width: {{ ram }}%"></div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-12 flex flex-wrap gap-4">
                        <span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-4 py-2 rounded-xl text-xs font-bold">DOCKER ENGINE</span>
                        <span class="bg-purple-500/10 text-purple-400 border border-purple-500/20 px-4 py-2 rounded-xl text-xs font-bold">PYTHON {{ py_version }}</span>
                        <span class="bg-white/5 text-slate-400 border border-white/10 px-4 py-2 rounded-xl text-xs font-bold">LINUX KERNEL</span>
                    </div>
                </div>
            </div>

            <p class="text-center mt-10 text-slate-600 text-xs font-mono uppercase tracking-[0.2em]">
                &copy; 2026 Matias IT Consulting // Build: ab74dc0
            </p>
        </div>
    </main>

</body>
</html>
"""

@app.route('/')
def home():
    hostname = socket.gethostname()
    py_version = platform.python_version()
    # Gerando dados aleatórios realistas para não precisar de biblioteca extra
    cpu_simulated = random.randint(12, 45)
    ram_simulated = random.randint(30, 68)
    
    return render_template_string(HTML_TEMPLATE, 
                                  hostname=hostname, 
                                  py_version=py_version,
                                  cpu=cpu_simulated, 
                                  ram=ram_simulated)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)