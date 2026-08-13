# structures/panel_vidrio_triangulo_fijo.py
import cadquery as cq
import math

GAP_TUBO = 32.0
INSET_VIDRIO = 35.0
OVERLAP_VIDRIO = 12.0
GROSOR_VIDRIO = 8.0
BEAD_GROSOR = 6.0


def _inset_triangle_2d(v0, v1, v2, d):
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


def build(v_abajo, v_arriba, v_punta, y_pos=0.0, signo_exterior=-1.0):
    nv0, nv1, nv2 = _inset_triangle_2d(v_abajo, v_arriba, v_punta, INSET_VIDRIO)
    ev0, ev1, ev2 = _inset_triangle_2d(v_abajo, v_arriba, v_punta, GAP_TUBO)
    mv0, mv1, mv2 = _inset_triangle_2d(v_abajo, v_arriba, v_punta, INSET_VIDRIO + OVERLAP_VIDRIO)

    Y_EXTERIOR = y_pos + signo_exterior * 30.0
    wp = cq.Workplane("XZ", origin=(0, Y_EXTERIOR, 0)).moveTo(*nv0).lineTo(*nv1).lineTo(*nv2).close()
    vidrio = wp.extrude(GROSOR_VIDRIO * signo_exterior)

    Y_INT_FACE = Y_EXTERIOR - GROSOR_VIDRIO * signo_exterior

    def bead_quad(pA1, pA2, pB2, pB1):
        wp2 = cq.Workplane("XZ", origin=(0, Y_INT_FACE, 0)).moveTo(*pA1).lineTo(*pA2).lineTo(*pB2).lineTo(*pB1).close()
        return wp2.extrude(BEAD_GROSOR * signo_exterior)

    beads = [
        bead_quad(ev0, ev1, mv1, mv0),
        bead_quad(ev1, ev2, mv2, mv1),
        bead_quad(ev2, ev0, mv0, mv2),
    ]

    piezas = {"vidrio": vidrio}
    for i, b in enumerate(beads):
        piezas[f"vidrio_bead_int_{i}"] = b
    return piezas, {}