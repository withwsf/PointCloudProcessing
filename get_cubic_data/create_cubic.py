# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 23:01:04 2015

@author: wsf
"""
DIM=3
GRIDSIZE=0.03
FEATURE_DIM=3
FEATURE_BEGIN_DIM=3
THRESHOLD=0.02
X_SIZE=20
Y_SIZE=20
Z_SIZE=20
X_STRIDE=5
Y_STRIDE=5
Z_STRIDE=5
import numpy as np

def get_min_point(data_mat):
    min=np.amin(data_mat,axis=0)
    return min[0:DIM]
def get_max_point(data_mat):
    max=np.amax(data_mat,axis=0)
    return max[0:DIM]
def positon_at_cube(relative_dist):
    return int(relative_dist/GRIDSIZE)

def save_list(list_object,save_path):
    '''
    将list对象用numpy中的格式进行保存，避免了读取的时候再进行parsing
    '''
    save_object=np.array(list_object)
    np.save(save_path,save_object)

    
def normalize_cube(cube,cube_count):
    '''
    接受cube和cube_count作为输入，输出normalized的cube和二值化的cube_count
    '''
    ###确定normalize data是没有问题的
    shape_array=cube_count.shape
    for i in range(shape_array[0]):
        for j in range(shape_array[1]):
            for k in range(shape_array[2]):
                if cube_count[i,j,k] >1:
                    cube[i,j,k]=cube[i,j,k]/np.linalg.norm(cube[i,j,k])
                    cube_count[i,j,k]=1
    return cube,cube_count 
def load_data(filepath):
    '''
    装载数据并给出数据的data_mat
    '''
    print "打开文件%s"%filepath
    with open(filepath) as f:
      lines=f.readlines()
      header_count=0
    
      for line in lines:#跳过文件的头文件
        header_count=header_count+1
        if "end_header" in line:  
          break
      dims=np.size(lines[header_count].strip().split(' '))
      sample_nums=np.size(lines)-header_count
      data_mat=np.empty((sample_nums,dims))
      for line_num in range(sample_nums):
        data_mat[line_num]=map(float,lines[header_count+line_num].strip().split(' '))
      
      print "文件的尺寸是："
      print data_mat.shape
      return data_mat
def create_cube(data_mat):
    '''
    接受data_mat作为输入，输出normalized的cube和标记是否有元素的cube_bool
    '''
    min_point=get_min_point(data_mat)
    max_point=get_max_point(data_mat)
    cube_size=np.array(map(positon_at_cube,(max_point-min_point)))+1
    cube=np.zeros((cube_size[0],cube_size[1],cube_size[2],FEATURE_DIM)) #cube的dim为x,y,zchannels
    cube_count=np.zeros((cube_size[0],cube_size[1],cube_size[2],1))
    for i in range(data_mat.shape[0]):
      corrds=map(positon_at_cube,(data_mat[i][0:DIM]- min_point))
      cube[corrds[0],corrds[1],corrds[2]]+=data_mat[i][FEATURE_BEGIN_DIM:FEATURE_BEGIN_DIM+FEATURE_DIM]
      cube_count[corrds[0],corrds[1],corrds[2]]+=1
    before_nomalize=np.sum(cube_count)  
    cube_normalized,cube_count_bool=normalize_cube(cube,cube_count)
    after_nomalize=np.sum(cube_count_bool)
    print "共有%d个点，分布在%d个格子内"%(before_nomalize,after_nomalize)
    print "创建的cube体积是%d,平均每个格子有%d个点"%(cube_size[0]*cube_size[1]*cube_size[2],before_nomalize/(cube_size[0]*cube_size[1]*cube_size[2]))
    print cube_normalized.shape
    return cube_normalized,cube_count_bool

def sliding_cube(cube,cube_bool,x_size=24,y_size=24,z_size=24,x_stride=10,y_stride=10,z_stride=10,accept_threshold=THRESHOLD):
    data_list=[]
    rate_list=[]
    cube_shape=cube.shape
    volume=x_size*y_size*z_size
    i=0.0
    j=0.0
    maxrate=0
    print "在x方向上步进%d"%int((cube_shape[0]-x_size)/x_stride)
    print "在y方向上步进%d"%int((cube_shape[1]-y_size)/y_stride)
    print "在z方向上步进%d"%int((cube_shape[2]-z_size)/z_stride)
    print "选择的阈值是%d"%accept_threshold
    for x_step in range(int((cube_shape[0]-x_size)/x_stride)):
        for y_step in range(int((cube_shape[1]-y_size)/y_stride)):
            for z_step in range(int((cube_shape[2]-z_size)/z_stride)):
                x_beg=x_step*x_stride
                y_beg=y_step*y_stride
                z_beg=z_step*z_stride
                x_end=x_beg+x_size
                y_end=y_beg+y_size
                z_end=z_beg+z_size
                mini_cube=cube[x_beg:x_end,y_beg:y_end,z_beg:z_end]
                mini_cube_bool=cube_bool[x_beg:x_end,y_beg:y_end,z_beg:z_end]
                rate=np.sum(mini_cube_bool)/float(volume)
                i+=1
                if rate>maxrate:
                        maxrate=rate
                if rate>=accept_threshold: 
                    data_list.append(mini_cube)
                    rate_list.append(mini_cube_bool)
                    j+=1
    print "共尝试了"+str(i)+"个 mini cube，有"+str(j)+"个符合要求"
    print"最大rate是%f"%maxrate
    return data_list,rate_list
    
def processing_data_mat(data_mat):
    '''
    想要修改参数的话来create_cubic来修改
    '''
    cube,cube_bool=create_cube(data_mat)
    data_list,rate_list=sliding_cube(cube,cube_bool)
    return data_list,rate_list
    



