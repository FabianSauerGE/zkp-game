# PCAP Course Project: Graph coloring generator

An interactive pygame visualiser that generates random planar graphs, refines their layout with a [Fruchterman-Reingold](https://www.mathe2.uni-bayreuth.de/axel/papers/reingold:graph_drawing_by_force_directed_placement.pdf) spring simulation, and colors the vertices greedily.

## Screenshots

| FR layout settling | Edge repulsion on | Edge repulsion off |
|---|---|---|
| ![FR layout settling](screenshots/01_animating.png) | ![Edge repulsion on](screenshots/02_edge_repulsion_on.png) | ![Edge repulsion off](screenshots/03_edge_repulsion_off.png) |

## What it does

- Generates a random connected planar graph using Delaunay triangulation with random edge thinning
- Animates the layout using the Fruchterman-Reingold force-directed algorithm (warm-started from the Delaunay positions to preserve planarity)
- Optionally repels vertices away from non-incident edges to reduce edge crossings
- Colors the vertices with a greedy algorithm (minimising the number of colors used)
- Renders the graph in a pygame window at 60 FPS

## Controls

| Key       | Action                                                       |
|-----------|--------------------------------------------------------------|
| `R`       | Regenerate graph with the current vertex count               |
| `↑` / `↓` | Increase / decrease vertex count (range 6–24) and regenerate |
| `E`       | Toggle vertex-edge repulsion on/off and regenerate           |
| `ESC`     | Quit                                                         |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Project structure

```
src/
  graph.py            — Graph / GraphEmbedding classes and random_planar_graph factory
  layout.py           — GraphLayout base class and FruchtermanReingoldLayout
  draw.py             — pygame rendering constants, draw() and draw_hud()
main.py               — pygame event loop
make_screenshots.py   — headless script to regenerate screenshots/
```

To regenerate the screenshots:

```bash
python make_screenshots.py
```
