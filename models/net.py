import logging
from typing import List
from simpy import Environment
from networkx import Graph, draw_planar
from matplotlib import pyplot as plt
from networkx.algorithms.traversal import bfs_successors
from .node import Node, ConsumerNode, ProducerNode

log = logging.getLogger()


class Net:
    def __init__(
        self, graph: Graph, initial_resources, env: Environment, with_visual=False
    ) -> None:
        super().__init__()
        self.graph = graph
        self.resources = initial_resources
        self.env = env
        self.score = 0.0
        self.steps = 0
        self.with_visual = with_visual

    def refresh(self):
        self.assign_resources()
        self.set_consumption()

    def assign_resources(self):
        for node in self.graph.nodes:
            if isinstance(node, ProducerNode) and self.resources > 0:
                resources = self.get_resources_to_assign(node)
                remainder = node.add_resources(resources)
                self.resources += remainder
                self.resources -= resources

    def set_consumption(self):
        for node in self.graph.nodes:
            if isinstance(node, ConsumerNode):
                node.set_consumption()

    def collect_resources(self):
        self.resources += sum(node.collect_resources() for node in self.graph.nodes)

    def resource_flow(self):
        producers = self.producer_nodes

        for producer in producers:
            power = producer.produce(self.estimate_production(producer))
            print(f"Produced {power} by node {producer.id}")
            for __unused, successors in bfs_successors(self.graph, producer):
                for successor in successors:
                    if isinstance(successor, ConsumerNode):
                        power = successor.feed(power)
                        print(f"Fed node {successor.id}. Remaining power: {power}")
                        if power <= 0:
                            break
                if power <= 0:
                    break

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

    def score_network(self):
        score = 0
        for node in self.consumer_nodes:
            if node.status == ConsumerNode.Status.ON:
                score += 1.0
            elif node.status == ConsumerNode.Status.PARTIAL:
                score += 0.5
        score = score / len(self.consumer_nodes)
        self.score = (self.score * self.steps + score) / (self.steps + 1)
        self.steps += 1

    def draw(self):
        sizes = [node.size() for node in self.graph.nodes]
        colors = [node.color() for node in self.graph.nodes]
        plt.clf()

        draw_planar(self.graph, node_size=sizes, node_color=colors)
        plt.show()

    def estimate_production(self, node: ProducerNode):
        return node.max_production

    def get_resources_to_assign(self, node: ProducerNode):
        """Returns the resources to assign to a node based on the current resources"""

        # TODO: This is a very naive implementation.
        return self.resources / len(self.producer_nodes)

    @property
    def producer_nodes(self) -> List[ProducerNode]:
        return [node for node in self.graph.nodes if isinstance(node, ProducerNode)]

    @property
    def consumer_nodes(self) -> List[ConsumerNode]:
        return [node for node in self.graph.nodes if isinstance(node, ConsumerNode)]


def build_graph_from_nodes(nodes, graph):
    g = Graph()
    for node in nodes:
        g.add_node(node)
    for edge in graph.edges:
        x, y = edge[0], edge[1]
        g.add_edge(nodes[x], nodes[y])
    return g
