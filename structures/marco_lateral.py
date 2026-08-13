# structures/marco_lateral.py
#
# CONVENCION DE ALTURA (importante):
# L_VERT es la ALTURA FINAL REAL de la estructura, medida de la cara
# inferior (la que toca el piso, z=0) a la cara superior externa del
# riel de arriba (z=L_VERT). El codigo descuenta internamente medio
# perfil (HALF = S/2) en cada extremo para que, sin importar que perfiles
# horizontales conectes arriba/abajo, la medida final siga siendo
# exactamente la que pediste - no se "suma" altura de mas.
#
# POSTES INTERMEDIOS:
# L_HORZ es el largo total del riel (inicio a fin). Se colocan postes
# verticales cada POST_SPACING mm, incluyendo el de inicio y el final.
# L_HORZ debe ser multiplo exacto de POST_SPACING (si no, se avisa por
# consola en vez de fallar silenciosamente).

import math
from config import PROFILE_SIZE as S
from profiles import make_tube_z, make_tube_x, make_tube_between

HALF = S / 2.0


def build(L_VERT=2000.0, L_HORZ=2700.0, angle_deg=67.5,
          l_inclinado_izq=1940.0, l_inclinado_der=1940.0,
          post_spacing=900.0):
    bot_cl = HALF
    top_cl = L_VERT - HALF
    largo_poste = top_cl - bot_cl

    # El riel (horiz_top/horiz_bot) se extiende medio perfil (HALF) mas alla
    # de cada poste extremo, para llegar a su CARA EXTERNA en vez de
    # quedarse en su centerline. L_HORZ sigue siendo la distancia
    # centro-a-centro entre el primer y ultimo poste (define el espaciado
    # de 900mm parejo); el riel fisico mide L_HORZ + 60mm (30 de cada lado).
    largo_riel = L_HORZ + S
    horiz_top = make_tube_x(largo_riel, top_cl).translate((HALF, 0, 0))
    horiz_bot = make_tube_x(largo_riel, bot_cl).translate((HALF, 0, 0))

    # --- Postes verticales cada post_spacing, incluyendo inicio y final ---
    resto = L_HORZ % post_spacing
    if abs(resto) > 1e-6 and abs(resto - post_spacing) > 1e-6:
        print(f"AVISO: L_HORZ ({L_HORZ}mm) no es multiplo exacto de "
              f"post_spacing ({post_spacing}mm) - el ultimo tramo va a "
              f"quedar mas corto que el resto.")

    n_postes = round(L_HORZ / post_spacing) + 1
    posiciones_x = [-i * post_spacing for i in range(n_postes)]

    piezas = {
        "horiz_top": horiz_top,
        "horiz_bot": horiz_bot,
    }

    puntos_top_centerline = {}
    for i, x in enumerate(posiciones_x):
        poste = make_tube_z(largo_poste, x=x).translate((0, 0, bot_cl))
        if i == 0:
            nombre = "vertical"
        elif i == len(posiciones_x) - 1:
            nombre = "vertical_final"
        else:
            nombre = f"vertical_centro_{i}"
        piezas[nombre] = poste
        # Punto en la centerline superior de este poste (z=top_cl), util
        # para conectar perfiles horizontales "por arriba" entre marcos.
        puntos_top_centerline[nombre] = (x, 0, top_cl)


# --- Inclinado izquierdo: arranca en el centerline del riel inferior,
    # en el ultimo poste (x=-L_HORZ) ---
    dx = -l_inclinado_izq * math.cos(math.radians(angle_deg))
    dz = l_inclinado_izq * math.sin(math.radians(angle_deg))
    end_incl_izq = (-L_HORZ + dx, 0.0, bot_cl + dz)
    inclinado_izq = make_tube_between((-L_HORZ, 0, bot_cl), end_incl_izq)
    conector_izq = make_tube_between((-L_HORZ, 0, top_cl), end_incl_izq)

    # --- Inclinado derecho (independiente, puede tener otro largo) ---
    dx_der = l_inclinado_der * math.cos(math.radians(angle_deg))
    dz_der = l_inclinado_der * math.sin(math.radians(angle_deg))
    end_incl_der = (dx_der, 0.0, bot_cl + dz_der)
    inclinado_der = make_tube_between((0, 0, bot_cl), end_incl_der)
    conector_der = make_tube_between((0, 0, top_cl), end_incl_der)

    piezas.update({
        "inclinado_izq": inclinado_izq,
        "conector_izq": conector_izq,
        "inclinado_der": inclinado_der,
        "conector_der": conector_der,
    })

    puntos_conexion = {
        "punta_inclinado_izq": end_incl_izq,
        "punta_inclinado_der": end_incl_der,
        "base_vertical_inicio": (0, 0, 0),
        "base_vertical_final": (-L_HORZ, 0, 0),
        "top_vertical_inicio": (0, 0, L_VERT),
        "top_vertical_final": (-L_HORZ, 0, L_VERT),
    }
    # Puntos "top" a nivel centerline (z=top_cl) de CADA poste (incluye
    # vertical, vertical_centro_1, vertical_centro_2, vertical_final) -
    # para conectar perfiles horizontales entre marcos "por arriba".
    for nombre, punto in puntos_top_centerline.items():
        puntos_conexion[f"top_cl_{nombre}"] = punto

    return piezas, puntos_conexion