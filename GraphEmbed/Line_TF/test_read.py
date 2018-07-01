import numpy as np
from utils import DBLPDataLoader
 

def main():
    train()


def train():
    data_loader = DBLPDataLoader(graph_file='data/co-authorship_graph.pkl')
    print(data_loader.g.number_of_nodes())
    print(data_loader.g.number_of_edges())
    print(data_loader.g.edges(data=True)[:5])
    #[('Siddartha Y. Ramamohan', 'Shivani Agarwal 0001', {'weight': 1}), ('Siddartha Y. Ramamohan', 'Arun Rajkumar', {'weight': 1}), ('Alexandra J. Golby', 'Carl-Fredrik Westin', {'weight': 1}), ('Alexandra J. Golby', 'Georg Langs', {'weight': 1}), ('Alexandra J. Golby', 'Arish A. Qazi', {'weight': 1})]
    for b in range(2):
        u_i, u_j, label = data_loader.fetch_batch(batch_size=16, K=5)
        print(len(u_i), len(u_j), len(label))  #shape=[args.batch_size * (args.K + 1)    negative sample  K 个负例， 1个正例             96 96 96 
        print(u_i, u_j, label)
    

if __name__ == '__main__':
    main()