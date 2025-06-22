/* Minimal netinet/in.h replacement */
#ifndef _NETINET_IN_H
#define _NETINET_IN_H

/* Internet address structure */
struct in_addr {
    unsigned long s_addr;
};

struct sockaddr_in {
    short sin_family;
    unsigned short sin_port;
    struct in_addr sin_addr;
    char sin_zero[8];
};

struct in6_addr {
    unsigned char s6_addr[16];
};

struct sockaddr_in6 {
    unsigned short sin6_family;
    unsigned short sin6_port;
    unsigned long sin6_flowinfo;
    struct in6_addr sin6_addr;
    unsigned long sin6_scope_id;
};

/* Constants */
#define INADDR_ANY        0x00000000
#define INADDR_BROADCAST  0xffffffff
#define INADDR_NONE       0xffffffff
#define INADDR_LOOPBACK   0x7f000001

/* Network byte order conversion */
unsigned short htons(unsigned short hostshort);
unsigned long htonl(unsigned long hostlong);
unsigned short ntohs(unsigned short netshort);
unsigned long ntohl(unsigned long netlong);

#endif /* _NETINET_IN_H */
