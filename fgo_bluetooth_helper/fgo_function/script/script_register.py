# function dict for register
from fgo_bluetooth_helper.fgo_function.script.CBA_3T import cba_3t_battle_script, cba_3t_load_parameters
from fgo_bluetooth_helper.fgo_function.script.AOE_3T import aoe_3t_load_parameters, aoe_3t_battle_script


def load_script(script):
    script_dict = {
        "CBA_3T": cba_3t_load_parameters,
        "AOE_3T": aoe_3t_load_parameters
    }
    method = script_dict.get(script, "")
    if method:
        print("script:{} loaded,loading parameters now!".format(script))
        result = method()
        return result
    else:
        print("script:{} cannot be loaded,please check script name and register it in script.script_register.py".format(
            script))


def load_battle_script(script, mouse_instance, repeat_times=1):
    script_dict = {
        "CBA_3T": cba_3t_battle_script,
        "AOE_3T": aoe_3t_battle_script
    }
    battle_func = script_dict.get(script, "")
    if battle_func:
        print("script:{} loaded,running battle script now!".format(script))
        battle_func(mouse_instance,repeat_times)
    else:
        print("script:{} cannot be loaded,please check script name and register it in script.script_register.py".format(
            script))
