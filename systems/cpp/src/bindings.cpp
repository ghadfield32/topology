#include "shape.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py=pybind11;
shape::Vec3 point(const std::vector<double>& v){if(v.size()!=3)throw std::invalid_argument("need three coordinates");return {v[0],v[1],v[2]};}
PYBIND11_MODULE(shape_cpp,m){
 m.doc()="Small explicit C++20 numerical kernels; no hidden fitting";
 m.def("predict",[](const std::vector<double>& p,const std::vector<double>& v,double t,double g){auto q=shape::predict(point(p),point(v),t,g);return std::vector<double>{q.x,q.y,q.z};},py::arg("position"),py::arg("velocity"),py::arg("dt"),py::arg("gravity")=9.81);
 m.def("mst_deaths",[](const std::vector<std::vector<double>>& xs){std::vector<shape::Vec3> p;for(const auto& x:xs)p.push_back(point(x));return shape::mst_deaths(p);});
}
