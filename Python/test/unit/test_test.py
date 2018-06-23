import unittest

class TestTest(unittest.TestCase):

	def test1(self):
		self.assertTrue(True)
		self.assertEqual(5,5)
		self.assertEqual(7,7)
		self.assertFalse(False)


if __name__ == '__main__':
	unittest.main()