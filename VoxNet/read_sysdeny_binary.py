import numpy as np
import os
names = ['t','intensity','id',
         'x','y','z',
         'azimuth','range','pid']

formats = ['int64', 'uint8', 'uint8',
           'float32', 'float32', 'float32',
           'float32', 'float32', 'int32']
binType=np.dtype(dict(names=names,formats=formats))

def load_binary_file(filepath):
    data=np.fromfile(filepath,binType)
    points=np.vstack([data['x'],data['y'],data['z']]).T
    return points
    
    
    
if __name__=="__main__":
   dir_of_dirs='E:/forest_data/sysdeny'
   dirs=os.listdir(dir_of_dirs)
   for dir in dirs:
       files=os.listdir(os.path.join(dir_of_dirs,dir))
       os.chdir(os.path.join(dir_of_dirs,dir))
       os.makedirs('xyz')
       os.makedirs('npy')
       print "处理文件夹%s"%dir
       for file in files:
          print "处理文件%s"%file
          filepath=os.path.join(dir_of_dirs,dir,file)
          points=load_binary_file(filepath)
          np.savetxt(os.path.join(dir_of_dirs,dir,'xyz',file+'.xyz'),points,fmt='%10.5f')
          np.save(os.path.join(dir_of_dirs,dir,'npy',file),points)
   
