# function dict for register
from script.AOE_3T import aoe_3t_load_parameters, aoe_3t_battle_script
from script.CBA_3T import cba_3t_battle_script, cba_3t_load_parameters
from script.CBA_DOOM_3T import cba_doom_3t_load_parameters, cba_doom_3t_battle_script
from script.CBA_Lancelot_3T import cba_lancelot_3t_battle_script, cba_lancelot_3t_load_parameters


def load_script(script):
    script_dict = {
        "CBA_3T": cba_3t_load_parameters,
        "AOE_3T": aoe_3t_load_parameters,
        "CBA_LANCELOT_3T": cba_lancelot_3t_load_parameters,
        "CBA_DOOM_3T": cba_doom_3t_load_parameters
    }
    method = script_dict.get(script, "")
    if method:
        print("script config:{} loaded,loading parameters now!".format(script))
        result = method()
        return result
    else:
        print(
            "script config:{} cannot be loaded,please check script name and register it in script.script_register.py".format(
                script))


def load_battle_script(script, mouse_instance, repeat_times=1):
    script_dict = {
        "CBA_3T": cba_3t_battle_script,
        "AOE_3T": aoe_3t_battle_script,
        "CBA_LANCELOT_3T": cba_lancelot_3t_battle_script,
        "CBA_DOOM_3T": cba_doom_3t_battle_script
    }
    battle_func = script_dict.get(script, "")
    if battle_func:
        print("script:{} loaded,running battle script now!".format(script))
        battle_func(mouse_instance, repeat_times)
    else:
        print("script:{} cannot be loaded,please check script name and register it in script.script_register.py".format(
            script))
