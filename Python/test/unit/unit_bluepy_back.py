import unittest
from unittest import mock

from mocker import MOCK_MAC
from mocker import _SETTINGS_SERVICE
from mocker import _DEVICE_INFO_SERVICE
from mocker import _BATTERY
from mocker import MOCK_UUID_DATA
from mocker import MOCK_UUID_ELSE
from mocker import _BATTERY_LEVEL
from mocker import _SENSOR_SERVICE
from mocker import _SHUT_DOWN_DATA
from CO2.bluepy_back import BluepyBack

#from __init__ import _


class TestBluePy (unittest.TestCase):


    def setUp(self):
        self.sensor1 = BluepyBack(MOCK_MAC, timeout=10, adapter='hci0')
        self.sensor2 = BluepyBack(MOCK_MAC, timeout=10, adapter='hci')      #This is suposed to thwrow an ValueError


    def tearDown(self):
        pass

    #test of bluepy.btle is available
    def test_is_available(self):
        pass

    #test connect funcion

    #@mock.patch('bluepy.btle.Peripheral.disconnect')
    @mock.patch('bluepy.btle.Peripheral')
    def test_connect_disconnect(self, mock_peripheral):

        self.sensor1.connect()
        mock_peripheral.assert_called_with(MOCK_MAC, "random", iface = 0)

        with self.assertRaises(ValueError):
            self.sensor2.connect()

       

        with mock.patch.object(self.sensor1, 'disconnect') as mock_disconnect:
            self.sensor1.disconnect()
            mock_disconnect.assert_called_with()

       




    #test getUUID
    @mock.patch('bluepy.btle.UUID')
    def test_getUUID(self, mock_uuid):
        # test for GATT defined UUID
        mock_uuid.return_value = MOCK_UUID_ELSE
        ret = self.sensor1.getUUID(_BATTERY)

        mock_uuid.assert_called_with(_BATTERY)

        self.assertEqual(ret, MOCK_UUID_ELSE)

        #test for Custom Service UUID
        ret2 = self.sensor1.getUUID(_SENSOR_SERVICE)
        self.assertEqual(ret2, MOCK_UUID_DATA)

       

    #test getService
    @mock.patch('CO2.BluepyBack.getUUID')
    def test_getService(self, mock_getUUID,):
        mock_getUUID.return_value = MOCK_UUID_ELSE

        self.sensor1.getService(_BATTERY)
        mock_getUUID.assert_called_with(_BATTERY)

    

    #test getCharacteristic

    def test_getCharacteristic(self):

        with mock.patch.object(self.sensor1, 'getCharacteristic') as mock_getChar:
            mock_getChar.return_value = MOCK_UUID_ELSE

            self.sensor1.getCharacteristic(_BATTERY, _BATTERY_LEVEL)

            mock_getChar.assert_called_with(_BATTERY, _BATTERY_LEVEL)

         
    @mock.patch('CO2.bluepy_back.BluepyBack.getCharacteristic')
    def test_read(self, mock_getChar):
        mock_getChar.return_value = MOCK_UUID_ELSE

        self.sensor1.read(_BATTERY, _BATTERY_LEVEL)

        mock_getChar.assert_called_with(_BATTERY, _BATTERY_LEVEL, 'r')

    
    @mock.patch('CO2.bluepy_back.BluepyBack.getCharacteristic')
    def test_write(self, mock_getChar):
        mock_getChar.return_value = MOCK_UUID_ELSE

        self.sensor1.write(_BATTERY, _BATTERY_LEVEL, _SHUT_DOWN_DATA)
        mock_getChar.assert_called_with(_BATTERY, _BATTERY_LEVEL)

  


    #test ble scan function
    @mock.patch('bluepy.btle.Scanner')
    def test_scan(self, mock_scanner):

        self.sensor1.scan(timeout=10.0)

        mock_scanner.assert_called_with()



if __name__ == '__main__':
    unittest.main()