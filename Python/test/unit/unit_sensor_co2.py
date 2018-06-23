import unittest
from datetime import datetime
import time
from unittest.mock import patch
from unittest import mock
from CO2.sensor_co2 import  Poller, Scanner
from CO2.sensor_co2 import Updater
from CO2.sensor_connection import DataHandler


from mocker import _DEVICE_INFO_SERVICE
from mocker import _FIRMWARE_REVISION
from mocker import _HARDWARE_REVISION
from mocker import _MANUFACTURER_NAME
from mocker import _SERIAL_NUMBER
from mocker import _SENSOR_SERVICE
from mocker import _CO2_LEVEL
from mocker import _SETTINGS_SERVICE, _SHUT_DOWN, _SHUT_DOWN_DATA

from mocker import MOCK_MAC
from mocker import MockedData

class TestSensorCo2(unittest.TestCase):


##Testing Updater Functions

    def setUp(self):
        self.sensor1 = DataHandler(MOCK_MAC)
        self.updater = Updater(MOCK_MAC)
        self.poller  = Poller(MOCK_MAC, adapter='hci0', cache_timeout=10, update_timer = False)
        self.mocked_data = MockedData()

    # Test updater
    def test_NotImplemented(self):
        with self.assertRaises(NotImplementedError) : self.updater.passkey(key=None)

    @mock.patch('CO2.sensor_connection.DataHandler.getParameter')
    def test_getHandle(self, mock_get):

        self.poller.getHandle('handle')

        mock_get.assert_called_with('handle')

    
    @mock.patch('CO2.sensor_co2.Updater.shutDown')    
    def test_setHandle(self, mock_off):
        self.assertTrue(self.poller.setHandle('turn_off', data = None))
        self.assertFalse(self.poller.setHandle('not_existing', data = None))
        mock_off.assert_called_once_with()

    @mock.patch('CO2.sensor_connection.DataHandler.getData')
    def test_updater(self, mock_getData):
        mock_getData.return_value = self.mocked_data.getData(_DEVICE_INFO_SERVICE, _MANUFACTURER_NAME)

        self.assertEqual('mockManu', self.updater.getManufacturerName())

        mock_getData.assert_called_with(_DEVICE_INFO_SERVICE, _MANUFACTURER_NAME)

    def test_isOnline(self):
        pass

    # Test Scanner
    def test_scan(self, timeout = 10):
        pass





if __name__ == '__main__':
    unittest.main()
