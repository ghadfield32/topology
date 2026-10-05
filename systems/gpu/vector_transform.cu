// CUDA counterpart of y=1.25*x+0.5. Input is finite whitespace-separated floats.
#include <cuda_runtime.h>
#include <cmath>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
__global__ void transform(const float* x,float* y,int n){int i=blockIdx.x*blockDim.x+threadIdx.x;if(i<n)y[i]=1.25f*x[i]+0.5f;}
void check(cudaError_t e){if(e!=cudaSuccess)throw std::runtime_error(cudaGetErrorString(e));}
struct Buffer{float* p=nullptr;explicit Buffer(size_t n){check(cudaMalloc(&p,n*sizeof(float)));}~Buffer(){if(p)cudaFree(p);}Buffer(const Buffer&)=delete;Buffer&operator=(const Buffer&)=delete;};
int main(int argc,char**argv){try{if(argc!=2)throw std::invalid_argument("usage: vector_transform finite-values.txt");std::ifstream f(argv[1]);if(!f)throw std::runtime_error("cannot open input");std::vector<float>x;float v;while(f>>v){if(!std::isfinite(v)||x.size()>=10000000)throw std::invalid_argument("invalid or oversized input");x.push_back(v);}if(!f.eof()||x.empty())throw std::invalid_argument("malformed/empty input");Buffer a(x.size()),b(x.size());check(cudaMemcpy(a.p,x.data(),x.size()*sizeof(float),cudaMemcpyHostToDevice));transform<<<(x.size()+255)/256,256>>>(a.p,b.p,static_cast<int>(x.size()));check(cudaGetLastError());check(cudaDeviceSynchronize());std::vector<float>y(x.size());check(cudaMemcpy(y.data(),b.p,y.size()*sizeof(float),cudaMemcpyDeviceToHost));double err=0;for(size_t i=0;i<x.size();i++)err=std::max(err,std::abs(double(y[i])-(1.25*double(x[i])+.5)));std::cout<<"{\"count\":"<<x.size()<<",\"max_abs_error\":"<<err<<"}\n";return err<1e-5?0:1;}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
