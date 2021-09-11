from queue import Queue
import threading
import time
from time import sleep
# import paho.mqtt.client as mqtt
from commands import SUBSC_DICT
from bottle import route,run,get,request

# debug
import sys
from icecream import ic

HOST = '0.0.0.0'
PORT = 8080
HTML = """
<form action="/pim" method="GET">
    command: <input name="cmd" type="text" />
    <input value="send" type="submit" />
</form>
<ul>
    <li>pim:led_no1_on</li>
    <li>pim:led_no1_off</li>
    <li>pim:led_no2_on</li>
    <li>pim:led_no2_off</li>
    <li>pim:buzzer_short</li>
    <li>pim:buzzer_long</li>
    <li>pim:motor_forward</li>
    <li>pim:motor_back</li>
    <li>pim:motor_stop</li>
    <li>pim:motor_left</li>
    <li>pim:motor_right</li>
    <li>pim:servo_left_raise</li>
    <li>pim:servo_left_down</li>
    <li>pim:servo_right_raise</li>
    <li>pim:servo_right_down</li>
    <li>pim:servo_left_swing</li>
    <li>pim:servo_right_swing</li>
    <li>pim:oled_ip</li>
    <li>pim:oled_clear</li>
</ul>
"""


class HttpdThread(threading.Thread):
    """
    Bottle - Httpd管理
    """
    def __init__(self, snd_que=None):
        ic()
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)
        self._snd_que = snd_que
        return


    def stop(self):
        ic()
        self.stop_event.set()
        return


    def run(self):
        ic()

        # 初期表示
        @route("/rc")
        def init():
            return HTML

        @route("/pim", method="GET")
        def disp1():
            str_cmd = request.query.get("cmd")

            if str_cmd in SUBSC_DICT:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, str_cmd, "SUBSC_DICT")
                self._send_msg(SUBSC_DICT[str_cmd])
                return "The command has been processed. - [{}]".format(str_cmd)

            return "No registered commands. - [{}]".format(str_cmd)


        run(host=HOST, port=PORT)
        return

   
    def _send_msg(self, item):
        if self._snd_que is None:
            return
        ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, item)
        self._snd_que.put(item)
        return


def main():
    q = Queue()
    httpd_th = HttpdThread(q)
    httpd_th.start()
    time.sleep(60*5)
    httpd_th.stop()
    
    while True:
        if q.empty():
            print("!!! q.empty !!!")
            break
        print(q.get())
    return

if __name__ == "__main__":
    main()
