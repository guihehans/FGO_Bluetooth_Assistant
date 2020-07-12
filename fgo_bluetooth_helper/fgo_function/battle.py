from fgo_bluetooth_helper.util import BlueToothMouse, CVModule
import time
from fgo_bluetooth_helper.util import config_6s


class State:
    @staticmethod
    def is_return_to_menu():
        found, location = CVModule.match_template('Return_button')
        return found

    @staticmethod
    def is_in_friend_menu():
        found, location = CVModule.match_template('friend_sign')
        return found


def enter_general_battle_procedure(mouse_instance, servant, servant_class):
    """
    enter the general battle procedure.

    1. 一般流程 手动选择战斗关卡
        a. 助战选择界面
            i. 助战职介
            ii. 助战选择
            iii. 开始战斗
        b. 战斗界面
            i. 等待loading
            ii. Turn 1 出招
            iii. 等待结果
            iv. Turn 2 出招
            v. 等待结果
            vi. Turn 3 出招
            vii. 等待结果
            viii. 等待战斗结算点击跳过
    finish

    :param mouse_instance:
    :param servant:
    :param servant_class:
    :return:
    """
    assist_select(mouse_instance, servant, servant_class)
    enter_battle(mouse_instance, battle_script="CBA_3T")

    pass


def assist_select(mouse_instance, servant, servant_class):
    completed = select_assist_servant_class(mouse_instance, servant_class)
    servant_found = False
    try_times = 5
    while completed and not servant_found and try_times > 0:
        servant_found = select_assist_servant(mouse_instance, servant)
    start_battle()


def enter_battle(instance, battle_script="CBA_3T"):
    pass


def select_assist_servant_class(mouse_instance, servant_class: str):
    """
    select and touch the given class of servant.

    :param mouse_instance: a bluetooth mouse instance.
    :param servant_class: the class of given servant.
    :return: touch the servant_class button
    """
    found, location = CVModule.match_template(servant_class)
    if not found:
        # try to match the selected version template
        found, location = CVModule.match_template(servant_class + "_selected")
    if found:
        mouse_instance.touch(location[0] - 20, location[1] + 65, 2)
        return True
    else:
        return False


def select_assist_servant(mouse_instance, servant, retry_times):
    """
    select given servant

    :param mouse_instance:
    :param servant:
    :return: touch and select given servant
    """
    found, location = CVModule.match_template(servant + "_skill_level")
    drag_times = 3
    while not found and drag_times > 0:
        found, location, drag_times = drag_and_find_servant(mouse_instance, servant, drag_times)
    if found:
        # select the servant
        mouse_instance.touch(location[0] - 20, location[1])
        return True, retry_times
    else:
        # refresh the assist servant
        refresh_servant(mouse_instance)
        retry_times = retry_times - 1
        return False, retry_times


def drag_and_find_servant(mouse_instance, servant, drag_times):
    """
    try to find the drag bar and drag down, to search more servant

    :param mouse_instance:
    :param servant:
    :param drag_times:
    :return:
    """
    # find the drag bar
    found, location = CVModule.match_template("drag_bar")
    if found:
        # touch the drag bar
        mouse_instance.touch(location[0] - 60, location[1] + 100)
        # drag for 1 screen long
        mouse_instance.drag(location[0], location[1] + 300)
        drag_times = drag_times - 1
        found, location = CVModule.match_template(servant + "_skill_level")
        return found, location, drag_times
    else:
        return False, (0, 0), 0


def refresh_servant(mouse_instance):
    # find the drag bar
    found, location = CVModule.match_template("Refresh_friend")
    if found:
        # click refresh button
        mouse_instance.touch(location[0] - 20, location[1] + 65)
        time.sleep(0.5)
        # click confirm button
        mouse_instance.touch(location[0] - 40, location[1] + 820)
    else:
        print("cannot refresh the assist servant!")
        raise Exception


def start_battle():
    pass


if __name__ == '__main__':
    bluemouse = BlueToothMouse.BlueToothMouse(port="com3", config="6sp")
    bluemouse.open()
    bluemouse.set_zero()
    enter_general_battle_procedure(bluemouse, servant="CBA", servant_class="Caster")
    bluemouse.close()
