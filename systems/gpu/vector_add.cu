// First CUDA lesson: a manufactured exact control, not a throughput benchmark.
#include <cuda_runtime.h>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>
static void checked(cudaError_t e){if(e!=cudaSuccess)throw std::runtime_error(cudaGetErrorString(e));}
struct Buffer{float* p=nullptr; explicit Buffer(size_t n){checked(cudaMalloc(&p,n*sizeof(float)));}~Buffer(){if(p)cudaFree(p);}Buffer(const Buffer&)=delete;Buffer&operator=(const Buffer&)=delete;};
__global__ void add(const float*a,const float*b,float*c,size_t n){size_t i=(size_t)blockIdx.x*blockDim.x+threadIdx.x;if(i<n)c[i]=a[i]+b[i];}
int main(){try{constexpr size_t n=1003;std::vector<float>a(n),b(n),c(n);for(size_t i=0;i<n;i++){a[i]=(float)i;b[i]=2.f;}
Buffer da(n),db(n),dc(n);checked(cudaMemcpy(da.p,a.data(),n*sizeof(float),cudaMemcpyHostToDevice));checked(cudaMemcpy(db.p,b.data(),n*sizeof(float),cudaMemcpyHostToDevice));
add<<<(n+255)/256,256>>>(da.p,db.p,dc.p,n);checked(cudaGetLastError());checked(cudaDeviceSynchronize());checked(cudaMemcpy(c.data(),dc.p,n*sizeof(float),cudaMemcpyDeviceToHost));
for(size_t i=0;i<n;i++)if(c[i]!=a[i]+b[i])throw std::runtime_error("addition mismatch");std::cout<<"1003 manufactured values checked; no benchmark claim\n";return 0;}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
