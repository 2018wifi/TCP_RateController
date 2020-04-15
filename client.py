import time
import socket

RATE = 50  # 发包速率，单位：包/秒
SERVER_IP = '192.168.0.100'
PORT = 8000
BYTE_NUM = 500   # 发送内容的字节长度(0...1472)

def udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    mes = ""                            # 构造一定字节的内容
    for i in range(0, BYTE_NUM + 1):
        mes += str(i)

    ts = int(time.time() * 1000)
    interval = 1000 / float(RATE)
    print("Initial ts:", ts)
    print("Interval: ", interval, "ms")

    while True:
        if int(time.time() * 1000) < ts + interval:
            continue
        else:
            ts += interval

        udp_socket.sendto(mes.encode(), (SERVER_IP, PORT))
        print("Have sent a packet to ", SERVER_IP, "\tts: ", int(time.time() * 1000))

def tcpip():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ip = SERVER_IP
    tcp_port = PORT
    tcp_socket.connect((tcp_ip, tcp_port))

    mes = "Something will be sent to server."

    ts = int(time.time() * 1000)
    interval = 1000 / float(RATE)
    print("Initial ts:", ts)
    print("Interval: ", interval, "ms")

    while True:
        if int(time.time() * 1000) < ts + interval:
            continue
        else:
            ts += interval

        tcp_socket.send(mes.encode())
        reply = tcp_socket.recv(4096)
        print("Have sent a packet to ", SERVER_IP, "\tReply: ", reply.decode(), "ts: ", int(time.time() * 1000))
    # tcp_socket.close()

if __name__ == '__main__':
    udp()