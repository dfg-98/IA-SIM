import numpy as np
from .node import HealthNode


class GeneratorNode(HealthNode):
    def __init__(
        self,
        id,
        *args,
        max_generation=100.0,
        generation_rate=1.0,
        generation_bias=10.0,
        generation_damage_rate=100,
        resources=0.0,
        max_resources=100.0,
        **kargs
    ) -> None:
        super().__init__(id, *args, **kargs)
        self.max_generation = max_generation
        self.generation_rate = generation_rate
        self.resources = resources
        self.max_resources = max_resources
        self.generation_bias = generation_bias
        self.generation_damage_rate = generation_damage_rate

    def produce(self, value):
        value = min(value, self.max_generation)
        actual_production = np.random.uniform(
            low=max(0.0, value - self.generation_bias),
            high=min(value + self.generation_bias, self.max_generation),
        )
        required_resources = actual_production * self.generation_rate
        if required_resources > self.resources:
            actual_production = self.resources * self.generation_rate
        damage = actual_production / self.generation_damage_rate
        if damage > self.health:
            actual_production = self.health * self.generation_damage_rate
            required_resources = actual_production * self.generation_rate
        self.resources = max(self.resources - required_resources, 0.0)
        self.health = max(self.health - damage, 0.0)
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
        parent_node = super().to_json()
        node = {
            "id": self.id,
            "type": "Generator",
            "max_generation": self.max_generation,
            "generation_rate": self.generation_rate,
            "max_resources": self.max_resources,
            "generation_bias": self.generation_bias,
            "generation_damage_rate": self.generation_damage_rate,
        }
        parent_node.update(node)
        return parent_node
