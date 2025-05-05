class RGBController:
    def __init__(self, state_dict, gpio=None):
        self.state = state_dict
        self.gpio = gpio  # Optional GPIO controller, injected later

    def toggle(self):
        self.state['on'] = not self.state['on']
        self.sync_gpio()

    def set_rgb(self, hexcode):
        hexcode = hexcode.lstrip('#')
        self.state['r'] = int(hexcode[0:2], 16)
        self.state['g'] = int(hexcode[2:4], 16)
        self.state['b'] = int(hexcode[4:6], 16)
        self.sync_gpio()

    def as_dict(self):
        return self.state

    def sync_gpio(self):
        if not self.gpio:
            return  # No hardware attached; do nothing

        if self.state['on']:
            self.gpio.set_rgb(
                self.state['r'],
                self.state['g'],
                self.state['b']
            )
        else:
            self.gpio.set_rgb(0, 0, 0)
