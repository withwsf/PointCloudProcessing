#include <fstream>
#include <sstream>
#include <iterator>
#include <vector>
#include <string>
#include <algorithm>
#include "Eigen\Dense"
using namespace std;
namespace tool{
	std::vector<float> parsing(std::string line){
		std::vector<float> tokens;
		std::stringstream ss(line);
		float i;
		while (ss >> i){
			tokens.push_back(i);
			if (ss.peek() == ',')
				ss.ignore();
		}
		return tokens;
	}
	template<typename T>
	bool save_2dvector(std::vector<std::vector<T>> save_vector,std::string savepath){
		std::ofstream output_file(savepath);
		std::ostream_iterator<T> output_iterator(output_file, " ");//so if the type is string, you can use string
		
		for (auto line : save_vector){

			std::copy(line.begin(), line.end(), output_iterator);
			output_file << "\n";
		}
		return true;
	}
	
	
	template<typename T>
	std::vector <size_t> sort_indexes(std::vector<T> &v) {

		// initialize original index locations
		std::vector<size_t> idx(v.size());
		for (size_t i = 0; i != v.size(); ++i)
			idx[i] = i;

		// sort indexes based on comparing values in v
		std::sort(idx.begin(), idx.end(),
			[&v](size_t i1, size_t i2) {return v[i1] > v[i2]; });
		return idx;
	}
	
	bool myfunction(float a, float b){
		return (a > b);
	}
	vector<float> process_es(Eigen::EigenSolver<Eigen::MatrixXd>& es,int dims){
		Eigen::VectorXd eigenValue = es.eigenvalues().real();
		Eigen::MatrixXd eigenVectors = es.eigenvectors().real();
		eigenValue.normalize();
		eigenVectors.normalize();
		vector<float> processed(dims+dims*dims);
		vector<float> get_index;
		for (int i = 0; i < dims; ++i){
			processed[i]=eigenValue(i);
			get_index.push_back(eigenValue(i));
		}

		std::vector<size_t> index = sort_indexes(get_index);
		std::sort(processed.begin(), processed.end(), myfunction);
		int jj = 0;
		for (auto ind : index){
			for (int j = 0; j < dims; ++j)
				processed[dims + jj*dims + j] = eigenVectors(j, ind);
			jj += 1;
		}
		return processed;

	}
}