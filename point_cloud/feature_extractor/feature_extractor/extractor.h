#pragma once
#include <string>
#include <vector>
#include "ANN.h"
#include "Eigen/Dense"
class extractor{
public:
	extractor(){};
	~extractor(){};
	bool load_data(std::string path);
	std::vector<std::vector<int>> get_knn(int k,std::string savename);
	bool calculate_PCA();
	std::vector<std::vector<float>> get_point_feature();
	void save_point_feature(std::string savepath);
private:
	std::vector<std::vector<float>> point_cloud;
	std::vector<std::vector<int>> knn_index;
	std::vector<std::vector<float>> point_feature;
	int num_points,dims;

};