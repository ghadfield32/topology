#include "shape.hpp"
#include <iostream>
#include <stdexcept>
#include <cmath>
void check(bool x) { if(!x)throw std::runtime_error("assertion failed"); }
int main(){
 auto p=shape::predict({0,0,2},{1,0,3},.5,9.81);check(std::abs(p.z-2.27375)<1e-12);check(p.x==.5);
 bool rejected=false;try{shape::predict({0,0,0},{0,0,0},1,-1);}catch(const std::invalid_argument&){rejected=true;}check(rejected);
 auto deaths=shape::mst_deaths({{0,0,0},{1,0,0},{1,1,0},{0,1,0}});check(deaths.size()==3);for(auto d:deaths)check(d==1);
 auto edges=shape::radius_components({{0,0,0},{1,0,0},{1,1,0},{0,1,0}},.9);check(edges==4);
 check(shape::radius_components({{0,0,0},{1,0,0},{1,1,0},{0,1,0}},1)==1);
 auto dup=shape::mst_deaths({{0,0,0},{0,0,0}});check(dup[0]==0);
 std::cout<<"6 core checks passed\n";
}
