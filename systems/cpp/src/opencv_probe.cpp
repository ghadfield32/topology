#include <opencv2/core.hpp>
#include <opencv2/calib3d.hpp>
#include <iostream>
#include <stdexcept>
int main(){
 cv::Mat image(8,8,CV_8UC3,cv::Scalar(1,2,3));auto roi=image(cv::Rect(1,1,3,4));
 if(roi.isContinuous())throw std::runtime_error("expected strided ROI");auto copy=roi.clone();
 if(!copy.isContinuous())throw std::runtime_error("clone should own contiguous rows");
 cv::Mat K=(cv::Mat_<double>(3,3)<<800,0,320,0,800,240,0,0,1);
 std::vector<cv::Point3d> points{{1,2,10}};std::vector<cv::Point2d> pixels;
 cv::projectPoints(points,cv::Vec3d(0,0,0),cv::Vec3d(0,0,0),K,cv::Mat(),pixels);
 if(cv::norm(pixels[0]-cv::Point2d(400,400))>1e-10)throw std::runtime_error("projection mismatch");
 std::cout<<"{\"projection\":[400,400],\"roi_contiguous\":false,\"clone_contiguous\":true}\n";
}
