import sys
import json
from models.node_parser import graph_from_json
from matplotlib import pyplot as plt
from networkx import draw_random


if __name__ == "__main__":
    if len(sys.argv):
        print("Expected json file as argument")
        print("Usage: vis.py [json]")

    try:
        with open(sys.argv[1], "r") as f:
            data = json.load(f)
            graph = graph_from_json(data)
            sizes = [node.size() for node in graph.nodes]
            colors = [node.color() for node in graph.nodes]

            draw_random(graph, node_size=sizes, node_color=colors)
            plt.show()

    except FileNotFoundError:
        print("No valid filename")
