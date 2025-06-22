/* Minimal unistd.h replacement */
#ifndef _UNISTD_H
#define _UNISTD_H

/* Basic type definitions */
typedef int pid_t;
typedef unsigned int uid_t;
typedef unsigned int gid_t;
typedef long ssize_t;
typedef unsigned long size_t;

/* Constants */
#define NULL ((void*)0)
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2

/* Function declarations */
int execl(const char *path, const char *arg, ...);
int execlp(const char *file, const char *arg, ...);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
pid_t fork(void);
int pipe(int pipefd[2]);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
int close(int fd);
int dup2(int oldfd, int newfd);
uid_t getuid(void);
gid_t getgid(void);
int chdir(const char *path);
char *getcwd(char *buf, size_t size);
unsigned int sleep(unsigned int seconds);

#endif /* _UNISTD_H */
