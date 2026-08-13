# structures/puerta_corrediza.py
#
# Marco de puerta corrediza (solo los 4 tubos - sin panel, para agregar
# policarbonato solido despues) que ocupa la abertura entre
# vertical_centro_1 (x=-900) y vertical_centro_2 (x=-1800).
# DOOR_APERTURA: 0.0 = cerrada (cubre la abertura), 1.0 = abierta
# (deslizada hacia -X, fuera de la abertura).

from profiles import make_tube_between

TRASLAPE = 50.0     # cuanto cubre el marco mas alla de cada borde de la abertura
Y_PUERTA = 60.0    # offset en Y, fuera del plano del marco (con holgura real)

RIEL_MARGEN = 100.0


def build(x_poste_1, x_poste_2, z_abajo, z_arriba, apertura=0.0):
    """
    x_poste_1, x_poste_2: coordenadas X (centerline) de los 2 postes que
                           forman la abertura.
    z_abajo, z_arriba:    altura Z de la cara superior de horiz_bot y la
                           cara inferior de horiz_top.
    apertura:              0.0 = cerrada, 1.0 = abierta.
    """
    x_izq = min(x_poste_1, x_poste_2)
    x_der = max(x_poste_1, x_poste_2)
    ancho_abertura = (x_der - 30) - (x_izq + 30)
    ancho_puerta = ancho_abertura + 2 * TRASLAPE
    x_centro_abertura = (x_izq + x_der) / 2

    recorrido = ancho_puerta * apertura
    x0 = x_centro_abertura - ancho_puerta / 2 - recorrido
    x1 = x0 + ancho_puerta

    z_abajo_cl = z_abajo + 30   # centerline del tubo, para que su cara toque horiz_bot
    z_arriba_cl = z_arriba - 30

    marco_abajo = make_tube_between((x0, Y_PUERTA, z_abajo_cl), (x1, Y_PUERTA, z_abajo_cl))
    marco_arriba = make_tube_between((x0, Y_PUERTA, z_arriba_cl), (x1, Y_PUERTA, z_arriba_cl))
    marco_izq = make_tube_between((x0, Y_PUERTA, z_abajo_cl), (x0, Y_PUERTA, z_arriba_cl))
    marco_der = make_tube_between((x1, Y_PUERTA, z_abajo_cl), (x1, Y_PUERTA, z_arriba_cl))

    # Riel superior: limitado a no pasarse del final real de horiz_top
    # (se pasa el limite max_x_horiz_top como parametro, ver assembly.py)
    piezas = {
        "puerta_marco_abajo": marco_abajo,
        "puerta_marco_arriba": marco_arriba,
        "puerta_marco_izq": marco_izq,
        "puerta_marco_der": marco_der,
    }
    puntos_conexion = {
        "centro_abertura": (x_centro_abertura, 0, (z_abajo + z_arriba) / 2),
    }
    return piezas, puntos_conexion


def build_riel(x_poste_1, x_poste_2, z_arriba_cl):
    """Riel FIJO por donde desliza la puerta. Va a la MISMA altura que
    el marco de la puerta (no a z_arriba directo, ahi chocan los
    conectores del techo), y un poco mas adentro en Y para no chocar
    con el marco movil."""
    Y_RIEL = 130.0   # 70mm mas adentro que Y_PUERTA (60), suficiente holgura

    x_izq = min(x_poste_1, x_poste_2)
    x_der = max(x_poste_1, x_poste_2)
    ancho_abertura = (x_der - 30) - (x_izq + 30)
    ancho_puerta = ancho_abertura + 2 * TRASLAPE
    x_centro_abertura = (x_izq + x_der) / 2

    x_riel_derecha = x_centro_abertura + ancho_puerta / 2 + 20
    x_riel_izquierda = x_centro_abertura - ancho_puerta / 2 - ancho_puerta - 20

    riel = make_tube_between((x_riel_izquierda, Y_RIEL, z_arriba_cl),
                              (x_riel_derecha, Y_RIEL, z_arriba_cl))
    return {"puerta_riel": riel}