import sys
from curses.ascii import isdigit



class BluepyBack(object):

    def __init__(self, mac, timeout=3, adapter='hci0'):
        self._mac = mac
        self._timeout = timeout
        self._adapter = adapter
        self._device = None
        self.sensor_service = None
        self.sensor_char    = None

    def is_available(self):           # function checks iig bluepy is installed or available
        try:
            import bluepy.btle
        except ImportError as e:
            print (e)                            #Insert error message


    def connect(self):

        from bluepy.btle import Peripheral, BTLEException
        if ('hci' in self._adapter and self._adapter[3:].isdigit()):
            try:
                self._device = Peripheral(self._mac, "random", iface = int(self._adapter[3:]))
            except BTLEException as e:
                print (e)
        else:
            raise ValueError('Invalid name "{}" for Bluetooth adapter.'.format(self._adapter))

    #disconnect sensor
    def disconnect(self):
        self._device.disconnect()
        self._device = None
        self.sensor_service = None
        self.sensor_char = None

    #get propper UUID for sensor
    def getUUID(self, uuid):

        from bluepy.btle import UUID
        id = hex(uuid)

        if id == hex(0xaa01):                                             #UUID for custom service
            return "6152aa01-eccc-4179-ac21-c4fdfa137d48"
        elif id == hex(0xaa02):
            return "429aaa02-d7bd-4f7d-afbb-03310da063d9"
        elif id == hex(0xbb01):
            return "6152bb01-eccc-4179-ac21-c4fdfa137d48"
        elif id == hex(0xbb02):
            return "6152bb02-eccc-4179-ac21-c4fdfa137d48"
        elif id == hex(0xbb03):
            return "6152bb03-eccc-4179-ac21-c4fdfa137d48"
        elif id == hex(0xbb04):                                           #UUID for (custom) CO2 characteristic
            return "6152bb04-eccc-4179-ac21-c4fdfa137d48"
        elif id == hex(0xbb05):                                           #UUID for (custom) CO2 characteristic
            return "429abb05-d7bd-4f7d-afbb-03310da063d9"
        elif id == hex(0xbb06):                                           #UUID for (custom) CO2 characteristic
            return "429abb06-d7bd-4f7d-afbb-03310da063d9"
        elif id == hex(0xbb07):                                           #UUID for (custom) CO2 characteristic
            return "429abb07-d7bd-4f7d-afbb-03310da063d9"
        else:
            return UUID(uuid)


    #get services using getUUID to get proper UUID
    def getService(self, serv_uuid):
        try:
            service_uuid = self.getUUID(serv_uuid)
            self.sensor_service = self._device.getServiceByUUID(service_uuid)
            return self.sensor_service
        except:
            pass

    #get characteristic by enterig service uuid and characteristic uuid
    def getCharacteristic(self, serv_uuid, char_uuid, action = None):

        self.sensor_service = self.getService(serv_uuid)
        try:
            ch_uuid = self.getUUID(char_uuid)
            char = self.sensor_service.getCharacteristics(ch_uuid)[0]

            #Checking if characteristic supports reading
            if action == 'r':
                if char.supportsRead():
                    return char
                else:
                    raise "Characteristic {} doesn't supports read".format(char_uuid)
                    return 0

            else: return char
        except:
            pass

 
    
    #Function is reading data from characteristic. 
      
    def read(self, serv_uuid, char_uuid):

        char = self.getCharacteristic(serv_uuid, char_uuid, 'r')

        try:
            return char.read()
        except:
            pass


    #Function is writing data to characteristic
    def write(self, serv_uuid, char_uuid, data):
        char = self.getCharacteristic(serv_uuid, char_uuid)
        try:
            char.write(data)
        except:
            pass



    #scan for devices using bluepy scanner
    @staticmethod
    def scan(timeout):
        from bluepy.btle import Scanner
        scanner = Scanner()

        result = scanner.scan(timeout)
        for device in result:
            result[device.addr] = device.getValueText(9)
        return result




