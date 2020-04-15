import socket
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import time
import datetime

BW = 20
NFFT = int(BW * 3.2)
PORT = 3600                      # 传输端口
TIMEMAX = 10                      # 程序运行时间最大值（单位：秒）


def tcpip():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", PORT))
    tcp_socket.listen(128)
    reply = "Received"
    print("Waiting for connection...")
    client_socket, client_addr = tcp_socket.accept()

    time_count = num = 0
    ts_matrix = []
    time_start = datetime.datetime.now()
    while time_count < TIMEMAX:
        print("Listening...")
        buffer = client_socket.recv(1024)
        if len(buffer) != 1024:
            continue
        time_now = datetime.datetime.now() - time_start  # 时间差
        time_now = time_now.total_seconds()
        num = num + 1  # 计数一秒内的收包量
        print(time_count, '<', num, '>')
        time_sub = int(time_now) - time_count
        if time_sub >= 1:       # 如果到了1秒
            if time_sub > 1:    # 如果在大于1秒内没有收到包
                ts_matrix.append(num)
                for i in range(time_sub - 1):
                    ts_matrix.append(0)
            else:
                if len(ts_matrix) < TIMEMAX + 1:
                    ts_matrix.append(num)
            print(ts_matrix)
            # print(time_count)
            packet_draw(ts_matrix, time_count)    #更新画图
            num = 1
            time_count = int(time_now)

        client_socket.send(reply.encode())
        data = parse(buffer)
        csi = read_csi(data)
        print(csi)
        # client_socket.close()

    plt.close()

def parse(buffer):      # 解析二进制流
    nbyte = int(len(buffer))        # 字节数
    data = np.array(struct.unpack(nbyte * "B", buffer), dtype=np.uint8)

    return data


def read_csi(data):     # 提取CSI信息，并转换成矩阵
    csi = np.zeros(NFFT, dtype=np.complex)
    sourceData = data[18:274]
    sourceData.dtype = np.int16
    csi_data = sourceData.reshape(-1, 2).tolist()

    i = 0
    for x in csi_data:
        csi[i] = np.complex(x[0], x[1])
        i += 1

    return csi


def packet_draw(ts_matrix, time):       # 根据矩阵画图
    x = [i + 1 for i in range(len(ts_matrix))]
    bn = plt.bar(x, ts_matrix, color = ['bisque','darkorange','burlywood', 'darkgoldenrod'])
    ax = plt.gca()
    plt.ylabel('number of packet')
    plt.xlabel('time')
    for b in bn:  # 在柱形上显示对应数字
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), b.get_height(), fontsize=7, ha='center', va='bottom')
    plt.draw()
    if time != TIMEMAX - 1:
        plt.pause(0.001)
    else:
        plt.savefig('test_picture')     # 保存最终TIMEMAX秒内的图片
        plt.show()      # 用show保留窗口，直到手动关闭(如果不需要保留显示可注释）



if __name__ == "__main__":
    tcpip()
