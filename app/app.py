from flask import Flask, render_template_string, Response, request
import socket
import platform
from datetime import datetime
import psutil
import time

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)


CPU = Gauge("system_cpu_percent", "CPU usage")
RAM = Gauge("system_ram_percent", "RAM usage")
DISK = Gauge("system_disk_percent", "Disk usage")


HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

HTTP_ERRORS_5XX = Counter(
    "http_5xx_errors_total",
    "Total 5xx errors",
    ["endpoint"]
)

HTTP_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency",
    ["endpoint"]
)


def update_metrics():
    CPU.set(psutil.cpu_percent())
    RAM.set(psutil.virtual_memory().percent)
    DISK.set(psutil.disk_usage('/').percent)



@app.before_request
def start_timer():
    if request.path == "/metrics":
        return
    request.start_time = time.time()


@app.after_request
def record_metrics(response):
    if request.path == "/metrics":
        return response

    latency = time.time() - getattr(request, "start_time", time.time())

    endpoint = request.path
    method = request.method
    status = response.status_code

    
    HTTP_REQUESTS.labels(method, endpoint, status).inc()

    
    HTTP_LATENCY.labels(endpoint).observe(latency)

    
    if status >= 500:
        HTTP_ERRORS_5XX.labels(endpoint).inc()

    return response



@app.route("/")
def home():
    update_metrics()

    return render_template_string("""
        <h1>OK DevSecOps App</h1>
        <p>System running</p>
    """)


@app.route("/error")
def error_route():
    return "error simulated", 500


@app.route("/slow")
def slow_route():
    time.sleep(1.2)
    return "slow response"



@app.route("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)