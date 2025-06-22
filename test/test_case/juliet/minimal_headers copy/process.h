/* Minimal process.h replacement */
#ifndef _PROCESS_H
#define _PROCESS_H

/* Spawn modes */
#define P_WAIT    0
#define P_NOWAIT  1
#define P_OVERLAY 2

/* Function declarations */
int spawnl(int mode, const char *path, const char *arg0, ...);
int spawnlp(int mode, const char *file, const char *arg0, ...);
int spawnv(int mode, const char *path, const char * const argv[]);
int spawnvp(int mode, const char *file, const char * const argv[]);

#endif /* _PROCESS_H */
