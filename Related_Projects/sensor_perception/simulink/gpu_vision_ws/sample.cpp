#include <opencv2/opencv.hpp>
#include <opencv2/gpu/gpu.hpp>

using namespace cv;

int main() {
	int i = 0;	

	Mat src = imread("sample.jpg", 0);
	if (!src.data) exit(1);

	for ( i=0; i < 500; i++) {
	gpu::GpuMat d_src(src);
	gpu::GpuMat d_dst;
	gpu::bilateralFilter(d_src, d_dst, -1, 50, 7);
	gpu::Canny(d_dst, d_dst, 35, 200, 3);
	Mat dst(d_dst);
	
	imwrite("out.png", dst);
	}
	return 0;
}
