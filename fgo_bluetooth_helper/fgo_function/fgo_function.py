from fgo_bluetooth_helper.fgo_function.State_Check import State
from fgo_bluetooth_helper.util import BlueToothMouse
import time
from fgo_bluetooth_helper.util import config_6s
from fgo_bluetooth_helper.util.config_6s import first_spot_location, COL_NUMBER, ROW_NUMBER, bottom_right_location, \
    pop_up_confirm_button_location, initial_card_x, x_move_step, initial_card_y, y_move_step


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

    time.sleep(1)
    flag = True
    while flag:
        # touch summon button position for 2 times
        mouse.touch(config_6s.x_summon_button, config_6s.y_summon_button, 2)
        # sleep 1 sec
        time.sleep(0.5)
        # touch re summon button position for 6 times
        mouse.touch(config_6s.x_re_summon_button, config_6s.y_re_summon_button, 2)


def make_experience_card(port, device_type="6sp"):
    """
    搓经验丸子. 使用前需要选中经验丸子，进入待合成页面，锁定所有需要锁定的卡片，开始运行后无限循环合成。

    :param port:
    :param device_type:
    :return:
    """
    mouse = BlueToothMouse.BlueToothMouse(port=port, config=device_type)
    mouse.open()
    mouse.set_zero()

    time.sleep(0.5)
    while True:
        # click one spot to start selecting cards to feed.
        mouse.touch(first_spot_location[0], first_spot_location[1])
        time.sleep(0.5)
        # loop in COL_NUM and ROW_NUMBER, to select cards to feed
        for col_index in range(COL_NUMBER):
            for row_index in range(ROW_NUMBER):
                mouse.touch(initial_card_x + x_move_step * row_index, initial_card_y + col_index * y_move_step)
        # click feed button at bottom right corner
        mouse.touch(bottom_right_location[0], bottom_right_location[1])
        time.sleep(0.3)
        mouse.touch(bottom_right_location[0], bottom_right_location[1])
        # click pop up confirm button
        time.sleep(0.3)
        mouse.touch(pop_up_confirm_button_location[0], pop_up_confirm_button_location[1])
        time.sleep(4)
        # click to ignore animation
        mouse.touch(bottom_right_location[0], bottom_right_location[1], 8)
        time.sleep(1)


if __name__ == '__main__':
    friendship_point_summon("com3")
    # make_experience_card("com3")
