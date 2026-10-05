#include "shape.hpp"
#include <algorithm>
#include <cmath>
#include <limits>
#include <stdexcept>
namespace shape {
static void valid(Vec3 p){if(!std::isfinite(p.x)||!std::isfinite(p.y)||!std::isfinite(p.z))throw std::invalid_argument("nonfinite point");}
Vec3 predict(Vec3 p,Vec3 v,double t,double g){
 valid(p);valid(v);if(!std::isfinite(t)||!std::isfinite(g)||t<0||g<=0)throw std::invalid_argument("invalid time/gravity");
 Vec3 out{p.x+v.x*t,p.y+v.y*t,p.z+v.z*t-.5*g*t*t};valid(out);return out;
}
double distance(Vec3 a,Vec3 b){valid(a);valid(b);return std::hypot(a.x-b.x,a.y-b.y,a.z-b.z);}
std::vector<double> mst_deaths(const std::vector<Vec3>& x){
 if(x.empty()||x.size()>4096)throw std::invalid_argument("bounded nonempty point set required");
 for(auto p:x)valid(p);
 std::vector<double> best(x.size(),std::numeric_limits<double>::infinity()),result;
 std::vector<bool> used(x.size(),false);best[0]=0;
 for(std::size_t step=0;step<x.size();++step){
  std::size_t i=x.size();for(std::size_t j=0;j<x.size();++j)if(!used[j]&&(i==x.size()||best[j]<best[i]))i=j;
  if(i==x.size()||!std::isfinite(best[i]))throw std::invalid_argument("distance overflow");
  used[i]=true;if(step)result.push_back(best[i]);
  for(std::size_t j=0;j<x.size();++j)if(!used[j])best[j]=std::min(best[j],distance(x[i],x[j]));
 }
 std::sort(result.begin(),result.end());return result;
}
std::size_t radius_components(const std::vector<Vec3>& x,double r){
 if(!std::isfinite(r)||r<0||x.size()>4096)throw std::invalid_argument("invalid radius/size");
 for(auto p:x)valid(p);
 std::vector<bool> seen(x.size(),false);std::size_t count=0;
 for(std::size_t i=0;i<x.size();++i)if(!seen[i]){
  ++count;seen[i]=true;std::vector<std::size_t> stack{i};
  while(!stack.empty()) {auto j=stack.back();stack.pop_back();for(std::size_t k=0;k<x.size();++k)if(!seen[k]&&distance(x[j],x[k])<=r){seen[k]=true;stack.push_back(k);}}
 }
 return count;
}
}
