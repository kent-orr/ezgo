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