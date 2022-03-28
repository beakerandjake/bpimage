#include <stdio.h>

int add(int lhs, int rhs)
{
    int result = lhs + rhs;
    printf("adding %i and %i result = %i\n", lhs, rhs, result);
    return result;
}