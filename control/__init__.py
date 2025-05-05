from flask import Flask, render_template, redirect, request

app = Flask(__name__, template_folder='templates', static_folder='static')

from control.rgb import rgb_bp

app.register_blueprint(rgb_bp, url_prefix='/rgb')

@app.route('/')
def index():
    return render_template('index.html')
