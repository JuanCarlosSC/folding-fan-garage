# structures/panel_vidrio_triangulo.py
#
# Vidrio completo para una pareja de triangulos del abanico:
#   - 1 panel "vientre" (el rectangulo entre conector_lado_a y conector_lado_b)
#   - 2 "tapas" triangulares (una en cada extremo, la forma de lado_a/lado_b/lado_c_cierre)
#   - beads (varillas delgadas) en todos los bordes, solo del lado interior.

import cadquery as cq
import math
from profiles import make_rod_between

GROSOR_VIDRIO = 8.0
INSET = 30.0        # medio tubo real (30mm) - el vidrio queda al ras, sin holgura
BEAD_GROSOR = 6.0


def _inset_triangle_2d(v0, v1, v2, d):
    """Encoge un triangulo (2D) moviendo cada arista hacia adentro d mm."""
    def normal_hacia_adentro(pa, pb, pc):
        ex, ez = pb[0] - pa[0], pb[1] - pa[1]
        largo = math.hypot(ex, ez)
        nx, nz = -ez / largo, ex / largo
        if (pc[0] - pa[0]) * nx + (pc[1] - pa[1]) * nz < 0:
            nx, nz = -nx, -nz
        return nx, nz

    def offset_line(pa, pb, nx, nz, d):
        return (pa[0] + nx * d, pa[1] + nz * d), (pb[0] + nx * d, pb[1] + nz * d)

    def interseccion(p1, p2, p3, p4):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

    n01 = normal_hacia_adentro(v0, v1, v2)
    n12 = normal_hacia_adentro(v1, v2, v0)
    n20 = normal_hacia_adentro(v2, v0, v1)
    e01a, e01b = offset_line(v0, v1, *n01, d)
    e12a, e12b = offset_line(v1, v2, *n12, d)
    e20a, e20b = offset_line(v2, v0, *n20, d)
    return (interseccion(e20a, e20b, e01a, e01b),
            interseccion(e01a, e01b, e12a, e12b),
            interseccion(e12a, e12b, e20a, e20b))


def _make_tapa(puntos, offset, y_exterior_face, signo_exterior):
    v0 = (puntos["vertice_base"][0], puntos["vertice_base"][2])
    v1 = (puntos["punta_lado_a"][0], puntos["punta_lado_a"][2])
    v2 = (puntos["punta_lado_b"][0], puntos["punta_lado_b"][2])
    nv0, nv1, nv2 = _inset_triangle_2d(v0, v1, v2, INSET)
    ox, oy, oz = offset
    y0 = y_exterior_face if signo_exterior == -1 else y_exterior_face - GROSOR_VIDRIO
    wp = cq.Workplane("XZ", origin=(0, y0, 0)).moveTo(ox + nv0[0], oz + nv0[1]).lineTo(
        ox + nv1[0], oz + nv1[1]).lineTo(ox + nv2[0], oz + nv2[1]).close()
    # OJO: el plano "XZ" incorporado de cadquery tiene su normal en -Y
    # (no +Y). Con y0 ya colocado en la cara exterior real (o interior,
    # segun el caso - ver arriba), en AMBOS casos hay que extruir -8
    # (no +8) para crecer siempre hacia ADENTRO del marco, nunca hacia
    # afuera. Antes esto dependia (mal) de signo_exterior.
    vidrio = wp.extrude(-GROSOR_VIDRIO)

    y_bead = (y_exterior_face - signo_exterior * GROSOR_VIDRIO) - signo_exterior * BEAD_GROSOR / 2
    pts3d = [(ox + p[0], y_bead, oz + p[1]) for p in (nv0, nv1, nv2)]
    beads = [make_rod_between(pts3d[i], pts3d[(i + 1) % 3], BEAD_GROSOR) for i in range(3)]
    return vidrio, beads


def _esquina_exterior(tubo, y_extremo, dir_ancho, p_extremo, pivote):
    """Vertice REAL (del solido) mas exterior de un tubo, en el extremo
    Y=y_extremo: usa la perpendicular a dir_ancho (igual criterio que en
    panel_vidrio_superior), orientada para apuntar hacia afuera del
    pivote del triangulo (vertice_base) - un criterio direccional, mas
    robusto que solo 'distancia al pivote' (que puede empatar entre 2
    esquinas)."""
    normal_hint = cq.Vector(-dir_ancho.z, 0, dir_ancho.x)
    p_extremo_v = cq.Vector(*p_extremo)
    pivote_v = cq.Vector(*pivote)
    if (p_extremo_v - pivote_v).dot(normal_hint) < 0:
        normal_hint = normal_hint.multiply(-1.0)
    verts = [v.Center() for v in tubo.Vertices() if abs(v.Center().y - y_extremo) < 1.0]
    return max(verts, key=lambda c: (c - p_extremo_v).dot(normal_hint))


