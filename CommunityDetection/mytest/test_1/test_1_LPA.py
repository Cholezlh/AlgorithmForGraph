import sys
sys.path.append('../../')
sys.path.append('../../algorithm')
from algorithm import LPA
from util import graph_helper
import time
        
if __name__ == '__main__':
    G = graph_helper.load_graph('staticInOut1.csv')
    max_iter = 2000000   #默认200
    algorithm = LPA.LPA(G,max_iter)
    
    start = time.time()
    communities = algorithm.execute()
    end = time.time()
    print "Algorithm done in " + str(end-start) + "s."
    
    community_id = 1
    with open("vertices_LPA_1.csv",'w') as FILEOUT:
        print >>FILEOUT, "Id,commnuity_id"
        for cset in communities:
            for c in cset:
                print >>FILEOUT, str(c) + ","+ str(community_id)
            
            community_id = community_id + 1
    
    print "Done"
 