#include "stdafx.h"
#include "extractor.h"
#include <fstream>
#include <algorithm>
#include <sstream>
#include <memory>
#include <iterator>
#include "tools.h"

using namespace std;

bool extractor::load_data(std::string file_path){



	std::ifstream file(file_path);
	std::string line;
	while (std::getline(file, line)){
		this->point_cloud.push_back(tool::parsing(line));

	}
	num_points = point_cloud.size();
	dims = 3;//为了增强拓展性后续还要更改这里
	point_feature.resize(num_points);
	return true;
}

void extractor::save_point_feature(string savepath){
	tool::save_2dvector(point_feature, savepath);
};
std::vector<std::vector<int>>  extractor::get_knn(int k,std::string savename)
{
	if (k >= point_cloud.size()){
		std::cout << "The k is larger than the number of points, the returned knn_index are empty!!! ";
		return knn_index;
	}
	ANNpointArray ptCloud = annAllocPts(num_points, dims);//要考虑避免泄露
	ANNpoint ptQuery = annAllocPt(dims);//要考虑避免泄露
	ANNidxArray pToIdx = new ANNidx[k];
	ANNdistArray pToDist = new ANNdist[k];
	for (int i = 0; i < num_points;i++){//from vector to points
		for (int j = 0; j < 3; j++){
			ptCloud[i][j]=point_cloud[i][j];

		}
	}

	std::shared_ptr<ANNkd_tree> pTree = std::make_shared<ANNkd_tree>(ptCloud,num_points,dims);
	for (auto point : point_cloud){
		for (int i = 0; i<3; i++){
			ptQuery[i] = point[i];
		}	
		pTree->annkSearch(ptQuery,k,pToIdx,pToDist,0.2);
		std::vector<int> temp;
		for (int j = 0; j < k; j++){
			temp.push_back(pToIdx[j]);
		}
		knn_index.push_back(temp);
	}
	delete pToDist;
	delete pToIdx;
	annClose();

	tool::save_2dvector(knn_index, savename);
	return knn_index;
}
std::vector<std::vector<float>> extractor::get_point_feature(){
	return point_feature;
}
bool extractor::calculate_PCA(){
    #pragma omp parallel for
	for (int i = 0; i <this->num_points;i++){
		//计算特征值和特征向量
		int k = knn_index[0].size();
		Eigen::MatrixXd near_points(k,dims);
		for (int j = 0; j < k;j++)
		{
			for (int z = 0; z < dims; z++){
				near_points(j, z) = point_cloud[knn_index[i][j]][z];
				
			}
		}
		//cout << near_points << endl;
		Eigen::MatrixXd mean = near_points.rowwise() - near_points.colwise().mean();
		Eigen::MatrixXd covariance = (mean.transpose()*mean) / (k - 1);
		Eigen::EigenSolver<Eigen::MatrixXd> es(covariance);
		vector<float> processed = tool::process_es(es, dims);
		point_feature[i].insert(point_feature[i].end(), processed.begin(), processed.end());
		//cout << covariance << endl;
    	//将计算结果放入point_feature矩阵
		//Eigen::VectorXd eValue=es.eigenvalues().real();

		//eValue.normalize();
		//for (int l = 0; l < dims; l++)
		//	point_feature[i].push_back(eValue(l));
		//std::vector<size_t> index = tool::sort_indexes(point_feature[i]);
		//std::sort(point_feature[i].begin(),point_feature[i].end(),tool::myfunction);
		////cout << es.eigenvalues() << endl;
		////cout << es.eigenvectors() << endl;
		//Eigen::MatrixXd eVector = es.eigenvectors().real();
		//eVector.normalize();
		//std::vector<float> eigen_vector(dims*dims);
		//size_t jj = 0;
		//for (auto ind : index){
		//	
		//	for (size_t ii = 0; ii < dims; ++ii)
		//		eigen_vector[jj*dims+ii] = eVector(ii, ind);
		//	jj += 1;
		//}
		//point_feature[i].insert(point_feature[i].end(),eigen_vector.begin(),eigen_vector.end());
		
	}
	knn_index.clear();
	//save_point_feature("test.txt");
	return true;
}