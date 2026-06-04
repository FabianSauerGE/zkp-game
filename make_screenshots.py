"""Headless screenshot generator — saves three PNG files to screenshots/.

Usage:
    python make_screenshots.py
"""
# pylint: disable=no-member
import os
import numpy as np
import pygame

from src.draw import MARGIN, draw
from src.graph import random_planar_graph
from src.layout import FruchtermanReingoldLayout

WIDTH, HEIGHT = 1280, 720
LAYOUT_SIZE = (WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN)

SHOTS = [
    dict(seed=3,  n=10, steps=5,   filename="01_animating.png",  label="FR layout settling  (10 vertices, step 5)"),
    dict(seed=42, n=18, steps=200, filename="02_large_graph.png", label="Converged layout  (18 vertices)"),
    dict(seed=17, n=8,  steps=200, filename="03_small_graph.png", label="Converged layout  (8 vertices)"),
]


def make_screenshot(screen, font, seed, n, steps, filename, label):
    np.random.seed(seed)
    graph = random_planar_graph(n, 0.2)
    graph.rescale(LAYOUT_SIZE)
    FruchtermanReingoldLayout(graph, size=LAYOUT_SIZE, c=0.9).steps(steps)
    draw(screen, graph)
    screen.blit(font.render(label, True, (200, 200, 200)), (MARGIN, HEIGHT - MARGIN))
    pygame.image.save(screen, f"screenshots/{filename}")
    print(f"Saved screenshots/{filename}")


def main():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.makedirs("screenshots", exist_ok=True)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("monospace", 22)

    for shot in SHOTS:
        make_screenshot(screen, font, **shot)

    pygame.quit()


if __name__ == "__main__":
    main()
