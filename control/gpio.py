
try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO module for non-Raspberry Pi environments
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'

        @staticmethod
        def setmode(mode):
            print(f"Mock setmode({mode})")

        @staticmethod
        def setwarnings(flag):
            print(f"Mock setwarnings({flag})")

        @staticmethod
        def setup(pin, mode):
            print(f"Mock setup(pin={pin}, mode={mode})")

        @staticmethod
        def PWM(pin, frequency):
            print(f"Mock PWM(pin={pin}, frequency={frequency})")
            return MockPWM()

        @staticmethod
        def cleanup():
            print("Mock cleanup()")

    class MockPWM:
        def start(self, duty_cycle):
            print(f"Mock PWM start(duty_cycle={duty_cycle})")

        def ChangeDutyCycle(self, duty_cycle):
            print(f"Mock PWM ChangeDutyCycle(duty_cycle={duty_cycle})")

        def stop(self):
            print("Mock PWM stop()")

    GPIO = MockGPIO()

class RGBColor(list):
    def __init__(self, r=0, g=0, b=0, brightness=1, hex=None):
        if hex:
            r, g, b = self.hex_to_rgb(hex)
        
        # Apply brightness to the RGB values
        self.brightness = brightness
        r, g, b = self.apply_brightness(r, g, b)
        
        # Initialize the list with RGB values
        super().__init__([r, g, b])

    def hex_to_rgb(self, hexcode):
        hexcode = hexcode.lstrip('#')
        return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
    
    def apply_brightness(self, r, g, b):
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        return r, g, b

    def __str__(self):
        return f'RGB({self[0]}, {self[1]}, {self[2]})'
    
    def __repr__(self):
        return f'RGB({self[0]}, {self[1]}, {self[2]})'
    
    def as_dict(self):
        return {
            'r': self[0],
            'g': self[1],
            'b': self[2]
        }


class RGBStrip:
    def __init__(self, pins=(2, 3, 4)):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pins = pins
        self.pwms = []
        self.last_color = RGBColor(255, 255, 255)  # Default to white
        self.state = 'off'

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 1000)
            pwm.start(0)
            self.pwms.append(pwm)

    @staticmethod
    def duty_cycle(val):
        return round((val / 255.0) * 100)

    def set_color(self, color: RGBColor):
        self.last_color = color  # Store the current color for future reference
        for pwm, val in zip(self.pwms, color):
            pwm.ChangeDutyCycle(self.duty_cycle(val))
        self.state = 'on' if any(color) else 'off'  # Update state based on color

    def off(self):
        for pwm in self.pwms:
            pwm.ChangeDutyCycle(0)
        self.state = 'off'

    def on(self):
        if self.state == 'off':
            self.set_color(self.last_color)  # Restore the last known color
        else:
            print('Warning: Tried to turn RGB strip on while it was already on')

    def toggle(self):
        if self.state == 'off':
            self.on()
        else:
            self.off()

    def cleanup(self):
        for pwm in self.pwms:
            pwm.stop()
        GPIO.cleanup()
        print('GPIO cleanup complete')
    
    def to_dict(self):
        return {
            'pins': self.pins,
            'last_color': self.last_color.as_dict(),
            'state': self.state
        }
