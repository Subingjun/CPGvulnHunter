/* Minimal stddef.h replacement */
#ifndef _STDDEF_H
#define _STDDEF_H

/* Basic type definitions */
typedef long size_t;
typedef long ptrdiff_t;
typedef int wchar_t;

/* Common constants */
#define NULL ((void*)0)
#define offsetof(type, member) ((size_t) &((type *)0)->member)

#endif /* _STDDEF_H */
