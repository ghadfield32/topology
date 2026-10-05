#include <vector>
#include <memory>
#include <optional>
#include <variant>
#include <string>
#include <numeric>
#include <algorithm>
#include <stdexcept>
#include <iostream>
template<class T>T square(T x){return x*x;}
int main(){std::vector<int>a{1,2,3};auto b=a;b[0]=8;if(a[0]!=1)throw std::runtime_error("value copy aliased");auto&ref=a;ref[0]=4;auto moved=std::move(b);if(moved[0]!=8)throw std::runtime_error("unexpected move destination");auto ptr=std::make_unique<int>(9);std::optional<int>missing;std::variant<int,std::string>state=std::string("validated");if(*ptr!=9||missing.has_value()||square(3)!=9||std::accumulate(a.begin(),a.end(),0)!=9||!std::holds_alternative<std::string>(state))throw std::runtime_error("concept assertion");std::cout<<"copy, reference, move destination, RAII, optional, variant, template and reduction checks passed\n";}
