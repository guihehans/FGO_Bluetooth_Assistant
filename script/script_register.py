# function dict for register
from script.AOE_3T import AOE_3T
from script.BaseScript import BaseScript
from script.NOMERCY_3T import NOMERCY_3T
from script.WUZANG import WUZANG


def load_script(script) -> BaseScript:
    script_dict = {
        'AOE_3T': AOE_3T,
        'NOMERCY_3T': NOMERCY_3T,
        'WUZANG': WUZANG
    }
    script_instance = script_dict.get(script)
    if script_instance:
        print("script config:{} loaded,loading parameters now!".format(script))
        result = script_instance()
        return result
    else:
        print(
            "script config:{} cannot be loaded,please check script name and register it in script.script_register.py".format(
                script))


if __name__ == '__main__':
    load_script("WUZANG")
