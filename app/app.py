from flask import Flask, render_template_string
import socket
import random
import platform
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MATIAS.IT // CyberOps Command Center</title>

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #050816;
            overflow-x: hidden;
            font-family: Arial, sans-serif;
        }

        canvas {
            position: fixed;
            top: 0;
            left: 0;
            z-index: -20;
        }

        .scanline {
            position: fixed;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                to bottom,
                transparent 95%,
                rgba(255,255,255,0.03) 100%
            );
            background-size: 100% 4px;
            z-index: -10;
            pointer-events: none;
        }

        .glow {
            box-shadow:
                0 0 10px rgba(59,130,246,0.4),
                0 0 20px rgba(59,130,246,0.2);
        }

        .hud-card {
            background: rgba(255,255,255,0.04);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255,255,255,0.08);
        }

        .terminal {
            background: #020617;
            border: 1px solid rgba(34,197,94,0.3);
            color: #22c55e;
            font-family: monospace;
            height: 250px;
            overflow: hidden;
        }

        .typing {
            animation: blink 1s infinite;
        }

        @keyframes blink {
            50% {
                opacity: 0;
            }
        }

        .pulse-glow {
            animation: pulseGlow 2s infinite;
        }

        @keyframes pulseGlow {
            0% {
                box-shadow: 0 0 5px rgba(34,197,94,0.2);
            }
            50% {
                box-shadow: 0 0 25px rgba(34,197,94,0.6);
            }
            100% {
                box-shadow: 0 0 5px rgba(34,197,94,0.2);
            }
        }

        .radar {
            width: 220px;
            height: 220px;
            border-radius: 50%;
            border: 2px solid rgba(34,197,94,0.2);
            position: relative;
            overflow: hidden;
        }

        .radar::before {
            content: "";
            position: absolute;
            width: 50%;
            height: 2px;
            background: #22c55e;
            top: 50%;
            left: 50%;
            transform-origin: left;
            animation: radar 3s linear infinite;
            box-shadow: 0 0 20px #22c55e;
        }

        @keyframes radar {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }

        .grid-bg {
            position: fixed;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: -15;
        }

    </style>
</head>

<body class="text-white min-h-screen">

<div class="grid-bg"></div>
<canvas id="stars"></canvas>
<div class="scanline"></div>

<nav class="border-b border-white/10 bg-black/30 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-8 py-5 flex justify-between items-center">

        <div>
            <h1 class="text-3xl font-black tracking-tight">
                MATIAS<span class="text-cyan-400">.IT</span>
            </h1>
            <p class="text-xs text-slate-500 uppercase tracking-[0.3em]">
                CyberOps Command Center
            </p>
        </div>

        <div class="flex items-center gap-3 text-emerald-400">
            <div class="w-3 h-3 bg-emerald-400 rounded-full animate-ping"></div>
            <span class="font-mono text-sm">SYSTEM ONLINE</span>
        </div>

    </div>
</nav>

