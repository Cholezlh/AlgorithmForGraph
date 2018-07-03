# coding: utf-8 
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def laplaEigen(dataMat,k,t):  
    m,n=np.shape(dataMat)  
    W=np.mat(np.zeros([m,m]))  
    D=np.mat(np.zeros([m,m]))  
    for i in range(m):  
        k_index=knn(dataMat[i,:],dataMat,k)  
        for j in range(k):  
            sqDiffVector = dataMat[i,:]-dataMat[k_index[j],:]  
            sqDiffVector=np.array(sqDiffVector)**2  
            sqDistances = sqDiffVector.sum()  
            W[i,k_index[j]]=np.math.exp(-sqDistances/t)  
            D[i,i]+=W[i,k_index[j]]  
    L=D-W  
    #Dinv=np.linalg.inv(D)  
    X=np.dot(D.I,L)  
    lamda,f=np.linalg.eig(X)    #lamda,f 特征值和特征向量是一一对应的
    return lamda,f 

 
def knn(inX, dataSet, k):  
    dataSetSize = dataSet.shape[0]  
    diffMat = np.tile(inX, (dataSetSize,1)) - dataSet  
    sqDiffMat = np.array(diffMat)**2  
    sqDistances = sqDiffMat.sum(axis=1)  
    distances = sqDistances**0.5  
    sortedDistIndicies = distances.argsort()      
    return sortedDistIndicies[0:k]  

def make_swiss_roll(n_samples=100, noise=0.0, random_state=None):  
    #Generate a swiss roll dataset.  
    t = 1.5 * np.pi * (1 + 2 * np.random.rand(1, n_samples))  
    x = t * np.cos(t)  
    y = 83 * np.random.rand(1, n_samples)  
    z = t * np.sin(t)  
    X = np.concatenate((x, y, z))  
    X += noise * np.random.randn(3, n_samples)  
    X = X.T  
    t = np.squeeze(t)  
    return X, t  


dataMat, color = make_swiss_roll(n_samples=2000)  
lamda,f=laplaEigen(dataMat,11,5.0)  
fm,fn =np.shape(f)  
print 'fm,fn:',fm,fn  
lamdaIndicies = np.argsort(lamda)  
first=0  
second=0  
print lamdaIndicies[0], lamdaIndicies[1]  
for i in range(fm):  
    if lamda[lamdaIndicies[i]].real>1e-5:  
        print lamda[lamdaIndicies[i]]  
        first=lamdaIndicies[i]  
        second=lamdaIndicies[i+1]  
        break  
print first, second  
redEigVects = f[:,lamdaIndicies]  
fig=plt.figure('origin')  
ax1 = fig.add_subplot(111, projection='3d')  
ax1.scatter(dataMat[:, 0], dataMat[:, 1], dataMat[:, 2], c=color,cmap=plt.cm.Spectral)  
fig=plt.figure('lowdata')  
ax2 = fig.add_subplot(111)  
ax2.scatter(f[:,first].tolist(), f[:,second].tolist(), c=color, cmap=plt.cm.Spectral)  
plt.show()  

