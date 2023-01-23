from optparse import OptionParser
from models.node_parser import load_from_json
from metaheuristics.utils import fitness_function_factory
from metaheuristics.genetic_algorithm import GeneticAlgorithm
from simpy import Environment
from models.net import Net, build_graph_from_nodes


if __name__ == "__main__":
    usage = "%prog [options] data[json]"
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-t", "--time", dest="time", default=10, type="int", help="Simulation time"
    )
    parser.add_option(
        "-s", "--sims", dest="sims", default=1, type="int", help="Number of simulations"
    )
    parser.add_option(
        "-r",
        "--resources",
        dest="resources",
        default=100.0,
        type="float",
        help="Initial resources",
    )
    parser.add_option(
        "-v",
        "--visual",
        dest="visual",
        default=False,
        action="store_true",
        help="Show graphs",
    )
    parser.add_option(
        "-p",
        "--population",
        dest="population",
        default=100,
        type="int",
        help="Population size for Genetic Algorithm",
    )
    parser.add_option(
        "-g",
        "--generations",
        dest="generations",
        default=500,
        type="int",
        help="Number of generations for Genetic Algorithm",
    )

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect number of arguments")

    nodes, weights = load_from_json(args[0])
    fitness_function = fitness_function_factory(
        nodes, options.resources, options.time, options.visual, options.sims
    )

    ga = GeneticAlgorithm(
        options.population, options.generations, weights, fitness_function
    )
    solutions = ga.run()

    print("Best solution: ", solutions[0])

    env = Environment()
    net = Net(
        build_graph_from_nodes(nodes, solutions[0]),
        options.resources,
        env,
        with_visual=True,
    )
    env.process(net.run())

    env.run(until=5)
