#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <stdlib.h>
#include <semaphore.h>

#define PORT 5500//树莓派端口号
#define BUF_LEN 1024//缓冲区大小
#define PC_PORT 3600//填入电脑的端口
char PC_IP[20] = “192.168.1.100”//填入电脑的IP地址

char buf[BUF_LEN];//定义共享的缓冲区
sem_t full;//表示buf是否满
sem_t empty;//表示buf是否空
sem_t mutex;//对buf缓冲区访问的互斥信号量

/*线程函数：接收UDP包*/
void recieve_udp(int fd){
	socklen_t len;//记录cilent_addr结构体的size
	struct sockaddr_in client_addr;  
	int count;

	sem_wait(&empty);//当缓冲区为空的时候工作
	sem_wait(&mutex);//互斥信号量-1
	memset(buf, 0, BUF_LEN);
	len = sizeof(client_addr);
	count = recvfrom(fd, buf, BUF_LEN, 0, (struct sockaddr*)&client_addr, &len);
	if (count == -1) {
		printf("recieve udp-data failed!\n");
		exit(1);
	}
	sem_post(&mutex);//互斥信号量+1
	sem_post(&full);//发出缓冲区为满的提示
	//printf("get a udp package!\n");
}

/*线程函数：从树莓派发送TCP包给电脑*/
void send_udp(struct sockaddr_in server_addr) {
	int server_fd2, ret2;
	server_fd2 = socket(AF_INET, SOCK_STREAM, 0);//建立TCP套接字
	if (server_fd2 < 0) {
		printf("create TCP socket failed!\n");
		exit(1);
	}

	struct sockaddr_in reciever_addr;  //电脑作为接收端的reciever_addr的地址信息
	reciever_addr.sin_family = AF_INET;
	reciever_addr.sin_addr.s_addr = inet_addr(PC_IP);
	reciever_addr.sin_port = htons(PC_PORT);

	if (connect(server_fd2, (struct sockaddr*)&reciever_addr, sizeof(reciever_addr)) < 0)
	{
		printf("Can Not Connect To %s\n", PC_IP);
		exit(1);
	}

	int buff[1024] = "this is a test code\n";//该行最终要注释掉

	sem_wait(&full);//等待缓冲区满
	sem_wait(&mutex);//互斥信号量-1
	int count2;
	count2 = send(server_fd2, buff, 1024, 0);//buff要改成buf
	if (count2 < 0)
	{
		perror("Send package imformation");
		exit(1);
	}
	sem_post(&mutex);//互斥信号量+1
	sem_post(&empty);//发出缓冲区为空的提示
}

int main() {
	printf("Listening...");
	int server_fd, ret;

	server_fd = socket(AF_INET, SOCK_DGRAM, 0);//建立UDP套接字
	if (server_fd < 0) {
		printf("create UDP socket failed!\n");
		return -1;
	}

	struct sockaddr_in server_addr;//记录树莓派接收端的地址信息
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = inet_addr("255.255.255.255");
	server_addr.sin_port = htons(PORT);

	ret = bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
	if (ret < 0) {
		printf("UDP socket bind failed!\n");
		return -1;
	}

	/*多线程操作*/
	pthread_t thrd1_id, thrd2_id;//用于存储两个新线程的ID
	int thrd1, thrd2;
	sem_init(&full, 0, 0); //信号量初始化
	sem_init(&mutex, 0, 1); //信号量初始化
	sem_init(&empty, 0, 1); //信号量初始化

	//创建线程
	thrd1 = pthread_create(&thrd1_id, NULL, recieve_udp, server_fd);
	thrd2 = pthread_create(&thrd2_id, NULL, send_udp, server_addr);
	if (thrd1 != 0) {
		printf("create thread1 failed! \n");
	}
	if (thrd2 != 0) {
		printf("create thread2 failed! \n");
	}

	while (1) {
		pthread_join(thrd1, NULL);
		pthread_join(thrd2, NULL);
	}
	sem_destroy(&sem); //销毁信号量
	return 0;
}