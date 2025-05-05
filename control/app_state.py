import json
from pathlib import Path
from .rgb_controller import RGBController  # Assuming RGBController is in its own module

APP_NAME = "ezgo"
STATE_DIR = Path.home() / ".local" / "share" / APP_NAME
STATE_FILE = STATE_DIR / "state.json"

DEFAULT_STATE = {
    "rgb": {
        'underglow': { "on": False, "r": 0, "g": 0, "b": 0 },
        'cabin':     { "on": False, "r": 0, "g": 0, "b": 0 }
    }
}

class AppState:
    def __init__(self, state_dict=None):
        state_dict = state_dict or DEFAULT_STATE.copy()
        self.rgb = {
            'underglow': RGBController(state_dict["rgb"]['underglow']),
            'cabin':     RGBController(state_dict["rgb"]['cabin']),
        }

    def to_dict(self):
        return {
            "rgb": {
                name: controller.as_dict()
                for name, controller in self.rgb.items()
            }
        }

    def save(self):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with STATE_FILE.open("w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls):
        if STATE_FILE.exists():
            try:
                with STATE_FILE.open("r") as f:
                    state_data = json.load(f)
                    return cls(state_data)
            except json.JSONDecodeError:
                print(f"Warning: Corrupt state file. Reinitializing.")
        return cls(DEFAULT_STATE.copy())
