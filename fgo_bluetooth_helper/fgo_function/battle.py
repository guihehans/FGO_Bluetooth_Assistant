import sys
import time

from fgo_bluetooth_helper.fgo_function import State_Check
from fgo_bluetooth_helper.util import BlueToothMouse, CVModule
from script import script_register


class BattleHelper(object):
    def __init__(self, port, script):

        self.mouse_instance = BlueToothMouse.BlueToothMouse(port=port, config="6sp")
        self.mouse_instance.open()
        self.servant = ""
        self.servant_class = ""
        self.servant_class_location_error = 0, 0
        self.servant_location_error = 0, 0
        self.battle_script = script
        self.script_instance = script_register.load_script(script)
        self.config_servant_parameters()

    def config_servant_parameters(self):
        config_data = self.script_instance.get_parameters()
        self.servant = config_data.get("servant")
        self.servant_class = config_data.get("servant_class")
        self.servant_class_location_error = config_data.get('servant_class_location_error', (0, 0))
        self.servant_location_error = config_data.get('servant_location_error', (0, 0))

    def enter_general_battle_procedure(self):
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
        :return:
        """
        if self.mouse_instance.get_is_open():
            print("Enter enter_general_battle_procedure with servant:[{}],servant class:[{}],battle_script:[{}]".format(
                self.servant,
                self.servant_class,
                self.battle_script
            ))

            # select assist servant
            self.assist_select(self.servant, self.servant_class, self.battle_script)
            # enter battle and act as setting battle script
            self.enter_battle(battle_script=self.battle_script)
        else:
            print("mouse not open!exit now.")

    def enter_repeated_battle_procedure(self, repeat_times=3):
        """
        enter the repeated battle procedure.

        1. 重复战斗流程 手动选择战斗关卡
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
                viii. 等待战斗结算 点击继续战斗 回到a
        战斗重复次数达到
        finish
        :return:
        """
        for i in range(repeat_times, 0, -1):
            if self.mouse_instance.get_is_open():
                if State_Check.State.is_ready_to_select_assist_servant():
                    print(
                        "Enter enter_general_battle_procedure with servant:[{}],servant class:[{}],battle_script:[{}]".format(
                            self.servant,
                            self.servant_class,
                            self.battle_script
                        ))
                    print("Current round {}.".format(repeat_times - i))
                    # select assist servant
                    self.assist_select(self.servant, self.servant_class, self.battle_script)
                    # enter battle and act as setting battle script
                    self.enter_repeat_battle(repeat_times, battle_script=self.battle_script)
                else:
                    print("can not be ready to select assist servant!")
            else:
                print("mouse not open!exit now.")

    def assist_select(self, servant, servant_class, battle_script):
        """
        select the assist servant.
        the process is :
            1.select the servant class
            2.select the servant within max retry times.

        :param servant:
        :param servant_class:
        :param battle_script:
        :return:
        """
        # select servant class
        completed = self.select_assist_servant_class(servant_class)
        servant_found = False
        retry_times = 1
        max_retry = 5
        # loop retry to select servant, within max retry times.
        while completed and not servant_found and retry_times < max_retry:
            print("try to select servant [{}],currently in {} times now.".format(servant, retry_times))
            servant_found, retry_times = self.select_assist_servant(servant, retry_times)
            if servant_found:
                print("servant [{}] found.".format(servant))
                self.select_team(battle_script=battle_script)
                time.sleep(0.5)

            elif retry_times >= max_retry:
                print("cannot find servant {} in given retry_times".format(servant))
                sys.exit()

    def enter_battle(self, battle_script="CBA_3T"):
        """
        battle function

        :param battle_script:
        :return:
        """
        self.start_battle()
        self.script_instance.run_battle_script(self.mouse_instance)

    def enter_repeat_battle(self, repeat_times, battle_script="CBA_3T"):
        """
        battle function

        :param battle_script:
        :param repeat_times:
        :return:
        """
        self.start_battle()
        self.script_instance.run_battle_script(self.mouse_instance, repeat_times)

    def select_assist_servant_class(self, servant_class: str):
        """
        select and touch the given class of servant.

        :param servant_class: the class of given servant.
        :return: touch the servant_class button
        """
        print("Start select servant_class [{}]".format(servant_class))
        found, location = CVModule.match_template(servant_class)
        if not found:
            # try to match the selected version template
            found, location = CVModule.match_template(servant_class + "_selected")
        if found:
            self.mouse_instance.set_zero()
            time.sleep(0.1)
            self.mouse_instance.touch(location[0] + self.servant_class_location_error[0],
                                      location[1] + self.servant_class_location_error[1], 2)
            print("Complete select servant_class [{}]".format(servant_class))
            return True
        else:
            print("Can not select servant_class [{}]".format(servant_class))
            return False

    def select_assist_servant(self, servant, retry_times):
        """
        select given servant. if not found, drag down the scroll bar for "drag_times",and search servant again.

        :param self:
        :param servant:
        :param retry_times: the current retry time. decrease when servant still not found when drag all down.
        :return: touch and select given servant
        """
        time.sleep(0.3)
        found, location = CVModule.match_template(servant)
        drag_times = 3
        while (not found) and (drag_times > 0):
            found, location, drag_times = self.drag_and_find_servant(servant, drag_times)
        if found:
            # select the servant
            time.sleep(0.1)
            self.mouse_instance.touch(location[0] + self.servant_location_error[0],
                                      location[1] + self.servant_location_error[1])
            return True, retry_times
        else:
            # refresh the assist servant
            self.refresh_servant()
            retry_times = retry_times + 1
            return False, retry_times

    def drag_and_find_servant(self, servant, drag_times):
        """
        try to find the drag bar and drag down, to search more servant

        :param self:
        :param servant:
        :param drag_times:
        :return:
        """
        # find the drag bar
        self.mouse_instance.set_zero()
        time.sleep(0.3)
        found, location = CVModule.match_template("drag_bar")
        if found:
            # touch the drag bar
            self.mouse_instance.touch(location[0] - 60, location[1] + 100)
            # drag for 1 screen long
            self.mouse_instance.drag(location[0] - 60, location[1] + 300)
            drag_times = drag_times - 1
            found, location = CVModule.match_template(servant)
            return found, location, drag_times
        else:
            return False, (0, 0), 0

    def refresh_servant(self):
        # find the drag bar
        found, location = CVModule.match_template("Refresh_friend")
        if found:
            # click refresh button
            self.mouse_instance.touch(location[0] - 55, location[1] + 80)
            time.sleep(0.5)
            # click confirm button
            self.mouse_instance.touch(location[0] - 55, location[1] + 820)
            time.sleep(1)
        else:
            print("cannot refresh the assist servant!")

    def select_team(self, battle_script):
        """
        select team according to battle script setting

        :param battle_script:
        :return:
        """
        pass

    def start_battle(self):
        time.sleep(1)
        found, location = CVModule.match_template("Start_button")
        if found:
            print("enter battle now.")
            self.mouse_instance.set_zero()
            self.mouse_instance.touch(location[0] - 50, location[1] + 450)
        else:
            print("cannot find Start_button, please check template!")
            print("exit battle.")


if __name__ == '__main__':
    battle_helper = BattleHelper(port="com3", script="CBA_3T")
    battle_helper.enter_general_battle_procedure()
    # enter_general_battle_procedure(blue_mouse, servant="CBA", servant_class="Caster", battle_script="CBA_3T")
    # enter_general_battle_procedure(blue_mouse, servant="Arjuna_Alter", servant_class="Berserker",
    #                                battle_script="AOE_3T")
