/* Minimal io.h replacement */
#ifndef _IO_H
#define _IO_H

/* Function declarations for file I/O */
int open(const char *pathname, int flags, ...);
int close(int fd);
long read(int fd, void *buf, unsigned long count);
long write(int fd, const void *buf, unsigned long count);
long lseek(int fd, long offset, int whence);

/* Constants for lseek */
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#endif /* _IO_H */
