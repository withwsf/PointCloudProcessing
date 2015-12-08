// feature_extractor.cpp : 定义控制台应用程序的入口点。
//
#include "stdafx.h"
#include "ANN.h"
#include "extractor.h"
#include <memory>
#include <iostream>
#include <omp.h>
void test(int n)
{
	for (int i = 0; i < 10000; ++i)
	{
		//do nothing, just waste time
	}
	//printf( "%d, ", n );
	std::cout <<" "<< n;
}

int _tmain(int argc, _TCHAR* argv[])
{
	extractor test;
    test.load_data("C:/Users/wsf/Desktop/point_cloud/data/big_tree5.txt");
	for (int i = 0; i < 50; ++i)
	{

		test.get_knn(6*(i+1), "result.txt");
		test.calculate_PCA();
	}
	test.save_point_feature("point_feature_big_tree5_600dim.txt");
	return 0;
}

