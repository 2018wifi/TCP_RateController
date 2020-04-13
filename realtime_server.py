import socket
import struct
import numpy as np

BW = 20
NFFT = int(BW * 3.2)
PORT = 3600                       # 传输端口

def tcpip():    
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", PORT))
    tcp_socket.listen(128)
    reply = "Received"
    print("Waiting for connection...")
    client_socket, client_addr = tcp_socket.accept()

    while True:
        print("Listening...")
        buffer = client_socket.recv(1024)
        if(len(buffer) != 1024):
            continue
        print(buffer)
        client_socket.send(reply.encode())
        data = parse(buffer)
        csi = read_csi(data)
        print(csi)
        #client_socket.close()

def parse(buffer):      # 解析二进制流
    nbyte = int(len(buffer))        # 字节数
    data = np.array(struct.unpack(nbyte * "B", buffer), dtype=np.uint8)

    return data


def read_csi(data):     # 提取CSI信息，并转换成矩阵
    csi = np.zeros(NFFT, dtype=np.complex)
    sourceData = data[18:274]      # 加上限
    sourceData.dtype = np.int16
    csi_data = sourceData.reshape(-1, 2).tolist()

    i = 0
    for x in csi_data:
        csi[i] = np.complex(x[0], x[1])
        i += 1

    return csi


if __name__ == "__main__":
    tcpip()

