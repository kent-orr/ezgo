from flask import Blueprint, render_template, request
from .rgb_controller import RGBController

rgb_bp = Blueprint('rgb', __name__, template_folder='templates')



@rgb_bp.route('/<destination>', methods=['GET', 'POST', 'DELETE'])
def rgb(destination):
    destination_state = app_state.rgb.get(destination.lower())
    controller = RGBController(
        destination_state.as_dict(), 
        getattr(board, destination.lower())
        )
    
    if request.method == 'POST':
        controller.set_rgb(request.json.get('hexcode'))
        app_state.save()
        return controller.as_dict(), 200
    elif request.method == 'DELETE':
        controller.toggle()
        app_state.save()
        if controller.state['on']:
            return controller.as_dict(), 200
        else:
            return controller.as_dict(), 201
    
    
    if request.method == 'GET':
        return controller.as_dict(), 200