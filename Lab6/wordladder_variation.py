"""
=====
Words
=====

Words/Ladder Graph
------------------
Generate  an undirected graph over the 5757 5-letter words in the
datafile `words_dat.txt.gz`.  Two words are connected by an edge
if they differ in one letter, resulting in 14,135 edges. This example
is described in Section 1.1 in Knuth's book (see [1]_ and [2]_).

References
----------
.. [1] Donald E. Knuth,
   "The Stanford GraphBase: A Platform for Combinatorial Computing",
   ACM Press, New York, 1993.
.. [2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html
"""
# Authors: Aric Hagberg (hagberg@lanl.gov),
#          Brendt Wohlberg,
#          hughdbrown@yahoo.com

#    Copyright (C) 2004-2018 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

import sys
import gzip
from string import ascii_lowercase as lowercase

import networkx as nx
import itertools

#-------------------------------------------------------------------
#   The Words/Ladder graph of Section 1.1
#-------------------------------------------------------------------


def generate_graph(words):
    G = nx.Graph(name="words")
    lookup = dict((c, lowercase.index(c)) for c in lowercase)

    def edit_distance_one(word):
        permutations = ["".join(att) for att in itertools.permutations(word, len(word))]
        for attempt in permutations:
            for i in range(len(attempt)):
                left, c, right = attempt[0:i], attempt[i], attempt[i + 1:]
                j = lookup[c]  # lowercase.index(c)
                for cc in lowercase[j + 1:]:
                    yield left + cc + right
        

    candgen = ((word, cand) for word in sorted(words)
               for cand in edit_distance_one(word) if cand in words)
    G.add_nodes_from(words)
    for word, cand in candgen:
        G.add_edge(word, cand)
    return G


def words_graph(filename, size):
    """Return the words example graph from the Stanford GraphBase"""
    fh = gzip.open(filename, 'r')
    words = set()
    for line in fh.readlines():
        line = line.decode()
        if line.startswith('*'):
            continue
        w = str(line[0:size])
        words.add(w)
    return generate_graph(words)


if __name__ == '__main__':
    filename = sys.argv[1]
    size = int(sys.argv[2])
    G = words_graph(filename, size)
    print("Loaded words_dat.txt containing %d %d-letter English words." % (nx.number_of_nodes(G), size))
    print("Two words are connected if they differ in one letter.")
    print("Graph has %d nodes with %d edges" % (nx.number_of_nodes(G), nx.number_of_edges(G)))
    print("%d connected components" % nx.number_connected_components(G))

    if (size == 5):
        words = [('chaos', 'order'),
                 ('nodes', 'graph'),
                 ('moron', 'smart'),
                 ('pound', 'marks')]
    elif (size == 4):
        words = [('cold', 'warm'),
                 ('love', 'hate')]
    for (source, target) in words:
        print("Shortest path between %s and %s is" % (source, target))
        try:
            sp = nx.shortest_path(G, source, target)
            for n in sp:
                print(n)
        except nx.NetworkXNoPath:
            print("None")

