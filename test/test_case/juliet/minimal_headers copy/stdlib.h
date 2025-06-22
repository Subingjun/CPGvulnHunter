/* Minimal stdlib.h replacement */
#ifndef _STDLIB_H
#define _STDLIB_H

/* Basic type definitions */
typedef long size_t;
typedef unsigned long size_t;

/* Common constants */
#define NULL ((void*)0)
#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1

/* Function declarations */
void *malloc(size_t size);
void free(void *ptr);
void *calloc(size_t nmemb, size_t size);
void *realloc(void *ptr, size_t size);
void exit(int status);
int atoi(const char *nptr);
long atol(const char *nptr);

#endif /* _STDLIB_H */
