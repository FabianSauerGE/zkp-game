"""Pygame rendering helpers for graph visualisation.

Constants:
    MARGIN         -- pixel margin between the window edge and the drawable area
    BG             -- background color
    EDGE_COLOR     -- color used to draw edges
    EDGE_WIDTH     -- line width for edges in pixels
    VERTEX_RADIUS  -- radius of vertex circles in pixels
    VERTEX_COLORS  -- mapping from greedy color index to RGB tuple

Functions:
    draw -- render a GraphEmbedding onto a pygame Surface
"""
import numpy as np
import pygame

from src.graph import GraphEmbedding


MARGIN = 50

BG = (18, 18, 18)

EDGE_WIDTH = 2
EDGE_COLOR = (80, 80, 80)

VERTEX_RADIUS = 18
VERTEX_COLORS = {
    0: (229, 115, 87),   # coral
    1: (29, 158, 117),   # teal
    2: (239, 159, 39),   # amber
    3: (150, 120, 200),  # fallback purple
}


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
        pygame.draw.line(screen, EDGE_COLOR, pts[u], pts[v], EDGE_WIDTH)

    for v, (x, y) in enumerate(pts):
        color = VERTEX_COLORS.get(graph.greedy_coloring[v], (120, 120, 120))
        pygame.draw.circle(screen, color, (x, y), VERTEX_RADIUS)
        pygame.draw.circle(screen, BG, (x, y), VERTEX_RADIUS, 2)


def draw_hud(screen: pygame.Surface, font: pygame.font.Font, graph: GraphEmbedding, edge_repulsion: bool) -> None:
    """Render the HUD overlay showing graph stats and current settings.

    :param screen: The pygame surface to draw onto.
    :param font: Font used to render the HUD text.
    :param graph: The current graph (used for vertex and edge counts).
    :param edge_repulsion: Whether edge repulsion is currently enabled.
    """
    er_label = "on" if edge_repulsion else "off"
    lines = [
        f"Vertices: {graph.n_vertices}   Edges: {len(graph.edges)}",
        f"Edge repulsion: {er_label}  [E]",
    ]
    for i, line in enumerate(lines):
        surf = font.render(line, True, (180, 180, 180))
        screen.blit(surf, (MARGIN, MARGIN // 2 + i * 20))
