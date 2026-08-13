# Folding Fan Garage

A fully parametric CAD model of a folding, fan-style glass garage enclosure, built entirely in Python with [CadQuery](https://github.com/CadQuery/cadquery).

The structure is a curved glazed frame supported by a "fan" of pivoting triangular braces that can fold open or closed, plus a hinged door, a sliding door, and full glazing on the roof, walls, and moving triangles.

![preview](docs/preview.png)

## Features

- **Parametric side frames** (`marco_lateral.py`) — vertical posts, top/bottom rails, and inclined braces, fully driven by height, width, angle, and post-spacing parameters.
- **Folding triangle fan mechanism** (`triangulo.py`, `soporte_pivote.py`) — pairs of pivoting triangular braces with pistons, clevises, and pivot supports, mirrored on both sides of the garage.
- **Doors** — a hinged swing door (`puerta_bisagra.py`) and a sliding door with rail (`puerta_corrediza.py`).
- **Glazing, everywhere:**
  - Wall panels between posts (`panel_vidrio.py`)
  - Roof panels (`panel_vidrio_techo.py`)
  - Sloped corner/gable panels, fixed and moving (`panel_vidrio_triangulo_fijo.py`, `panel_vidrio_triangulo.py`)
  - Upper corner panels between frames (`panel_vidrio_superior.py`)
  - Every glass panel ships with its own retention beads (the thin strips that hold it in the frame)
- **A single opening parameter (`APERTURA`)** drives the entire fan mechanism from fully closed (`0.0`) to fully open (`1.0`), with intermediate positions in between.
- **Real geometry, not approximations** — glass panels are fit to the *actual* exterior corners of their surrounding tube profiles (extracted directly from the solids), not assumed offsets, so panels sit flush with 0mm gaps against the frame wherever the geometry allows it.

## Requirements

- Python 3.10+
- [CadQuery](https://github.com/CadQuery/cadquery)
- [ocp_vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) (for live viewing in VS Code) — optional, only needed to run `main.py` as-is

```bash
pip install cadquery ocp_vscode
```

## Project structure

```
.
├── main.py                          # entry point — builds the assembly and shows it
├── assembly.py                      # build_all(): wires every structure together
├── config.py                        # global constants (tube profile size, wall thickness)
├── profiles.py                      # low-level tube/rod/plate/clevis builders
│
└── structures/
    ├── marco_lateral.py             # side frame (posts, rails, inclined braces)
    ├── triangulo.py                 # single folding triangle brace
    ├── soporte_pivote.py            # pivot axle support + reinforcement gusset
    ├── puerta_bisagra.py            # hinged swing door
    ├── puerta_corrediza.py          # sliding door + rail
    ├── panel_vidrio.py              # rectangular wall glass + beads
    ├── panel_vidrio_techo.py        # roof glass + beads
    ├── panel_vidrio_superior.py     # upper corner glass (between two side frames)
    ├── panel_vidrio_triangulo.py    # glass for a pair of moving fan triangles
    └── panel_vidrio_triangulo_fijo.py  # glass for the fixed corner triangles
```

## Usage

Run the whole assembly and open the interactive viewer (VS Code + [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer) extension):

```bash
python main.py
```

This calls `assembly.build_all()`, which returns:

- `piezas`: a dict of `{name: CadQuery shape}` for every part in the model
- `puntos`: a dict of named connection points (frame corners, pivot axes, triangle tips, etc.) that other structures use to position themselves

Glass is colored translucent light blue, retention beads are black, and structural tubes are the default gold/yellow.

### Key parameters (in `assembly.py`)

| Parameter | Description |
|---|---|
| `APERTURA` | `0.0` = fan closed/sealed, `1.0` = fan fully open/retracted |
| `PUERTA_ANGULO` | `0` = hinged door closed, `90` = fully open |
| `OFFSET_TRIANGULO_*` | Y-offset of each of the 12 folding triangles |
| `PLACA_PISTONES_X`, `PLACA_PISTONES_X_DER` | X-position of the piston anchor plates |

## Known limitations / roadmap

- `marco_frontal.py` is currently a stub (empty) — the front frame is not yet modeled.
- Where two tube profiles meet at an angle (e.g. a triangle's closing side and the connector to its paired triangle), the joint is currently a simple butt connection — there's a small visible step rather than a mitered/fused weld seam. A v2 pass will merge these joints so they read as a single welded piece.

## License

_Add your license here._