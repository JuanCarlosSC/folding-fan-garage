# structures/panel_vidrio_superior.py
import cadquery as cq

GROSOR_VIDRIO = 8.0
INSET_PROF = 30.0
BEAD_GROSOR = 6.0
BEAD_TRASLAPE = 20.0


def _esquina_exterior(tubo, y_extremo, normal_hint, p_extremo):
    """Encuentra el vertice mas exterior (real, del solido) de un tubo
    en el extremo Y=y_extremo. normal_hint ya viene garantizado con
    componente Z negativa (ver build) para que 'afuera' sea siempre
    hacia arriba, sin importar de que lado (izq/der) sea el panel."""
    p_extremo_v = cq.Vector(*p_extremo)
    verts = [v.Center() for v in tubo.Vertices() if abs(v.Center().y - y_extremo) < 1.0]
    return min(verts, key=lambda c: (c - p_extremo_v).dot(normal_hint))


def build(pa1, pa3, pb1, pb3, tubo_pa, tubo_pb, grosor=GROSOR_VIDRIO,
          inset_prof=INSET_PROF, bead_grosor=BEAD_GROSOR, bead_traslape=BEAD_TRASLAPE):
    """
    pa1, pa3: puntos (centerline) del perfil vertical en cada marco
               (ej: top_cl_vertical_final, top_cl_vertical_final_2).
    pb1, pb3: puntos (centerline) del extremo del inclinado en cada marco
               (ej: punta_inclinado_izq, punta_inclinado_izq_2).
    tubo_pa:  el SOLIDO real del conector que une pa1-pa3 (ej:
               conector_top_vertical_final) - se usa para encontrar su
               esquina exterior EXACTA (no una aproximacion).
    tubo_pb:  el SOLIDO real del conector que une pb1-pb3 (ej:
               conector_longitudinal_izq) - idem.

    El plano del vidrio se arma pasando EXACTAMENTE por la esquina
    exterior real de ambos conectores, asi el canto del vidrio queda
    al ras (0mm de separacion) con esos 2 perfiles - no una aproximacion
    con un inset fijo.
    """
    # Pista de "hacia donde es afuera": perpendicular a la pendiente del
    # panel (misma precision que antes, sensible a la inclinacion real
    # de cada tubo), pero forzada a que su componente Z sea siempre
    # NEGATIVA - asi "afuera" es consistentemente hacia ARRIBA (+Z) sin
    # importar si el panel es el del lado izq o el espejado del lado der
    # (la formula perpendicular sola se invertia mal en el lado der).
    dir_aprox = cq.Vector(pb1[0] - pa1[0], 0, pb1[2] - pa1[2])
    normal_hint = cq.Vector(-dir_aprox.z, 0, dir_aprox.x)
    if normal_hint.z > 0:
        normal_hint = normal_hint.multiply(-1.0)

    corner_pa = _esquina_exterior(tubo_pa, pa1[1], normal_hint, pa1)
    corner_pb = _esquina_exterior(tubo_pb, pb1[1], normal_hint, pb1)

    dir_ancho = cq.Vector(corner_pb.x - corner_pa.x, 0, corner_pb.z - corner_pa.z)
    ancho_vidrio = dir_ancho.Length
    dir_ancho_unit = dir_ancho.multiply(1.0 / ancho_vidrio)
    normal = cq.Vector(-dir_ancho_unit.z, 0, dir_ancho_unit.x)
    # El vidrio siempre crece hacia ADENTRO (interior = hacia abajo, Z
    # negativa) desde la cara exterior. "normal" puede salir apuntando
    # hacia arriba o hacia abajo segun el lado (izq/der) - normalizamos
    # aqui para que "avanzar hacia adentro" sea siempre extrude(+grosor),
    # sin importar el signo que le toco a "normal" en este panel.
    signo_interior = -1.0 if normal.z > 0 else 1.0

    profundidad_vidrio = (pa3[1] - pa1[1]) - 2 * inset_prof

    # origen_ext = la esquina exterior real (pa), bajada inset_prof en Y
    # -> esta ES la cara EXTERIOR/visible del vidrio, exactamente al ras
    # de ambos perfiles (conector_top_vertical_final y
    # conector_longitudinal_izq).
    origen_ext = cq.Vector(corner_pa.x, pa1[1] + inset_prof, corner_pa.z)
    plane_v = cq.Plane(origin=origen_ext, xDir=dir_ancho_unit, normal=normal)
    # El vidrio crece hacia ADENTRO (interior) desde la cara exterior.
    vidrio = cq.Workplane(plane_v).rect(ancho_vidrio, profundidad_vidrio, centered=False).extrude(grosor * signo_interior)

    # Los beads van pegados a la cara INTERIOR del vidrio (la cara
    # opuesta a origen_ext) y se extienden aun mas hacia adentro, para
    # quedar escondidos detras del vidrio.
    origen_int = origen_ext + normal.multiply(grosor * signo_interior)
    plane_bead = cq.Plane(origin=origen_int, xDir=dir_ancho_unit, normal=normal)
    wp_bead = cq.Workplane(plane_bead)
    bead_dist = bead_grosor * signo_interior
    b_abajo = wp_bead.moveTo(0, 0).rect(ancho_vidrio, bead_traslape, centered=False).extrude(bead_dist)
    b_arriba = wp_bead.moveTo(0, profundidad_vidrio - bead_traslape).rect(
        ancho_vidrio, bead_traslape, centered=False).extrude(bead_dist)
    b_izq = wp_bead.moveTo(0, 0).rect(bead_traslape, profundidad_vidrio, centered=False).extrude(bead_dist)
    b_der = wp_bead.moveTo(ancho_vidrio - bead_traslape, 0).rect(
        bead_traslape, profundidad_vidrio, centered=False).extrude(bead_dist)

    piezas = {
        "vidrio": vidrio,
        "vidrio_bead_int_abajo": b_abajo,
        "vidrio_bead_int_arriba": b_arriba,
        "vidrio_bead_int_izq": b_izq,
        "vidrio_bead_int_der": b_der,
    }
    return piezas, {}