/* Minimal stdio.h replacement */
#ifndef _STDIO_H
#define _STDIO_H

/* Basic type definitions */
typedef struct _FILE FILE;
typedef long size_t;

/* Common constants */
#define NULL ((void*)0)
#define EOF (-1)

/* Function declarations (empty implementations) */
int printf(const char *format, ...);
int sprintf(char *str, const char *format, ...);
int fprintf(FILE *stream, const char *format, ...);
FILE *fopen(const char *filename, const char *mode);
int fclose(FILE *stream);
int fflush(FILE *stream);

extern FILE *stdin;
extern FILE *stdout;
extern FILE *stderr;

#endif /* _STDIO_H */
