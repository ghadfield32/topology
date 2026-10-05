#include "shape.hpp"
#include <iomanip>
#include <iostream>
#include <string>
#include <stdexcept>
#include <cmath>
double number(const char* s){std::size_t n;double v=std::stod(s,&n);if(n!=std::string(s).size()||!std::isfinite(v))throw std::invalid_argument("invalid numeric input");return v;}
int main(int argc,char **argv){try{
 if(argc!=11)throw std::invalid_argument("usage: trajectory_cpp t0 x y z vx vy vz gravity dt count");
 double t0=number(argv[1]);shape::Vec3 p{number(argv[2]),number(argv[3]),number(argv[4])},v{number(argv[5]),number(argv[6]),number(argv[7])};
 double g=number(argv[8]),dt=number(argv[9]),nd=number(argv[10]);
 if(t0<0||dt<=0||nd<1||nd>100000||std::floor(nd)!=nd)throw std::invalid_argument("invalid sample contract");
 std::cout<<std::setprecision(17)<<"time,x,y,z\n";
 for(int i=0;i<static_cast<int>(nd);i++){auto q=shape::predict(p,v,i*dt,g);std::cout<<t0+i*dt<<","<<q.x<<","<<q.y<<","<<q.z<<"\n";}
 return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 2;}}
