import RPi.GPIO as GPIO

class GPIOBoard:
    _instance = None

    def __init__(self):
        if GPIOBoard._instance is not None:
            raise Exception("Use GPIOBoard.get()")
        self.allocated = {}  # pin_number: mode
        self.services = {}   # name: module instance
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = GPIOBoard()
        return cls._instance

    def reserve_pin(self, pin, mode, service_name=None):
        if pin in self.allocated:
            raise ValueError(f"Pin {pin} already allocated to '{self.allocated[pin]['service']}'")
        GPIO.setup(pin, mode)
        self.allocated[pin] = {"mode": mode, "service": service_name or "unlabeled"}

    def register(self, name, instance):
        if name in self.services:
            raise ValueError(f"Service '{name}' already registered")
        self.services[name] = instance

    def unregister(self, name):
        if name in self.services:
            del self.services[name]

    def __getattr__(self, name):
        if name in self.services:
            return self.services[name]
        raise AttributeError(f"No such GPIO service registered: '{name}'")

    def cleanup(self):
        GPIO.cleanup()
        self.allocated.clear()
        self.services.clear()


class GPIORGB:
    def __init__(self, r_pin, g_pin, b_pin, gpio_board):
        self.gpio = gpio_board
        self.pins = {'r': r_pin, 'g': g_pin, 'b': b_pin}
        self.pwms = {}

        for color, pin in self.pins.items():
            self.gpio.reserve_pin(pin, GPIO.OUT, service_name='cabin_lights')
            pwm = GPIO.PWM(pin, 1000)  # 1kHz PWM
            pwm.start(0)  # Start with LED off
            self.pwms[color] = pwm

    def set_rgb(self, r, g, b):
        # Convert 0–255 range to 0–100% duty cycle
        for color, value in zip(('r', 'g', 'b'), (r, g, b)):
            duty_cycle = max(0, min(100, (value / 255) * 100))
            self.pwms[color].ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        for pwm in self.pwms.values():
            pwm.stop()
