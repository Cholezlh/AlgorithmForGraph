# coding=utf-8
import string
import numpy as np

def loadData(filePath):
    f = open(filePath)
    vector_dict = {}
    edge_dict_out = {}
    edge_dict_in = {}
    edge_dict = {}
    
    for line in f.readlines():
        lines = line.strip().split(",")

        for i in xrange(2):
            if lines[i] not in vector_dict:
                #put the vector into the vector_dict
                vector_dict[lines[i]] = True
                
            if lines[i] not in edge_dict:
                #put the vector into the vector_dict
                vector_dict[lines[i]] = True   #True或者和其他什么都行，就是个占位用的，告诉我们vector_dict是个dict类型，这里推荐用collections.defaultdict(dict)
                #put the edges into the edge_dict
                edge_list = []
                #print len(lines)
                if len(lines) == 3:
                    edge_list.append(lines[1-i]+":"+lines[2])
                else:
                    edge_list.append(lines[1-i]+":"+"1")
                edge_dict[lines[i]] = edge_list
            else:
                edge_list = edge_dict[lines[i]]
                if len(lines) == 3:
                    edge_list.append(lines[1-i]+":"+lines[2])
                else:
                    edge_list.append(lines[1-i]+":"+"1")
                edge_dict[lines[i]] = edge_list
                              
        if lines[0] not in edge_dict_out:
            edge_list_out = []
            if len(lines) == 3:
                edge_list_out.append(lines[1]+":"+lines[2])
            else:
                edge_list_out.append(lines[1]+":"+"1")
            edge_dict_out[lines[0]] = edge_list_out
        else:
            edge_list_out = edge_dict_out[lines[0]]
            if len(lines) == 3:
                edge_list_out.append(lines[1]+":"+lines[2])
            else:
                edge_list_out.append(lines[1]+":"+"1")
            edge_dict_out[lines[0]] = edge_list_out
                         
        if lines[1] not in edge_dict_in:
            edge_list_in = []
            if len(lines) == 3:
                edge_list_in.append(lines[0]+":"+lines[2])
            else:
                edge_list_in.append(lines[0]+":"+"1")
            edge_dict_in[lines[1]] = edge_list_in
        else:
            edge_list_in = edge_dict_in[lines[1]]
            if len(lines) == 3:
                edge_list_in.append(lines[0]+":"+lines[2])
            else:
                edge_list_in.append(lines[0]+":"+"1")
            edge_dict_in[lines[1]] = edge_list_in
 
            
    return vector_dict, edge_dict_out, edge_dict_in, edge_dict

def modularity(vector_dict, edge_dict, edge_dict_out, edge_dict_in):
    Q = 0.0
    # m represents the total wight
    m = 0
    for i in edge_dict.keys():
        edge_list = edge_dict[i]  #每个edge_list是与节点i相连的节点列表
        for j in xrange(len(edge_list)):
            l = edge_list[j].strip().split(":")
            m += string.atof(l[1].strip())   #m是统计与节点i相连边的权重和

    # cal community of every vector
    #find member in every community
    community_dict = {}
    for i in vector_dict.keys():  #遍历每个节点    
    #例如倒数第二轮只有4个节点了，vector_dict是{'1': '0', '0': '0', '3': '2', '2': '2'}, vector_dict[i]只有两种取值0和2，将这两个逐步加到community_dict中去
        if vector_dict[i] not in community_dict:
            community_list = []
        else:
            community_list = community_dict[vector_dict[i]]   #类似['1', '0']   先取旧的后append形成新的
        
        community_list.append(i)
        community_dict[vector_dict[i]] = community_list
    #最终形成一个community_dict  {'0': ['1', '0'], '2': ['3']}   每个社团对应的节点标号（压缩后的节点标号）
    
    #cal inner link num and degree
    #innerLink_dict = {}
    for i in community_dict.keys():  #遍历每个社团
        sum_in = 0.0
        sum_tot_out = []
        sum_tot_in = []
        #vector num
        vector_list = community_dict[i]  #vector_list是社团i的节点列表
        #print "vector_list : ", vector_list
        
        #two loop cal inner link   计算sum_in：社区i内的边的权重之和
        if len(vector_list) == 1:   #如果社团只有1个节点
            tmp_list = edge_dict[vector_list[0]]
            tmp_dict = {}
            for link_mem in tmp_list:
                l = link_mem.strip().split(":")
                tmp_dict[l[0]] = l[1]
                
            if vector_list[0] in tmp_dict:
                sum_in = string.atof(tmp_dict[vector_list[0]])
            else:
                sum_in = 0.0
                
        else: #如果社团不止1个节点
            for j in xrange(0,len(vector_list)):
                link_list = edge_dict[vector_list[j]]
                tmp_dict = {}
                for link_mem in link_list:
                    l = link_mem.strip().split(":")
                    #split the vector and weight
                    tmp_dict[l[0]] = l[1]

                for k in xrange(0, len(vector_list)):
                    if vector_list[k] in tmp_dict:
                        sum_in += string.atof(tmp_dict[vector_list[k]])

        #cal degree
        for vec in vector_list:
            if vec in edge_dict_out.keys():
                link_list_out = edge_dict_out[vec]
                for i in link_list_out:
                    l = i.strip().split(":")
                    sum_tot_out.append(string.atof(l[1]))
                    
            if vec in edge_dict_in.keys():
                link_list_in = edge_dict_in[vec]
                for i in link_list_in:
                    l = i.strip().split(":")
                    sum_tot_in.append(string.atof(l[1]))  
          
        dot_inout_sum = 0.0    
        for i in sum_tot_out:
            for j in sum_tot_in:
                dot_inout_sum = dot_inout_sum + i*j 
                
        #print "dot_inout_sum is ", dot_inout_sum
        Q += ((sum_in / (2*m)) - (dot_inout_sum/((2*m)*(2*m))))
    return Q

