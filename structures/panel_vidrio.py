# structures/panel_vidrio.py
import cadquery as cq

CLEARANCE = 5.0
GROSOR_VIDRIO = 8.0
BEAD_TRASLAPE = 20.0
BEAD_GROSOR = 6.0


def build(x_poste_a, x_poste_b, z_abajo_cara, z_arriba_cara, grosor=GROSOR_VIDRIO, signo_exterior=-1.0):
    x_izq_poste, x_der_poste = min(x_poste_a, x_poste_b), max(x_poste_a, x_poste_b)
    x_izq = x_izq_poste + 30 + CLEARANCE
    x_der = x_der_poste - 30 - CLEARANCE
    z_abajo = z_abajo_cara + CLEARANCE
    z_arriba = z_arriba_cara - CLEARANCE

    Y_EXTERIOR_FACE = signo_exterior * 30.0  # al ras de la cara exterior del propio tubo
    Y_MIN_VIDRIO = Y_EXTERIOR_FACE if signo_exterior == -1 else Y_EXTERIOR_FACE - grosor
    vidrio = cq.Workplane("XY", origin=(x_izq, Y_MIN_VIDRIO, z_abajo)).box(
        x_der - x_izq, grosor, z_arriba - z_abajo, centered=False)

    Y_INT_FACE = Y_EXTERIOR_FACE - signo_exterior * grosor
    Y_INT = Y_INT_FACE if signo_exterior == -1 else Y_INT_FACE - BEAD_GROSOR
    beads = {}
    for nombre, z_cara, hacia_adentro in [("abajo", z_abajo_cara, 1), ("arriba", z_arriba_cara, -1)]:
        z0 = z_cara if hacia_adentro == 1 else z_cara - BEAD_TRASLAPE
        beads[f"vidrio_bead_{nombre}_int"] = cq.Workplane(
            "XY", origin=(x_izq_poste + 30, Y_INT, z0)).box(
            (x_der_poste - 30) - (x_izq_poste + 30), BEAD_GROSOR, BEAD_TRASLAPE, centered=False)
    for nombre, x_cara, hacia_adentro in [("izq", x_izq_poste, 1), ("der", x_der_poste, -1)]:
        x0 = x_cara + 30 if hacia_adentro == 1 else x_cara - 30 - BEAD_TRASLAPE
        beads[f"vidrio_bead_{nombre}_int"] = cq.Workplane(
            "XY", origin=(x0, Y_INT, z_abajo_cara + 30)).box(
            BEAD_TRASLAPE, BEAD_GROSOR, (z_arriba_cara - 30) - (z_abajo_cara + 30), centered=False)

    piezas = {"vidrio": vidrio}
    piezas.update(beads)
    puntos_conexion = {"centro": ((x_izq + x_der) / 2, 0, (z_abajo + z_arriba) / 2)}
    return piezas, puntos_conexion