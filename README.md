# PCAP Course Project: Graph coloring generator

An interactive pygame visualiser that generates random planar graphs and colors them greedily.

## What it does

- Generates a random connected planar graph using Delaunay triangulation with random edge thinning
- Colors the vertices with a greedy algorithm (minimising the number of colors used)
- Renders the graph in a pygame window at 60 FPS

## Controls

| Key       | Action                                      |
|-----------|---------------------------------------------|
| `R`       | Regenerate graph with the current vertex count |
| `↑` / `↓` | Increase / decrease vertex count (range 6–24) and regenerate |
| `ESC`     | Quit                                        |

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
graph.py   — Graph / GraphEmbedding classes and random_planar_graph factory
main.py    — pygame event loop and rendering
```
