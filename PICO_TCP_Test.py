# 깃허브 파일명은 PICO_TCP_Text.py

import time
import W5500_EVB_PICO_TCP as W5500

class MainFW:
    def __init__(self):
        # I2C 0,1번 초기화

        self.ipAddress = '166.79.26.140'
        self.portNumber = 6571

        self.rxMessage = str()
        self.txMessage = str()

        W5500.init(ipAddress=self.ipAddress, server_ip='166.79.26.142', gateway='166.79.26.1', server_port=6571)

    def func_1msec(self):
        pass

    def func_10msec(self):
        message = W5500.readMessage()
        if message is not None:
            self.rxMessage = message.decode('utf-8')
            print(self.rxMessage)
            self.sendback()

    def sendback(self):
        W5500.sendMessage(f"데이터 수신에 성공했습니다. 수신한 데이터는 {self.rxMessage} 입니다.")

if __name__ == "__main__":
    cnt_msec = 0
    main = MainFW()

    while True:
        cnt_msec += 1
        main.func_1msec()

        if not cnt_msec % 10:
            main.func_10msec()

        time.sleep_ms(1)
