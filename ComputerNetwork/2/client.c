#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include "sock.h"

int sock_fd;

void perror_exit(const char *err)
{
    close(sock_fd);
    perror(err);
    exit(EXIT_FAILURE);
}

void sigint_handler(int signum)
{
    close(sock_fd);
    printf("\nClient stopped!\n");
    exit(0);
}

int main()
{
    sock_fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock_fd < 0)
        perror_exit("socket");

    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(SOCK_PORT),
        .sin_addr.s_addr = INADDR_ANY,
    };

    int len = sizeof(addr);

    signal(SIGINT, sigint_handler);

    char buf[BUF_SIZE];

    while (1)
    {
        printf("Input message:\t");
        scanf("%16s", buf);

        if (sendto(sock_fd, buf, strlen(buf)+1, 0, (struct sockaddr *)&addr, len) == -1)
            perror_exit("sendto");
    }

    return 0;
}
