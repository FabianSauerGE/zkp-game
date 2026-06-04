import numpy as np
import pygame

from graph import GraphEmbedding


BG = (18, 18, 18)
EDGE_COLOR = (80, 80, 80)
COLORS = [
    (229, 115, 87),   # coral
    (29, 158, 117),   # teal
    (239, 159, 39),   # amber
    (150, 120, 200),  # fallback purple
    (150, 150, 150)   # fallback grey
]
VERTEX_RADIUS = 18

def draw(screen: pygame.Surface, graph: GraphEmbedding, margin: int = 50) -> None:
    screen.fill(BG)

    pts = np.array([margin, margin]) + graph.vertices
    pts = pts.astype(int)

    for u, v in graph.edges:
        pygame.draw.line(screen, EDGE_COLOR, pts[u], pts[v], 2)

    for v, (x, y) in enumerate(pts):
        color = COLORS[graph.greedy_coloring[v]]
        pygame.draw.circle(screen, color, (x, y), VERTEX_RADIUS)
        pygame.draw.circle(screen, BG, (x, y), VERTEX_RADIUS, 2)
