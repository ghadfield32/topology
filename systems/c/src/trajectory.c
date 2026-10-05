#include "trajectory.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <limits.h>
_Static_assert(sizeof(double)==8 && CHAR_BIT==8 && DBL_MANT_DIG==53, "requires IEEE binary64");
static uint32_t u32(const unsigned char *p) {
    return (uint32_t)p[0] | ((uint32_t)p[1]<<8) | ((uint32_t)p[2]<<16) | ((uint32_t)p[3]<<24);
}
static double f64(const unsigned char *p) {
    uint64_t bits=0; for (unsigned j=0;j<8;j++) bits |= (uint64_t)p[j] << (8*j);
    double x; memcpy(&x,&bits,8); return x;
}
static int fail(FILE *f,char *error,size_t n,const char *message) {
    if(f) { fclose(f); }
    if(error && n) { snprintf(error,n,"%s",message); }
    return 1;
}
int trajectory_read(const char *path,TrajectorySummary *out,char *error,size_t n) {
    if(!path || !out) return fail(NULL,error,n,"null argument");
    FILE *f=fopen(path,"rb"); if(!f)return fail(NULL,error,n,"cannot open input");
    unsigned char h[12],r[48];
    if(fread(h,1,12,f)!=12 || memcmp(h,"SHPTRJ01",8))return fail(f,error,n,"invalid/truncated header");
    uint32_t count=u32(h+8); if(count==0 || count>1000000)return fail(f,error,n,"record count outside bounds");
    TrajectorySummary s={0}; s.count=count;uint32_t prev=0;double time_prev=-1;
    for(uint32_t i=0;i<count;i++) {
        if(fread(r,1,48,f)!=48)return fail(f,error,n,"truncated record");
        uint32_t id=u32(r),flags=u32(r+4);double t=f64(r+8),x=f64(r+16),y=f64(r+24),z=f64(r+32),c=f64(r+40);
        if(flags>1 || !isfinite(c) || (flags==0 && c!=0) || (flags==1 && (c<0 || c>1)))return fail(f,error,n,"invalid confidence");
        if(!isfinite(t)||t<0||t<=time_prev||(i&&id<=prev))return fail(f,error,n,"invalid observation order");
        if(!isfinite(x)||!isfinite(y)||!isfinite(z))return fail(f,error,n,"nonfinite coordinate");
        if(i==0) { s.start=t; }
        s.end=t;s.known_confidence+=flags;
        double v[3]={x,y,z};for(unsigned j=0;j<3;j++){ s.mean[j]+=(v[j]-s.mean[j])/(double)(i+1); if(!isfinite(s.mean[j])) return fail(f,error,n,"summary overflow"); }
        prev=id;time_prev=t;
    }
    if(fgetc(f)!=EOF || ferror(f))return fail(f,error,n,"trailing bytes/read error");
    fclose(f);*out=s;if(error&&n)error[0]='\0';return 0;
}
