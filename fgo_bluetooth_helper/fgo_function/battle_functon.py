import random

from fgo_bluetooth_helper.fgo_function.State_Check import State
from fgo_bluetooth_helper.util import CVModule
import time


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
    time.sleep(0.2)
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
    print("Character {}'s skill {} has pressed.".format(character_number, skill_number))


def act_and_use_ultimate_skill(mouse_instance, ultimate_skill=1):
    """

    :param mouse_instance:
    :param ultimate_skill:
    :return:
    """
    mouse_instance.touch(1100, 970, 1)  # 点击attack按钮
    time.sleep(1.7)
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


def quit_battle(mouse_instance, repeat_times=1):
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
        retry = 5
        is_battle_exited = False
        while (not is_battle_exited) and retry > 0:
            # TODO: repeat situation
            is_battle_exited, location = CVModule.match_template("LastOrder_sign", show_switch=False)
            mouse_instance.touch(1000, 1100, 2)
            time.sleep(1)
            retry = retry - 1

        print('Quit success')
        return True
