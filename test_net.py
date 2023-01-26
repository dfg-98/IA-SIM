import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from pyvis.network import Network
from simpy import Environment
from models.consumers import ConsumerNode, MinMaxConsumerNode, TurnBasedConsumerNode
from models.producers import ResourceProducerNode
from models.generators import GeneratorNode
from models.node_parser import write_json
from models.net import Net


nodes = [
    GeneratorNode(0, max_generation=1000, repair_cost_rate=1),
    ConsumerNode(1, min_consumption=10, max_consumption=20),
    ConsumerNode(2),
    ConsumerNode(3),
    ConsumerNode(4),
    ConsumerNode(5),
    ConsumerNode(6),
    GeneratorNode(7),
    ResourceProducerNode(8),
    ResourceProducerNode(9),
    MinMaxConsumerNode(10, min=10, max=30),
    TurnBasedConsumerNode(11, mean_consumption=500, on_turns=2, off_turns=1),
    GeneratorNode(12, max_generation=500, repair_cost_rate=0.5),
]

G = nx.Graph()
for node in nodes:
    G.add_node(node)
G.add_edge(nodes[0], nodes[1])
G.add_edge(nodes[0], nodes[2])
G.add_edge(nodes[0], nodes[3])
G.add_edge(nodes[2], nodes[3])
G.add_edge(nodes[2], nodes[4])
G.add_edge(nodes[5], nodes[6])
G.add_edge(nodes[4], nodes[6])
G.add_edge(nodes[7], nodes[2])
G.add_edge(nodes[8], nodes[3])
G.add_edge(nodes[9], nodes[3])
G.add_edge(nodes[10], nodes[0])
G.add_edge(nodes[11], nodes[0])
G.add_edge(nodes[12], nodes[0])


nx.draw_planar(G)
plt.show()

env = Environment()
net = Net(G, 10000, env, with_visual=False)
env.process(net.run())

env.run(until=10)

weights = np.zeros((13, 13))


write_json(net.graph.nodes, weights, "test.json")
