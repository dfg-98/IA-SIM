import networkx as nx
import numpy as np

class genetic_algorithm:

    def __init__(self, population_lenght, cost_matrix, beta = 1.6, alpha = 0.15) -> None:
        self.cost_matrix = cost_matrix
        self.beta = beta
        self.n_nodes = np.shape(cost_matrix)[0]
        self.population = []

        for i in range(population_lenght):
            graph = nx.erdos_renyi_graph(self.n_nodes, alpha)
            graph = self.add_edge_weigth(graph)
            self.population.append(graph)


    def  add_edge_weigth(self, graph : nx.Graph):
        for u, v in graph.edges():
            graph[u][v]['weight'] = self.cost_matrix[u][v]

        return graph


    def get_gen(self, graph : nx.Graph):
        gen = [False for i in range(self.n_nodes**2)]

        for u, v in graph.edges():
            index = self.get_flattened_index(u, v)
            gen[index] = True

        return gen


    def get_matrix_indexes(self, flattened_index):
        row = flattened_index // self.n_nodes
        col = flattened_index % self.n_nodes

        return row, col

    
    def get_flattened_index(self, row, col):
        return row * self.n_nodes + col



# graph = nx.erdos_renyi_graph(5, 0.15)
# print(graph.edges()) 
# for u,v in graph.edges():
#     print(u)
#     print(v)  

print(not 0)