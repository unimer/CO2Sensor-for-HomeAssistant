import time
import unittest
from datetime import datetime
from struct import unpack, pack 

from unittest import mock
from unittest.mock import patch

from mocker import MOCK_MAC
from mocker import MockedData

from mocker import _DEVICE_INFO_SERVICE
from mocker import _FIRMWARE_REVISION
from mocker import _HARDWARE_REVISION
from mocker import _MANUFACTURER_NAME
from mocker import _SERIAL_NUMBER
from mocker import _SENSOR_SERVICE
from mocker import _CO2_LEVEL
from mocker import _SETTINGS_SERVICE, _SHUT_DOWN, _SHUT_DOWN_DATA


from CO2.sensor_co2 import Poller, Scanner

#Testing Classes
from CO2.sensor_connection import DeviceCache
from CO2.sensor_connection import DataHandler
from CO2.sensor_connection import BleConnection


class TestSensorConnection(unittest.TestCase):

    def setUp(self):
        self.sensor1 = DataHandler(MOCK_MAC)
        self.mocked_data = MockedData()
        self.cache = DeviceCache(time_out = 30)        

    def tearDown(self):
        pass

    def test_deviceCache(self):
        self.assertEqual(0, self.cache.temperature)
        self.assertEqual(0, self.cache.pressure)
        self.assertEqual(0, self.cache.humidity_level)
        self.assertEqual(0, self.cache.co2_level)
        self.assertEqual(0, self.cache.battery_level)
    

    def test_updateAllData(self):
        with mock.patch.object(DataHandler, 'updateAllData', return_value = None) as mock_method:
            thing = DataHandler(MOCK_MAC)
            thing.updateAllData()

            mock_method.assert_called_with()

    @mock.patch('CO2.sensor_connection.DataHandler.updateAllData')     
    def test_getParameter(self, mock_update):
            updater = DataHandler(MOCK_MAC, update_cache = False)

            with self.assertRaises(ValueError): updater.getParameter('parameter')
            mock_update.assert_called_with()


            

    def test_timedif(self):
       t1 = datetime.now()
       time.sleep(3)
       t2 = datetime.now()
       self.assertEqual(3,self.sensor1._timedif(t1, t2))





if __name__ == '__main__':
    unittest.main()