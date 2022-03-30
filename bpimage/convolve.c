#include <stdio.h>

int fn(int *arr, int size)
{
    int i;
    int sum = 0;
    for (i = 0; i < size; i++) 
    {
        sum += arr[i];
    }
    return sum;
}