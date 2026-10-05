#include "trajectory.h"
#include <stdio.h>
int main(int argc,char **argv) {
    if(argc!=2){fprintf(stderr,"usage: trajectory_reader FILE\n");return 2;}
    TrajectorySummary s;char error[256];
    if(trajectory_read(argv[1],&s,error,sizeof error)){fprintf(stderr,"invalid: %s\n",error);return 2;}
    printf("{\"count\":%u,\"known_confidence\":%u,\"start\":%.17g,\"end\":%.17g,\"mean\":[%.17g,%.17g,%.17g]}\n",
        s.count,s.known_confidence,s.start,s.end,s.mean[0],s.mean[1],s.mean[2]);return 0;
}
