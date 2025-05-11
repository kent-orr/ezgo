from flask import Blueprint, render_template, request
from .gpio import RGBColor, RGBStrip

rgb_bp = Blueprint('rgb', __name__, template_folder='templates')

import json
import os

class AppState:
    def __init__(self):
        self.default = {
            'cabin': {
                'last_color': {'r': 255, 'g': 255, 'b': 255},
                'pins': [2, 3, 4],
                'state': 'off'
            },
            'underglow': {
                'last_color': {'r': 255, 'g': 255, 'b': 255},
                'pins': [13, 19, 26],
                'state': 'off'
            }
        }
        self.path = os.path.join(os.path.dirname(__file__), 'app_state.json')
        self.state = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                state = json.load(f)
                if state:
                    return state
        # If file doesn't exist or is empty, return default
        return self.default

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.state, f, indent=4)

app_state = AppState()

cabin = RGBStrip((2, 3, 4))
cabin.set_color(RGBColor(**app_state.state['cabin']['last_color']))
underglow = RGBStrip((13, 19, 26))
underglow.set_color(RGBColor(**app_state.state['underglow']['last_color']))


@rgb_bp.route('/<destination>', methods=['GET', 'POST', 'DELETE'])
def rgb(destination):
    if destination == 'cabin':
        strip = cabin
    else:
        strip = underglow
    
    if request.method == 'POST':
        hexcol = RGBColor(hex=request.json.get('hex', '#000000'))
        strip.set_color(hexcol)
        return hexcol, 200
    elif request.method == 'DELETE':
        print(strip.state)
        strip.toggle()
        print(strip.state)
        return strip.state, 200 if strip.state == 'on' else 201
    
    app_state.state[destination] = strip.to_dict()
    app_state.save()
    
    if request.method == 'GET':
        return strip.to_dict(), 200