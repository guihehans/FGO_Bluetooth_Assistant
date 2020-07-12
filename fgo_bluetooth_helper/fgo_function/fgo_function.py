from fgo_bluetooth_helper.util import BlueToothMouse
import time
from fgo_bluetooth_helper.util import config_6s


def friendship_point_summon(port="com3", device_type="6sp"):
    """
    auto friendship point summon function

    :param port: the serial port name for bluetooth
    :param device_type: the phone device type. default is 6sp
    :return:
    """
    mouse = BlueToothMouse.BlueToothMouse(port=port, config=device_type)
    mouse.open()
    mouse.set_zero()

    mouse.touch(config_6s.x_center, config_6s.y_center)
    time.sleep(1)
    flag = True
    while flag:
        # touch summon button position for 2 times
        mouse.touch(config_6s.x_summon_button, config_6s.y_summon_button, 2)
        # sleep 1 sec
        time.sleep(1)
        # touch re summon button position for 6 times
        mouse.touch(config_6s.x_re_summon_button, config_6s.y_re_summon_button, 6)


if __name__ == '__main__':
    friendship_point_summon("com3")
