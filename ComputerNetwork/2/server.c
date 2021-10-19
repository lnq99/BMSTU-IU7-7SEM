#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <signal.h>
#include "sock.h"

#define DIGITS      "0123456789abcde"
#define SWAP(a, b)  { a ^= b; b ^= a; a ^= b; }


int listen_fd;


void perror_exit(const char *err)
{
    close(listen_fd);
    perror(err);
    exit(EXIT_FAILURE);
}

void sigint_handler(int signum)
{
    close(listen_fd);
    printf("\nServer stopped!\n");
    exit(0);
}

// 11(10) -> 13(8) -> '13'
void base_convert(long long unsigned n, unsigned base, char *result)
{
    int l = 0;
    do
    {
        result[l++] = DIGITS[n % base];
        n /= base;
    } while (n);
    result[l] = '\0';

    for (int i = 0; i < l / 2; i++)
        SWAP(result[i], result[l - 1 - i]);
}

void handle_client(char *msg)
{
    printf("Message: %s\n", msg);

    int n = atoi(msg);
    if (n < 0 || (n == 0 && msg[0] != '0'))
        return;

    printf("Base 10: %d\n", n);

    char buf[32];
    int base[] = {2,3,8,16};
    int l = sizeof(base) / sizeof(base[0]);

    for (int i = 0; i < l; i++)
    {
        base_convert(n, base[i], buf);
        printf("Base %2d: %s\n", base[i], buf);
    }
    printf("\n");
}


int main()
{
    listen_fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (listen_fd < 0)
        perror_exit("socket");

    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(SOCK_PORT),
        .sin_addr.s_addr = INADDR_ANY,
    };

    char buf[BUF_SIZE];

    if (bind(listen_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
        perror_exit("bind");

    signal(SIGINT, sigint_handler);

    printf("Server is listening on %s:%d\n", inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));

    struct sockaddr_in client_addr;
    int len;

    while (1)
    {
        if (recvfrom(listen_fd, buf, BUF_SIZE, 0, &client_addr, &len) == -1)
            perror_exit("recvfrom");

        handle_client(buf);
    }

    return 0;
}
