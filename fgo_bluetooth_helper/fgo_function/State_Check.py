import time

from fgo_bluetooth_helper.util import CVModule


class State:
    @staticmethod
    def is_return_to_menu():
        found, location = CVModule.match_template('Return_button')
        return found

    @staticmethod
    def is_in_friend_menu():
        found, location = CVModule.match_template('friend_sign')
        return found

    @staticmethod
    def is_ready_to_act():
        """
        check if in battle state

        :return: True if in battle, False if not.
        """
        retry = 60
        found, location = CVModule.match_template('Attack_button')
        while retry > 0 and not found:
            time.sleep(1)
            found, location = CVModule.match_template('Attack_button')
            retry = retry - 1
        if not found:
            print("ERROR: can not check if in ready to act states.")
        return found

    @staticmethod
    def is_ready_to_make_experience_card():
        """
        check if is ready to make an experience_card

        :return: True if ready, False if not.
        """
        retry = 60
        found, location = CVModule.match_template('Attack_button')
        while retry > 0 and not found:
            time.sleep(1)
            found, location = CVModule.match_template('Attack_button')
            retry = retry - 1
        if not found:
            print("ERROR: can not check if in ready to act states.")
        return found

    @staticmethod
    def is_ready_to_select_assist_servant():
        """
        check if is ready to select assist servant.

        :return: True if ready, False if not.
        """
        retry = 10
        found = False
        while retry > 0 and not found:
            time.sleep(1)
            found, location = CVModule.match_template('drag_bar')
            retry = retry - 1
        if not found:
            print("ERROR: can not check if in ready to select assist servant states.")
        return found
