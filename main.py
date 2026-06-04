import sys

# pylint: disable=no-member
import pygame

from graph import GraphEmbedding, random_planar_graph
from draw import draw

WIDTH, HEIGHT = 1200, 800
FPS = 60
N_VERTICES = 10
DROP_PROB = 0.2


def build() -> GraphEmbedding:
    graph = random_planar_graph(N_VERTICES, DROP_PROB)
    graph.rescale((WIDTH - 100, HEIGHT - 100))
    return graph


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph 3-Coloring  |  R = regenerate  |  ESC = quit")
    clock = pygame.time.Clock()

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
                    global N_VERTICES  # pylint: disable=global-statement
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
