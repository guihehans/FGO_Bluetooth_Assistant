import serial
from serial.serialutil import *

from fgo_bluetooth_helper.util import config_6s


def read_config(config):
    """
    read config file by device type.

    :param config: device type.currently only 6sp supported
    :return:
    """
    if config == "6sp":
        return config_6s.x_range, config_6s.y_range


class BlueToothMouse:
    # mouse serial object.
    serial
    # mouse init coordination set to 0,0
    x_pre, y_pre = 0, 0
    # phone screen pixel range
    x_range, y_range = 0, 0
    # for blueTooth mouse, the sending data is a 8 byte array
    # the first 4 byte is fixed [0x08, 0x00, 0xA1, 0x02]
    # the 5 byte is mouse button, the 6 7 is x,y and 8th is wheel
    bytes = [0x08, 0x00, 0xA1, 0x02, 0, 0, 0, 0]

    def __init__(self, port, config="6sp"):
        self.serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate = 9600  # set baudrate
        self.serial.bytesize = 8  # set bytesize
        self.serial.stopbits = 1  # set stopbits
        self.serial.parity = "N"  # set parity
        # default device model is 6s plus. the x y range is
        # 1334,750
        self.x_range, self.y_range = read_config(config)
        time.sleep(0.3)

    def open(self):
        try:
            if self.get_is_open():
                print("serial is already open.")
            else:
                self.serial.open()  # 打开串口,要找到对的串口号才会成功
                if self.get_is_open():
                    print("serial open success")
                else:
                    print("serial cannot open")
        finally:
            return self.get_is_open()

    def close(self):
        self.serial.close()
        if self.get_is_open():
            print("serial close failed")
        else:
            print("serial close success")

    def get_is_open(self):
        return self.serial.isOpen()

    def set_zero(self):
        """
        set the mouse button to 0,0 point. by default the mouse is located
        in the center (width/2,height/2)
        :returns set the mouse button to 0,0 point. by default the mouse is located
        in the center (width/2,height/2)
        """
        # repeat move cursor toward zero point
        for i in range(12):
            self.serial.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 0, 128, 128, 0]))
        self.x_pre = 0
        self.y_pre = 0

    def click(self):
        """
        send mouse button 1 clicked and release command to simulate click operation
        :return:
        """
        self.serial.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 1, 0, 0, 0]))
        time.sleep(0.05)
        self.serial.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 0, 0, 0, 0]))
        time.sleep(0.3)

    def move(self, x, y, key=0):
        dx = x - self.x_pre
        dy = y - self.y_pre
        X = list()
        Y = list()
        max = 127
        if dx > 0:
            # 向着X正方向移动

            cyc_x = dx // max
            mod_x = dx % max
            for i in range(0, cyc_x):
                X.append(max)
            if mod_x != 0:
                X.append(mod_x)
        else:
            # 向着X负方向移动
            dx = -dx
            cyc_x = dx // max
            mod_x = dx % max
            for i in range(0, cyc_x):
                X.append(256 - max)
            if mod_x != 0:
                X.append(256 - mod_x)
        if dy > 0:
            # 向着Y正方向移动
            cyc_y = dy // max
            mod_y = dy % max
            for i in range(0, cyc_y):
                Y.append(max)
            if mod_y != 0:
                Y.append(mod_y)
        else:
            # 向着Y负方向移动
            dy = -dy
            cyc_y = dy // max
            mod_y = dy % max
            for i in range(0, cyc_y):
                Y.append(256 - max)
            if mod_y != 0:
                Y.append(256 - mod_y)

        if len(X) > len(Y):
            for i in range(len(X) - len(Y)):
                Y.append(0)
        elif len(Y) > len(X):
            for i in range(len(Y) - len(X)):
                X.append(0)

        for i in range(len(X)):
            self.serial.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, key, X[i], Y[i], 0]))
        time.sleep(0.2)
        self.x_pre = x
        self.y_pre = y

    def touch(self, x, y, times=1):
        if self.serial.isOpen():
            for i in range(times):
                self.move(x, y)
                self.click()
        else:
            print("发送失败，串口未打开")

    def drag(self, x, y):
        if self.serial.isOpen():
            self.move(x, y, key=1)
        else:
            print("发送失败，串口未打开")


if __name__ == '__main__':
    mouse = BlueToothMouse(port="com3")
    mouse.open()
    mouse.set_zero()
    mouse.move(800, 1000)
    time.sleep(0.5)
    mouse.close()
