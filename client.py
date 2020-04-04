import time
import socket

rate = 45  # 发包速率，单位：包/秒
server_ip = "192.168.0.105"

def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ip = server_ip
    tcp_port = 9000
    tcp_socket.connect((tcp_ip, tcp_port))

    mes = "Something will be sent to server."

    ts = int(time.time() * 1000)
    interval = 1000 / float(rate)
    print("Initial ts:", ts)
    print("Interval: ", interval, "ms")

    while True:
        if int(time.time() * 1000) < ts + interval:
            continue
        else:
            ts += interval

        tcp_socket.send(mes.encode())
        reply = tcp_socket.recv(4096)
        print("Have sent a packet to ", server_ip, "\tReply: ", reply.decode(), "ts: ", int(time.time() * 1000))
    # tcp_socket.close()

if __name__ == '__main__':
    main()