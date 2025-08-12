#ifndef TOYOS_TYPES_H
#define TOYOS_TYPES_H

typedef unsigned int uint32_t;
typedef unsigned long uint64_t;

_Static_assert(sizeof(uint32_t) == 4, "Problem with type definition!");
_Static_assert(sizeof(uint64_t) == 8, "Problem with type definition!");

typedef uint64_t addr_t;

#endif /* TOYOS_TYPES_H */
