# structures/soporte_pivote.py
#
# Soporte del eje de pivote de los triangulos tipo abanico:
#   - Una PLACA plana atornillada al piso (representa el anclaje real).
#   - 2 CARTELAS triangulares de refuerzo que salen de la placa hacia
#     el poste (una a cada lado, en +Y y -Y).
#   - La VARILLA (eje de pivote) en z=30 (la misma altura donde
#     confluyen horiz_bot, vertical_final e inclinado_izq), para que
#     atraviese fisicamente esos perfiles fijos y, mas adelante, los
#     4 lados de los triangulos moviles (que ya se subieron a z=30
#     tambien, ver OFFSET_TRIANGULO en assembly.py).
#
# Por ahora NO se implementa el giro/repliegue en si - esto solo pone
# la geometria de soporte en su lugar.

from profiles import make_rod_between, make_plate, make_gusset_yz

ROD_DIAMETER = 20.0    # diametro de la varilla/perno (mm)
MARGEN_EXTRA = 30.0    # cuanto se extiende la varilla mas alla del ultimo triangulo

PLATE_WIDTH_X = 200.0   # ancho de la placa (en X)
PLATE_DEPTH_Y = 200.0   # profundidad de la placa (en Y)
PLATE_THICK = 10.0      # espesor de la placa

GUSSET_SIZE_Y = 100.0   # que tanto se extiende la cartela en Y
GUSSET_SIZE_Z = 150.0   # que tanto sube la cartela en Z
GUSSET_THICK = 10.0     # espesor de la cartela (en X)


def build(p_base_vertical_final, y_triangulos, x_pivote, z_pivote):
    """
    p_base_vertical_final: punto fisico (x, y, z=0) del poste
                            vertical_final - el suelo, donde va la placa.
    y_triangulos:           lista de coordenadas Y de cada triangulo.
    x_pivote, z_pivote:     posicion (x, z) del eje de pivote - debe
                            coincidir con el nodo real del marco
                            (z=30, la centerline de horiz_bot) y con
                            el vertice_base de los triangulos (ya
                            alineado a esa misma z en assembly.py).
    """
    x_base, y_base, z_suelo = p_base_vertical_final
    y_inicio = y_base

    # Detecta automaticamente hacia que lado quedan los triangulos
    # (pueden estar en +Y o -Y respecto al poste, segun de que esquina
    # del marco cuelgue este mecanismo) y ajusta la varilla y la cartela
    # de refuerzo para crecer del lado correcto.
    y_promedio_triangulos = sum(y_triangulos) / len(y_triangulos)
    hacia_mas_y = y_promedio_triangulos >= y_inicio

    if hacia_mas_y:
        y_fin = max(y_triangulos) + MARGEN_EXTRA
    else:
        y_fin = min(y_triangulos) - MARGEN_EXTRA

    # --- Placa atornillada al piso ---
    placa = make_plate(
        PLATE_WIDTH_X, PLATE_DEPTH_Y, PLATE_THICK,
        center_x=x_pivote, center_y=y_base, top_z=z_suelo,
    )

    # --- Varilla / eje de pivote ---
    p_inicio = (x_pivote, y_inicio, z_pivote)
    p_fin = (x_pivote, y_fin, z_pivote)
    varilla_pivote = make_rod_between(p_inicio, p_fin, ROD_DIAMETER)

    # --- Cartela de refuerzo hacia el lado SEGURO (opuesto a donde
    # quedan los triangulos, para no invadir su espacio de giro) ---
    cartela = make_gusset_yz(
        GUSSET_SIZE_Y, GUSSET_SIZE_Z, GUSSET_THICK,
        center_x=x_pivote, corner_y=y_base, corner_z=z_suelo,
        flip_y=hacia_mas_y,
    )
    nombre_cartela = "cartela_menos_y" if hacia_mas_y else "cartela_mas_y"

    piezas = {
        "placa_base": placa,
        "varilla_pivote": varilla_pivote,
        nombre_cartela: cartela,
    }

    puntos_conexion = {
        "eje_pivote_inicio": p_inicio,
        "eje_pivote_fin": p_fin,
    }

    return piezas, puntos_conexion