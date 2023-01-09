from enum import Enum
import numpy as np


class Node:
    def __init__(self, id) -> None:
        self.id = id

    def collect_resources(self):
        return 0

    def color(self):
        raise NotImplemented

    def size(self):
        return 100

    def to_json(self):
        raise NotImplemented


class ConsumerNode(Node):
    class Status(Enum):
        OFF = 0
        PARTIAL = 2
        ON = 1

    def __init__(self, id, min_consumption=30.0, max_consumption=50.0) -> None:
        super().__init__(id)
        self.min_consumption = min_consumption
        self.max_consumption = max_consumption
        self.status = ConsumerNode.Status.OFF
        self.current_consumption = 0.0

    def set_consumption(self):
        consumption = np.random.uniform(
            low=self.min_consumption, high=self.max_consumption
        )
        self.current_consumption = consumption
        self.status = ConsumerNode.Status.OFF
        return consumption

    def feed(self, power):
        if power > self.current_consumption:
            self.status = ConsumerNode.Status.ON
            reminder = power - self.current_consumption
            self.current_consumption = 0.0
            return reminder
        if 0 < power <= self.current_consumption:
            self.status = ConsumerNode.Status.PARTIAL
            self.current_consumption -= power
        else:
            self.status = ConsumerNode.Status.OFF
        return 0.0

    def color(self):
        if self.status == ConsumerNode.Status.OFF:
            return "red"
        elif self.status == ConsumerNode.Status.PARTIAL:
            return "orange"
        elif self.status == ConsumerNode.Status.ON:
            return "green"

    def size(self):
        return 500

    def to_json(self):
        return {
            "id": self.id,
            "type": "Consumer",
            "min_consumption": self.min_consumption,
            "max_consumption": self.max_consumption,
        }


class ProducerNode(Node):
    def __init__(
        self,
        id,
        max_production=100.0,
        production_rate=1.0,
        resources=0.0,
        production_bias=10.0,
        max_resources=100.0,
    ) -> None:
        super().__init__(id)
        self.max_production = max_production
        self.production_rate = production_rate
        self.production_bias = production_bias
        self.resources = resources
        self.max_resources = max_resources

    def produce(self, value):
        value = min(value, self.max_production)
        actual_production = np.random.uniform(
            low=value - self.production_bias,
            high=min(value + self.production_bias, self.max_production),
        )
        required_resources = actual_production * self.production_rate
        if required_resources > self.resources:
            actual_production = self.resources * self.production_rate
        self.resources = max(self.resources - required_resources, 0.0)
        return actual_production

    def add_resources(self, resources):
        total = self.resources + resources
        self.resources = min(total, self.max_resources)
        return max(total - self.max_resources, 0.0)

    def color(self):
        return "blue"

    def size(self):
        return 1000

    def to_json(self):
        return {
            "id": self.id,
            "type": "Producer",
            "max_production": self.max_production,
            "production_rate": self.production_rate,
            "production_bias": self.production_bias,
            "resources": self.resources,
            "max_resources": self.max_resources,
        }


class ResourceProducerNode(ConsumerNode):
    def __init__(
        self,
        id,
        max_resource_production=100.0,
        resource_production_rate=10.0,
        resource_production_bias=10.0,
    ) -> None:
        super().__init__(id, min_consumption=None, max_consumption=None)
        self.max_resource_production = max_resource_production
        self.resource_production_rate = resource_production_rate
        self.resource_production_bias = resource_production_bias
        self.current_production = 0.0

    def set_consumption(self):
        low_production = max(
            self.max_resource_production - self.resource_production_bias, 0.0
        )
        production = np.random.uniform(
            low=low_production, high=self.max_resource_production
        )
        self.current_consumption = production * self.resource_production_rate
        self.current_production = 0.0
        self.status = ConsumerNode.Status.OFF
        return self.current_consumption

    def feed(self, power):
        if power > self.current_consumption:
            self.status = ConsumerNode.Status.ON
            reminder = power - self.current_consumption
            self.current_production = (
                self.current_consumption / self.resource_production_rate
            )
            self.current_consumption += 0.0
            return reminder
        if 0 < power <= self.current_consumption:
            self.status = ConsumerNode.Status.PARTIAL
            self.current_production += power / self.resource_production_rate
            self.current_consumption -= power
        else:
            self.status = ConsumerNode.Status.OFF
        return 0.0

    def color(self):
        if self.status == ConsumerNode.Status.OFF:
            return "red"
        elif self.status == ConsumerNode.Status.PARTIAL:
            return "orange"
        elif self.status == ConsumerNode.Status.ON:
            return "green"

    def size(self):
        return 200 * self.current_production

    def to_json(self):
        return {
            "id": self.id,
            "type": "ResourceProducer",
            "max_resource_production": self.max_resource_production,
            "resource_production_rate": self.resource_production_rate,
            "resource_production_bias": self.resource_production_bias,
        }


import json


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
    if node["type"] == "Consumer":
        return ConsumerNode(
            node["id"],
            min_consumption=node["min_consumption"],
            max_consumption=node["max_consumption"],
        )
    elif node["type"] == "Producer":
        return ProducerNode(
            node["id"],
            max_production=node["max_production"],
            production_rate=node["production_rate"],
            production_bias=node["production_bias"],
            resources=node["resources"],
            max_resources=node["max_resources"],
        )
    elif node["type"] == "ResourceProducer":
        return ResourceProducerNode(
            node["id"],
            max_resource_production=node["max_resource_production"],
            resource_production_rate=node["resource_production_rate"],
            resource_production_bias=node["resource_production_bias"],
        )
    else:
        raise ValueError("Unknown node type")


def load_from_json(path):

    with open(path, "r") as f:
        data = json.load(f)
        nodes = [parse_node(node) for node in data["nodes"]]
        weights = np.zeros((len(nodes), len(nodes)))
        for weight in data["weights"]:
            value = np.inf if weight["weight"] == "inf" else weight["weight"]
            weights[weight["node1"], weight["node2"]] = value

    return nodes, weights
