import networkx as nx
import matplotlib.pyplot as plt
import sys
import community
import operator

def set_partition(G,partition,n):
    partition[n]=n
    for node in G.neighbors(n):
        partition[node] = n

def best_partition(G):
    # partition:
    #   A dictionary where keys are the nodes and the values are the set it belongs to
    partition={}
    for node in G.nodes():
        partition[node]=1
    n_edges=G.size() # number of edges
    best=-1
    for i in xrange(n_edges-1):
        # edges_betweenness:
        #   Dictionary of edges with betweenness centrality as the value
        edges_betweenness=nx.edge_betweenness_centrality(G)
        to_remove=max(edges_betweenness.iteritems(), key=operator.itemgetter(1))[0]
        G.remove_edge(to_remove[0],to_remove[1])
        set_partition(G,partition,to_remove[0])
        set_partition(G,partition,to_remove[1])
        current=community.modularity(partition, G)
        if current>best:
            best=current
            best_partition=partition.copy()
    return best_partition

def main():
    G=nx.Graph()
    fn=sys.argv[1]
    image_name=sys.argv[2]
    with open(fn,'r') as f:
        for line in f:
            line=line.strip().split()
            G.add_edge(int(line[0]),int(line[1]))
    #first compute the best partition
    partition = best_partition(G.copy())
    #drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        print list_nodes
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 500, node_color = str(count / size))
    nx.draw_networkx_edges(G,pos, alpha=0.5)
    plt.show()
    plt.savefig(image_name)

if __name__ =='__main__':
    main()
