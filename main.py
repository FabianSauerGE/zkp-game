import sys

# pylint: disable=no-member
import pygame  

WIDTH, HEIGHT = 1200, 800
FPS = 60
N_VERTICES = 22
DROP_PROB = 0.35


def build():
    return 0


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

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
