import sys
from icecream import ic

class SystemsData:
    _instance = None
    inited = False

    def __init__(self):
        ic()
        if False == SystemsData.inited:
            ic()
            self.__display = "clear"
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


def main():
    import time

    sysdat = SystemsData()

    print(sysdat.display)
    sysdat.display = "ip"
    print(sysdat.display)

    return

if __name__ == "__main__":
    main()