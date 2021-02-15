# A Kneser graph (K(n,m)) is a graph whose vertices correspond to the m element subsets of a set containing n elements.
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class Kneser_graph():
    def __init__(self, elements, choose):
        # create main set from which we take all subsets
        self.elements={x for x in range(elements)}
        self.choose=choose
        # create the set of all subsets of the main set which contain self.choose elements
        self.vertices = {x:[] for x in combinations(self.elements, self.choose)}
        
        # build edges if two vertices are disjoint
        for x in self.vertices:
            for y in self.vertices:
                if y in self.vertices[x]:
                    pass
                else:
                    for elem in x:
                        if elem in y:
                            nogo = True
                            break
                        nogo = False
                    if nogo == False:
                        self.vertices[x].append(y)
                        self.vertices[y].append(x)

    # helper function to calculate disjoints quickly
    def is_disjoint(self,item1,item2):
        if item1 < item2:
            small, large = item1, item2
        else:
            large, small = item1, item2

        for element in small:
            if element in large:
                return False

        return True

    # find the first path from an arbitrary node to itself. We do this via breadth first search
    # which guarantees that the first path found is shortest. 
    def shortest_cycle(self, starting_vertex = None):
        if starting_vertex == None:
            starting_vertex = list(self.vertices.keys())[0]
        # assign all nodes a path from the start to that node 
        paths = {starting_vertex:[starting_vertex]}
        queue = [starting_vertex]
        while queue:
            current = queue.pop(0)
            for neighbor in self.vertices[current]:
                # if two nodes have been covered and share an edge, check if their paths
                # intersect at all, if they don't, this is a shortest cycle
                if neighbor in paths:
                    if (len(paths[neighbor]) >= 2 and len(paths[current]) >= 2) and self.is_disjoint(paths[neighbor][1:], paths[current][1:]) == True:
                        
                        return (paths[neighbor] + list(reversed(paths[current][1:])))
                    else:
                        pass
                else:
                    paths[neighbor] = paths[current] + [neighbor]
                    queue.append(neighbor)

        return 'no cycles exist'

    # recursive 
    def traverse(self, starting_vertex = None, parents = {}):
        if starting_vertex == None:
            starting_vertex = list(self.vertices.keys())[0]
        for node in self.vertices[starting_vertex]:
            if node not in parents:
                parents[node] = starting_vertex
                self.traverse(node, parents)
            else:
                pass
        return parents
            
    
    def is_connected(self):
        parents = self.traverse()
        if parents.keys() == self.vertices.keys():
            return True
        else:
            return False
                  
        
    
    
    def show_graph(self, show_shortest=False, show_connected=False):
        g = nx.from_dict_of_lists(self.vertices)
        pos = nx.circular_layout(g)
        if show_connected==True:
            if self.is_connected() == False:
                print('the graph is not connected!')
            else:
                parents = self.traverse()
                spanning_tree_edges = [(node, parents[node]) for node in parents.keys()]
                nx.draw_networkx_nodes(g, pos, nodelist = [node for node in parents.keys()]) 
                nx.draw_networkx_edges(g, pos, edgelist=spanning_tree_edges, edge_color='g')
        if show_shortest==True:
            cycle=self.shortest_cycle()
            short_cycle_edges = [(cycle[i],cycle[i+1]) for i in range(len(cycle)-1)] + [(cycle[-1], cycle[0])]
            nx.draw_networkx_nodes(g,pos, node_color='black',nodelist=one.shortest_cycle())
            nx.draw_networkx_edges(g,pos,edgelist=short_cycle_edges, edge_color='g')
        if not (show_connected):
            nx.draw(g,pos, with_labels=0,node_color='b', edge_color='orange')
        plt.show()
    

