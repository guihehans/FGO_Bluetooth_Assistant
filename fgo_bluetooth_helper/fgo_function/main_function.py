from fgo_bluetooth_helper.fgo_function.battle import BattleHelper

if __name__ == '__main__':
    battle = BattleHelper(port="com3", script="CBA_LANCELOT_3T")
    battle.enter_repeated_battle_procedure(repeat_times=60)
