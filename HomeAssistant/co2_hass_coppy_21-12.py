""" 
Suport for CO2 Infinion sensor
Author: Nikola Marin
"""

import logging
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (ATTR_ATTRIBTION, CONF_MONITORED_CONDITIONS, CONF_NAME, CONF_MAC)

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['co2-sensor==1.0']

CONF_ADAPTER = 'adapter'
CONF_CACHE   = 'cache_value'
CONF_TIMEOUT = 'timeout'


DEFAULT_ADAPTER 		= 'hci0'
#DEFAULT_CO2_UNIT 		= 'ppm'
DEFAULT_UPDATE_INTERVAL = 1200
DEFAULT_NAME 			= 'CO2 sensor'
DEFAULT_TIMEOUT			= 10



#defining sensor types: 'key' : ['name', 'units']
SENSOR_TYPES = {
	'co2_level'		: ['CO2', 'ppm'  ],
	'battery_level'	: ['Battery', '%']
}

#SENSOR_ATTRIBUTES = {
#	'battery_level' : ['Battery', '%']
#}



#platfor schema
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_MAC) : cv.string,
	vol.Optional(CONF_MONITORED_CONDITIONS, default=SENSOR_TYPES) : vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
#	vol.Optional(CONF_STATE_ATTRIBUTES, default=SENSOR_ATTRIBUTES) : vol.ALL(cv.ensure_list, [vol.In(SENSOR_ATTRIBUTES)]),
	vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
	vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT) : cv.positive_int,
	vol.Optional(CONF_CACHE, default=DEFAULT_UPDATE_INTERVAL) : cv.positive_int,
	vol.Optional(CONF_ADAPTER, default=DEFAULT_ADAPTER) : cv.string
})


def setup_platform(hass, config, add_devices, discovery_info = None):
	""" SetUp CO2 sensor"""

	from CO2 import sensor_co2

	cache = config.get(CONF_CACHE)
	poller = sensor_co2.Poller(config.get(CONF_MAC), adapter=config.get(CONF_ADAPTER), cache_timeout=config.get(CONF_TIMEOUT))

	devs = []

	for parameter in config[CONF_MONITORED_CONDITIONS]:
		name = SENSOR_TYPES[parameter][0]
		unit = SENSOR_TYPES[parameter][1]
		
		prefix = config.get(CONF_NAME)

		if prefix:
			name = "{} {}".format(prefix, name)

		devs.append(SensorCO2(poller, name, unit,  parameter))
		print(parameter)

	add_devices(devs)
	#add_entity('serial_number', platform=devs[0], update_before_add=False)


class SensorCO2(Entity):

	def __init__(self, poller, name, unit, parameter, force_update = True):
		""" Initialise CO2 sensor """
		self.poller = poller
		self.parameter = parameter
		self._name = name
		self._unit = unit
		self._state = None
		self._force_update = force_update
		self._feature = None
		self.update()

	@property
	def name(self):
		""" Return the name of the sensor """ 
		return self._name

	@property
	def state(self):
		return self._state


	@property
	def unit_of_measurement(self):
		return self._unit

	@property
	def should_poll(self) -> bool:
		return True

	@property
	def force_update(self):
		return self._force_update

	@property
	def suported_features(self):
		return self._feature


	def update(self):
		self._state = self.poller.getParameter(self.parameter)
		self._feature = self.poller.getParameter('serial_number')


