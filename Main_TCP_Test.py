# 이 코드는 TCP 서버 테스트 코드임

import time
import sys
import socket
import threading

class TCPReceiver(threading.Thread):

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('166.79.26.142', self.port))                     # 12345 포트에서 수신
        self.sock.listen(1)                                              # 연결 대기
        self.conn = None

    def run(self):
        try:
            print(f"[*] TCP 서버 대기 중... {self.ip}:{self.port}")
            self.conn, addr = self.sock.accept()
            print(f"[+] 클라이언트 연결됨: {addr}")
            while self._running:
                try :
                    data = self.conn.recv(1024)                           # 최대 1024바이트 수신
                    if not data :
                        break
                    print(f"[서버] 수신된 데이터: {data.decode()}")
                except Exception as e :
                    print(f"Error: {str(e)}")
                time.sleep(0.1)
        except Exception as e :
            print(f"TCP 서버 에러: {str(e)}")
        finally :
            if self.conn:
                self.conn.close()
            self.sock.close()

    def stop(self):
        self._running = False
        if self.conn:
            self.conn.close()
        self.sock.close()
        print("[*] TCP 서버 종료")

    def send_data(self, target: tuple, msg: str) -> None:
        try :
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           # 서버 소켓과 데이터 전송 소켓을 분리하기 위해 별도 변수 사용.
            temp_sock.connect(target)
            temp_sock.sendall(msg.encode())
            temp_sock.close()
            print(f"[+] 데이터 전송 완료: {msg}")
        except Exception as e :
            print(f"Error : {str(e)}")

class MainTest():
    def __init__(self):
        self.sensorID = 'A1B1'
        self.serverIp = '166.79.26.142'                                      # Sever(나)의 IP가 들어가야 함. 클라이언트도 서버 IP와 포트번호 사용하여 연결
        self.serverIpPort = (self.serverIp, 6571)
        self.writeCardIpPort = ('166.79.26.140', 6571)

    def sending(self):
        sender = TCPReceiver(self.serverIp, 6571)
        sender.send_data(self.writeCardIpPort, self.sensorID)
        time.sleep(0.1)

    def receiving_and_printing(self):
        receiver = TCPReceiver(self.serverIp, 6571)
        receiver.start()
        print("[*] 데이터 수신 시작")
        while True:
            try:
                if receiver.conn:
                    data = receiver.conn.recv(1024)
                    if data:
                        print(f"[+] 수신된 데이터: {data.decode()}")
            except Exception as e:
                print(f"Error: {str(e)}")
            time.sleep(0.1)

    def stop_receiving(self, receiver):
        receiver.stop()
        print("[*] 데이터 수신 종료")

    def print_received_data(self):
        receiver = TCPReceiver(self.serverIp, 6571)
        receiver.start()
        print("[*] 데이터 수신 시작")
        while True:
            try:
                if receiver.conn:
                    data = receiver.conn.recv(1024)
                    if data :
                        print(f"[+] 수신된 데이터 : {data.decode()}")
            except Exception as e:
                print(f"Error: {str(e)}")
            time.sleep(0.1)



if __name__ == "__main__":
    test = MainTest()

    # 데이터 전송
    test.sending()

    # 데이터 수신
    receiver = test.receiving_and_printing()

    # 데이터를 수신하다가 일정 시간 후 종료
    time.sleep(3)
    test.stop_receiving(receiver)

    # 수신된 데이터 출력
    test.print_received_data()
