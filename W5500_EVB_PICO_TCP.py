
from machine import Pin, SPI
import time
import network
import socket

tcpSocket = None

# W5x00 chip init
def init(ipAddress: str, gateway : str, server_ip : str, server_port: int) -> None:
    global tcpSocket

    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    eth = network.WIZNET5K(spi, Pin(17), Pin(20))  # spi,cs,reset pin
    eth.active(True)

    # None DHCP, Set static network address
    eth.ifconfig((ipAddress, '255.255.255.0', gateway, '0.0.0.0'))

    # TCP 클라이언트 소켓 생성 및 서버 연결
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.connect((server_ip, server_port))
    tcpSocket.setblocking(False)

    print(f"[*] Connected to TCP Server: {server_ip} : {server_port}")

# 서버로 메시지 전송
def readMessage() -> None:
    global tcpSocket

    try :
        data = tcpSocket.recv(1024)
        if data :
            return data.decode()
    except Exception as e:
        print(f"[-] Receive Error: {str(e)}")
    return None

# 서버로부터 메시지 수신
def sendMessage(msg: str) -> None:
    global tcpSocket

    try :
        # 메시지 전송
        tcpSocket.sendall(msg.encode())
        print(f"[*] Message sent: {msg}")
    except Exception as e:
        print(f"[-] send Error: {str(e)}")


# 소켓 종료
def closeSocket() -> None:
    global tcpSocket

    if tcpSocket:
        tcpSocket.close()
        print("[*] Disconnected from TCP Server")
