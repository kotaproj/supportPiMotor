import time
# debug
import sys
from icecream import ic

from presenter import PreThread

from led import LedThread
# from buzzer import BuzzerThread
# from servo import ServoThread
# from dcm import DcmThread
# from oled import OledThread

from sw import SwThread
# from httpd import HttpdThread

def main():

    # ic.enable()
    ic.disable()

    # 出力側のスレッド - メッセージを受け取る
    out_ths_led = LedThread()
    out_que_led = out_ths_led.rcv_que
    out_ths_led.start()

    # メッセージの交通整理のスレッド - メッセージの交通整理
    pre_th = PreThread({"led": out_que_led, })
    que_pre = pre_th.rcv_que
    pre_th.start()

    # 入力側のスレッド - メッセージを送信する
    in_ths_sw = SwThread(que_pre)
    in_ths_sw.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("stop")

    # 終了処理
    out_ths_led.stop()
    in_ths_sw.stop()
    return

if __name__ == "__main__":
    main()