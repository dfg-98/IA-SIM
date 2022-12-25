import networkx as nx
import numpy as np

class genetic_algorithm:

    def __init__(self, population_lenght, cost_matrix, get_fitness, beta = 1.6, alpha = 0.15) -> None:
        self.cost_matrix = cost_matrix
        self.beta = beta
        self.n_nodes = np.shape(cost_matrix)[0]
        self.population = []
        self.gen_list = []
        self.get_fitness = get_fitness
        self.population_fitnesses = []

        for i in range(population_lenght):
            graph = nx.erdos_renyi_graph(self.n_nodes, alpha)
            graph = self.add_edge_weigth(graph)
            gen = self.get_gen(graph)
            self.population.append((graph, gen, 0))


    def reproduction(self): #TODO check if this work fine because the indexes of the population 
        p_max = self.beta / len(self.population)
        p_min = (2 - self.beta) / len(self.population)
        n = len(self.population)
        intermediate_population = []
        p_selection = [] 

        for i in range(n):
            p_i = p_min + (p_max - p_min)*((n - i)/(n - 1))

            p = p_i * n

            if p >= 1.5: #duplicate the graph
                intermediate_population.append(self.population[i])
                intermediate_population.append(self.population[i])

            if p >= 0.5 and p < 1.5: #mantain the graph
                intermediate_population.append(self.population[i])

        self.population = intermediate_population
        




    def calculate_population_fitnesses(self):
        for item in self.population:
            fitness = self.get_fitness(item[0])
            item[2] = fitness

        self.population.sort(key= lambda x: x[2], reverse=True)     


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

a = [3, 5, 6, 6, 4]
a.sort()
print(a)