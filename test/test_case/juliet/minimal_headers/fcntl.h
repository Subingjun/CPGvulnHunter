/* Minimal fcntl.h replacement */
#ifndef _FCNTL_H
#define _FCNTL_H

/* File access modes */
#define O_RDONLY 00
#define O_WRONLY 01
#define O_RDWR   02
#define O_CREAT  0100
#define O_EXCL   0200
#define O_TRUNC  01000
#define O_APPEND 02000

/* Function declarations */
int open(const char *pathname, int flags, ...);
int close(int fd);
int fcntl(int fd, int cmd, ...);

#endif /* _FCNTL_H */
