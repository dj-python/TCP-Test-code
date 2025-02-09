# 2025.2.9 통신 성공함.
# 기존 코드는 데이터 전송과 수신이 비동기적으로 실행되기 때문에 타이밍 문제로 실패한 것으로 추정.

import time
import socket
import threading


class TCPReceiver(threading.Thread):

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))  # 포트에서 수신
        self.sock.listen(1)  # 연결 대기
        self.conn = None

    def run(self):
        try:
            print(f"[*] TCP 서버 대기 중... {self.ip}:{self.port}")
            self.conn, addr = self.sock.accept()  # 클라이언트 연결 대기
            print(f"[+] 클라이언트 연결됨: {addr}")

            # 클라이언트로 데이터를 전송
            self.conn.sendall(b'A1B1')
            print(f"[서버] 데이터 전송: A1B1")

            while self._running:
                try:
                    data = self.conn.recv(1024)  # 최대 1024바이트 수신
                    if not data:
                        break
                    print(f"[서버] 수신된 데이터: {data.decode()}")
                except Exception as e:
                    print(f"Error: {str(e)}")
                time.sleep(0.1)
        except Exception as e:
            print(f"TCP 서버 에러: {str(e)}")
        finally:
            if self.conn:
                self.conn.close()
            self.sock.close()

    def stop(self):
        self._running = False
        if self.conn:
            self.conn.close()
        self.sock.close()
        print("[*] TCP 서버 종료")


class MainTest():
    def __init__(self, serverIp, serverPort):  # 수정된 부분
        self.serverIp = serverIp  # 서버의 IP
        self.serverPort = serverPort
        self.serverIpPort = (self.serverIp, self.serverPort)
        self.receiver = TCPReceiver(self.serverIp, self.serverPort)

    def run(self):
        self.receiver.start()
        print("[*] 데이터 수신 시작")
        while self.receiver.is_alive():
            time.sleep(0.1)

    def stop(self):
        if self.receiver:
            self.receiver.stop()
            self.receiver.join()
            print("[*] 데이터 수신 종료")


if __name__ == "__main__":
    server_ip = '127.0.0.1'  # 로컬 호스트 IP 주소 사용
    server_port = 8000

    test = MainTest(server_ip, server_port)

    # 서버 실행
    test.run()

    # 데이터를 수신하다가 일정 시간 후 종료
    time.sleep(3)
    test.stop()
