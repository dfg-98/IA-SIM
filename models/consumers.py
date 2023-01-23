import numpy as np
from .node import Node
from utils import clamp
from enum import Enum

DEFAULT_CONSUMPTION_BIAS = 10.0
ELECTRICITY_PRICE = 10.0


class ConsumerNode(Node):
    class Status(Enum):
        OFF = 0
        PARTIAL = 2
        ON = 1

    def __init__(self, id, mean_consumption=10, *args, **kwargs) -> None:
        super().__init__(id)
        self.status = ConsumerNode.Status.OFF
        self.current_consumption = 0.0
        self.mean_consumption = mean_consumption
        self.consumptions = []
        self.generated_resources = 0

    def set_consumption(self):
        self.consumptions.append(self.current_consumption)
        self.mean_consumption = np.mean(self.consumptions)
        self.status = ConsumerNode.Status.OFF
        return self.current_consumption

    def feed(self, power):
        if self.status == ConsumerNode.Status.ON:
            return power

        if power > self.current_consumption:
            self.status = ConsumerNode.Status.ON
            reminder = power - self.current_consumption
            self.generated_resources += self.current_consumption * ELECTRICITY_PRICE
            self.current_consumption = 0.0
            return reminder
        if 0 < power <= self.current_consumption:
            self.status = ConsumerNode.Status.PARTIAL
            self.current_consumption -= power
            self.generated_resources += power * ELECTRICITY_PRICE
        else:
            self.status = ConsumerNode.Status.OFF
        return 0.0

    def collect_resources(self):
        resources = self.generated_resources
        self.generated_resources = 0
        print(f"[Node {self.id}] COLLECTED RESOURCES: ", resources)
        return resources

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
            "mean_consumption": self.mean_consumption,
        }


class MinMaxConsumerNode(ConsumerNode):
    def __init__(self, id, min, max, *args, **kwargs) -> None:
        super().__init__(id, np.mean([min, max]), *args, **kwargs)
        self.min_consumption = min
        self.max_consumption = max

    def set_consumption(self):
        consumption = np.random.uniform(
            low=self.min_consumption, high=self.max_consumption
        )
        self.current_consumption = consumption
        return super().set_consumption()

    def to_json(self):
        return {
            "id": self.id,
            "type": "MinMaxConsumer",
            "min": self.min_consumption,
            "max": self.max_consumption,
        }


class TurnBasedConsumerNode(ConsumerNode):
    def __init__(
        self, id, mean_consumption, on_turns, off_turns, *args, **kwargs
    ) -> None:
        super().__init__(id, mean_consumption, *args, **kwargs)
        self.on_turns = on_turns
        self.off_turns = off_turns
        self.turns_to_change = on_turns
        self.consumming = True

    def set_consumption(self):
        if self.consumming:
            low = self.mean_consumption - DEFAULT_CONSUMPTION_BIAS
            high = self.mean_consumption + DEFAULT_CONSUMPTION_BIAS
            consumption = np.random.uniform(
                low=clamp(low, 0, low), high=clamp(high, 0, high)
            )
            self.current_consumption = consumption
        else:
            self.current_consumption = 0.0
        consumption = super().set_consumption()
        self._check_for_turn()
        return consumption

    def _check_for_turn(self):
        if self.turns_to_change == 0:
            self.consumming = not self.consumming
        else:
            self.turns_to_change -= 1
        self.turns_to_change = self.on_turns if self.consumming else self.off_turns

    def to_json(self):
        node = super().to_json()
        node["type"] = "TurnBasedConsumer"
        node["on_turns"] = self.on_turns
        node["off_turns"] = self.off_turns
        return node
