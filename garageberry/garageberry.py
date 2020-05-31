from gpiozero import LED, InputDevice

try:
    from gpiozero.pins.rpigpio import RPiGPIOFactory as DefaultPinFactory
except ModuleNotFoundError:
    from gpiozero.pins.mock import MockFactory as DefaultPinFactory

class GarageDoor(object):
    def __init__(self, sensor_pin=None, switch_pin=None, light_pin=None, pin_factory=DefaultPinFactory()):
        self._pin_factory = pin_factory
        self.sensor = InputDevice(pin=sensor_pin, pin_factory=pin_factory)
        self.door = LED(pin=switch_pin, pin_factory=pin_factory)
        self.light = LED(pin=light_pin, pin_factory=pin_factory)

    @property
    def door_status(self):
        return 'closed' if self.is_closed else 'open'

    @property
    def is_closed(self):
        return self.sensor.is_active

    def toggle_door(self):
        self.door.blink(on_time=0.5, n=1)

    def close_door(self):
        if not self.is_closed:
            self.toggle_door()

    def open_door(self):
        if self.is_closed:
            self.toggle_door()

    def toggle_light(self):
        self.light.blink(on_time=0.5, n=1)