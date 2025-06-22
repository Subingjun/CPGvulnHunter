/* Minimal arpa/inet.h replacement */
#ifndef _ARPA_INET_H
#define _ARPA_INET_H

/* Include netinet/in.h for address structures */
#include "../netinet/in.h"

/* Function declarations for address conversion */
char *inet_ntoa(struct in_addr in);
int inet_aton(const char *cp, struct in_addr *inp);
unsigned long inet_addr(const char *cp);
const char *inet_ntop(int af, const void *src, char *dst, unsigned int size);
int inet_pton(int af, const char *src, void *dst);

#endif /* _ARPA_INET_H */
