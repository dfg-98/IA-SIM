import json
import numpy as np
from .node import HealthNode
from .consumers import ConsumerNode, MinMaxConsumerNode, TurnBasedConsumerNode
from .generators import GeneratorNode
from .producers import ResourceProducerNode


def write_json(nodes, weights, path):
    nodes = [node.to_json() for node in nodes]
    weights = [
        {
            "node1": x,
            "node2": y,
            "weight": "inf" if weights[x][y] == np.inf else weights[x][y],
        }
        for x in range(len(nodes))
        for y in range(len(nodes))
    ]
    with open(path, "w") as f:
        json.dump({"nodes": nodes, "weights": weights}, f)


def parse_node(node):

    types = {
        "Consumer": ConsumerNode,
        "Generator": GeneratorNode,
        "Health": HealthNode,
        "ResourceProducer": ResourceProducerNode,
        "MinMaxConsumer": MinMaxConsumerNode,
        "TurnBasedConsumer": TurnBasedConsumerNode,
    }

    if node["type"] in types:
        return types[node["type"]](**node)

    else:
        raise ValueError(f"Unknown node type {node['type']}")


def load_from_json(path):

    with open(path, "r") as f:
        data = json.load(f)
        nodes = [parse_node(node) for node in data["nodes"]]
        weights = np.zeros((len(nodes), len(nodes)))
        for weight in data["weights"]:
            value = np.inf if weight["weight"] == "inf" else weight["weight"]
            weights[weight["node1"], weight["node2"]] = value

    return nodes, weights
