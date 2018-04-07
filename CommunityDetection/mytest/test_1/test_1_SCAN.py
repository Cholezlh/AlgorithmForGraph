import sys
sys.path.append('../../')
sys.path.append('../../algorithm')
from algorithm import SCAN
from util import graph_helper
import time
        
if __name__ == '__main__':
    G = graph_helper.load_graph('staticInOut1.csv')
    algorithm = SCAN.SCAN(G, 0.1, 3)
    
    start = time.time()
    communities = algorithm.execute()
    end = time.time()
    print "Algorithm done in " + str(end-start) + "s."
    
    community_id = 1
    with open("vertices_SCAN_1.csv",'w') as FILEOUT:
        print >>FILEOUT, "Id,commnuity_id"
        for cset in communities:
            for c in cset:
                print >>FILEOUT, str(c) + ","+ str(community_id)
            
            community_id = community_id + 1
    
    hubs_outliers = algorithm.get_hubs_outliers(communities)
    print 'hubs: ', hubs_outliers[0]
    print 'outliers: ', hubs_outliers[1]
    
    print "Done"
 