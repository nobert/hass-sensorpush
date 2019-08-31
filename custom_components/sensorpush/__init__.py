"""
SensorPush for Home Assistant

See also:

* https://github.com/rsnodgrass/hass-sensorpush
* http://www.sensorpush.com/api/docs
* https://community.home-assistant.io/t/sensorpush-humidity-and-temperature-sensors/105711

"""
import logging
import json
import requests
import time
from threading import Thread, Lock

from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.const import ( CONF_USERNAME, CONF_PASSWORD, CONF_NAME, CONF_SCAN_INTERVAL )
#from homeassistant.components.sensor import ( PLATFORM_SCHEMA )

_LOGGER = logging.getLogger(__name__)

SENSORPUSH_DOMAIN = 'sensorpush'
SENSORPUSH_USER_AGENT = 'Home Assistant (https://homeassistant.io/; https://github.com/rsnodgrass/hass-sensorpush)'

# cache expiry in minutes; TODO: make this configurable (with a minimum to prevent DDoS)
SENSORPUSH_CACHE_EXPIRY=10

SENSORPUSH_API = 'https://api.sensorpush.com/api/v1'

UNIT_SYSTEMS = {
    'imperial': { 
        'system':   'imperial',
        'temp':     '°F',
        'humidity': 'Rh'
    },
    'metric': { 
        'system':   'metric',
        'temp':     '°C',
        'humidity': 'Rh'
    }
}

mutex = Lock()

#CONFIG_SCHEMA = vol.Schema({
#    SENSORPUSH_DOMAIN: vol.Schema({
#        vol.Required(CONF_USERNAME): cv.string,
#        vol.Required(CONF_PASSWORD): cv.string
#        vol.Optional(CONF_SCAN_INTERVAL, default=600): cv.positive_int
#    })
#}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up the SensorPush integration"""
#    conf = config[SENSORPUSH_DOMAIN]
#    conf = {}
#    for component in ['sensor', 'switch']:
#        discovery.load_platform(hass, component, SENSORPUSH_DOMAIN, conf, config)
    return True

class SensorPushEntity(Entity):
    """Base Entity class for SensorPush devices"""

    def __init__(self, sensorpush_service):
        """Store service upon init."""
        self._service = sensorpush_service
        self._attrs = {}

        if self._name is None:
            self._name = 'SensorPush' # default if unspecified

    @property
    def name(self):
        """Return the display name for this sensor"""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        return self._attrs

class SensorPushService:
    """Client interface to the SensorPush service API"""

    def __init__(self, config):
        self._auth_token = None
        self._auth_token_expiry = 0
        
        self._username = config[CONF_USERNAME]
        password = config[CONF_PASSWORD]
        self._sensorpush = PySensorPush(self._username, password)

        self._units = UNIT_SYSTEMS['imperial']

    # FIXME: cache the results (throttle to avoid DoS API)
    def get_devices(self):
        devices = self._sensorpush.devices

    # FIXME: cache the results (throttle to avoid DoS API)
    def get_samples(self):
        samples = self._sensorpush.samples