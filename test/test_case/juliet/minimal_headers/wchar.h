/* Minimal wchar.h replacement */
#ifndef _WCHAR_H
#define _WCHAR_H

/* Basic wide character type definitions */
typedef int wchar_t;
typedef int wint_t;
typedef struct {
    int __state;
} mbstate_t;

/* Constants */
#define WEOF ((wint_t)-1)
#define NULL ((void*)0)

/* Function declarations */
int wprintf(const wchar_t *format, ...);
int swprintf(wchar_t *wcs, long maxlen, const wchar_t *format, ...);
long wcslen(const wchar_t *s);
wchar_t *wcscpy(wchar_t *dest, const wchar_t *src);
wchar_t *wcsncpy(wchar_t *dest, const wchar_t *src, long n);
int wcscmp(const wchar_t *s1, const wchar_t *s2);
int wcsncmp(const wchar_t *s1, const wchar_t *s2, long n);

#endif /* _WCHAR_H */
