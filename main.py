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
from src.draw import MARGIN, draw, draw_hud, draw_welcome

FPS = 60
WIDTH, HEIGHT = 800, 600

N_VERTICES = 10
DROP_PROB = 0.2
EDGE_REPULSION = False


def build() -> tuple[GraphEmbedding, GraphLayout]:
    """Generate a new graph and scale its coordinates to fit the display area.

    :returns: Tuple of the new :class:`~graph.GraphEmbedding` (vertices scaled
        to the drawable region ``[MARGIN, WIDTH-MARGIN] x [MARGIN, HEIGHT-MARGIN]``)
        and the :class:`~layout.FruchtermanReingoldLayout` warm-started from it.
    """
    layout_size = (WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN)
    graph = random_planar_graph(N_VERTICES, DROP_PROB)
    graph.rescale(layout_size)
    layout = FruchtermanReingoldLayout(graph, size=layout_size, c=0.9, temp=8, edge_repulsion=EDGE_REPULSION)
    return graph, layout


def main():
    """Initialise pygame and run the event loop until the user quits."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph 3-Coloring  |  R = regenerate  |  ESC = quit")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    global N_VERTICES  # pylint: disable=global-statement
    global EDGE_REPULSION  # pylint: disable=global-statement

    welcome = True
    graph, layout = None, None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if welcome:
                    if event.key == pygame.K_RETURN:
                        welcome = False
                        graph, layout = build()
                else:
                    if event.key == pygame.K_r:
                        graph, layout = build()
                    if event.key == pygame.K_e:
                        EDGE_REPULSION = not EDGE_REPULSION
                        graph, layout = build()
                    if event.key == pygame.K_UP:
                        N_VERTICES = min(N_VERTICES + 1, 24)
                        graph, layout = build()
                    if event.key == pygame.K_DOWN:
                        N_VERTICES = max(N_VERTICES - 1, 6)
                        graph, layout = build()

        if welcome:
            draw_welcome(screen)
        else:
            if layout.temp > 0.01:
                layout.step()
            draw(screen, graph)
            draw_hud(screen, font, graph, EDGE_REPULSION)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
