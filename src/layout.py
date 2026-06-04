"""Force-directed graph layout algorithms.

Classes:
    GraphLayout                  -- abstract base for iterative layout animators
    FruchtermanReingoldLayout    -- FR spring-embedder with exponential cooling
"""
import math
import numpy as np

from abc import ABC, abstractmethod

from src.graph import GraphEmbedding


class GraphLayout(ABC):
    """Abstract base class for iterative, frame-by-frame graph layout animators.

    Subclasses implement :meth:`step` to advance the layout by one iteration.
    The base class tracks the iteration counter used for e.g. cooling schedules.
    """

    @abstractmethod
    def __init__(self, g: GraphEmbedding, size: tuple[float, float]):
        """Initialise the layout with a given embedding.

        :param g: The embedded graph whose current vertex positions are used
            as the starting state.
        :param size: ``(width, height)`` of the drawable area in pixels,
            used by subclasses for clamping and spring-length calculation.
        """
        self._g = g
        self._size = size

        self._i = 0

    @abstractmethod
    def step(self):
        """Advance the layout by one iteration and increment the counter."""
        self._i += 1

    def steps(self, n_steps):
        """Advance the layout by *n_steps* iterations.

        :param n_steps: Number of iterations to run.
        """
        for _ in range(n_steps):
            self.step()


class FruchtermanReingoldLayout(GraphLayout):
    """Fruchterman-Reingold force-directed layout with exponential cooling.

    Vertices repel each other and edges attract their endpoints, with all
    displacements clamped to a temperature that decreases geometrically each
    step. Starting from an existing :class:`~graph.GraphEmbedding`
    preserves planarity established by the Delaunay construction.
    """

    def __init__(self, g: GraphEmbedding, size: tuple[float, float], c: float = 1, temp: float = 10, edge_repulsion=True):
        """Set up the FR layout.

        :param g: Start embedding; its vertex positions are updated
            in-place on each :meth:`step` call.
        :param size: ``(width, height)`` of the drawable area in pixels.
            Vertices are clamped to ``[0, width] x [0, height]``.
        :param c: Scaling constant for the optimal spring length *k*.
            Higher values spread vertices further apart. Defaults to ``1``.
        :param temp: Initial temperature controlling the maximum displacement
            per step. Defaults to ``10`` pixels.
        """
        super().__init__(g, size)

        self._k = c * math.sqrt(self._size[0] * self._size[1] / len(self._g.vertices))

        self._alpha = 0.95
        self._temp0 = temp

        self._edge_repulsion = edge_repulsion

    @property
    def temp(self):
        """Current temperature: ``temp0 * alpha ** i`` where *i* is the step count."""
        return self._temp0 * self._alpha**self._i

    @staticmethod
    def _dir(u, v):
        """Return the unit vector from *u* to *v* and their distance.

        :param u: Source position as a 1-D array.
        :param v: Target position as a 1-D array.
        :returns: Tuple ``(unit_vector, distance)``.
        """
        _dir = v - u
        norm = np.linalg.norm(_dir)
        return _dir / norm, norm

    def _attraction(self, u, v):
        """Compute the attractive force on *u* toward *v* along a shared edge.

        Uses the FR formula ``dist² / k`` scaled to the unit direction.

        :param u: Position of the first endpoint.
        :param v: Position of the second endpoint.
        :returns: Force vector to be added to *u*'s displacement (and subtracted from *v*'s).
        """
        uv, dist = self._dir(u, v)
        return dist**2 / self._k * uv

    def _repulsion(self, u, v):
        """Compute the repulsive force on *u* away from *v*.

        Uses the FR formula ``-k² / dist`` scaled to the unit direction.

        :param u: Position of the first vertex.
        :param v: Position of the second vertex.
        :returns: Force vector to be added to *u*'s displacement (and subtracted from *v*'s).
        """
        uv, dist = self._dir(u, v)
        return - self._k**2 / max(dist, 0.01) * uv

    @staticmethod
    def _closest_on_segment(a, b, p) -> np.typing.NDArray:
        """Return the closest point on segment *ab* to point *p*.

        :param a: Start of the segment.
        :param b: End of the segment.
        :param p: Query point.
        :returns: Point on ``[a, b]`` nearest to *p*.
        """
        ab = b - a
        t = np.dot(p - a, ab) / np.dot(ab, ab)
        return a + np.clip(t, 0, 1) * ab

    def _forces(self) -> np.typing.NDArray:
        """Compute the net force on every vertex for the current positions.

        Applies vertex-vertex repulsion and edge attraction (standard FR), plus
        optional repulsion between each vertex and the closest point on every
        non-incident edge.

        :param edge_repulsion: Whether to include vertex-edge repulsion.
            Defaults to ``True``.
        :returns: Array of shape ``(n, 2)`` with the net force vector per vertex.
        """
        vertices = self._g.vertices
        forces = np.zeros(vertices.shape)

        for u in range(self._g.n_vertices):
            for v in range(u + 1, self._g.n_vertices):
                f = self._repulsion(vertices[u], vertices[v])
                forces[u] += f
                forces[v] -= f

        for u, v in self._g.edges:
            f = self._attraction(vertices[u], vertices[v])
            forces[u] += f
            forces[v] -= f

        if self._edge_repulsion:
            for u in range(self._g.n_vertices):
                for v, w in self._g.edges:
                    if u in (v, w):
                        continue
                    closest = self._closest_on_segment(vertices[v], vertices[w], vertices[u])
                    forces[u] += 0.5 * self._repulsion(vertices[u], closest)

        return forces

    def step(self):
        """Advance the layout by one FR iteration.

        Computes forces, clamps displacements to the current temperature, applies
        them to vertex positions, clamps positions to the drawable area, then
        decrements the temperature via the cooling schedule.
        """
        forces = self._forces()
        np.clip(forces, - self.temp, self.temp, out=forces)

        self._g.vertices += forces
        np.clip(self._g.vertices, (0, 0), self._size, out=self._g.vertices)

        super().step()


if __name__ == "__main__":
    from src.graph import random_planar_graph
    layout_size = (800, 600)
    graph = random_planar_graph(6)
    graph.rescale(layout_size)
    print(graph)
    layout = FruchtermanReingoldLayout(graph, size=layout_size)
    for _ in range(5):
        layout.step()
        print(graph)
