
from CO2.sensor_connection import DataHandler
from CO2.sensor_connection import BleConnection
from struct import unpack, pack


#Services and Characteristics handles:
#Services:
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

_RATE_DATA              = 0x00000012



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


    
class Updater(object):
    def __init__(self, mac, adapter = 'hci0'):
        self.data = DataHandler(mac, adapter)

    # Sensor settings functions

    def setSampleRate(self, sample_rate):
        data = int(str(0x000000) + str(sample_rate))
        byte = pack('i', data)
        self.data.setHandle(_SETTINGS_SERVICE, _SENSORS_SAMPLE_RATE, byte)

    def shutDown(self):
        byte = pack('i', _SHUT_DOWN_DATA)
        self.data.setHandle(_SETTINGS_SERVICE, _SHUT_DOWN, byte)

    def passkey(self, key):
        raise NotImplementedError

    #Device info returning functions
    def getSampleRate(self):
        return self.data.getData(_SETTINGS_SERVICE, _SENSORS_SAMPLE_RATE) 

    def getManufacturerName(self):
        return self.data.getData(_DEVICE_INFO_SERVICE, _MANUFACTURER_NAME)

    def getSerialNumber(self):
        return self.data.getData(_DEVICE_INFO_SERVICE, _SERIAL_NUMBER)

    def getHardwareRevision(self):
        return self.data.getData(_DEVICE_INFO_SERVICE, _HARDWARE_REVISION)

    def getFirmwareRevision(self):
        return self.data.getData(_DEVICE_INFO_SERVICE, _FIRMWARE_REVISION)

    #Sensors readings
    def getTemperature(self):
        return self.data.getData(_SENSOR_SERVICE, _TEMPERATURE)

    def getPressure(self):
        return self.data.getData(_SENSOR_SERVICE, _PRESSURE)

    def getHumidity(self):
        return self.data.getData(_SENSOR_SERVICE, _HUMIDITY_LEVEL)

    def getCO2(self):
        return self.data.getData(_SENSOR_SERVICE, _CO2_LEVEL)

    def getBatteryLevel(self):
        return self.data.getData(_BATTERY, _BATTERY_LEVEL)   
   


class Poller(object):                                                          #poller has a functions to read or write sensors data. functions can call functions from DataHandler, getData, and setData

    def __init__(self, mac, adapter='hci0', cache_timeout=120, update_timer = True, sensor_sample_rate = 10):
        self.handler      = DataHandler(mac, adapter, cache_timeout, update_timer, sensor_sample_rate)
        self.updater      = Updater(mac, adapter)
    """
    Funcion Get Handle
    Returns wanted handle
    """
    def getHandle(self, handle):
        return self.handler.getParameter(handle)    

    """
    This function sets a parameter to sensor that is enabled to set like Sample Rate or Turn Off.
    """
    def setHandle(self, parameter, data = None):
        if parameter == 'turn_off':
            self.updater.shutDown()
            return True
        if parameter == 'sample_rate':
            self.updater.setSampleRate(data)
            return True
        else:
            return False

  



class Scanner(object):
    def scan(self, timeout = 10.0):
        ret = {}
        devices = BluepyBack.scan(timeout)

        for dev in devices:
           ret[dev] = devices[dev]

        return ret






