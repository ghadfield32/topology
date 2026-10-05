#pragma once
#include <vector>
#include <cstddef>
namespace shape {
struct Vec3 { double x,y,z; };
Vec3 predict(Vec3 position,Vec3 velocity,double dt,double gravity=9.81);
double distance(Vec3 a,Vec3 b);
std::vector<double> mst_deaths(const std::vector<Vec3>& points);
std::size_t radius_components(const std::vector<Vec3>& points,double radius);
}