def _make_belly(pa1, pa3, pb1, pb3, tubo_a, tubo_b, pivote_1):
    """pa1,pa3: punta_lado_a de triangulo 1 y 3 (CON offset).
    pb1,pb3: punta_lado_b de triangulo 1 y 3 (CON offset).
    tubo_a, tubo_b: solidos REALES de conector_lado_a/conector_lado_b -
    se usan para encontrar sus esquinas exteriores EXACTAS (0mm de gap),
    igual que se hizo para panel_vidrio_superior."""
    dir_ancho_aprox = cq.Vector(pb1[0] - pa1[0], 0, pb1[2] - pa1[2])
    corner_a = _esquina_exterior(tubo_a, pa1[1], dir_ancho_aprox, pa1, pivote_1)
    corner_b = _esquina_exterior(tubo_b, pb1[1], dir_ancho_aprox, pb1, pivote_1)

    dir_ancho = cq.Vector(corner_b.x - corner_a.x, 0, corner_b.z - corner_a.z)
    ancho_vidrio = dir_ancho.Length
    dir_ancho_unit = dir_ancho.multiply(1.0 / ancho_vidrio)
    normal = cq.Vector(-dir_ancho_unit.z, 0, dir_ancho_unit.x)

    profundidad_vidrio = (pa3[1] - pa1[1]) - 2 * INSET

    origen = cq.Vector(corner_a.x, pa1[1] + INSET, corner_a.z)
    plane = cq.Plane(origin=origen, xDir=dir_ancho_unit, normal=normal)

    # El vidrio crece hacia adentro (hacia el pivote) desde la cara
    # exterior real - detectamos el sentido correcto comparando con
    # donde esta el pivote respecto al plano.
    hacia_pivote = cq.Vector(*pivote_1) - origen
    signo_interior = 1.0 if hacia_pivote.dot(normal) > 0 else -1.0

    vidrio = cq.Workplane(plane).rect(ancho_vidrio, profundidad_vidrio, centered=False).extrude(
        GROSOR_VIDRIO * signo_interior)

    origen_bead = origen + normal.multiply((GROSOR_VIDRIO + BEAD_GROSOR / 2.0) * signo_interior)
    c1 = origen_bead
    c2 = origen_bead + dir_ancho_unit.multiply(ancho_vidrio)
    c3 = c2 + cq.Vector(0, profundidad_vidrio, 0)
    c4 = c1 + cq.Vector(0, profundidad_vidrio, 0)
    esquinas = [(c1.x, c1.y, c1.z), (c2.x, c2.y, c2.z), (c3.x, c3.y, c3.z), (c4.x, c4.y, c4.z)]
    beads = [make_rod_between(esquinas[i], esquinas[(i + 1) % 4], BEAD_GROSOR) for i in range(4)]
    return vidrio, beads


def build(puntos_1, puntos_3, offset_1, offset_3, y_exterior_1, y_exterior_3,
          tubo_conector_a, tubo_conector_b):
    """
    puntos_1, puntos_3: puntos_conexion (LOCALES, sin offset) de los 2
                        triangulos de la pareja.
    offset_1, offset_3: los OFFSET_TRIANGULO_X usados para cada uno.
    y_exterior_1, y_exterior_3: cara exterior (Y) de cada tapa - el
                        extremo MAS ALEJADO del otro triangulo de la
                        pareja (ej: para triangulo/y=70, es 40; para su
                        pareja en y=3930, es 3960).
    tubo_conector_a, tubo_conector_b: solidos REALES de conector_lado_a
                        y conector_lado_b de esta pareja - para que el
                        panel "vientre" quede al ras exacto (0mm) con
                        ellos, en vez de una aproximacion.
    """
    p1 = {n: tuple(a + b for a, b in zip(p, offset_1)) for n, p in puntos_1.items()}
    p3 = {n: tuple(a + b for a, b in zip(p, offset_3)) for n, p in puntos_3.items()}

    vidrio_tapa1, beads_tapa1 = _make_tapa(puntos_1, offset_1, y_exterior_1, signo_exterior=-1)
    vidrio_tapa3, beads_tapa3 = _make_tapa(puntos_3, offset_3, y_exterior_3, signo_exterior=1)
    vidrio_belly, beads_belly = _make_belly(
        p1["punta_lado_a"], p3["punta_lado_a"], p1["punta_lado_b"], p3["punta_lado_b"],
        tubo_conector_a, tubo_conector_b, p1["vertice_base"])

    piezas = {
        "vidrio_tapa1": vidrio_tapa1,
        "vidrio_tapa3": vidrio_tapa3,
        "vidrio_belly": vidrio_belly,
    }
    for i, b in enumerate(beads_tapa1):
        piezas[f"vidrio_bead_tapa1_{i}"] = b
    for i, b in enumerate(beads_tapa3):
        piezas[f"vidrio_bead_tapa3_{i}"] = b
    for i, b in enumerate(beads_belly):
        piezas[f"vidrio_bead_belly_{i}"] = b

    return piezas, {}