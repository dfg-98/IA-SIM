from models.net import Net, build_graph_from_nodes
from simpy import Environment


def score_simulation(graph, initial_resources=100.0, sim_time=10, with_visual=False):
    env = Environment()
    net = Net(graph, initial_resources, env, with_visual=with_visual)
    env.process(net.run())

    env.run(until=sim_time)
    return net.score


def fitness_function_factory(
    nodes, initial_resources, sim_time, with_visual, num_of_simulation
):
    def _func(graph):
        g = build_graph_from_nodes(nodes, graph)
        score = 0
        score = sum(
            score_simulation(g, initial_resources, sim_time, with_visual)
            for _ in range(num_of_simulation)
        )
        return score / num_of_simulation

    return _func
