from queue import Queue
import threading
import time
from time import sleep
import paho.mqtt.client as mqtt
from commands import SUBSC_DICT

# debug
import sys
from icecream import ic

HOST = '192.168.11.12'
PORT = 1883
TOPIC = 'topic_1'


class SubscThread(threading.Thread):
    """
    MQTT - Subscribe管理
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
        def on_connect(client, userdata, flags, respons_code):
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, respons_code)
            client.subscribe(TOPIC)
            return

        def on_message(client, userdata, msg):
            msg_payload = str(msg.payload,'utf-8')
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, msg_payload)
            # 完全一致
            if msg_payload in SUBSC_DICT:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, msg_payload, "SUBSC_DICT")
                self._send_msg(SUBSC_DICT[msg_payload])
                return
            else:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "!!!ERROR!!!")
            return

        client = mqtt.Client(protocol=mqtt.MQTTv311)

        client.on_connect = on_connect
        client.on_message = on_message


        client.connect(HOST, port=PORT, keepalive=60)

        client.loop_forever()
        return

   
    def _send_msg(self, item):
        if self._snd_que is None:
            return
        ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, item)
        self._snd_que.put(item)
        return


def main():
    q = Queue()
    subsc_th = SubscThread(q)
    subsc_th.start()
    time.sleep(10)
    subsc_th.stop()
    
    while True:
        if q.empty():
            print("!!! q.empty !!!")
            break
        print(q.get())
    return

if __name__ == "__main__":
    main()