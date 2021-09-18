import time

from fgo_bluetooth_helper.fgo_function.State_Check import State
from fgo_bluetooth_helper.fgo_function.battle_functon import character_skill, act_and_use_ultimate_skill, \
    cast_master_skill, \
    quit_battle

SERVANT_CONFIG_DATA = {
    "servant": "CBA",
    "servant_class": "Caster",
    "servant_class_location_error": (-20, 65),
    "servant_location_error": (-20, 250)
}


def get_parameters():
    return SERVANT_CONFIG_DATA


def run_battle_script(mouse_instance, repeat_times=1):
    # 鼠标复位,防止误差累积
    mouse_instance.set_zero()
    # 等待战斗开始
    # 判断是否进入战斗界面
    State.is_ready_to_act()
    time.sleep(3)  # 等待6秒，因为礼装效果掉落暴击星会耗时
    # Turn 1
    print("Turn 1")
    character_skill(mouse_instance=mouse_instance, character_number=1, skill_number=3)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=1, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=2, skill_target=1)
    # 换人
    cast_master_skill(mouse_instance=mouse_instance, skill_number=3, swap_target_1=2, swap_target_2=4)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=1, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=1, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=3, skill_target=1)
    # 1号角色使用宝具
    act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)

    # 鼠标复位,防止误差累积
    mouse_instance.set_zero()
    State.is_ready_to_act()
    # Turn 2
    print("Turn 2")
    act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)

    # 鼠标复位,防止误差累积
    mouse_instance.set_zero()
    State.is_ready_to_act()
    # Turn3
    print("Turn 3")

    character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=3, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=2)
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=2)
    cast_master_skill(mouse_instance=mouse_instance, skill_number=1)
    act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)
    # quit battle
    quit_battle(mouse_instance, repeat_times=repeat_times)