<main class="max-w-7xl mx-auto px-8 py-10">

    <!-- HERO -->
    <div class="mb-12">
        <h2 class="text-6xl font-black leading-none">
            CLOUD
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 italic">
                DEFENSE GRID
            </span>
        </h2>

        <p class="text-slate-400 mt-4 max-w-2xl">
            Real-time monitoring, infrastructure telemetry,
            security analysis and AWS cloud operations.
        </p>
    </div>

    <!-- STATUS CARDS -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">

        <div class="hud-card rounded-3xl p-6 glow">
            <p class="text-xs text-slate-500 uppercase mb-3">Cloud Provider</p>

            <div class="flex justify-between items-center">
                <h3 class="text-3xl font-black text-orange-400">AWS</h3>
                <i class="fab fa-aws text-4xl opacity-30"></i>
            </div>
        </div>

        <div class="hud-card rounded-3xl p-6">
            <p class="text-xs text-slate-500 uppercase mb-3">Instance ID</p>

            <h3 class="text-xl font-mono text-cyan-400">
                {{ hostname }}
            </h3>
        </div>

        <div class="hud-card rounded-3xl p-6 border-l-4 border-emerald-500 pulse-glow">
            <p class="text-xs text-slate-500 uppercase mb-3">Threat Level</p>

            <h3 class="text-3xl font-black text-emerald-400">
                LOW
            </h3>
        </div>

        <div class="hud-card rounded-3xl p-6">
            <p class="text-xs text-slate-500 uppercase mb-3">DevOps Rank</p>

            <h3 class="text-2xl font-black text-purple-400">
                SRE III
            </h3>
        </div>

    </div>

    <!-- MAIN GRID -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <!-- METRICS -->
        <div class="lg:col-span-2 hud-card rounded-[2rem] p-8">

            <div class="flex justify-between items-center mb-10">
                <h2 class="text-4xl font-black">
                    Real-time Metrics
                </h2>

                <span class="text-xs font-mono text-slate-500">
                    LIVE TELEMETRY
                </span>
            </div>

            <!-- CPU -->
            <div class="mb-8">
                <div class="flex justify-between mb-2 font-mono text-sm">
                    <span>CPU LOAD</span>
                    <span id="cpuText">{{ cpu }}%</span>
                </div>

                <div class="w-full h-4 bg-white/5 rounded-full overflow-hidden">
                    <div id="cpuBar"
                        class="h-full bg-gradient-to-r from-cyan-400 to-blue-600 rounded-full transition-all duration-1000"
                        style="width: {{ cpu }}%">
                    </div>
                </div>
            </div>

            <!-- RAM -->
            <div class="mb-8">
                <div class="flex justify-between mb-2 font-mono text-sm">
                    <span>RAM ALLOCATION</span>
                    <span id="ramText">{{ ram }}%</span>
                </div>

                <div class="w-full h-4 bg-white/5 rounded-full overflow-hidden">
                    <div id="ramBar"
                        class="h-full bg-gradient-to-r from-pink-500 to-purple-600 rounded-full transition-all duration-1000"
                        style="width: {{ ram }}%">
                    </div>
                </div>
            </div>

            <!-- TAGS -->
            <div class="flex flex-wrap gap-3 mt-10">

                <span class="px-4 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-bold">
                    DOCKER ENGINE
                </span>

                <span class="px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold">
                    PYTHON {{ py_version }}
                </span>

                <span class="px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold">
                    SECURITY ACTIVE
                </span>

            </div>

        </div>

        <!-- RADAR -->
        <div class="hud-card rounded-[2rem] p-8 flex flex-col items-center justify-center">

            <h2 class="text-2xl font-black mb-8">
                Threat Scanner
            </h2>

            <div class="radar mb-8"></div>

            <div class="text-center">
                <p class="text-emerald-400 font-mono">
                    No threats detected
                </p>

                <p class="text-slate-500 text-xs mt-2">
                    last scan: {{ time }}
                </p>
            </div>

        </div>

    </div>

    <!-- TERMINAL -->
    <div class="mt-10 hud-card rounded-[2rem] p-8">

        <div class="flex justify-between items-center mb-5">
            <h2 class="text-3xl font-black">
                System Terminal
            </h2>

            <span class="text-xs text-emerald-400 font-mono">
                LIVE LOG STREAM
            </span>
        </div>

        <div class="terminal rounded-2xl p-5" id="terminal">

        </div>

    </div>

    <!-- FOOTER -->
    <footer class="mt-12 text-center text-slate-600 text-xs font-mono uppercase tracking-[0.2em]">
        © 2026 MATIAS.IT // BUILD v3.4.9
    </footer>

</main>

<script>

    // ===========================
    // STARS BACKGROUND
    // ===========================

    const canvas = document.getElementById("stars");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let stars = [];

    for(let i = 0; i < 150; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 1.5,
            speed: Math.random() * 0.5
        });
    }

    function animateStars() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "white";

        stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fill();

            star.y += star.speed;

            if(star.y > canvas.height) {
                star.y = 0;
            }
        });

        requestAnimationFrame(animateStars);
    }

    animateStars();

    // ===========================
    // TERMINAL EFFECT
    // ===========================

    const terminal = document.getElementById("terminal");

    const logs = [
        "[INFO] Docker Engine initialized",
        "[INFO] Security scan completed",
        "[OK] AWS EC2 reachable",
        "[OK] Kubernetes cluster healthy",
        "[INFO] Monitoring pipelines active",
        "[WARN] CPU spike normalized",
        "[OK] Threat analysis completed",
        "[INFO] Cloud telemetry synchronized",
        "[OK] SSL certificates validated",
        "[INFO] Firewall operational"
    ];

    let index = 0;

    function addLog() {
        if(index < logs.length) {
            terminal.innerHTML += `
                <div class="mb-2">
                    ${logs[index]}
                </div>
            `;

            terminal.scrollTop = terminal.scrollHeight;
            index++;
        } else {
            index = 0;
            terminal.innerHTML = "";
        }
    }

    setInterval(addLog, 1200);

    // ===========================
    // RANDOM METRICS
    // ===========================

    function randomMetrics() {

        const cpu = Math.floor(Math.random() * 50) + 20;
        const ram = Math.floor(Math.random() * 50) + 30;

        document.getElementById("cpuBar").style.width = cpu + "%";
        document.getElementById("ramBar").style.width = ram + "%";

        document.getElementById("cpuText").innerText = cpu + "%";
        document.getElementById("ramText").innerText = ram + "%";
    }

    setInterval(randomMetrics, 3000);

</script>

</body>
</html>
"""

@app.route("/")
def home():

    hostname = socket.gethostname()
    py_version = platform.python_version()

    cpu = random.randint(20, 50)
    ram = random.randint(30, 70)

    return render_template_string(
        HTML_TEMPLATE,
        hostname=hostname,
        py_version=py_version,
        cpu=cpu,
        ram=ram,
        time=datetime.now().strftime("%H:%M:%S")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)