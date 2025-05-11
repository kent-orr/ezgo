from flask import Blueprint, render_template, request
from .gpio import RGBColor, RGBStrip
from .app_state import AppState

rgb_bp = Blueprint('rgb', __name__, template_folder='templates')

app_state = AppState()

# rgb.py

cabin = None
underglow = None
_strip_initialized = False

def init_strips():
    global cabin, underglow, _strip_initialized
    from .gpio import RGBColor, RGBStrip

    if _strip_initialized:
        return

    cabin = RGBStrip((2, 3, 4))
    cabin.set_color(RGBColor(**app_state.state['cabin']['last_color']))
    
    underglow = RGBStrip((13, 19, 26))
    underglow.set_color(RGBColor(**app_state.state['underglow']['last_color']))
    _strip_initialized = True


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