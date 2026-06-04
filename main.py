"""Pygame visualiser for random planar graph 3-coloring.

Displays a greedy-colored planar graph and lets the user regenerate it
or adjust the vertex count interactively.

Controls:
    R        -- regenerate graph with the current vertex count
    UP/DOWN  -- increase/decrease vertex count (range 6-24) and regenerate
    ESC/Q    -- quit
"""
# pylint: disable=no-member
import pygame
import sys

from src.graph import GraphEmbedding, random_planar_graph
from src.layout import GraphLayout, FruchtermanReingoldLayout
from src.draw import MARGIN, draw

FPS = 60
WIDTH, HEIGHT = 1280, 720

N_VERTICES = 10
DROP_PROB = 0.2


def build() -> tuple[GraphEmbedding, GraphLayout]:
    """Generate a new graph and scale its coordinates to fit the display area.

    :returns: Tuple of the new :class:`~graph.GraphEmbedding` (vertices scaled
        to the drawable region ``[MARGIN, WIDTH-MARGIN] x [MARGIN, HEIGHT-MARGIN]``)
        and the :class:`~layout.FruchtermanReingoldLayout` warm-started from it.
    """
    layout_size = (WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN)
    graph = random_planar_graph(N_VERTICES, DROP_PROB)
    graph.rescale(layout_size)
    layout = FruchtermanReingoldLayout(graph, size=layout_size, c=0.9)
    return graph, layout


def main():
    """Initialise pygame and run the event loop until the user quits."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph 3-Coloring  |  R = regenerate  |  ESC = quit")
    clock = pygame.time.Clock()

    global N_VERTICES  # pylint: disable=global-statement
    graph, layout = build()

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
                    graph, layout = build()
                if event.key == pygame.K_UP:
                    N_VERTICES = min(N_VERTICES + 1, 24)
                    graph, layout = build()
                if event.key == pygame.K_DOWN:
                    N_VERTICES = max(N_VERTICES - 1, 6)
                    graph, layout = build()

        if layout.temp > 0.01:
            layout.step()
            draw(screen, graph)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
