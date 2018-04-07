import sys
sys.path.append('../../')
from algorithm import Louvain
import time

if __name__ == '__main__':
    G = Louvain.load_graph('staticInOut1.csv')
    algorithm = Louvain.Louvain(G)
    
    start = time.time()
    communities = algorithm.execute()
    end = time.time()
    print "Algorithm done in " + str(end-start) + "s."
    
    community_id = 1
    with open("vertices_1.csv",'w') as FILEOUT:
        for cset in communities:
            for c in cset:
                print >>FILEOUT,c,",",community_id
            
            community_id = community_id + 1
    
    print "Done"