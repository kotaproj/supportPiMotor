import sys
from icecream import ic
import pigpio

class SysPig:
    _instance = None
    inited = False

    def __init__(self):
        ic()
        if False == SysPig.inited:
            ic()
            self.__borrow_count = 0
            self.__pi = None
            SysPig.inited = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def borrow_pigpio(self):
        ic()
        if 0 == self.__borrow_count:
            self.__pi = pigpio.pi()
        self.__borrow_count += 1
        return self.__pi
    
    def release_pigpio(self):
        ic()
        if self.__borrow_count <= 0:
            ic.enable()
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "ERROR!")
            return
        self.__borrow_count -= 1
        if 0 == self.__borrow_count:
            self.__pi.stop()
        return

def main():

    syspig = SysPig()
    
    for _ in range(5):
        pi = syspig.borrow_pigpio()
        ic(pi, id(pi))

    for _ in range(8):
        syspig.release_pigpio()

    return

if __name__ == "__main__":
    main()
