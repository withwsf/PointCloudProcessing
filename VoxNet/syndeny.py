# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:35:07 2016

@author: wsf
"""
import numpy as np
import os 
import knn_normal as knn
import re
def get_min_point(data_mat,dim=3):
    '''
    输入一个data_mat，返回沿axis=0方向的最小值；
    '''
    min=np.amin(data_mat,axis=0)
    return min[0:dim]
def get_max_point(data_mat,dim=3):
    '''
    输入一个data_mat，返回沿axis=0方向的最大值；
    '''
    max=np.amax(data_mat,axis=0)
    return max[0:dim]
def creat_cube_of_object(points,grid_size=0.2,x_size=32,y_size=32,z_size=32,feature_dim=3,,rotate_angle=0,filename='null'):
    '''
    创建包含分割完毕的对象的cube体
    points:待处理对象的点云
    grid_size:cube的分辨率（每个格子的尺寸）
    x_size,y_size,x_size:cube对象的尺寸
    feature_dim:feature_dim对象的维度
    rotate_angle:如果此对象augmentation过，旋转角度是多少（用于输出日志信息）
    filename:处理对象的文件名，同样用于输出日志
    '''
    #max_points=get_max_point(points[:,0:3])
    #min_points=get_min_point(points[:,0:3])
    #center_of_boundingbox=(max_points-min_points)/2
    #points[:,0:3]=points[:,0:3]-center_of_boundingbox
    cube=np.zeros((x_size,y_size,z_size,feature_dim))
    
    j=0
    for point in points:
        corrd_to_boundingbox_center=map(lambda x:int(x/grid_size),point[0:3])
        corrd_to_cube=corrd_to_boundingbox_center+np.array([x_size/2,y_size/2,z_size/2])
        condit1= corrd_to_cube[0]>=0 and corrd_to_cube[0]<32
        condit2= corrd_to_cube[1]>=0 and corrd_to_cube[1]<32
        condit3= corrd_to_cube[2]>=0 and corrd_to_cube[2]<32
                 
        if(condit1 and condit2 and condit3):
            cube[corrd_to_cube[0],corrd_to_cube[1],corrd_to_cube[2]]=point[3:3+feature_dim]
        else:
            j+=1.0
            #print "第%i个点出界"%i
            #print "坐标是"
            #print poin
    print "有%f的点在%s外面,旋转角度是%i"%((j/len(points)),filename,rotate_angle)
    return cube,j/len(points)
    
    
    
    
def data_augmentation(points,rotate_angle,filepath):
    '''
    对点云对象在xy平面上进行旋转
    points:待处理对象的点云
    rotate_angle:旋转角度，旋转后数据增加360/rotate_angle倍
    filepath:augmentation后的数据保存路径
    return:list对象，每个元素是numpy的array对象，保存这旋转不同角度的点云对象
    '''
    max_points=get_max_point(points[:,0:3])
    min_points=get_min_point(points[:,0:3])
    center_of_boundingbox=(max_points-min_points)/2+min_points
    points[:,0:3]=points[:,0:3]-center_of_boundingbox
    np.savetxt("init.xyz",points,fmt='%0.4f',delimiter=' ')  #temp
    xy=points[:,0:2]
    z=points[:,2]
    list_of_rotated_points=[]
    num_of_rotated=int(360/rotate_angle)
    list_of_rotate_matrix=[]
    for i in range(num_of_rotated):
        angle=((i*rotate_angle)/180.)*np.pi
        roate_matrix=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        list_of_rotate_matrix.append(roate_matrix)
    count=0    
    for matrix in list_of_rotate_matrix:
        rotated_points=np.column_stack(( xy.dot(matrix),z))
        list_of_rotated_points.append(rotated_points)
        #np.savetxt(os.path.join('E','forest_data','augmentated',(filepath.strip().split('/')[-1]+str(count*rotate_angle)+'.xyz')),rotated_points,fmt='%0.5f')
        count+=1
    return list_of_rotated_points
    
def parsing_file(file_path,line_skip=0):
    with open(file_path) as f:
       lines=f.readlines()
       lines=lines[line_skip:]
       #line=lines[0].strip().split('   ')
       #print line
       #points=np.array(map(lambda line:map(float,line.strip().split('   '))[0:3] ,lines))#为了sysdeny数据修改成了三个空格
       #points=[[float(v) for v in re.compile(" +").split(line.strip())]for line in lines]       
       #point=lines[0].strip().split('   ')
       #point=map(float,point)
       points=[]       
       for line in lines:
           point=re.compile(" +").split(line.strip())
           point=map(float,point)
           points.append(point)
       return np.array(points)
       
def function_pack(filepath):
    '''
    对上面针对syndeny数据处理的封装
    输入：点云文件
    输出：augmentation 12倍的数据
    '''
    points=parsing_file(filepath)
    return data_augmentation(points,30,filepath)
    
    

def aug_and_normal(filedir,k=6):
    '''
    综述：对文件夹内的数据进行augmentation，然后对augmentation之后的数据计算normal并保存
    20160223添加
    返回：
    返回一个list of cube，每个cube是一个样本旋转一定角度后的结果；
    '''
    list_of_cube=[]
    files=os.listdir(filedir)
    list_of_occupy_rates=[]
    for file in files:
        fullPath=os.path.join(filedir,file)
        augeds=function_pack(fullPath)
        i=0
        for auged in augeds:
            augedWithNormal=knn.get_pca_normal(auged,k)
            cube,rate=creat_cube_of_object(augedWithNormal,i*30,file)
            #np.save(cube,)
            list_of_cube.append(cube)
            list_of_occupy_rates.append(file+' '+str(i*30)+' '+str(rate))
            i=i+1
    return list_of_cube,list_of_occupy_rates
if __name__=='__main__':
    dirofDir='E:/forest_data/sysdeny'
    dirs=os.listdir(dirofDir)
    list_rate_toSave=[]
    for dir in dirs:
     filedir=os.path.join(dirofDir,dir,'xyz')
     list_of_cube,list_of_occupy_rates=aug_and_normal(filedir,6)
     np.save(dir,np.array(list_of_cube))
     list_rate_toSave.extend(list_of_occupy_rates)
    np.savetxt('occupy_rate.txt',np.array(list_rate_toSave),fmt='%0.5f')
     