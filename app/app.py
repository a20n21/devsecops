from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "DevSecOps OK"

app.run(host="0.0.0.0", port=5000)