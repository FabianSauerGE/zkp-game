"""Planar graph construction and layout in the Euclidean plane.

Provides the Graph dataclass with greedy coloring
and a random_planar factory that builds connected graphs via Delaunay
triangulation with random edge thinning.
"""
import numpy as np
import numpy.typing as npt
import random

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from scipy.spatial import Delaunay  # pylint: disable=no-name-in-module


@dataclass
class Graph:
    """Mutable undirected graph with vertices embedded in the unit square."""

    vertices: npt.NDArray[np.float64]       # shape (n, 2), coordinates in [0, 1]
    edges: list[tuple[np.int32, np.int32]]  # undirected pairs (i, j) with i < j

    def __str__(self):
        vertices = ", ".join(f'({x:.2}, {y:.2})' for x, y in self.vertices)
        edges = ", ".join(f'({v}, {w})' for v, w in sorted(self.edges))
        return f"G(V[{vertices}], E[{edges}])"

    @property
    def neighbors(self) -> dict:
        """Adjacency dict: vertex index -> set of neighbor indices."""
        neighbors = defaultdict(set)
        for a, b in self.edges:
            neighbors[a].add(b)
            neighbors[b].add(a)
        return neighbors

    @property
    def greedy_coloring(self) -> dict:
        """Greedy coloring dict: vertex index -> color."""
        coloring = {}
        for i, _ in enumerate(self.vertices):
            # Choose lowest availabe color not used by any neighbor
            used = {coloring[nb] for nb in self.neighbors[i] if nb in coloring}
            coloring[i] = next(c for c, _ in enumerate(self.vertices) if c not in used)
        return coloring

    def is_connected(self) -> bool:
        """Returns True iff the graph is connected."""
        if len(self.neighbors) < len(self.vertices):
            return False

        visited = set()
        stack = [0]
        while stack:
            i = stack.pop()
            if i not in visited:
                visited.add(i)
                stack.extend(self.neighbors[i] - visited)
        return len(visited) == len(self.vertices)


def random_planar_graph(n: int = 10, drop_prob: float = 0.3) -> Graph:
    """Generate random planar graph.

        - Delaunay triangulation of random points
        - edges dropped with prob drop_prob, retried until connected
    """
    while True:
        # Generate n random points
        vertices = np.random.rand(n, 2)
        # Compute Delaunay triangulation
        tri = Delaunay(vertices)

        # Add all sides of the triangles as edges
        # E.g., combinations((0, 1, 2), 2) -> (0, 1), (1, 2), (2, 3)
        # Use set comprehension to omit duplicates
        edges = list({(a, b) for simplex in tri.simplices for a, b in combinations(simplex, 2)})

        # Thin out edges at random
        n_edges = max(int(len(edges) * (1 - drop_prob)), n - 1)
        edges = random.sample(edges, n_edges)

        g = Graph(vertices, edges)
        if g.is_connected():
            return g


if __name__ == "__main__":
    g1 = random_planar_graph(7)
    print(g1)
    print(g1.greedy_coloring)
