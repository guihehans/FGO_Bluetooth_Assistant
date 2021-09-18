class BaseScript:
    def __init__(self):
        self.SERVANT_CONFIG_DATA = {
            "servant": "CBA",
            "servant_class": "Caster",
            "servant_class_location_error": (-20, 65),
            "servant_location_error": (-20, 250)
        }

    def get_parameters(self) -> dict:
        return self.SERVANT_CONFIG_DATA

    def run_battle_script(self, mouse_instance, repeat_times=1):
        print("This is an abstract method. No script instance found! ")
        pass
