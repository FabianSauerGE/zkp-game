# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Interactive pygame visualizer for random planar graph generation, force-directed layout animation, and greedy 3-coloring. A PCAP course project.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the interactive visualizer
python main.py

# Generate example screenshots (headless, writes to screenshots/)
python make_screenshots.py
```

**Interactive controls:** `R` regenerate, `UP/DOWN` change vertex count (6–24), `E` toggle edge repulsion, `ESC` quit.

No test suite or linter is configured.

## Architecture

### Data flow

```
random_planar_graph()          src/graph.py
  → Delaunay triangulation + random edge thinning
  → returns GraphEmbedding (vertices + 2D positions)

build() in main.py
  → rescales embedding to drawable area
  → hands off to FruchtermanReingoldLayout

60 FPS event loop (main.py)
  → layout.step() while temp > 0.01
  → draw() + draw_hud() render current state
```

### Module responsibilities

- **[src/graph.py](src/graph.py)** — `Graph` (edge list + greedy coloring + connectivity), `GraphEmbedding` (adds numpy position array), `random_planar_graph()` factory.
- **[src/layout.py](src/layout.py)** — `GraphLayout` abstract base; `FruchtermanReingoldLayout` implements FR spring embedder with exponential cooling (`temp = temp0 * 0.95^i`) and optional vertex-edge repulsion for uncrossing edges.
- **[src/draw.py](src/draw.py)** — stateless pygame rendering; `VERTEX_COLORS` maps color indices 0–3 to RGB; `MARGIN=50`, `VERTEX_RADIUS=18`.
- **[main.py](main.py)** — event loop, global state (`N_VERTICES`, `EDGE_REPULSION`, `DROP_PROB=0.2`), wires all modules together.

### Key design points

- **Planarity** is preserved by seeding the FR layout from Delaunay positions (planar by construction) rather than random positions.
- **Edge repulsion** (optional, `E` key) adds O(n·e) repulsive forces per iteration between vertices and non-incident edges to reduce crossings.
- **Greedy coloring** runs on `GraphEmbedding.greedy_coloring` (lazy property, O(n²)); planar graphs typically resolve in ≤3 colors.
- `random_planar_graph()` retries until the thinned graph is connected; it keeps at least `n-1` edges to make retry rare.
