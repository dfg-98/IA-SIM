import networkx as nx
from matplotlib import pyplot as plt
from pyvis.network import Network
from simpy import Environment
from models.node import ConsumerNode, ProducerNode
from models.net import Net


nodes = [
    ProducerNode(0, max_production=500),
    ConsumerNode(1, min_consumption=10, max_consumption=20),
    ConsumerNode(2),
    ConsumerNode(3),
    ConsumerNode(4),
    ConsumerNode(5),
    ConsumerNode(6),
    ProducerNode(7),
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


# nx.draw_planar(G)
# plt.show()

env = Environment()
net = Net(G, 10000, env, with_visual=False)
env.process(net.run())

env.run(until=10)
