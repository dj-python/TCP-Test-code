# 2025.2.7 시분할 루프에서 스레드 사용하는 것으로 수정.
# 2025.2.7 Loopback 수정하는 것으로 수정함.

import time
import threading
import W5500_EVB_PICO_TCP as W5500

class MainFW(threading.Thread):
    def __init__(self, run_duration):
        super().__init__()
        self.ipAddress = '127.0.0.1'  # loopback 주소로 변경
        self.serverIpAddress = '127.0.0.1'  # loopback 주소로 변경
        self.gateway = '127.0.0.1'  # loopback 주소로 변경
        self.portNumber = 8000
        self.rxMessage = str()
        self.run_duration = run_duration  # 실행 시간 추가

        W5500.init(ipAddress=self.ipAddress, server_ip=self.serverIpAddress, gateway=self.gateway,
                   server_port=self.portNumber)

        self.running = True

    def run(self):
        start_time = time.time()
        while self.running and (time.time() - start_time < self.run_duration):
            try:
                message = W5500.readMessage()
                if message is not None:
                    self.rxMessage = message.decode('utf-8')
                    print(f"[클라이언트] 수신된 메시지: {self.rxMessage}")
                    self.sendback()
                    self.rxMessage = str()  # 무한 반복되는 것을 방지하기 위해 변수를 초기화
            except Exception as e:
                print(f"메시지 읽기 오류: {e}")
            time.sleep(0.01)  # 10ms 대기

    def func_1msec(self):
        # 필요한 기능 구현
        pass

    def sendback(self):
        try:
            W5500.sendMessage(f"데이터 수신에 성공했습니다. 수신한 데이터는 {self.rxMessage} 입니다.")
        except Exception as e:
            print(f"메시지 전송 오류: {e}")

    def stop(self):
        self.running = False

if __name__ == "__main__":
    run_duration = 10  # 실행 시간 (초 단위)
    main = MainFW(run_duration)
    main.start()

    try:
        start_time = time.time()
        while time.time() - start_time < run_duration:
            main.func_1msec()
            time.sleep(0.001)  # 1ms 대기
    except KeyboardInterrupt:
        print("프로그램 종료")
    finally:
        main.stop()
        main.join()
