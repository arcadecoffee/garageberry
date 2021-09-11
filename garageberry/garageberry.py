from gpiozero import Button, LED

try:
    from gpiozero.pins.rpigpio import RPiGPIOFactory as DefaultPinFactory
except ModuleNotFoundError:
    from gpiozero.pins.mock import MockFactory as DefaultPinFactory


class GarageDoor(object):
    def __init__(self, sensor_pin=None, switch_pin=None, light_pin=None, pin_factory=DefaultPinFactory()):
        self._pin_factory = pin_factory
        self._sensor = Button(pin=sensor_pin, pin_factory=pin_factory)
        self._door = LED(pin=switch_pin, pin_factory=pin_factory)
        self._light = LED(pin=light_pin, pin_factory=pin_factory)

    @property
    def door_status(self):
        return 'closed' if self.is_closed else 'open'

    @property
    def is_closed(self):
        return self._sensor.is_active

    def toggle_door(self):
        self._door.blink(on_time=0.5, n=1)

    def close_door(self):
        if not self.is_closed:
            self.toggle_door()

    def open_door(self):
        if self.is_closed:
            self.toggle_door()

    def toggle_light(self):
        self._light.blink(on_time=0.5, n=1)