def chage_community(vector_dict, edge_dict, Q):   #和chage_community组合使用，为每个节点分配社团
    vector_tmp_dict = {}
    for key in vector_dict:
        vector_tmp_dict[key] = vector_dict[key]

    #for every vector chose it's neighbor
    for key in vector_tmp_dict.keys():
        neighbor_vector_list = edge_dict[key]
        for vec in neighbor_vector_list:
            ori_com = vector_tmp_dict[key]
            vec_v = vec.strip().split(":")

            #compare the list_member with ori_com
            if vec_v[0] in vector_tmp_dict:
                if ori_com != vector_tmp_dict[vec_v[0]]:
                    vector_tmp_dict[key] = vector_tmp_dict[vec_v[0]]
                    Q_new = modularity(vector_tmp_dict, edge_dict, edge_dict_out, edge_dict_in)
                    #print Q_new
                    deltaQ = Q_new - Q
                    #print "deltaQ: ",deltaQ
                    if (deltaQ) > 0:   #保证最大max_deltaQ>0
                        Q = Q_new
                    else:
                        vector_tmp_dict[key] = ori_com
    return vector_tmp_dict, Q    #返回目前的vector_dict以及最新的Q

def modify_community(vector_dict):  #
    #modify the community
    community_dict = {}
    community_num = 0
    for community_values in vector_dict.values():
        if community_values not in community_dict:
            community_dict[community_values] = community_values
            community_num += 1
    for key in vector_dict.keys():
        vector_dict[key] = community_dict[vector_dict[key]]
    return community_num

def rebuild_graph(vector_dict, edge_dict, community_num):   #根据分配好的结果压缩社团
    vector_new_dict = {}
    edge_new_dict = {}
    # cal the inner connection in every community
    community_dict = {}
    for key in vector_dict.keys():
        if vector_dict[key] not in community_dict:
            community_list = []
        else:
            community_list = community_dict[vector_dict[key]]

        community_list.append(key)
        community_dict[vector_dict[key]] = community_list

    # cal vector_new_dict
    for key in community_dict.keys():
        vector_new_dict[str(key)] = str(key)

    # put the community_list into vector_new_dict

    #cal inner link num
    #innerLink_dict = {}
    for i in community_dict.keys():
        sum_in = 0.0
        #vector num
        vector_list = community_dict[i]
        #two loop cal inner link
        if len(vector_list) == 1:
            sum_in = 0.0
        else:
            for j in xrange(0,len(vector_list)):
                link_list = edge_dict[vector_list[j]]
                tmp_dict = {}
                for link_mem in link_list:
                    l = link_mem.strip().split(":")
                    #split the vector and weight
                    tmp_dict[l[0]] = l[1]
                for k in xrange(0, len(vector_list)):
                    if vector_list[k] in tmp_dict:
                        sum_in += string.atof(tmp_dict[vector_list[k]])

        inner_list = []
        inner_list.append(str(i) + ":" + str(sum_in))
        edge_new_dict[str(i)] = inner_list

    #cal outer link num
    community_list = community_dict.keys()
    for i in xrange(len(community_list)):
        for j in xrange(len(community_list)):
            if i != j:
                sum_outer = 0.0
                member_list_1 = []
                member_list_2 = []
                if community_list[i] in community_dict:
                    member_list_1 = community_dict[community_list[i]]
                if community_list[j] in community_dict:    
                    member_list_2 = community_dict[community_list[j]]

                for i_1 in xrange(len(member_list_1)):
                    tmp_dict = {}
                    tmp_list = edge_dict[member_list_1[i_1]]

                    for k in xrange(len(tmp_list)):
                        tmp = tmp_list[k].strip().split(":");
                        tmp_dict[tmp[0]] = tmp[1]
                    for j_1 in xrange(len(member_list_2)):
                        if member_list_2[j_1] in tmp_dict:
                            sum_outer += string.atof(tmp_dict[member_list_2[j_1]])

                if sum_outer != 0:
                    inner_list = edge_new_dict[str(community_list[i])]
                    inner_list.append(str(j) + ":" + str(sum_outer))
                    edge_new_dict[str(community_list[i])] = inner_list
    return vector_new_dict, edge_new_dict, community_dict

