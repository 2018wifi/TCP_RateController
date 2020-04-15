import time
import socket

CLIENT_IP = ""
PORT = 8000

def udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((CLIENT_IP, PORT))

    count = 0
    time1 = int(time.time())
    while True:
        if int(time.time()) >= time1 + 1:    # 过了一秒
            print("Time: ", int(time.time()), "Packet num: ", count)
            count = 0
            time1 = int(time.time())
        else:
            count += 1
        mes = udp_socket.recv(2048)
        # print(mes.decode(), count)
    # udp_socket.close()

def tcpip():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", PORT))
    tcp_socket.listen(128)
    print("Listening...")
    reply = "Server Received!"

    client_socket, client_addr = tcp_socket.accept()

    while True:
        mes = client_socket.recv(4096)
        print("Received a packet from ", client_addr, "\tmessage len: ", len(mes))
        # client_socket.send(reply.encode())
        # client_socket.close()
    # tcp_socket.close()


if __name__ == "__main__":
    udp()
