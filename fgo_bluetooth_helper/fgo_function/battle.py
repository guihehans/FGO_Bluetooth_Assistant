import random
import sys

from fgo_bluetooth_helper.fgo_function.State_Check import State
from fgo_bluetooth_helper.util import BlueToothMouse, CVModule
import time
from fgo_bluetooth_helper.util import config_6s


def enter_general_battle_procedure(mouse_instance, servant, servant_class, battle_script):
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
    :param battle_script:
    :return:
    """
    if mouse_instance.get_is_open():
        print("Enter enter_general_battle_procedure with servant:[{}],servant class:[{}],battle_script:[{}]".format(
            servant,
            servant_class,
            battle_script))
        # select assist servant
        assist_select(mouse_instance, servant, servant_class, battle_script)
        # enter battle and act as setting battle script
        enter_battle(mouse_instance, battle_script=battle_script)
    else:
        print("mouse not open!")


def assist_select(mouse_instance, servant, servant_class, battle_script):
    """
    select the assist servant.
    the process is :
        1.select the servant class
        2.select the servant within max retry times.

    :param mouse_instance:
    :param servant:
    :param servant_class:
    :return:
    """
    # select servant class
    completed = select_assist_servant_class(mouse_instance, servant_class)
    servant_found = False
    retry_times = 1
    max_retry = 5
    # loop retry to select servant, within max retry times.
    while completed and not servant_found and retry_times < max_retry:
        print("try to select servant [{}],currently in {} times now.".format(servant, retry_times))
        servant_found, retry_times = select_assist_servant(mouse_instance, servant, retry_times)
    if servant_found:
        print("servant [{}] found.".format(servant))
        select_team(mouse_instance, battle_script=battle_script)
        start_battle(mouse_instance)
    else:
        print("cannot find servant {} in given retry_times".format(servant))


def enter_battle(mouse_instance, battle_script="CBA_3T"):
    """
    battle function

    :param mouse_instance:
    :param battle_script:
    :return:
    """
    # 鼠标复位,防止误差累积
    mouse_instance.set_zero()
    # 等待战斗开始
    # 判断是否进入战斗界面
    State.is_ready_to_act()
    time.sleep(3)  # 等待6秒，因为礼装效果掉落暴击星会耗时
    # Turn 1
    print("Turn 1")
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=2)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=3)
    character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=1, skill_target=1)
    act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)

    # 鼠标复位,防止误差累积
    mouse_instance.set_zero()
    State.is_ready_to_act()
    # Turn 2
    print("Turn 2")
    character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=3, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=1, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=1, skill_number=3)
    cast_master_skill(mouse_instance=mouse_instance, skill_number=3, swap_target_1=2, swap_target_2=4)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=1, skill_target=1)
    act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)

    # 鼠标复位,防止误差累积
    mouse_instance.set_zero()
    State.is_ready_to_act()
    # Turn3
    print("Turn 3")
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=3, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=2)
    character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=2)
    cast_master_skill(mouse_instance=mouse_instance, skill_number=1)
    act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)
    # quit battle
    quit_battle(mouse_instance)


def select_assist_servant_class(mouse_instance, servant_class: str):
    """
    select and touch the given class of servant.

    :param mouse_instance: a bluetooth mouse instance.
    :param servant_class: the class of given servant.
    :return: touch the servant_class button
    """
    print("Start select servant_class [{}]".format(servant_class))
    found, location = CVModule.match_template(servant_class)
    if not found:
        # try to match the selected version template
        found, location = CVModule.match_template(servant_class + "_selected")
    if found:
        time.sleep(0.1)
        mouse_instance.touch(location[0] - 20, location[1] + 65, 2)
        print("Complete select servant_class [{}]".format(servant_class))
        return True
    else:
        print("Can not select servant_class [{}]".format(servant_class))
        return False


def select_assist_servant(mouse_instance, servant, retry_times):
    """
    select given servant. if not found, drag down the scroll bar for "drag_times",and search servant again.

    :param mouse_instance:
    :param servant:
    :param retry_times: the current retry time. decrease when servant still not found when drag all down.
    :return: touch and select given servant
    """
    found, location = CVModule.match_template(servant + "_skill_level")
    drag_times = 3
    while not found and drag_times > 0:
        found, location, drag_times = drag_and_find_servant(mouse_instance, servant, drag_times)
    if found:
        # select the servant
        time.sleep(0.1)
        mouse_instance.touch(location[0] - 20, location[1] + 250)
        return True, retry_times
    else:
        # refresh the assist servant
        refresh_servant(mouse_instance)
        retry_times = retry_times + 1
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
    time.sleep(0.3)
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
        time.sleep(1)
    else:
        print("cannot refresh the assist servant!")


def select_team(mouse_instance, battle_script):
    """
    select team according to battle script setting

    :param mouse_instance:
    :param battle_script:
    :return:
    """
    pass


def start_battle(mouse_instance):
    time.sleep(1)
    found, location = CVModule.match_template("Start_button")
    if found:
        print("enter battle now.")
        mouse_instance.set_zero()
        mouse_instance.touch(location[0] - 50, location[1] + 450)
    else:
        print("cannot find Start_button, please check template!")


def character_skill(mouse_instance, character_number, skill_number, skill_target="None"):  # 角色编号，技能编号，选人（可选）
    """
    use character_skill, by given character_number,skill_number and skill_target if skill_target != "None"

    :param mouse_instance:
    :param character_number:
    :param skill_number:
    :param skill_target:
    :return:
    """
    # reset to zero
    mouse_instance.set_zero()
    time.sleep(0.1)
    # build skill position coordination
    position = (65 + (character_number - 1) * 300 + (skill_number - 1) * 90, 970)
    # click skill
    mouse_instance.touch(position[0], position[1])
    # if the skill has target
    if skill_target != "None":
        position = (300 + (skill_target - 1) * 300, 700)  # 技能选人
        time.sleep(0.2)
        mouse_instance.touch(position[0], position[1])
    time.sleep(2)  # 等待技能动画时间
    # Current_state.WaitForBattleStart()
    print("Character {}'s skill {} has pressed.".format(character_number, skill_number))


def act_and_use_ultimate_skill(mouse_instance, ultimate_skill=1):
    """

    :param mouse_instance:
    :param ultimate_skill:
    :return:
    """
    mouse_instance.touch(1100, 970, 1)  # 点击attack按钮
    time.sleep(2.3)
    mouse_instance.touch(370 + (ultimate_skill - 1) * 230, 250)  # 打手宝具,参数可选1-3号宝具位
    time.sleep(0.2)
    card_indexes = random.sample(range(0, 4), 2)  # 随机两张牌
    mouse_instance.touch(115 + (card_indexes[0]) * 250, 800)
    time.sleep(0.2)
    mouse_instance.touch(115 + (card_indexes[1]) * 250, 800)
    time.sleep(0.2)
    print("act and use ultimate_skill {}".format(ultimate_skill))


def cast_master_skill(mouse_instance, skill_number, swap_target_1=None, swap_target_2=None):
    """
    use master skill. swap target if the skill_number=3,which is "swap team member"

    :param mouse_instance:
    :param skill_number:
    :param swap_target_1:
    :param swap_target_2:
    :return:
    """
    # 御主技能按键
    print('Ready to cast Master skill {}.'.format(skill_number))
    mouse_instance.touch(1130, 525, 1)
    time.sleep(1)
    if skill_number == 1:
        mouse_instance.touch(855, 525)
    if skill_number == 2:
        mouse_instance.touch(855 + 85 * (skill_number - 1), 525)
    if skill_number == 3:  # 换人
        mouse_instance.touch(855 + 85 * (skill_number - 1), 525)
        # select swap_target_1
        mouse_instance.set_zero()
        mouse_instance.touch(110 + (swap_target_1 - 1) * 200, 600)
        time.sleep(0.5)
        # select swap_target_2
        mouse_instance.set_zero()
        mouse_instance.touch(110 + (swap_target_2 - 1) * 200, 600)
        # confirm
        mouse_instance.touch(620, 1050)
    time.sleep(1)
    State.is_ready_to_act()
    print('Complete casting Master skill {}.'.format(skill_number))
    time.sleep(0.5)


def act_and_use_random_cards(mouse_instance):
    """
    :param mouse_instance:
    :return:
    """
    mouse_instance.touch(1100, 970, 1)  # 点击attack按钮
    time.sleep(2)
    card_indexes = random.sample(range(0, 4), 3)  # 随机两张牌
    mouse_instance.touch(115 + (card_indexes[0]) * 250, 800)
    time.sleep(0.2)
    mouse_instance.touch(115 + (card_indexes[1]) * 250, 800)
    time.sleep(0.2)
    mouse_instance.touch(115 + (card_indexes[2]) * 250, 800)
    time.sleep(0.2)
    print("act and use random cards.")


def quit_battle(mouse_instance):
    time.sleep(5)
    battle_finish, still_in_battle = False, False
    while not battle_finish:
        time.sleep(1)
        battle_finish, position_1 = CVModule.match_template('Battle_finish_sign3')
        still_in_battle, position_2 = CVModule.match_template('Attack_button')
        if still_in_battle:
            print("Can not finish battle as scripted, use random cards now.")  # 翻车检测
            act_and_use_random_cards(mouse_instance)
            time.sleep(10)
    if battle_finish:
        print("Battle finished.")
        time.sleep(1)
        retry = 20
        is_battle_exited = False
        while (not is_battle_exited) and retry > 0:
            is_battle_exited, location = CVModule.match_template("LastOrder_sign", show_switch=False)
            mouse_instance.touch(1000, 1100, 2)
            time.sleep(1)
            retry = retry - 1

        print('Quit success')
        return True


if __name__ == '__main__':
    bluemouse = BlueToothMouse.BlueToothMouse(port="com3", config="6sp")
    bluemouse.open()
    bluemouse.set_zero()
    enter_general_battle_procedure(bluemouse, servant="CBA", servant_class="Caster", battle_script="CBA_3T")
    bluemouse.close()
