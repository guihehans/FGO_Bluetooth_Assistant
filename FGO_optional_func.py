# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 20:17:33 2020

@author: McLaren
"""

import sys
sys.path.append(r'C:\Users\guihehans\PycharmProjects\fgo_origin_1')
import Serial
import Base_func
import time

#无限池抽取函数
def InfinatePool():
    Serial.port_open('com3')
    Serial.mouse_set_zero()
    Serial.mouse_move((320,360))
    for i in range(100):
        Serial.mouse_click()

#友情池抽取函数
def FriendPointSummon():
    Serial.port_open('com3')
    time.sleep(0.5)
    
    Serial.mouse_set_zero()

    Serial.touch(540,472)

    flag=True
    while flag:

        Serial.touch(707+500,480+300,2)
        time.sleep(1)
        Serial.touch(647+500,570+300,8)

#搓丸子        
def MakeCraftEssenceEXCard():
    Serial.port_open('com3')
    Serial.mouse_set_zero()
    
    while True:
        Serial.touch(720,280)
        time.sleep(0.5)
        Serial.mouse_swipe((150,250),(600,600),0.5)
        Serial.touch(990,570,3)
        time.sleep(0.5)
        Serial.touch(720,507,10)

if __name__=='__main__':
    FriendPointSummon()

    # from pynput import keyboard
    #
    # from pynput import keyboard
    #
    # # The event listener will be running in this block
    # with keyboard.Events() as events:
    #     for event in events:
    #         if event.key == keyboard.Key.esc:
    #             FriendPointSummon()
    #         else:
    #             print('Received event {}'.format(event))