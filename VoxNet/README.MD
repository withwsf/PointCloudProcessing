#### 文件说明
read_sysdeny_binary.py：从[原始数据集](http://www.acfr.usyd.edu.au/papers/SydneyUrbanObjectsDataset.shtml)中读取数据并存储成xyz格式
syndeny.py：对数据进行旋转augmentation并创建cube
create_train_test.ipynb:从保存好的.npy文件中创建训练和测试集
nn_sysdeny.ipynb:Lua脚本，创建CNN网络并使用数据进行训练和测试