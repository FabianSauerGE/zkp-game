"""Pygame visualiser for random planar graph 3-coloring.

Displays a greedy-colored planar graph and lets the user regenerate it
or adjust the vertex count interactively.

Controls:
    R        -- regenerate graph with the current vertex count
    UP/DOWN  -- increase/decrease vertex count (range 6-24) and regenerate
    ESC/Q    -- quit
"""
# pylint: disable=no-member
import numpy as np
import pygame
import sys

from graph import GraphEmbedding, random_planar_graph

WIDTH, HEIGHT = 1200, 800
MARGIN = 50
FPS = 60

BG = (18, 18, 18)
EDGE_COLOR = (80, 80, 80)
EDGE_WIDTH = 2
VERTEX_COLORS = [
    (229, 115, 87),   # coral
    (29, 158, 117),   # teal
    (239, 159, 39),   # amber
    (150, 120, 200),  # fallback purple
    (150, 150, 150)   # fallback grey
]
VERTEX_RADIUS = 18

N_VERTICES = 10
DROP_PROB = 0.2


def build() -> GraphEmbedding:
    """Generate a new graph and scale its coordinates to fit the display area.

    :returns: A :class:`GraphEmbedding` whose vertices lie within the drawable
        region ``[MARGIN, WIDTH-MARGIN] x [MARGIN, HEIGHT-MARGIN]``.
    """
    graph = random_planar_graph(N_VERTICES, DROP_PROB)
    graph.rescale((WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN))
    return graph


def draw(screen: pygame.Surface, graph: GraphEmbedding) -> None:
    """Render the graph onto *screen* for the current frame.

    Draws edges as grey lines, then vertices as filled circles colored by
    their greedy coloring index into :data:`VERTEX_COLORS`.

    :param screen: The pygame surface to draw onto.
    :param graph: The embedded graph to render.
    """
    screen.fill(BG)

    pts = np.array([MARGIN, MARGIN]) + graph.vertices
    pts = pts.astype(int)

    for u, v in graph.edges:
        pygame.draw.line(screen, EDGE_COLOR, pts[u], pts[v], 2)

    for v, (x, y) in enumerate(pts):
        color = VERTEX_COLORS[graph.greedy_coloring[v]]
        pygame.draw.circle(screen, color, (x, y), VERTEX_RADIUS)
        pygame.draw.circle(screen, BG, (x, y), VERTEX_RADIUS, 2)


def main():
    """Initialise pygame and run the event loop until the user quits."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph 3-Coloring  |  R = regenerate  |  ESC = quit")
    clock = pygame.time.Clock()

    global N_VERTICES  # pylint: disable=global-statement
    graph = build()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    graph = build()
                if event.key == pygame.K_UP:
                    N_VERTICES = min(N_VERTICES + 1, 24)
                    graph = build()
                if event.key == pygame.K_DOWN:
                    N_VERTICES = max(N_VERTICES - 1, 6)
                    graph = build()

        draw(screen, graph)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
