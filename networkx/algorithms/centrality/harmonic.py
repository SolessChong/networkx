"""
Harmonic centrality measure.
"""
#    Copyright (C) 2015 by
#    Alessandro Luongo
#    BSD license.
from __future__ import division
import functools
import networkx as nx

__author__ = "\n".join(['Alessandro Luongo (alessandro.luongo@studenti.unimi.it'])
__all__ = ['harmonic_centrality']


def harmonic_centrality(G, distance=None):
    """Compute harmonic centrality for nodes.

    Harmonic centrality [1]_ of a node `u` is the sum of the reciprocal
    of the shortest path distances from all other nodes to `u`.

    .. math::

        C(u) = \sum_{v \neq u \epsilon G} \frac{1}{d(v, u)},

    where `d(v, u)` is the shortest-path distance between `v` and `u`.

    Notice that higher values indicate higher centrality.

    Parameters
    ----------
    G : graph
      A NetworkX graph
    distance : edge attribute key, optional (default=None)
      Use the specified edge attribute as the edge distance in shortest
      path calculations.  If `None`, then each edge will have distance equal to 1.

    Returns
    -------
    nodes : dictionary
      Dictionary of nodes with harmonic centrality as the value.

    See Also
    --------
    betweenness_centrality, load_centrality, eigenvector_centrality,
    degree_centrality, closeness_centrality

    Notes
    -----
    If the 'distance' keyword is set to an edge attribute key then the
    shortest-path length will be computed using Dijkstra's algorithm with
    that edge attribute as the edge weight.

    References
    ----------
    .. [1] Boldi, Paolo, and Sebastiano Vigna. "Axioms for centrality."
           Internet Mathematics 10.3-4 (2014): 222-262.
    """
    if len(G) <= 1:
        return {singleton: 0.0 for singleton in G.nodes()}
    
    if G.is_directed():
        G = G.reverse()
        
    if distance is not None:
        # use Dijkstra's algorithm with specified attribute as edge weight
        sp = nx.all_pairs_dijkstra_path_length(G, weight=distance)
    else:
        sp = nx.all_pairs_shortest_path_length(G)

    return {n: sum(1/d if d > 0 else 0 for d in dd.values()) for n, dd in sp}
