""" 
Support for CO2 Infinion sensor
 Author: Nikola Marin 
"""
import os
import os.path
import logging
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity, ToggleEntity
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_MONITORED_CONDITIONS, CONF_NAME, CONF_MAC, ATTR_ENTITY_ID)
from homeassistant.const import STATE_ON, STATE_OFF, STATE_UNKNOWN

_LOGGER = logging.getLogger(__name__)


REQUIREMENTS = ['co2-sensor==1.0']

CONF_ADAPTER = 'adapter'
CONF_CACHE   = 'cache_value'
CONF_TIMEOUT = 'timeout'
CONF_SAMPLE_RATE = 'sample_rate'


DEFAULT_ADAPTER 		= 'hci0'
#DEFAULT_CO2_UNIT 		= 'ppm'
DEFAULT_UPDATE_INTERVAL = 60
DEFAULT_NAME 			= 'CO2 sensor'
DEFAULT_TIMEOUT			= 10

FILEPATH = 'can_read'
 ""
#defining sensor types: 'key' : ['name', 'units']
SENSOR_TYPES = {
	'temperature'	: ['Temperature', '°C'],
	'pressure'		: ['Pressure', 'hPa'],
	'humidity_level': ['Humidity', '%'],
	'co2_level'		: ['CO2', 'ppm'  ],
	'battery_level'	: ['Battery', '%']
}


#platfor schema
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_MAC) : cv.string,
	vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
	vol.Optional(CONF_MONITORED_CONDITIONS, default=SENSOR_TYPES) : vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
	vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT) : cv.positive_int,
	vol.Optional(CONF_CACHE, default=DEFAULT_UPDATE_INTERVAL) : cv.positive_int,
	vol.Optional(CONF_ADAPTER, default=DEFAULT_ADAPTER) : cv.string,
	vol.Optional(CONF_SAMPLE_RATE, default = 10) : cv.positive_int
})


def setup_platform(hass, config, add_devices, discovery_info = None):
	""" SetUp CO2 sensor"""

	from CO2 import sensor_co2

	sample_rate = config.get(CONF_SAMPLE_RATE)

	cache = config.get(CONF_CACHE)
	poller = sensor_co2.Poller(config.get(CONF_MAC), adapter=config.get(CONF_ADAPTER), cache_timeout = config.get(CONF_CACHE), sensor_sample_rate = sample_rate)
 		
	devs = []

	if config.get(ATTR_ENTITY_ID) != 'switchco2':

		
		for parameter in config[CONF_MONITORED_CONDITIONS]:
			name = SENSOR_TYPES[parameter][0]
			unit = SENSOR_TYPES[parameter][1]
		
			prefix = config.get(CONF_NAME)
			if prefix:
				name = "{} {}".format(prefix, name)
				
			devs.append(SensorCO2(poller, name, unit,  parameter, prefix))
			
			print(parameter)
		#devs.append(SensorCO2Toggle(poller, "CO2 Sensor"))				# add feature to know when sensor is on
	else:
		name = SENSOR_TYPES['co2_level'][0]		
		prefix = config.get(CONF_NAME)
		if prefix:
			name = "{} {}".format(prefix, name, prefix)
			
		devs.append(SensorCO2Toggle(poller, name, prefix))	
	add_devices(devs)



class SensorCO2(Entity):
	
	def __init__(self, poller, name, unit, parameter, file_name, force_update = True):
		""" Initialise CO2 sensor """
		self.poller = poller
		self.parameter = parameter
		self._name = name
		self._unit = unit
		self._state = None
		self._file = file_name
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

	def update(self):
		try:
			self._state = self.poller.getHandle(self.parameter)

		except:
			self._state = STATE_UNKNOWN

		if (self._state != STATE_UNKNOWN):
			f = open(self._file, 'w')
			f.close()
		else:
			if os.path.isfile(self._file):
				os.remove(self._file) 


class SensorCO2Toggle(ToggleEntity):

	def __init__(self, poller, name, file_name):
		self._active = True
		self._name = name
		self._poller = poller
		self._file = file_name

	@property
	def name(self):
		return self._name

	@property
	def state(self):
		return STATE_ON if self.is_on  else STATE_OFF

	@property
	def is_on(self):
		if(os.path.isfile(self._file)):
			return True
		else:
			return False		#return self._poller.is_online()

	
	def toggle(self, **kwargs):
		if self.is_on:
			return self.turn_off()
		else:
			return self.turn_on()


	def turn_on(self):
		pass

	def turn_off(self):
		try:
			if (self._poller.setHandle('turn_off', data = None)):
				os.remove(self._file)
		except:
			print ("Unabled to turn_off")
	

