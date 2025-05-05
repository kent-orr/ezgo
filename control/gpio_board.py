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
