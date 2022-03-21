import sys
from enum import Enum
from icecream import ic


class RoboMode(Enum):
    ARM = 0
    GEAR = 1
    TIMER = 2

class SystemsData:
    _instance = None
    inited = False

    def __init__(self):
        ic()
        if False == SystemsData.inited:
            ic()
            self.__display = "clear"
            self.__robo_mode = RoboMode.ARM
            self.__dcm_stat = "stop"
            self.__dcm_speed = "fast"
            SystemsData.inited = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    def display(self):
        return self.__display

    @display.setter
    def display(self, display):
        self.__display = display

    def get_next_display(self):
        conv_tbl = {
            "clear":{"next": "ip", "prev": "ip"},
            "ip":{"next": "clear", "prev": "clear"},
        }

        self.__display = conv_tbl[self.__display]["next"]
        return self.__display

    @property
    def robo_mode(self):
        return self.__robo_mode

    @robo_mode.setter
    def robo_mode(self, robo_mode):
        self.__robo_mode = robo_mode

    def update_next_robo_mode(self, dirct=True):
        conv_tbl = {
            RoboMode.ARM:{"next":RoboMode.GEAR},
            RoboMode.GEAR:{"next":RoboMode.TIMER},
            RoboMode.TIMER:{"next":RoboMode.ARM},
        }
        self.__robo_mode = conv_tbl[self.__robo_mode]["next"]
        return


    @property
    def dcm_stat(self):
        return self.__dcm_stat

    @dcm_stat.setter
    def dcm_stat(self, dcm_stat):
        self.__dcm_stat = dcm_stat

    @property
    def dcm_speed(self):
        return self.__dcm_speed

    @dcm_speed.setter
    def dcm_speed(self, dcm_speed):
        self.__dcm_speed = dcm_speed

    def update_next_dcm_speed(self, dirct=True):
        conv_tbl = {
            "slow":{"next": "mid", "prev": "slow"},
            "mid":{"next": "fast", "prev": "slow"},
            "fast":{"next": "fast", "prev": "mid"},
        }
        key = "next" if dirct else "prev"
        self.__dcm_speed = conv_tbl[self.__dcm_speed][key]
        return


def main():
    import time

    sysdat = SystemsData()

    print(sysdat.display)
    sysdat.display = "ip"
    print(sysdat.display)

    return

if __name__ == "__main__":
    main()
