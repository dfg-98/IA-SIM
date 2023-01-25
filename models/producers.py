import numpy as np
from .node import HealthNode
from .consumers import ConsumerNode


class ResourceProducerNode(HealthNode, ConsumerNode):
    def __init__(
        self,
        id,
        *args,
        max_resource_production=100.0,
        resource_production_rate=10.0,
        resource_production_bias=10.0,
        production_damage_rate=100,
        **kwargs,
    ) -> None:
        super().__init__(id, *args, **kwargs)
        self.max_resource_production = max_resource_production
        self.resource_production_rate = resource_production_rate
        self.resource_production_bias = resource_production_bias
        self.production_damage_rate = production_damage_rate
        self.current_production = 0.0
        self.fails = 0

    def set_consumption(self):
        low_production = max(
            self.max_resource_production - self.resource_production_bias, 0.0
        )
        production = np.random.uniform(
            low=low_production, high=self.max_resource_production
        )
        self.current_consumption = production * self.resource_production_rate
        self.current_production = 0.0
        return super().set_consumption()

    def feed(self, power):
        if not self.allow_production():
            self.fails += 1
            return power
        if power <= 0:
            return 0.0
        used_power = min(power, self.current_consumption)
        production_reminder = self._produce(used_power)
        reminder = production_reminder + (power - used_power)
        if reminder > 0:
            self.status = ConsumerNode.Status.ON
        else:
            self.status = ConsumerNode.Status.PARTIAL

        return reminder

    def _produce(self, power):
        production = power / self.resource_production_rate
        production_damage = production / self.production_damage_rate
        if self.health < production_damage:
            production_damage = self.health
            production = self.health * self.production_damage_rate
        consumed_power = production * self.resource_production_rate
        self.health -= production_damage
        self.current_production += production
        self.current_consumption -= consumed_power
        return consumed_power

    def color(self):
        if self.status == ConsumerNode.Status.OFF:
            return "pink"
        elif self.status == ConsumerNode.Status.PARTIAL:
            return "yellow"
        elif self.status == ConsumerNode.Status.ON:
            return "black"

    def allow_production(self):
        """Allow production if the node has health"""
        p = np.random.uniform(0.0, 1.0) ** 2
        p *= 100
        return self.health > p

    def repair(self, resources):
        self.fails = 0
        return super().repair(resources)

    def size(self):
        return 200 * (self.current_production + 1)

    def to_json(self):
        parent_node = super().to_json()
        node = {
            "id": self.id,
            "type": "ResourceProducer",
            "max_resource_production": self.max_resource_production,
            "resource_production_rate": self.resource_production_rate,
            "resource_production_bias": self.resource_production_bias,
            "production_damage_rate": self.production_damage_rate,
        }
        parent_node.update(node)
        return parent_node