def fast_unfolding(vector_dict, edge_dict, edge_dict_out, edge_dict_in):
#1. initilization:put every vector into different communities
    #   the easiest way:use the vector num as the community num
    for i in vector_dict.keys():
        vector_dict[i] = i
    
    #print "vector_dict : ", vector_dict
    #print "edge_dict : ", edge_dict

    Q = modularity(vector_dict, edge_dict, edge_dict_out, edge_dict_in)  

#2. for every vector, chose the community
    Q_new = 0.0
    while (Q_new != Q):
        Q_new = Q
        vector_dict, Q = chage_community(vector_dict, edge_dict, Q)
    community_num = modify_community(vector_dict)

    print "Q = ", Q
    #print "vector_dict.key : ", vector_dict.keys()
    #print "vector_dict.value : ", vector_dict.values()
    Q_best = Q
    while (True):
#3. rebulid new graph, re_run the second step
        #print "edge_dict : ",edge_dict
        #print "vector_dict : ",vector_dict
        #print "\n rebuild"
        vector_dict, edge_new_dict, community_dict = rebuild_graph(vector_dict, edge_dict, community_num)
        #print vector_dict
#        print "community num is: : ", len(community_dict.keys())
#        print "community_dict : ", community_dict

##################### 重复步骤#2 #######################################################
        Q_new = 0.0
        while (Q_new != Q):
            Q_new = Q
            vector_dict, Q = chage_community(vector_dict, edge_new_dict, Q)
        community_num = modify_community(vector_dict)   
        #print community_num
        print "Q = ", Q
##################### 重复步骤#2 #######################################################
        
        if (Q_best == Q):  #没有变化，可以结束了
            break
        Q_best = Q
        vector_result = {}
        for key in community_dict.keys():
            value_of_vector = community_dict[key]
            for i in xrange(len(value_of_vector)):
                vector_result[value_of_vector[i]] = str(vector_dict[str(key)])
        for key in vector_result.keys():
            vector_dict[key] = vector_result[key]
        #print "vector_dict.key : ", vector_dict.keys()
        #print "vector_dict.value : ", vector_dict.values()

    #get the final result
    vector_result = {}
    for key in community_dict.keys():
        value_of_vector = community_dict[key]
        for i in xrange(len(value_of_vector)):
            vector_result[value_of_vector[i]] = str(vector_dict[str(key)])
    for key in vector_result.keys():
        vector_dict[key] = vector_result[key]
    print "Q_best : ", Q_best
    #print "vector_result.key : ", vector_dict.keys()
    #print "vector_result.value : ", vector_dict.values()
    return community_dict

if __name__ == "__main__":
    (vector_dict, edge_dict_out, edge_dict_in, edge_dict ) = loadData("staticInOut4_1.csv")
#    print "vector_dict", vector_dict   #{'1': True, '0': True, '3': True, '2': True,...}
#    print "edge_dict_out", edge_dict_out     #{'1': ['2:1', '4:1', '7:1'], '0': ['2:1', '3:1', '4:1', '5:1'],...}
#    print "edge_dict_in", edge_dict_in
#    print "edge_dict", edge_dict
    community_dict = fast_unfolding(vector_dict, edge_dict, edge_dict_out, edge_dict_in)
    with open("vertice_directedLouvain.csv",'w') as FILEOUT:
        for cid in community_dict.keys():
            vlist = community_dict[cid]
            for v in vlist:
                print >>FILEOUT,v.strip()+","+cid.strip()
        
    
    print "Done"