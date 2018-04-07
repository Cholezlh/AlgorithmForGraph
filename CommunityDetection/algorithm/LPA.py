# -*- coding: utf-8 -*-
from __future__ import division  #整形相除得到float ，否则要这样写float(float(changed)/float(self._n))
import collections
import random
import networkx as nx
import numpy as np


'''
paper : <<Near linear time algorithm to detect community structures in large-scale networks>>
'''

class LPA():
    
    def __init__(self, G, max_iter = 200, tol = 1e-3):
        self._G = G
        self._n = len(G.node) #number of nodes
        self._max_iter = max_iter
        self.tol = tol
        
    def can_stop(self):
        # all node has the label same with its most neighbor
        #for i in range(self._n):
        for i in self._G.node:
            node = self._G.node[i]
            label = node["label"]
            max_labels = self.get_max_neighbor_label(i)
            if(label not in max_labels):
                return False
        return True
        
    def stop_tol(self):
        # all node has the label same with its most neighbor
        #for i in range(self._n):
        for i in self._G.node:
            node = self._G.node[i]
            label = node["label"]
            max_labels = self.get_max_neighbor_label(i)
            if(label not in max_labels):
                return False
        return True    
        
    def get_max_neighbor_label(self,node_index):    #get the max_neighbor_label for node of node_index
        m = collections.defaultdict(int)  #  http://www.tuicool.com/articles/YbmYbyf
        for neighbor_index in self._G.neighbors(node_index):  #neighbors 是 networkx的函数   该for循环是对节点node_index的所有邻居的标签数进行统计
            neighbor_label = self._G.node[neighbor_index]["label"]
            m[neighbor_label] += 1
        max_v = max(m.itervalues())   #itervalues返回dict的value的迭代器
        return [item[0] for item in m.items() if item[1] == max_v]   #返回节点node_index标签类别最多的邻居的类别的列表（因为可能有多个类别同时具有最大类别数max_v）

    
    '''asynchronous update'''
    def populate_label(self):
        #random visit
        visitSequence = random.sample(self._G.nodes(),len(self._G.nodes()))  #random.sample(sequence, k)，从指定序列中随机获取指定长度的片断。
        for i in visitSequence:
            node = self._G.node[i]
            label = node["label"]
            max_labels = self.get_max_neighbor_label(i)
            if(label not in max_labels):
                newLabel = random.choice(max_labels)
                node["label"] = newLabel
        
    def get_communities(self):
        communities = collections.defaultdict(lambda:list())
        for node in self._G.nodes(True):     #True表示返回节点带标签
            label = node[1]["label"]
            communities[label].append(node[0])
        return communities.values()

    def execute(self):
        #initial label
        #for i in range(self._n):    这样写有问题，原始列表中可能不包含名称为0的节点
        for i in self._G.node:
            self._G.node[i]["label"] = i
        
        iter_time = 0
        
        oldlabels = np.zeros(len(self._G.node), np.int32) 
        newlabels = np.zeros(len(self._G.node), np.int32) 
        diffarray = np.zeros(len(self._G.node), np.int32)         
        changeRatio = 1        
        
        #populate label
        while(not self.can_stop() and iter_time < self._max_iter and changeRatio>self.tol):
            oldlabels = newlabels
            self.populate_label()
            newlabels = np.array([item[1]["label"] for item in self._G.nodes(True)])
            diffarray = newlabels - oldlabels           
            changed = np.abs([bool(i) for i in diffarray]).sum()
            changeRatio =  changed/self._n
            #print changeRatio
            iter_time += 1
        return self.get_communities()
    
    
if __name__ == '__main__':
    G = nx.karate_club_graph()
    algorithm = LPA(G)     
#    max_iter = 2000   #默认200
#    algorithm = LPA(G,max_iter)
    
    communities = algorithm.execute()
    for community in communities:
        print community