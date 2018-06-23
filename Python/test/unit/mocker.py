MOCK_MAC = 'AA:BB:CC:DD:EE:FF'
MOCK_UUID_SETTINGS = "6152aa02-eccc-4179-ac21-c4fdfa137d48"
MOCK_UUID_DATA = "6152aa01-eccc-4179-ac21-c4fdfa137d48"
MOCK_UUID_ELSE = "6152alll-eccc-4179-ac21-c4fdfa137d48"
#Services and Characteristics handles:
#Services:
_BATTERY                = 0X180F
_NAME                   = None
_SENSOR_SERVICE         = 0xAA01
_SETTINGS_SERVICE       = 0XAA02
_DEVICE_INFO_SERVICE    = 0X180A

#Characteristics:
#Battery
_BATTERY_LEVEL     = 0X2A19

#Settings
_SENSORS_SAMPLE_RATE    = 0XBB05
_SHUT_DOWN              = 0XBB06
_PASSKEY                = 0XBB07

#Settings write data
_SHUT_DOWN_DATA         =b'\x01\xAA\x01\xAA'

#Device Info
_SERIAL_NUMBER          = 0x2A25
_FIRMWARE_REVISION      = 0x2A26
_HARDWARE_REVISION      = 0x2A27
_MANUFACTURER_NAME      = 0x2A29

#Sensor readings
_CO2_LEVEL              = 0xBB04

class MockedData(object):

    def __init__(self):
        self.co2level = 1000
        self.serial_number = '12345'
        self.firmware_rev = 'mockFirm'
        self.hardware_rev = 'mockHard'
        self.manufacturer = 'mockManu'
        self.battery_level = 40


    def getData(self, service_uuid, char_uuid):
        if service_uuid == _BATTERY and char_uuid == _BATTERY_LEVEL:
            return self.battery_level
        elif service_uuid == _DEVICE_INFO_SERVICE:
            if char_uuid == _SERIAL_NUMBER:
                return self.serial_number
            elif char_uuid == _FIRMWARE_REVISION:
                return self.firmware_rev
            elif char_uuid == _HARDWARE_REVISION:
                return self.hardware_rev
            elif char_uuid == _MANUFACTURER_NAME:
                return  self.manufacturer

        elif service_uuid == _SENSOR_SERVICE and char_uuid == _CO2_LEVEL:
            return self.co2level

        else:
            pass



