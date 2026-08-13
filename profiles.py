import cadquery as cq
from config import PROFILE_SIZE as S, WALL_THICK as T


def make_tube_z(length, x=0.0, y=0.0):
    """Tubo cuadrado hueco, eje a lo largo de Z, de z=0 a z=length,
    centrado en (x, y) en el plano XY."""
    return (
        cq.Workplane("XY", origin=(x, y, 0))
        .rect(S, S)
        .rect(S - 2 * T, S - 2 * T)
        .extrude(length)
    )


def make_tube_x(length, z_center):
    """Tubo cuadrado hueco, eje a lo largo de X, a la altura z_center,
    extendiendose hacia -X (izquierda) desde x=0."""
    plane = cq.Workplane("YZ", origin=(0, 0, z_center))
    return plane.rect(S, S).rect(S - 2 * T, S - 2 * T).extrude(-length)


def make_tube_between(p0, p1, x_dir=None):
    """Tubo cuadrado hueco entre dos puntos cualquiera. Si se pasa x_dir,
    la seccion cuadrada se rota sobre su propio eje para alinearse con
    esa direccion (util para que un conector coincida visualmente con
    la inclinacion de otro perfil)."""
    p0v, p1v = cq.Vector(*p0), cq.Vector(*p1)
    direction = p1v - p0v
    if x_dir is not None:
        plane = cq.Plane(origin=p0v, xDir=cq.Vector(*x_dir), normal=direction)
    else:
        plane = cq.Plane(origin=p0v, normal=direction)
    return (
        cq.Workplane(plane)
        .rect(S, S)
        .rect(S - 2 * T, S - 2 * T)
        .extrude(direction.Length)
    )

def make_rod_between(p0, p1, diameter):
    """Varilla/perno cilindrico entre dos puntos (para ejes de pivote,
    tornillos, bisagras - a diferencia de make_tube_between que es
    cuadrado, esto es redondo)."""
    p0v, p1v = cq.Vector(*p0), cq.Vector(*p1)
    direction = p1v - p0v
    plane = cq.Plane(origin=p0v, normal=direction)
    return cq.Workplane(plane).circle(diameter / 2).extrude(direction.Length)


def make_plate(width_x, depth_y, thickness_z, center_x, center_y, top_z):
    """Placa plana rectangular (para bases atornilladas al piso). La
    placa queda centrada en (center_x, center_y), con su cara SUPERIOR
    en top_z (y el resto del grosor hacia abajo, como si estuviera
    empotrada/anclada en el piso)."""
    return (
        cq.Workplane("XY", origin=(center_x, center_y, top_z - thickness_z))
        .rect(width_x, depth_y)
        .extrude(thickness_z)
    )


def make_gusset_yz(size_y, size_z, thickness_x, center_x, corner_y, corner_z,
                    flip_y=False):
    """Cartela/refuerzo triangular plano: una placa delgada en X, con
    forma de triangulo rectangulo en el plano Y-Z. corner_y y corner_z
    son el vertice del angulo recto (la esquina donde se junta con el
    poste y la placa). flip_y decide hacia que lado (+Y o -Y) apunta
    el triangulo."""
    signo = -1 if flip_y else 1
    p0 = (corner_y, corner_z)
    p1 = (corner_y + signo * size_y, corner_z)
    p2 = (corner_y, corner_z + size_z)
    face = (
        cq.Workplane("YZ", origin=(center_x - thickness_x / 2, 0, 0))
        .moveTo(*p0)
        .lineTo(*p1)
        .lineTo(*p2)
        .close()
    )
    return face.extrude(thickness_x)

def make_clevis(center_x, center_y, base_z, pin_z, piston_diametro=20.0):
    """Horquilla real tipo fork: 2 paredes separadas con un hueco entre
    ellas, donde encaja el 'ojo' del piston (un disco con agujero), y un
    perno que atraviesa pared-ojo-pared, permitiendo que el piston pivote
    libremente."""
    OJO_DIAM = piston_diametro + 14
    OJO_GROSOR = 10.0
    PARED_GROSOR = 6.0
    HUECO_PIN = 12.0
    separacion = OJO_GROSOR + 2.0

    y0_1 = center_y - separacion / 2
    pared_1_solida = cq.Workplane("XZ", origin=(center_x, y0_1, base_z)).rect(
        35, 50, centered=(True, False)).extrude(PARED_GROSOR)
    b1 = pared_1_solida.val().BoundingBox()
    hoyo1 = cq.Workplane("XZ", origin=(center_x, b1.ymax + 2, pin_z)).circle(
        HUECO_PIN / 2).extrude(b1.ymax - b1.ymin + 4)
    pared_1 = pared_1_solida.cut(hoyo1)

    y0_2 = center_y + separacion / 2
    pared_2_solida = cq.Workplane("XZ", origin=(center_x, y0_2, base_z)).rect(
        35, 50, centered=(True, False)).extrude(-PARED_GROSOR)
    b2 = pared_2_solida.val().BoundingBox()
    hoyo2 = cq.Workplane("XZ", origin=(center_x, b2.ymax + 2, pin_z)).circle(
        HUECO_PIN / 2).extrude(b2.ymax - b2.ymin + 4)
    pared_2 = pared_2_solida.cut(hoyo2)

    base = cq.Workplane("XY", origin=(center_x - 17.5, b1.ymin, base_z)).box(
        35, b2.ymax - b1.ymin, 8, centered=False)
    horquilla = pared_1.union(pared_2).union(base)

    gap_centro = (b1.ymax + b2.ymin) / 2
    ojo = cq.Workplane("XZ", origin=(center_x, gap_centro + OJO_GROSOR / 2, pin_z)).circle(
        OJO_DIAM / 2).circle(HUECO_PIN / 2 + 0.5).extrude(OJO_GROSOR)

    largo_perno = (b2.ymax + 3) - (b1.ymin - 3)
    perno = cq.Workplane("XZ", origin=(center_x, b1.ymin - 3, pin_z)).circle(
        HUECO_PIN / 2 - 0.5).extrude(-largo_perno)

    return horquilla, ojo, perno