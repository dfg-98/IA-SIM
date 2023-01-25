import numpy as np


class GenerationEstimatorAgent:
    def __init__(self, net, production_step=10) -> None:
        self.net = net
        self.production_step = production_step
        self.productions = [
            {node.id: node.max_generation for node in net.generator_nodes}
        ]

    def calculate_estimations(self):
        last_productions = self.productions[-1]
        remainders = self.net.reminders[-1]
        self.productions.append({})

        for node in self.net.generator_nodes:
            node_remainder = remainders[node.id]
            node_last_production = last_productions[node.id]
            node_production = node_last_production
            if node_remainder >= 0.0:
                node_production = max(
                    0.0,
                    np.random.uniform(
                        node_last_production - self.production_step,
                        node_last_production,
                    ),
                )
            else:
                node_production = min(
                    node.max_production,
                    np.random.uniform(
                        node_last_production,
                        node_last_production + self.production_step,
                    ),
                )
            self.productions[-1][node.id] = node_production

    def estimate(self, node):
        return self.productions[-1][node.id]
