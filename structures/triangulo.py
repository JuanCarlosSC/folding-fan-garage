# structures/triangulo.py
import math
from profiles import make_tube_between, make_rod_between

BOSS_DIAMETER = 60.0   # diametro del nudillo/boss en el vertice (mm)
BOSS_WIDTH_Y = 60.0    # ancho del boss en Y (mm) - por donde pasa la varilla

def punto_anclaje_piston(puntos, distancia=400.0):
    v = puntos['vertice_base']
    p = puntos['punta_lado_a']
    direccion = tuple(a - b for a, b in zip(p, v))
    largo = math.sqrt(sum(d**2 for d in direccion))
    unitario = tuple(d / largo for d in direccion)
    return tuple(v[i] + unitario[i] * distancia for i in range(3))

def build(lado_largo=1928.0, angulo_a_deg=67.5, angulo_b_deg=45.0,
          fold_angle=0.0, signo_x=-1.0):
    """Triangulo con dos lados largos iguales que parten de un mismo
    vertice, cada uno a su propio angulo desde la horizontal. El tercer
    lado (el que cierra el triangulo) se calcula automaticamente.

    fold_angle: rotacion adicional (grados) sobre el eje de pivote
    (vertice_base), que se suma a AMBOS angulos por igual - simula girar
    todo el triangulo como cuerpo rigido sobre la varilla. 0 = posicion
    "cerrada/sellada" (los angulos tal cual se pasaron). Por ejemplo,
    con angulo_a=67.5 y angulo_b=45, un fold_angle=22.5 deja lado_a a
    90 grados (vertical) y lado_b a 67.5 grados - alineados con
    vertical_final e inclinado_izq del marco, para "esconderse" contra
    ellos.

    En el vertice se agrega un "boss" (nudillo cilindrico) para que el
    eje de pivote (varilla) atraviese material solido real, en vez de
    solo rozar la cara donde arrancan los tubos diagonales."""

    angulo_a_efectivo = angulo_a_deg + fold_angle
    angulo_b_efectivo = angulo_b_deg + fold_angle

    origen = (0.0, 0.0, 0.0)

    end_a = (
        signo_x * lado_largo * math.cos(math.radians(angulo_a_efectivo)),
        0.0,
        lado_largo * math.sin(math.radians(angulo_a_efectivo)),
    )
    end_b = (
        signo_x * lado_largo * math.cos(math.radians(angulo_b_efectivo)),
        0.0,
        lado_largo * math.sin(math.radians(angulo_b_efectivo)),
    )

    lado_a = make_tube_between(origen, end_a)
    lado_b = make_tube_between(origen, end_b)
    lado_c = make_tube_between(end_a, end_b)   # el lado "desconocido"

    # Boss/nudillo centrado en el vertice, a lo largo de Y, unido a
    # lado_a y lado_b para que quede rigido con el resto del triangulo.
    p_boss_0 = (origen[0], origen[1] - BOSS_WIDTH_Y / 2, origen[2])
    p_boss_1 = (origen[0], origen[1] + BOSS_WIDTH_Y / 2, origen[2])
    boss_pivote = make_rod_between(p_boss_0, p_boss_1, BOSS_DIAMETER)

    dx = end_a[0] - end_b[0]
    dz = end_a[2] - end_b[2]
    longitud_lado_c = math.sqrt(dx**2 + dz**2)

    piezas = {
        "lado_a_67.5": lado_a,
        "lado_b_45": lado_b,
        "lado_c_cierre": lado_c,
        "boss_pivote": boss_pivote,
    }

    puntos_conexion = {
        "vertice_base": origen,
        "punta_lado_a": end_a,
        "punta_lado_b": end_b,
    }

    print(f"Lado de cierre (lado_c) calculado: {longitud_lado_c:.2f} mm "
          f"({longitud_lado_c/10:.2f} cm)")

    return piezas, puntos_conexion