import numpy as np
import logging
from typing import List
from simpy import Environment
from networkx import Graph, draw_planar, draw_shell
from matplotlib import pyplot as plt
from networkx.algorithms.traversal import bfs_successors
from .node import HealthNode
from .consumers import ConsumerNode
from .generators import GeneratorNode
from .generation_estimation import GenerationEstimatorAgent

log = logging.getLogger()


class Net:
    def __init__(
        self,
        graph: Graph,
        env: Environment,
        initial_resources=1000,
        with_visual=False,
        edge_damage_rate=1,
        edge_reparation_cost=10,
    ) -> None:
        super().__init__()
        self.graph = graph
        self.resources = initial_resources
        self.env = env
        self.score = 0.0
        self.steps = 0
        self.with_visual = with_visual
        self.edge_damage_rate = edge_damage_rate
        self.edge_reparation_cost = edge_reparation_cost
        self.reminders = []
        self.estimator_agent = GenerationEstimatorAgent(self)

    def refresh(self):
        self.assign_resources()
        self.set_consumption()
        self.repair()

    def post_step(self):
        self.estimator_agent.calculate_estimations()

    def assign_resources(self):
        for node in self.graph.nodes:
            if isinstance(node, GeneratorNode) and self.resources > 0:
                resources = self.get_resources_to_assign(node)
                remainder = node.add_resources(resources)
                self.resources += remainder
                self.resources -= resources

    def set_consumption(self):
        for node in self.graph.nodes:
            if isinstance(node, ConsumerNode):
                node.set_consumption()

    def repair(self):
        for edge in self.graph.edges():
            if self.resources <= 0:
                break
            self.resources = self.repair_edge(edge[0], edge[1], self.resources)
        for node in self.health_nodes:
            if self.resources <= 0:
                break
            self.resources = node.repair(self.resources)

    def repair_edge(self, node1, node2, resources):
        income_health = resources / self.edge_reparation_cost
        edge = self.graph[node1][node2]
        needed_healh = 100.0 - edge["health"]
        if income_health > needed_healh:
            edge["health"] = 100.0
            resource_cost = (income_health - needed_healh) * self.edge_reparation_cost
            remainder = resources - resource_cost
            return remainder

        edge["health"] += income_health
        edge["fails"] = 0
        return 0.0

    def collect_resources(self):
        resources = sum(node.collect_resources() for node in self.graph.nodes)
        self.resources += resources

    def resource_flow(self):
        producers = self.generator_nodes
        self.reminders.append({})

        for producer in producers:
            power = producer.produce(self.estimate_production(producer))
            print(f"Produced {power} by node {producer.id}")
            for node, successors in bfs_successors(self.graph, producer):
                for successor in successors:
                    if isinstance(successor, ConsumerNode):
                        if self.allow_edge(node, successor):
                            current_power = power
                            power = successor.feed(power)
                            # print(f"Fed node {successor.id}. Remaining power: {power}")
                            consumed = current_power - power
                            damage = consumed / self.edge_damage_rate
                            self.graph[node][successor]["health"] -= damage
                        else:
                            self.graph[node][successor]["fails"] -= 1

                        if power <= 0:
                            break
                if power <= 0:
                    break
            self.reminders[-1][producer.id] = power

    def run(self):
        while True:
            self.refresh()

            self.resource_flow()

            print("Simulation time: ", self.env.now)
            if self.with_visual:
                self.draw()
            yield self.env.timeout(1)
            self.collect_resources()
            self.score_network()
            print("Resources: ", self.resources)
            print("Score: ", self.score)
            self.post_step()

    def allow_edge(self, node1, node2):
        p = np.random.uniform(0.0, 1.0) ** 2
        p *= 100
        return self.graph[node1][node2]["health"] > p

    def score_network(self):
        score = 0
        for node in self.consumer_nodes:
            if node.status == ConsumerNode.Status.ON:
                score += 1.0
        health_score = 0
        for node in self.health_nodes:
            health_score += node.health / 100.0
        health_score = health_score / len(self.health_nodes)
        score = score / len(self.consumer_nodes)
        score = score * health_score
        self.score = (self.score * self.steps + score) / (self.steps + 1)
        self.steps += 1

    def draw(self):
        sizes = [node.size() for node in self.graph.nodes]
        colors = [node.color() for node in self.graph.nodes]
        labels = {node: node.id for node in self.graph.nodes}
        plt.clf()

        draw_shell(self.graph, node_size=sizes, node_color=colors, labels=labels)
        plt.show()

    def estimate_production(self, node: GeneratorNode):
        return self.estimator_agent.estimate(node)

    def get_resources_to_assign(self, node: GeneratorNode):
        """Returns the resources to assign to a node based on the current resources"""

        # TODO: This is a very naive implementation.
        return self.resources / len(self.generator_nodes)

    @property
    def generator_nodes(self) -> List[GeneratorNode]:
        return [node for node in self.graph.nodes if isinstance(node, GeneratorNode)]

    @property
    def consumer_nodes(self) -> List[ConsumerNode]:
        return [node for node in self.graph.nodes if isinstance(node, ConsumerNode)]

    @property
    def health_nodes(self) -> List[HealthNode]:
        return [node for node in self.graph.nodes if isinstance(node, HealthNode)]


def build_graph_from_nodes(nodes, graph):
    g = Graph()
    for node in nodes:
        g.add_node(node)
    for edge in graph.edges:
        x, y = edge[0], edge[1]
        g.add_edge(nodes[x], nodes[y], health=100.0, fails=0)
    return g
