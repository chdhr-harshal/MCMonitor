#!/usr/local/bin/python

"""
ASS edges objective evolution with increasing k
"""

import sys
sys.path.insert(1, '..')
import __builtin__

from MarkovChain import *
from MarkovChain.edge_objectives import *
import networkx as nx
import pandas as pd

DATA_DIR = "/home/grad3/harshal/Desktop/MCMonitor/data/ass/"
PLOTS_DATA_DIR = "/home/grad3/harshal/Desktop/MCMonitor/Plots_data/"

dataframe_rows = []

def read_txt_file(filename):
    filename = DATA_DIR + filename
    data = pd.read_csv(filename, sep="\t", header=0)
    ass = nx.from_pandas_dataframe(data, 'source', 'target')
    return ass

def get_mc_attributes(G):
    G = G.to_directed()
    G = nx.stochastic_graph(G)
    return G

def get_objective_evolution(method, k, edges_per_step, iteration):
    rows = get_evolution(method, k, edges_per_step)
    for row in rows:
        row['iteration'] = iteration
    global dataframe_rows
    dataframe_rows += rows
    df = pd.DataFrame(dataframe_rows)
    df.to_csv(PLOTS_DATA_DIR + "ass1_edges_k_objective_evolution.csv.gz", sep=",",
            header=True, index=False, compression="gzip")

if __name__ == "__main__":
    filename = "ass1.txt"
    G = read_txt_file(filename)
    G = get_mc_attributes(G)

    num_nodes = len(G)
    num_items = len(G)
    k = 50
    item_distributions = ["uniform", "direct", "inverse", "ego"]

    for item_distribution in item_distributions:
        if item_distribution == 'ego':
            iterations = 10
        else:
            iterations = 1
        for iteration in xrange(iterations):
            print "Evaluating item distribution {}".format(item_distribution)
            __builtin__.mc = MarkovChain(num_nodes=num_nodes,
                                         num_items=num_items,
                                         item_distribution=item_distribution,
                                         G=G)

            print "Starting evaluation of methods"
            methods = [random_edges,
                       highest_item_edges,
                       highest_probability_edges,
                       highest_betweenness_centrality_edges,
                       smart_greedy_parallel]

            for method in methods:
                print "Evaluating method {}".format(method.func_name)
                get_objective_evolution(method, k, 5, iteration)