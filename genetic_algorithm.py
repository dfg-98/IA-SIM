import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

class GeneticAlgorithm:

    def __init__(self, population_lenght, iter_number, cost_matrix, get_fitness, beta = 1.6, alpha = 0.15, crossing_prob = 0.6, mutation_prob = 0.001, to_mutate = 1) -> None:
        self.cost_matrix = cost_matrix
        self.beta = beta
        self.crossing_prob = crossing_prob
        self.n_nodes = np.shape(cost_matrix)[0]
        self.population = []
        self.intermediate_population = []
        self.new_generation_chromos = []
        self.get_fitness = get_fitness
        self.mutation_prob = mutation_prob
        self.to_mutate = to_mutate
        self.iter_number = iter_number

        for i in range(population_lenght):
            graph = nx.erdos_renyi_graph(self.n_nodes, alpha)
            graph = self.add_edge_weigth(graph)
            chromo = self.get_chromosome(graph)
            self.population.append([graph, chromo, 0])

    
    def run(self):
        best_network = (nx.Graph(), [], 0)

        for i in range(self.iter_number):
            self.calculate_population_fitnesses()
            best_of_iter = max(self.population, key=lambda x: x[2])

            if best_of_iter[2] > best_network[2]:
                best_network = best_of_iter

            self.reproduction()
            self.crossing()
            self.mutation()

            new_generation = []

            for chromo in self.new_generation_chromos:
                graph = self.build_from_chromosome(chromo)
                graph = self.add_edge_weigth(graph)
                new_generation.append([graph, chromo, 0])

            self.population = new_generation

        return best_network


    def reproduction(self): #TODO check if this work fine because the indexes of the population 
        p_max = self.beta / len(self.population)
        p_min = (2 - self.beta) / len(self.population)
        n = len(self.population)
        intermediate_population = []

        for i in range(n):
            p_i = p_min + (p_max - p_min)*((n - (i+1))/(n - 1))

            p = p_i * n

            if p >= 1.5: #duplicate the graph
                intermediate_population.append(self.population[i])
                intermediate_population.append(self.population[i])

            if p >= 0.5 and p < 1.5: #mantain the graph
                intermediate_population.append(self.population[i])

        self.intermediate_population = intermediate_population #TODO check the lenght of the final population
        

    def crossing(self):
        n = len(self.intermediate_population)
        population_chromosomes = [graph[1] for graph in self.intermediate_population]
        population_pairs = []
        crossed_population = []
        selected_population_pairs = []

        for i in range(n):
            for j in range(i+1, n):
                population_pairs.append((population_chromosomes[i], population_chromosomes[j]))

        for i in range(len(population_pairs)):
            p = random.uniform(0, 1)
            if p < self.crossing_prob:
                selected_population_pairs.append(population_pairs[i])

        for parent1, parent2 in selected_population_pairs:
            gen_len = len(parent1)
            crossing_index = random.randint(0, gen_len - 1)

            child1 = []
            child1.extend(parent1[0:crossing_index])
            child1.extend(parent2[crossing_index:gen_len])

            child2 = []
            child2.extend(parent2[0:crossing_index])
            child2.extend(parent1[crossing_index:gen_len])

            crossed_population.append(child1)
            crossed_population.append(child2)

        self.new_generation_chromos = crossed_population
    
    
    def mutation(self):
        for i in range(len(self.new_generation_chromos)):
            p = random.uniform(0, 1)

            if p < self.mutation_prob:
                chromo_len = len(self.new_generation_chromos[0])
                index = random.randint(0, chromo_len - 1)
                self.new_generation_chromos[i][index] = not self.new_generation_chromos[i][index]


    def calculate_population_fitnesses(self):
        for i in range(len(self.population)):
            fitness = self.get_fitness(self.population[i][0])
            self.population[i][2] = fitness

        self.population.sort(key= lambda x: x[2], reverse=True)     


    def  add_edge_weigth(self, graph : nx.Graph):
        for u, v in graph.edges():
            graph[u][v]['weight'] = self.cost_matrix[u][v]

        return graph


    def get_chromosome(self, graph : nx.Graph):
        chromosome = [False for i in range(self.n_nodes**2)]

        for u, v in graph.edges():
            index = self.get_flattened_index(u, v)
            chromosome[index] = True

        return chromosome


    def build_from_chromosome(self, chromosome):
        graph = nx.Graph()
        vertex_number = np.shape(self.cost_matrix)[0] 

        for i in range(vertex_number):
            graph.add_node(i)

        for i in range(len(chromosome)):
            if chromosome[i]:
                u, v = self.get_matrix_indexes(i)
                graph.add_edge(u, v)

        return graph


    def get_matrix_indexes(self, flattened_index):
        row = flattened_index // self.n_nodes
        col = flattened_index % self.n_nodes

        return row, col

    
    def get_flattened_index(self, row, col):
        return row * self.n_nodes + col



distances = np.array([[np.inf, 2, 2, 5, 7],

                      [2, np.inf, 4, 8, 2],

                      [2, 4, np.inf, 1, 3],

                      [5, 8, 1, np.inf, 2],

                      [7, 2, 3, 2, np.inf]]) 

def provisional_fitnees(graph:nx.Graph):
    fitness = 0
    for u,v,w in graph.edges().data('weight'):
        fitness += w
    return fitness

genetic_algorithm = GeneticAlgorithm(3, 5, distances, provisional_fitnees)

sol = genetic_algorithm.run()

print(sol[0].edges())