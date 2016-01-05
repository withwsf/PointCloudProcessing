# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 15:54:56 2015

@author: wsf
"""
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import os
import sys
sys.path.append('C:/Users/wsf/Desktop/point_cloud/data/forest_data/spyder')
import create_cubic as cc
def parsingline(line):
    '''
    将输入的string转化成list of float
    '''
    return map(float,line.strip().split(' '))[0:3]
    
def get_normal(matrix):
    '''
   根据矩阵计算并返回normal    
    '''
    pca=PCA()
    pca.fit(matrix)
    if pca.components_[2][0]>0:
       return pca.components_[2]
    else:
       return -pca.components_[2]
    
def get_pca_normal(data_matrix,nn):
    '''
    根据输入的数据矩阵返回一个nn邻域的normal矩阵
    '''
    nbrs = NearestNeighbors(n_neighbors=nn,algorithm='ball_tree').fit(data_matrix)
    distance,indices=nbrs.kneighbors(data_matrix)
    points=data_matrix[indices]
    normals=np.array(map(get_normal,points))
    final=np.concatenate((data_matrix,normals),axis=1)
    return final




def processing_dir(dirpath,k=20,save_dir='',save_prefix='_withnormal',line_skip=12):
 '''
 计算一个文件夹内的k近邻的normal，然后保存起来
 '''
 names=os.listdir(dirpath)
 print "计算%d近邻"%k   
 for name in names:
    filepath=os.path.join(dirpath,name)
    if not os.path.isdir(filepath):
      print '正在处理文件%s'%filepath  
      with open(dirpath+os.sep+name) as f:
          lines=f.readlines()
          lines=lines[line_skip:]#为了读取ply文件
          lines=np.array(map(parsingline,lines))
          final=get_pca_normal(lines,k)      
          print "保存在 %s"%(save_dir+name.split('.')[0]+save_prefix+str(k)+'_neighbor_.xyz')
          print '\n'
          np.savetxt(save_dir+name.split('.')[0]+save_prefix+str(k)+'_neighbor_.xyz',final,fmt='%10.5f')




def dir_to_cubic_data(dirpath,feature_dir,cubic_data_save_dir,k=12,line_skip=12,save_prefix="cubic_data"):
 '''
 把文件夹变成一个cubic data！
 '''
 all_data_list=[]
 names=os.listdir(dirpath)
 print "计算的是%d近邻"%k   
 for name in names:
    filepath=os.path.join(dirpath,name)
    if not os.path.isdir(filepath):
      print '正在处理文件%s'%filepath  
      with open(dirpath+os.sep+name) as f:
          lines=f.readlines()
          lines=lines[line_skip:]#为了读取ply文件
          lines=np.array(map(parsingline,lines))
          final=get_pca_normal(lines,k) 
          ##基本可以确定计算的normal是没有错的
          print "保存文件%s的%d近邻normal"%(name,k)
          np.savetxt(feature_dir+os.sep+name+'normal_'+str(k)+'.xyz',final,fmt='%10.5f')
          data_list,rate_list=cc.processing_data_mat(final)
          all_data_list.extend(data_list)


    if len(all_data_list)>20000:
        break
 all_data_list=np.array(all_data_list)
 #np.save(dirpath.split('/')[0]+save_prefix+str(len(all_data_list)),all_data_list)
 print "正在保存文件%s,共有%d个对象"%(dirpath+os.sep+names[0],len(all_data_list))
 np.save(cubic_data_save_dir+os.sep+names[0]+'_'+str(len(all_data_list)),all_data_list)



header='E:/forest_data'          
dirs=['Willow/0.06','SheKouTree/0.06','Pine/0.06','Palm/0.06','Mahogany_PTC/0.06','Lagerstroemia/0.06','Delonix/0.06','Terminalia/0.06']
#dirs=['E:/forest_data/Willow/0.06']
for dirpath in dirs:
    fullpath=header+os.sep+dirpath
    print '\n\n开始处理文件%s'%fullpath
    dir_to_cubic_data(fullpath,k=6)       





