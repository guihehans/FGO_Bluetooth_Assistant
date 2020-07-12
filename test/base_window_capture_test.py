import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')

    def test_mouse_open(self):
        from fgo_bluetooth_helper.util import BlueToothMouse
        mouse = BlueToothMouse.BlueToothMouse(port="com3")
        mouse.open()
        self.assertEqual(True, mouse.get_is_open())
        mouse.close()
        self.assertEqual(False, mouse.get_is_open())


if __name__ == '__main__':
    unittest.main()
