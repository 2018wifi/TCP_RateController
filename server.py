import socket

def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", 9000))
    tcp_socket.listen(128)
    print("Listening...")
    reply = "Server Received!"

    client_socket, client_addr = tcp_socket.accept()
    while True:
        mes = client_socket.recv(4096)
        print("Received a packet from ", client_addr, "\tmessage len: ", len(mes))
        client_socket.send(reply.encode())
        # client_socket.close()
    # tcp_socket.close()

if __name__ == "__main__":
    main()
