"""Planar graph construction and layout in the Euclidean plane.

Classes:
    Graph            -- undirected graph with greedy coloring
    GraphEmbedding   -- Graph extended with 2-D vertex coordinates

Factory:
    random_planar_graph -- builds a connected planar graph via Delaunay
                           triangulation with random edge thinning
"""
import numpy as np
import random

from collections import defaultdict
from itertools import combinations
from scipy.spatial import Delaunay  # pylint: disable=no-name-in-module


class Graph:
    """Undirected graph represented as an adjacency structure."""

    def __init__(self, edges: list[tuple[int, int]]):
        """Build a graph from a list of (u, v) edge pairs.

        :param edges: List of ``(u, v)`` pairs representing undirected edges.
        """
        self.n_vertices = len({v for e in edges for v in e})

        self.edges = edges

        self._neighbors = self._get_neighbors(edges)

    def __str__(self):
        return f"G: n = {self.n_vertices}, E = {self.edges}"

    @staticmethod
    def _get_neighbors(edges) -> dict[int, set[int]]:
        """Build an adjacency map from an edge list.

        :param edges: Iterable of ``(u, v)`` pairs representing undirected edges.
        :returns: A ``defaultdict`` mapping each vertex to the set of its neighbors.
        """
        # defaultdict(set) automatically creates an empty set() when accessing a missing key
        # instead of raising KeyError as an ordinary dict would.
        neighbors = defaultdict(set)
        for u, v in edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        return neighbors

    @property
    def greedy_coloring(self) -> dict[int, int]:
        """Return a vertex coloring produced by the greedy sequential algorithm.

        Vertices are processed in order 0..n-1. Each vertex receives the
        smallest non-negative integer not already used by one of its neighbors.

        :returns: Dict mapping vertex id to color index.
        """
        coloring = {}
        for u in range(self.n_vertices):
            # Choose lowest availabe color not used by any neighbor
            used = {coloring[nb] for nb in self._neighbors[u] if nb in coloring}
            coloring[u] = next(c for c in range(self.n_vertices) if c not in used)
        return coloring

    def is_connected(self) -> bool:
        """Return ``True`` if the graph is connected, ``False`` otherwise.

        Uses iterative DFS from vertex 0.

        :returns: Whether all vertices are reachable from vertex 0.
        """
        visited = set()
        stack = [0]
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                stack.extend(self._neighbors[v] - visited)
        return len(visited) == self.n_vertices


class InvalidEmbedding(Exception):
    """Raised when the number of coordinate embeddings doesn't match the vertex count."""

    def __init__(self, n_embeddings, n_vertices, *args):
        msg = "Number of embeddings ({0}) does not match number of vertices ({1})"
        super().__init__(msg.format(n_embeddings, n_vertices), *args)


class GraphEmbedding(Graph):
    """A Graph with 2-D Euclidean coordinates assigned to each vertex."""

    def __init__(self, vertices: np.typing.NDArray, edges):
        """Create an embedded graph.

        :param vertices: Array of shape ``(n, 2)`` with ``(x, y)`` coordinates
            for each vertex.
        :param edges: Edge list as accepted by :meth:`Graph.__init__`.
        :raises InvalidEmbedding: If ``len(vertices)`` does not equal the number
            of distinct vertices in *edges*.
        """
        super().__init__(edges)

        if not len(vertices) == self.n_vertices:
            raise InvalidEmbedding(len(vertices), self.n_vertices)

        self.vertices = vertices

    def __str__(self):
        vertices_str = ", ".join(f'({x:.2}, {y:.2})' for x, y in self.vertices)
        return super().__str__() + f", V = [{vertices_str}]"

    def rescale(self, factor: tuple[float, float]) -> None:
        """Scale all vertex coordinates in-place by ``(sx, sy)``.

        :param factor: A ``(sx, sy)`` tuple applied element-wise to every vertex.
        """
        self.vertices *= np.array(factor)


def random_planar_graph(n: int = 10, drop_prob: float = 0.2) -> GraphEmbedding:
    """Generate a random connected planar graph embedded in the unit square.

    Builds a Delaunay triangulation of *n* uniformly random points, then
    randomly drops edges (keeping at least ``n-1`` to allow connectivity). If
    the resulting graph is disconnected the whole process is retried until a
    connected graph is produced.

    :param n: Number of vertices.
    :param drop_prob: Fraction of Delaunay edges to discard (``0`` keeps all,
        ``1`` keeps the minimum spanning set). Defaults to ``0.2``.
    :returns: A :class:`GraphEmbedding` whose vertex coordinates lie in
        ``[0, 1] x [0, 1]``.
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

        try:
            graph = GraphEmbedding(vertices, edges)
        except InvalidEmbedding:
            # If thinning produces orphan vertices, try again
            continue

        if graph.is_connected():
            return graph


if __name__ == "__main__":
    np.random.seed(42)
    g = random_planar_graph(5)
    print(g)
    g.rescale((800, 600))
    print(g)
