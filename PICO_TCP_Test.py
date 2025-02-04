# 깃허브 파일명은 PICO_TCP_Text.py

import time
import W5500_EVB_PICO_TCP as W5500

class MainFW:
    def __init__(self):
        # I2C 0,1번 초기화

        self.ipAddress = '166.79.26.140'
        self.serverIpAddress = '166.79.26.142'
        self.gateway = '166.79.26.1'
        self.portNumber = 6571
        self.rxMessage = str()

        W5500.init(ipAddress=self.ipAddress, server_ip=self.serverIpAddress, gateway=self.gateway, server_port=self.portNumber)

    def func_1msec(self):
        pass

    def func_10msec(self):
        try:
            message = W5500.readMessage()
            if message is not None:
                self.rxMessage = message.decode('utf-8')
                print(f"[클라이언트] 수신된 메시지: {self.rxMessage}")
                self.sendback()
                self.rxMessage = str()                      # 무한 반복되는 것을 방지하기 위해 변수를 초기화
        except Exception as e:
            print(f"메시지 읽기 오류: {e}")


    def sendback(self):
        try:
            W5500.sendMessage(f"데이터 수신에 성공했습니다. 수신한 데이터는 {self.rxMessage} 입니다.")

        except Exception as e:
            print(f"메시지 전송 오류: {e}")


if __name__ == "__main__":
    cnt_msec = 0
    main = MainFW()

    try:
        while True:
            cnt_msec += 1
            main.func_1msec()

            if not cnt_msec % 10:
                main.func_10msec()

            time.sleep(0.001)
    except KeyboardInterrupt:
        print("프로그램 종료")
