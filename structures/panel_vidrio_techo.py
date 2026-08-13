# structures/panel_vidrio_techo.py
import cadquery as cq

GAP_EMPAQUE = 2.0
GROSOR_VIDRIO = 8.0
BEAD_TRASLAPE = 20.0
BEAD_GROSOR = 6.0


def build(x_poste_a, x_poste_b, y_min, y_max, z_centro):
    x_izq = min(x_poste_a, x_poste_b) + 30 + GAP_EMPAQUE
    x_der = max(x_poste_a, x_poste_b) - 30 - GAP_EMPAQUE

    Z_EXTERIOR = z_centro + 30  # al ras de la cara superior (exterior) del tubo
    techo = cq.Workplane("XY", origin=(x_izq, y_min, Z_EXTERIOR - GROSOR_VIDRIO)).box(
        x_der - x_izq, y_max - y_min, GROSOR_VIDRIO, centered=False)

    Z_INF = Z_EXTERIOR - GROSOR_VIDRIO - BEAD_GROSOR
    beads = {}
    for nombre, x_cara, sentido in [("izq", min(x_poste_a, x_poste_b), 1),
                                      ("der", max(x_poste_a, x_poste_b), -1)]:
        x0 = x_cara + 30 if sentido == 1 else x_cara - 30 - BEAD_TRASLAPE
        beads[f"techo_bead_{nombre}_int"] = cq.Workplane(
            "XY", origin=(x0, y_min, Z_INF)).box(BEAD_TRASLAPE, y_max - y_min, BEAD_GROSOR, centered=False)
    for nombre, y_cara, sentido in [("ymin", y_min, 1), ("ymax", y_max, -1)]:
        y0 = y_cara if sentido == 1 else y_cara - BEAD_TRASLAPE
        beads[f"techo_bead_{nombre}_int"] = cq.Workplane(
            "XY", origin=(x_izq, y0, Z_INF)).box(x_der - x_izq, BEAD_TRASLAPE, BEAD_GROSOR, centered=False)

    piezas = {"techo_vidrio": techo}
    piezas.update(beads)
    puntos_conexion = {"centro": ((x_izq + x_der) / 2, (y_min + y_max) / 2, z_centro)}
    return piezas, puntos_conexion