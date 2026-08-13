# structures/puerta_bisagra.py
from profiles import make_tube_between
import cadquery as cq

GAP_EMPAQUE = 2.0
GROSOR_VIDRIO = 8.0
BEAD_TRASLAPE = 20.0
BEAD_GROSOR = 6.0


def build(x_poste_bisagra, x_poste_otro, z_abajo, z_arriba, angulo_apertura=0.0):
    signo = 1 if x_poste_otro > x_poste_bisagra else -1
    cara_interna_bisagra = x_poste_bisagra + signo * 30
    cara_interna_otro = x_poste_otro - signo * 30
    x_bisagra_cl = cara_interna_bisagra + signo * 30
    ancho_puerta = signo * (cara_interna_otro - signo * 30 - x_bisagra_cl)
    x_lejos_cl = x_bisagra_cl + ancho_puerta * signo
    x_min_marco, x_max_marco = min(x_bisagra_cl, x_lejos_cl), max(x_bisagra_cl, x_lejos_cl)

    z_abajo_p = z_abajo + 30
    z_arriba_p = z_arriba - 30

    # --- Todo construido en angulo=0 (cerrado), rotado al final ---
    p1, p2 = (x_bisagra_cl, 0, z_abajo_p), (x_bisagra_cl, 0, z_arriba_p)
    p3, p4 = (x_lejos_cl, 0, z_abajo_p), (x_lejos_cl, 0, z_arriba_p)
    marco_abajo = make_tube_between(p1, p3)
    marco_arriba = make_tube_between(p2, p4)
    marco_bisagra_lado = make_tube_between(p1, p2)
    marco_lejos_lado = make_tube_between(p3, p4)

    x0v = x_bisagra_cl + signo * (30 + GAP_EMPAQUE)
    x1v = x_lejos_cl - signo * (30 + GAP_EMPAQUE)
    z0v, z1v = z_abajo_p + 30 + GAP_EMPAQUE, z_arriba_p - 30 - GAP_EMPAQUE
    Y_EXTERIOR = -30.0
    vidrio = cq.Workplane("XY", origin=(min(x0v, x1v), Y_EXTERIOR, z0v)).box(
        abs(x1v - x0v), GROSOR_VIDRIO, z1v - z0v, centered=False)

    Y_INT = Y_EXTERIOR + GROSOR_VIDRIO
    beads = {}
    for nombre, z_cara, hacia_adentro in [("abajo", z_abajo_p, 1), ("arriba", z_arriba_p, -1)]:
        z0 = z_cara if hacia_adentro == 1 else z_cara - BEAD_TRASLAPE
        beads[f"puerta_bead_{nombre}_int"] = cq.Workplane(
            "XY", origin=(x_min_marco + 30, Y_INT, z0)).box(
            (x_max_marco - 30) - (x_min_marco + 30), BEAD_GROSOR, BEAD_TRASLAPE, centered=False)
    for nombre, x_cara, hacia_adentro in [
        ("bisagra", x_bisagra_cl, 1 if x_lejos_cl > x_bisagra_cl else -1),
        ("lejos", x_lejos_cl, -1 if x_lejos_cl > x_bisagra_cl else 1),
    ]:
        x0 = x_cara + 30 if hacia_adentro == 1 else x_cara - 30 - BEAD_TRASLAPE
        beads[f"puerta_bead_{nombre}_int"] = cq.Workplane(
            "XY", origin=(x0, Y_INT, z_abajo_p + 30)).box(
            BEAD_TRASLAPE, BEAD_GROSOR, (z_arriba_p - 30) - (z_abajo_p + 30), centered=False)

    eje_p0 = (x_bisagra_cl, 0, 0)
    eje_p1 = (x_bisagra_cl, 0, 100)
    rot = -angulo_apertura

    piezas = {
        "puerta_abajo": marco_abajo.rotate(eje_p0, eje_p1, rot),
        "puerta_arriba": marco_arriba.rotate(eje_p0, eje_p1, rot),
        "puerta_bisagra_lado": marco_bisagra_lado.rotate(eje_p0, eje_p1, rot),
        "puerta_lejos_lado": marco_lejos_lado.rotate(eje_p0, eje_p1, rot),
        "puerta_vidrio": vidrio.rotate(eje_p0, eje_p1, rot),
    }
    for nombre, bead in beads.items():
        piezas[nombre] = bead.rotate(eje_p0, eje_p1, rot)

    puntos_conexion = {
        "eje_bisagra_abajo": p1,
        "eje_bisagra_arriba": p2,
    }
    return piezas, puntos_conexion