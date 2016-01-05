# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 00:30:41 2015

@author: wsf
"""
import h5py
import numpy as np
import os
def get_train_test(nparray,trainnum,testnum):
    assert(nparray.shape[0]>=trainnum+testnum)
    nparray=np.random.permutation(nparray)
    trainset=nparray[0:trainnum]
    testset=nparray[trainnum:trainnum+testnum]
    return trainset,testset

def transpose_data(nparray):
    #assert(len(nparray.shape)!= 5)
    return np.transpose(nparray,(0,4,1,2,3))
        
def create_train_test_set(dirpath,trainnum,testnum):
  '''
  dirapth：指向文件夹的路径，里面的每个文件都是都是numpy array文件，为5维文件
  trainnum：从每个文件选择的训练样本的数量
  testnum：从每个文件选择测试样本的数量
  '''   
  names=os.listdir(dirpath)
  print "共有%d个文件"%len(names)  


  trainpath=dirpath+os.sep+'trainset.h5'
  testpath=dirpath+os.sep+'testset.h5'
  trainset=h5py.File(trainpath,'w')
  testset=h5py.File(testpath,'w')
  trainset.create_dataset('data',(trainnum*len(names),3,24,24,24),dtype='f8')
  trainset.create_dataset('label',(trainnum*len(names),1),dtype='i')
  testset.create_dataset('data',(testnum*len(names),3,24,24,24),dtype='f8')
  testset.create_dataset('label',(testnum*len(names),1),dtype='i')
  print '创建 %s 和 %s'%(trainpath,testpath)
  
  i=0
  for name in names:
      print "处理文件%s, label是%d"%(name,i+1)
      lines=np.load(dirpath+os.sep+name)
      lines=transpose_data(lines)
      sub_train,sub_test=get_train_test(lines,trainnum,testnum)
      for k in range(trainnum):
          trainset['data'][i*trainnum+k]=sub_train[k]
          trainset['label'][i*trainnum+k]=i+1
      for j in range(testnum):
          testset['data'][i*testnum+j]=sub_test[j]
          testset['label'][i*testnum+j]=i+1
      i=i+1
  print "准备对hdf5文件进行重排序"
  trainset_reorder=np.random.permutation(trainnum*len(names))
  testset_reorder=np.random.permutation(testnum*len(names))
  for train_sample in range(trainnum*len(names)):
      trainset['data'][train_sample]=trainset['data'][trainset_reorder[train_sample]]
      trainset['label'][train_sample]=trainset['label'][trainset_reorder[train_sample]]
  for test_sample in range(testnum*len(names)):
      testset['data'][test_sample]=testset['data'][testset_reorder[test_sample]]
      testset['label'][test_sample]=testset['label'][testset_reorder[test_sample]]
  print "保存并关闭文件"
  trainset.close()
  testset.close()
  


def create_train_test_set2(dirpath,trainnum,testnum):
  '''
  dirapth：指向文件夹的路径，里面的每个文件都是都是numpy array文件，为5维文件
  trainnum：从每个文件选择的训练样本的数量
  testnum：从每个文件选择测试样本的数量
  '''   
  names=os.listdir(dirpath)
  print "共有%d个文件"%len(names)  


  trainpath=dirpath+os.sep+'trainset.h5'
  testpath=dirpath+os.sep+'testset.h5'
  trainset=h5py.File(trainpath,'w')
  testset=h5py.File(testpath,'w')
  trainset.create_dataset('data',(trainnum*len(names),3,24,24,24),dtype='f8')
  trainset.create_dataset('label',(trainnum*len(names),1),dtype='i')
  testset.create_dataset('data',(testnum*len(names),3,24,24,24),dtype='f8')
  testset.create_dataset('label',(testnum*len(names),1),dtype='i')
  print '创建 %s 和 %s'%(trainpath,testpath)
  
  i=0
  for name in names:
      print "处理文件%s, label是%d"%(name,i+1)
      lines=np.load(dirpath+os.sep+name)
      lines=transpose_data(lines)
      sub_train,sub_test=get_train_test(lines,trainnum,testnum)
      for k in range(trainnum):
          trainset['data'][i*trainnum+k]=sub_train[k]
          trainset['label'][i*trainnum+k]=i+1
      for j in range(testnum):
          testset['data'][i*testnum+j]=sub_test[j]
          testset['label'][i*testnum+j]=i+1
      i=i+1
  print "准备对hdf5文件进行重排序"
  trainset_reorder=np.random.permutation(trainnum*len(names))
  testset_reorder=np.random.permutation(testnum*len(names))
  for train_sample in range(trainnum*len(names)):
      trainset['data'][train_sample]=trainset['data'][trainset_reorder[train_sample]]
      trainset['label'][train_sample]=trainset['label'][trainset_reorder[train_sample]]
  for test_sample in range(testnum*len(names)):
      testset['data'][test_sample]=testset['data'][testset_reorder[test_sample]]
      testset['label'][test_sample]=testset['label'][testset_reorder[test_sample]]
  print "保存并关闭文件"
  trainset.close()
  testset.close()

  
dirpath='E:/forest_data/cubes'
                             
create_train_test_set(dirpath,1500,500)

