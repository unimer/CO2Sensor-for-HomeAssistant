
from CO2.bluepy_back import BluepyBack
from datetime import datetime
import time
from struct import unpack, pack


_BATTERY                = 0X180F
_SENSOR_SERVICE         = 0xAA01
_SETTINGS_SERVICE       = 0XAA02
_DEVICE_INFO_SERVICE    = 0X180A
_GENERIC_ACCESS         = 0x1800

#Characteristics:
#Battery
_BATTERY_LEVEL          = 0X2A19

#Settings
_SENSORS_SAMPLE_RATE    = 0XBB05
_SHUT_DOWN              = 0XBB06
_PASSKEY                = 0XBB07

#Settins data to write
_SHUT_DOWN_DATA         = 0x01AA01AA

#Device Info
_SERIAL_NUMBER          = 0x2A25
_FIRMWARE_REVISION      = 0x2A26
_HARDWARE_REVISION      = 0x2A27
_MANUFACTURER_NAME      = 0x2A29

#Sensor readings
_TEMPERATURE            = 0xBB01
_PRESSURE               = 0xBB02
_HUMIDITY_LEVEL         = 0xBB03
_CO2_LEVEL              = 0xBB04


class BleConnection(object):
    def __init__(self, mac, adapter = 'hci0'):
        self._mac = mac
        self._connect = BluepyBack(self._mac)  #_connect is a BluepyBack object

    def __enter__(self):
        self._connect.connect()    #_connect cals a function connect of BlueBack class
        return self._connect                # and __eneter__ returns object connect

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._connect.disconnect()
            self._connect = None
        except:
            pass    

"""
Class DeviceCache stores values updated by last update that happened.
Later in applicaton, function getParameter from Poller Class returns values from DeviceCache.
Main idea of this principle is to save battery life of the sensor, because sensor is measuring slow changing parameters.
"""
class DeviceCache(object):
    temperature     = 0
    pressure        = 0
    humidity_level  = 0
    co2_level       = 0
    battery_level   = 0
    firmware        = None
    hardware        = None
    serial          = None
    manufacturer    = None
    first_update    = False
    is_cached       = False

    def __init__(self, time_out):
        self._timeout = time_out
        self._update_time = datetime.now()



class DataHandler(object):
    def __init__(self, mac, adapter = 'hci0', cache_timeout = 300, update_cache = True, sensor_sample_rate = 10):    
        self._mac = mac
        self._adapter = adapter
        self._cache = DeviceCache(cache_timeout)
        self._sample_rate = sensor_sample_rate
        self.update_timer = update_cache                             #knowing mac address we can connect using  (with <class> as <new object>:)
    # Function that gets data from sensor

    def updateAllData(self):

        # Updating sensor readings
        # unpacking them also to "translate C values to python values"
        with BleConnection(self._mac) as sensor:

            """
            We need to read those informations only once, when initiating the sensor.
            those data don't change their value very often, so there is no need to waste battery on those updates.
            """
            if self._cache.first_update == False:

                ##Setting sample rate
                data = int(str(0x000000) + str(self._sample_rate))
                byte = pack('i', data)
                sensor.write(_SETTINGS_SERVICE, _SENSORS_SAMPLE_RATE, byte)

                self._cache.firmware        = sensor.read(_DEVICE_INFO_SERVICE, _FIRMWARE_REVISION).decode("utf-8")
                self._cache.hardware        = sensor.read(_DEVICE_INFO_SERVICE, _HARDWARE_REVISION).decode("utf-8")
                self._cache.serial          = sensor.read(_DEVICE_INFO_SERVICE, _SERIAL_NUMBER).decode("utf-8")
                self._cache.manufacturer    = sensor.read(_DEVICE_INFO_SERVICE, _MANUFACTURER_NAME).decode("utf-8")
                self._cache.first_update    = True 


            self._cache.battery_level,   = unpack('B', sensor.read(_BATTERY, _BATTERY_LEVEL))
            self._cache.temperature,     = unpack('f', sensor.read(_SENSOR_SERVICE, _TEMPERATURE))
            self._cache.pressure,        = unpack('f', sensor.read(_SENSOR_SERVICE, _PRESSURE))
            self._cache.humidity_level,  = unpack('f', sensor.read(_SENSOR_SERVICE, _HUMIDITY_LEVEL))
            self._cache.co2_level,       = unpack('f', sensor.read(_SENSOR_SERVICE, _CO2_LEVEL))
     

            self._cache._update_time = datetime.now()
            self._cache.is_cached = True



    """ 
    Function is checking if cache is cached, and updates cache depending on variable 'update_timer'.
    If update timer is enabled, cache will be updated only when cache_timeout overflow, in other case
    cache will be updated every time when function is called
    This principle of updating and chaching , together with class DeviceCache and class Updater is allowing us to save battery lifetime.4
    When cache uptade is over function returns wanted parameter.
    """
    def getParameter(self, parameter):   

        if self.update_timer == True:       #checking if update-timer is enabled
            if (self._cache.is_cached == False or self._timedif(self._cache._update_time, datetime.now()) > self._cache._timeout):
                self._cache.is_cached = False
                self.updateAllData()
        else:
            self._cache.is_cached = False
            self.updateAllData()

        if self._cache.is_cached:

            if parameter == 'battery_level':
                return self._cache.battery_level
            elif parameter == 'temperature':
                return round(self._cache.temperature, 2)
            elif parameter == 'pressure':
                return round(self._cache.pressure, 2)
            elif parameter == 'humidity_level':
                return round(self._cache.humidity_level, 2)
            elif parameter == 'co2_level':
                return round(self._cache.co2_level, 2)
            elif parameter == 'firmware_revision':
                return self._cache.firmware
            elif parameter == 'hardware_revision':
                return self._cache.hardware
            elif parameter == 'serial_number':
                return self._cache.serial
            elif parameter == 'manufacturer_name':
                return self._cache.manufacturer
            else:
                raise ValueError('Unknown request. There is no such parameter')
        else:
            raise ValueError('Chache is empty!')



    def getData(self, service_uuid, char_uuid):                 #getData returns requested data using BluepyBack.getCharacteristic
        with BleConnection(self._mac) as sensor:
            data = sensor.read(service_uuid, char_uuid)            
        return data


    # Function that sets data to sensor
    def setHandle(self, service_uuid, char_uuid, data):
        with BleConnection(self._mac) as sensor:
            sensor.write(service_uuid, char_uuid, data)


    """Function calculates diference between times when update_cache called last time and current time."""
    def _timedif(self, t1,t2=datetime.now()):
        return (t2 - t1).seconds
