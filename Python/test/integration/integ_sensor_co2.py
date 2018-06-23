import unittest
from CO2.sensor_co2 import Poller, Updater

SENSOR_MAC = "EC:F9:FC:E3:91:D3"
ADAPTER    = 'hci0'
CACHE_TO   = 300



class TestCO2Sensor(unittest.TestCase):

	def setUp(self):
		self._poller = Poller(SENSOR_MAC, ADAPTER, CACHE_TO)
		self.updater = Updater(SENSOR_MAC)


	def test_getParameter(self):

		data = self._poller.getHandle('battery_level')
		self.assertTrue(0 <= data <= 100)

		data = self._poller.getHandle('temperature')
		self.assertTrue(0 <= data <= 100)
		
		data = self._poller.getHandle('pressure')
		self.assertTrue(0 <= data <= 2000)
		
		data = self._poller.getHandle('humidity_level')
		self.assertTrue(0 <= data <= 100)
		
		data = self._poller.getHandle('co2_level')
		self.assertTrue(0 <= data <= 3000)

		#Sensor info test
		
		info = self._poller.getHandle('firmware_revision')
		self.assertEqual('Rev_1', info)
	
		info = self._poller.getHandle('serial_number')
		self.assertEqual('Serial_1', info)
		
		info = self._poller.getHandle('hardware_revision')
		self.assertEqual('Rev_1', info)	
		
		info = self._poller.getHandle('manufacturer_name')
		self.assertEqual('Infineon', info)

		with self.assertRaises(ValueError): self._poller.getHandle('non_existing_parameter') 

		#test set sample_rate
		#print (self.updater.getSampleRate())

		#self._poller.setHandle('sample_rate', 5)

		#test set parameeter (shut_down)	
		
		#self._poller.setHandle('turn_off', data = None)
		

		


if __name__ == "__main__":
	unittest.main()