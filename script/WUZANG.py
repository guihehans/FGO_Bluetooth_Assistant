import time

from fgo_bluetooth_helper.fgo_function.State_Check import State
from fgo_bluetooth_helper.fgo_function.battle_functon import character_skill, act_and_use_ultimate_skill, \
    cast_master_skill, quit_battle
from script.BaseScript import BaseScript


class WUZANG(BaseScript):
    def __init__(self):
        self.SERVANT_CONFIG_DATA = {
            "servant": "CABER",
            "servant_class": "Caster",
            "servant_class_location_error": (-20, 65),
            "servant_location_error": (-20, 240)
        }

    def get_parameters(self):
        return self.SERVANT_CONFIG_DATA

    def run_battle_script(self, mouse_instance, repeat_times=1):
        # 鼠标复位,防止误差累积
        mouse_instance.set_zero()
        # 等待战斗开始
        # 判断是否进入战斗界面
        State.is_ready_to_act()
        time.sleep(3)  # 等待6秒，因为礼装效果掉落暴击星会耗时
        # Turn 1
        print("Turn 1")
        # caber in pos 2, cast skill 1,2,3 to pos 3
        character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=1)
        character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=2, skill_target=1)
        character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=3, skill_target=1)
        # caber 2 in pos 2, cast skill 1,2,3 to pos 3 again
        character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=1)
        character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=2, skill_target=1)
        character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=3, skill_target=1)
        # 武藏2技能
        character_skill(mouse_instance=mouse_instance, character_number=1, skill_number=2)
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
        # 泳装加buff 充能 3号武藏
        # cast_master_skill(mouse_instance=mouse_instance, skill_number=1, swap_target_1=1)
        cast_master_skill(mouse_instance=mouse_instance, skill_number=4, swap_target_1=1, swap_target_2=5,
                          othersuite=True)
        # 武藏3技能
        character_skill(mouse_instance=mouse_instance, character_number=1, skill_number=3)
        act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)
        # quit battle
        quit_battle(mouse_instance, repeat_times=repeat_times)
