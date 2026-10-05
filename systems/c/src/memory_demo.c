#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
typedef struct { double x,y,z,t; uint32_t frame; } Observation;
int main(void){int x=10;int*p=&x;*p=20;double*heap=malloc(3*sizeof *heap);if(!heap)return 2;for(size_t i=0;i<3;i++)heap[i]=(double)i;uint32_t max=UINT32_MAX;printf("{\"pointer_changed_x\":%d,\"observation_size\":%zu,\"frame_offset\":%zu,\"unsigned_wrap\":%u,\"heap_last\":%.1f}\n",x,sizeof(Observation),offsetof(Observation,frame),max+1,heap[2]);free(heap);return x==20?0:1;}
