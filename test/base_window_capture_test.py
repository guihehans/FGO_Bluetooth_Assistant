import glob
import os
import unittest
import fgo_bluetooth_helper.util.config_6s


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print('清空output文件夹')
        files = glob.glob('../output/*')
        for f in files:
            os.remove(f)

    def tearDown(self):
        print('清空output文件夹')
        files = glob.glob('../output/*')
        for f in files:
            os.remove(f)

    def test_mouse_open(self):
        from fgo_bluetooth_helper.util import BlueToothMouse
        mouse = BlueToothMouse.BlueToothMouse(port="com3")
        mouse.open()
        self.assertEqual(True, mouse.get_is_open())
        mouse.close()
        self.assertEqual(False, mouse.get_is_open())

    def test_window_capture(self):
        from fgo_bluetooth_helper.util import CVModule


if __name__ == '__main__':
    unittest.main()
