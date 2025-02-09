# 2025.2.9 통신 성공함.
# 기존 코드는 데이터 전송과 수신이 비동기적으로 실행되기 때문에 타이밍 문제로 실패한 것으로 추정.

import socket
import time

class TCPClient:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
        print(f"[*] 서버에 연결됨: {self.server_ip}:{self.server_port}")

    def receive_data(self):
        try:
            data = self.sock.recv(1024)  # 최대 1024바이트 수신
            print(f"[클라이언트] 수신된 데이터: {data.decode()}")
            if data.decode() == 'A1B1':
                self.send_response(data.decode())
        except Exception as e:
            print(f"Error: {str(e)}")

    def send_response(self, received_data):
        response = f"데이터 수신에 성공했습니다. 수신한 데이터는 '{received_data}' 입니다"
        try:
            self.sock.sendall(response.encode())
            print(f"[클라이언트] 응답 메시지 전송: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def close_connection(self):
        self.sock.close()
        print("[*] 서버 연결 종료")

if __name__ == "__main__":
    server_ip = '127.0.0.1'  # 로컬 호스트 IP 주소 사용
    server_port = 8000

    client = TCPClient(server_ip, server_port)

    # 서버로부터 데이터 수신 및 응답
    client.receive_data()

    # 연결 종료
    time.sleep(1)
    client.close_connection()
