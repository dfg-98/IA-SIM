import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, costs, n_ants, n_iterations, decay, alpha=1, beta=0.5, delta_tau = 2):
        self.costs  = costs
        self.pheromone = np.zeros(self.costs.shape)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.delta_tau = delta_tau
        
    def run(self):
        '''
        Return a list of tuples (T,C) where T is a list of tree edges, extracted from graph cost, and C is
        the cost of the Tree defined by T. 
        '''

        min_cost_tree = None
        list_of_trees = []
        
        for i in range(self.n_iterations):
            all_trees = self.gen_all_trees()
            self.spread_pheronome(all_trees)
            min_cost_tree = min(all_trees, key=lambda x: x[1])
            list_of_trees.append(min_cost_tree)
            self.evaporate_pheromone()

        list_of_trees.sort(key= lambda x : x[1])
            
        return list_of_trees

    def spread_pheronome(self, all_trees):
        for tree in all_trees:
            for edge in tree[0]:
                self.pheromone[edge[0], edge[1]] += self.delta_tau 

        return None

    def tree_cost(self, tree):
        cost = 0

        for i in range(len(tree)):
            cost += self.costs[tree[i][0], tree[i][1]]

        return cost

    def gen_all_trees(self):
        all_trees = []
        for i in range(self.n_ants):
            tree = self.gen_tree(0)
            all_trees.append((tree, self.tree_cost(tree)))
        return all_trees

    def gen_tree(self, start):
        tree_edges = []
        n_nodes = np.shape(self.costs)[0]
        visited = [True] + [False for i in range(n_nodes - 1)]

        while visited.__contains__(False):
            neighbor_pheromons = self.pheromone[start]
            neighbor_distance = self.costs[start]
            numerators = [neighbor_pheromons[i]**self.alpha + 1/neighbor_distance[i]**self.beta for i in range(n_nodes)]
            numerators[start] = 0
            denominator = np.sum(numerators)
            probabilities = [i/denominator for i in numerators]
            move = np_choice(range(n_nodes), p = probabilities)

            if not visited[move]:
                tree_edges.append((start, move))
                visited[move] = True

            start = move

        return tree_edges

    def evaporate_pheromone(self):
        for i in self.pheromone:
            i = i * self.decay

        return None