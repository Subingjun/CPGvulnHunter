/* Minimal sys/socket.h replacement */
#ifndef _SYS_SOCKET_H
#define _SYS_SOCKET_H

/* Socket types */
#define SOCK_STREAM 1
#define SOCK_DGRAM  2

/* Address families */
#define AF_INET  2
#define AF_INET6 10

/* Protocol families */
#define PF_INET  AF_INET
#define PF_INET6 AF_INET6

/* Socket address structure */
struct sockaddr {
    unsigned short sa_family;
    char sa_data[14];
};

struct sockaddr_in {
    short sin_family;
    unsigned short sin_port;
    struct in_addr sin_addr;
    char sin_zero[8];
};

struct in_addr {
    unsigned long s_addr;
};

/* Function declarations */
int socket(int domain, int type, int protocol);
int connect(int sockfd, const struct sockaddr *addr, unsigned int addrlen);
int bind(int sockfd, const struct sockaddr *addr, unsigned int addrlen);
int listen(int sockfd, int backlog);
int accept(int sockfd, struct sockaddr *addr, unsigned int *addrlen);
long send(int sockfd, const void *buf, unsigned long len, int flags);
long recv(int sockfd, void *buf, unsigned long len, int flags);
int shutdown(int sockfd, int how);

#endif /* _SYS_SOCKET_H */
