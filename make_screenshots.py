"""Headless screenshot generator — saves three PNG files to screenshots/.

Usage:
    python make_screenshots.py
"""
# pylint: disable=no-member
import os
import numpy as np
import pygame

from src.draw import MARGIN, draw, draw_hud
from src.graph import random_planar_graph
from src.layout import FruchtermanReingoldLayout

SHOTS = [
    # (seed, n_vertices, fr_steps, edge_repulsion, width, height, filename)
    dict(seed=5,  n=12, steps=8,   edge_repulsion=True,  w=800, h=600, filename="01_animating.png"),
    dict(seed=73, n=16, steps=300, edge_repulsion=True,  w=800, h=600, filename="02_edge_repulsion_on.png"),
    dict(seed=73, n=16, steps=300, edge_repulsion=False, w=800, h=600, filename="03_edge_repulsion_off.png"),
]


def make_screenshot(seed, n, steps, edge_repulsion, w, h, filename):
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"

    pygame.init()
    screen = pygame.display.set_mode((w, h))
    font = pygame.font.SysFont("monospace", 16)

    layout_size = (w - 2 * MARGIN, h - 2 * MARGIN)
    np.random.seed(seed)
    graph = random_planar_graph(n, 0.2)
    graph.rescale(layout_size)
    FruchtermanReingoldLayout(graph, size=layout_size, c=0.9, edge_repulsion=edge_repulsion).steps(steps)

    draw(screen, graph)
    draw_hud(screen, font, graph, edge_repulsion)
    pygame.image.save(screen, f"screenshots/{filename}")
    pygame.quit()
    print(f"Saved screenshots/{filename}")


def main():
    os.makedirs("screenshots", exist_ok=True)
    for shot in SHOTS:
        make_screenshot(**shot)


if __name__ == "__main__":
    main()
