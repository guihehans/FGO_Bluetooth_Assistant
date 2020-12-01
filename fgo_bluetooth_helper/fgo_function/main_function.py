from fgo_bluetooth_helper.fgo_function.battle import BattleHelper

if __name__ == '__main__':
    battle = BattleHelper(port="com3", script="CBA_DOOM_3T")
    # battle.enter_general_battle_procedure()
    battle.enter_repeated_battle_procedure(repeat_times=30)
