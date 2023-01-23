import numpy as np


class Node:
    def __init__(self, id, *args, **kwargs) -> None:
        self.id = id

    def collect_resources(self):
        return 0

    def color(self):
        raise NotImplemented

    def size(self):
        return 100

    def to_json(self):
        raise NotImplemented


class HealthNode(Node):
    def __init__(self, id, reparation_cost_rate=10, *args, **kwargs) -> None:
        super().__init__(id, *args, **kwargs)
        self.health = 100.0
        self.reparation_cost_rate = reparation_cost_rate

    @property
    def damage(self):
        return 100.0 - self.health

    def repair(self, resources):
        income_health = resources * self.reparation_cost_rate
        needed_healh = self.damage
        if income_health > needed_healh:
            self.health = 100.0
            resource_cost = (income_health - needed_healh) / self.reparation_cost_rate
            remainder = resources - resource_cost
            return remainder

        self.health += income_health
        return 0.0

    def to_json(self):
        return {
            "id": self.id,
            "type": "Health",
            "reparation_cost_rate": self.reparation_cost_rate,
        }
