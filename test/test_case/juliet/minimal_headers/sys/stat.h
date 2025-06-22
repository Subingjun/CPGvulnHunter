/* Minimal sys/stat.h replacement */
#ifndef _SYS_STAT_H
#define _SYS_STAT_H

#include "types.h"

/* File type and mode constants */
#define S_IFMT   0170000
#define S_IFREG  0100000
#define S_IFDIR  0040000
#define S_IFCHR  0020000
#define S_IFBLK  0060000
#define S_IFIFO  0010000
#define S_IFLNK  0120000
#define S_IFSOCK 0140000

/* Permission bits */
#define S_IRWXU 0700
#define S_IRUSR 0400
#define S_IWUSR 0200
#define S_IXUSR 0100
#define S_IRWXG 070
#define S_IRGRP 040
#define S_IWGRP 020
#define S_IXGRP 010
#define S_IRWXO 07
#define S_IROTH 04
#define S_IWOTH 02
#define S_IXOTH 01

struct stat {
    mode_t st_mode;
    off_t st_size;
    long st_mtime;
};

/* Function declarations */
int stat(const char *path, struct stat *buf);
int fstat(int fd, struct stat *buf);
int mkdir(const char *pathname, mode_t mode);

#endif /* _SYS_STAT_H */
