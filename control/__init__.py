from flask import Flask, render_template, redirect, request

app = Flask(__name__, template_folder='templates', static_folder='static')

from control.rgb import rgb_bp
from control.gpio_board import GPIOBoard, GPIORGB
from control.app_state import AppState

board = GPIOBoard.get()
board.register('cabin', GPIORGB(13, 19, 26))
board.register('underglow', GPIORGB(17, 27, 22))

app_state = AppState.load()
board.cabin.set_rgb(
    app_state.rgb['cabin']['r'], 
    app_state.rgb['cabin']['g'], 
    app_state.rgb['cabin']['b']
    )
board.underglow.set_rgb(
    app_state.rgb['underglow']['r'], 
    app_state.rgb['underglow']['g'], 
    app_state.rgb['underglow']['b']
    )

app.register_blueprint(rgb_bp, url_prefix='/rgb')


@app.route('/')
def index():
    return render_template('index.html')
