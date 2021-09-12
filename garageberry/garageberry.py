from datetime import datetime, timedelta
from enum import auto, Enum

from gpiozero import Button, LED

try:
    from gpiozero.pins.rpigpio import RPiGPIOFactory as DefaultPinFactory
except ModuleNotFoundError:
    from gpiozero.pins.mock import MockFactory as DefaultPinFactory


class GarageDoorStatus(Enum):
    OPEN = auto()
    CLOSED = auto()
    OPENING = auto()
    CLOSING = auto()
    UNKNOWN = auto()


class GarageDoor(object):
    def __init__(self, closed_sensor_pin=None, open_sensor_pin=None, door_relay_pin=None, light_relay_pin=None,
                 door_transit_time=30, relay_blip_time=0.3, pin_factory=DefaultPinFactory()):
        self._pin_factory = pin_factory
        self._closed_sensor = Button(pin=closed_sensor_pin, pin_factory=pin_factory)
        self._closed_sensor.when_activated = self._refresh_door_status
        self._closed_sensor.when_deactivated = self._refresh_door_status
        self._open_sensor = Button(pin=open_sensor_pin, pin_factory=pin_factory)
        self._open_sensor.when_activated = self._refresh_door_status
        self._open_sensor.when_deactivated = self._refresh_door_status
        self._door_relay = LED(pin=door_relay_pin, pin_factory=pin_factory)
        self._light_relay = LED(pin=light_relay_pin, pin_factory=pin_factory)
        self.door_transit_time = door_transit_time
        self.relay_blip_time = relay_blip_time
        self._door_status = GarageDoorStatus.UNKNOWN
        self._refresh_door_status()

    def _refresh_door_status(self):
        print("Refreshing door status")
        if self._door_status == GarageDoorStatus.OPEN and not (self._is_open or self._is_closed):
            self._door_status = GarageDoorStatus.CLOSING
        elif self._door_status == GarageDoorStatus.CLOSED and not (self._is_open or self._is_closed):
            self._door_status = GarageDoorStatus.OPENING
        elif self._is_open:
            self._door_status = GarageDoorStatus.OPEN
        elif self._is_closed:
            self._door_status = GarageDoorStatus.CLOSED
        else:
            self._door_status = GarageDoorStatus.UNKNOWN
        self._last_status_update = datetime.now()
        return self._door_status

    @property
    def door_status(self):
        if datetime.now() - self._last_status_update > timedelta(seconds=self.door_transit_time) \
                or self._door_status == GarageDoorStatus.UNKNOWN:
            self._refresh_door_status()
        return self._door_status

    @property
    def _is_closed(self):
        return self._closed_sensor.is_active and not self._open_sensor.is_active

    @property
    def _is_open(self):
        return self._open_sensor.is_active and not self._closed_sensor.is_active

    def toggle_door(self):
        self._door_relay.blink(on_time=self.relay_blip_time, n=1)

    def close_door(self):
        if self.door_status not in (GarageDoorStatus.CLOSED, GarageDoorStatus.CLOSING):
            self.toggle_door()

    def open_door(self):
        if self.door_status not in (GarageDoorStatus.OPEN, GarageDoorStatus.OPENING):
            self.toggle_door()

    def toggle_light(self):
        self._light_relay.blink(on_time=self.relay_blip_time, n=1)
