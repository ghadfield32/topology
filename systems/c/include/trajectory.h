#ifndef SHAPE_TRAJECTORY_H
#define SHAPE_TRAJECTORY_H
#include <stddef.h>
#include <stdint.h>
/* No allocation crosses this API. Output is assigned only on success. */
typedef struct { uint32_t count, known_confidence; double start, end, mean[3]; } TrajectorySummary;
int trajectory_read(const char *path, TrajectorySummary *out, char *error, size_t error_size);
#endif
