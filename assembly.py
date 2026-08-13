from structures import marco_lateral, triangulo, soporte_pivote
from profiles import make_tube_between
from profiles import make_rod_between, make_plate, make_clevis
from structures import puerta_bisagra
from structures import panel_vidrio
from structures import panel_vidrio_techo
from structures import panel_vidrio_superior
from structures import panel_vidrio_triangulo_fijo
from structures import panel_vidrio_triangulo


# Que tan separada (en mm) va a quedar la estructura del triangulo
# respecto al marco principal, para que no se encimen visualmente.
# Por ahora NO estan conectadas entre si.
OFFSET_TRIANGULO = (-2700.0, 70.0, 50.0)
OFFSET_TRIANGULO_2 = (-2700.0, 140.0, 50.0)   # segundo triangulo (45 / 22.5)
# Triangulos espejo, anclados al otro lado (vertical_final_2 / inclinado_izq_2),
# creciendo hacia -Y (adentro del garage) en vez de +Y.
OFFSET_TRIANGULO_3 = (-2700.0, 4000.0 - 70.0, 50.0)
OFFSET_TRIANGULO_4 = (-2700.0, 4000.0 - 140.0, 50.0)
OFFSET_TRIANGULO_5 = (-2700.0, 210.0, 50.0)
OFFSET_TRIANGULO_6 = (-2700.0, 4000.0 - 210.0, 50.0)

# Segunda copia del marco lateral, desplazada 4 metros en Y positivo
# (por ejemplo, el marco del otro lado del garage / la otra pared).
OFFSET_MARCO_2 = (0.0, 4000.0, 0.0)

# Control unico de apertura del abanico: 0.0 = cerrado/sellado
# (posicion original, angulos tal cual), 1.0 = totalmente abierto/retraido
# (repliegan escondidas contra vertical_final/inclinado_izq).
# Cualquier valor entre 0 y 1 es una posicion intermedia.
APERTURA = 0
PUERTA_ANGULO = 0   # 0 = cerrada, 90 = completamente abierta

FOLD_MAX = {1: 22.5, 2: 45.0, 5: 67.5}
PISTON_ANCLAJE_DIST = 400.0
PISTON_DIAMETRO = 25.0
PLACA_PISTONES_X = -2250.0   # entre vertical_final (-2700) y vertical_centro_2 (-1800)

PLACA_PISTONES_X_DER = -450.0   # entre vertical (x=0) y vertical_centro_1 (x=-900)

def build_all():
    piezas_marco, puntos_marco = marco_lateral.build()

    piezas_marco_2, puntos_marco_2 = marco_lateral.build()
    piezas_marco_2 = {
        f"{nombre}_2": pieza.translate(OFFSET_MARCO_2)
        for nombre, pieza in piezas_marco_2.items()
    }
    puntos_marco_2 = {
        nombre: tuple(a + b for a, b in zip(punto, OFFSET_MARCO_2))
        for nombre, punto in puntos_marco_2.items()
    }

    piezas_triangulo, puntos_triangulo = triangulo.build(
        lado_largo=1840.0, fold_angle=APERTURA * FOLD_MAX[1]
    )
    puntos_triangulo_local = puntos_triangulo   # sin offset, para el vidrio
    piezas_triangulo = {
        nombre: pieza.translate(OFFSET_TRIANGULO)
        for nombre, pieza in piezas_triangulo.items()
    }
    puntos_triangulo = {
        nombre: tuple(a + b for a, b in zip(punto, OFFSET_TRIANGULO))
        for nombre, punto in puntos_triangulo.items()
    }

    # --- Segundo triangulo: mismo patron, angulos distintos (45 / 22.5),
    # lados largos un poco mas cortos que el primer triangulo (1866 vs 1928)
    piezas_triangulo_2, puntos_triangulo_2 = triangulo.build(
        lado_largo=1760.0, angulo_a_deg=45.0, angulo_b_deg=22.5,
        fold_angle=APERTURA * FOLD_MAX[2]
    )
    puntos_triangulo_2_local = puntos_triangulo_2   # sin offset, para el vidrio
    piezas_triangulo_2 = {
        f"{nombre}_2": pieza.translate(OFFSET_TRIANGULO_2)
        for nombre, pieza in piezas_triangulo_2.items()
    }
    puntos_triangulo_2 = {
        nombre: tuple(a + b for a, b in zip(punto, OFFSET_TRIANGULO_2))
        for nombre, punto in puntos_triangulo_2.items()
    }

    # --- Triangulo 3: espejo de triangulo (1), anclado del lado de marco_lateral_2 ---
    piezas_triangulo_3, puntos_triangulo_3 = triangulo.build(
        lado_largo=1840.0, fold_angle=APERTURA * FOLD_MAX[1]
    )
    puntos_triangulo_3_local = puntos_triangulo_3   # sin offset, para el vidrio
    piezas_triangulo_3 = {
        f"{nombre}_3": pieza.translate(OFFSET_TRIANGULO_3)
        for nombre, pieza in piezas_triangulo_3.items()
    }
    puntos_triangulo_3 = {
        nombre: tuple(a + b for a, b in zip(punto, OFFSET_TRIANGULO_3))
        for nombre, punto in puntos_triangulo_3.items()
    }

    # --- Triangulo 4: espejo de triangulo_2 ---
    piezas_triangulo_4, puntos_triangulo_4 = triangulo.build(
        lado_largo=1760.0, angulo_a_deg=45.0, angulo_b_deg=22.5,
        fold_angle=APERTURA * FOLD_MAX[2]
    )
    puntos_triangulo_4_local = puntos_triangulo_4   # sin offset, para el vidrio
    piezas_triangulo_4 = {
        f"{nombre}_4": pieza.translate(OFFSET_TRIANGULO_4)
        for nombre, pieza in piezas_triangulo_4.items()
    }
    puntos_triangulo_4 = {
        nombre: tuple(a + b for a, b in zip(punto, OFFSET_TRIANGULO_4))
        for nombre, punto in puntos_triangulo_4.items()
    }
    # --- Triangulo 5: angulos 22.5 / 0, hermano de triangulo_2 ---
    piezas_triangulo_5, puntos_triangulo_5 = triangulo.build(
        lado_largo=1680.0, angulo_a_deg=22.5, angulo_b_deg=0.0,
        fold_angle=APERTURA * FOLD_MAX[5]
    )
    puntos_triangulo_5_local = puntos_triangulo_5   # sin offset, para el vidrio
    piezas_triangulo_5 = {
        f"{nombre}_5": pieza.translate(OFFSET_TRIANGULO_5)
        for nombre, pieza in piezas_triangulo_5.items()
    }
    puntos_triangulo_5 = {
        nombre: tuple(a + b for a, b in zip(punto, OFFSET_TRIANGULO_5))
        for nombre, punto in puntos_triangulo_5.items()
    }

    # --- Triangulo 6: espejo de triangulo_5 ---
    piezas_triangulo_6, puntos_triangulo_6 = triangulo.build(
        lado_largo=1680.0, angulo_a_deg=22.5, angulo_b_deg=0.0,
        fold_angle=APERTURA * FOLD_MAX[5]
    )
    puntos_triangulo_6_local = puntos_triangulo_6   # sin offset, para el vidrio
    piezas_triangulo_6 = {
        f"{nombre}_6": pieza.translate(OFFSET_TRIANGULO_6)
        for nombre, pieza in piezas_triangulo_6.items()
    }
    puntos_triangulo_6 = {
        nombre: tuple(a + b for a, b in zip(punto, OFFSET_TRIANGULO_6))
        for nombre, punto in puntos_triangulo_6.items()
    }

    # --- Placa compartida de anclaje de pistones (cerca del piso, entre
    # vertical_final y vertical_centro_2) ---
    placa_pistones = make_plate(
        width_x=150.0, depth_y=240.0, thickness_z=10.0,
        center_x=PLACA_PISTONES_X, center_y=150.0, top_z=0.0,
    )

    # --- 3 pistones: de la placa a cada lado_a (triangulo, _2, _5) ---
    pistones_config = [
        (puntos_triangulo, OFFSET_TRIANGULO),
        (puntos_triangulo_2, OFFSET_TRIANGULO_2),
        (puntos_triangulo_5, OFFSET_TRIANGULO_5),
    ]
    piezas_pistones = {"placa_pistones": placa_pistones}
    for i, (puntos_t, offset_t) in enumerate(pistones_config, start=1):
        y_pos = offset_t[1]
        horquilla_base, horquilla_ojo, horquilla_pin = make_clevis(
            PLACA_PISTONES_X, y_pos, base_z=0.0, pin_z=50.0
        )
        piezas_pistones[f"horquilla_{i}"] = horquilla_base
        piezas_pistones[f"horquilla_ojo_{i}"] = horquilla_ojo
        piezas_pistones[f"horquilla_pin_{i}"] = horquilla_pin

        punto_fijo = (PLACA_PISTONES_X, y_pos, 50.0)
        anclaje_movil = triangulo.punto_anclaje_piston(puntos_t, PISTON_ANCLAJE_DIST)
        piezas_pistones[f"piston_{i}"] = make_rod_between(
            punto_fijo, anclaje_movil, PISTON_DIAMETRO
        )

    # --- Placa y pistones espejo (para triangulo_3, _4, _6, lado de marco_lateral_2) ---
    placa_pistones_2 = make_plate(
        width_x=150.0, depth_y=240.0, thickness_z=10.0,
        center_x=PLACA_PISTONES_X, center_y=3860.0, top_z=0.0,
    )

    pistones_config_2 = [
        (puntos_triangulo_3, OFFSET_TRIANGULO_3),
        (puntos_triangulo_4, OFFSET_TRIANGULO_4),
        (puntos_triangulo_6, OFFSET_TRIANGULO_6),
    ]
    piezas_pistones_2 = {"placa_pistones_2": placa_pistones_2}
    for i, (puntos_t, offset_t) in enumerate(pistones_config_2, start=1):
        y_pos = offset_t[1]
        horquilla_base, horquilla_ojo, horquilla_pin = make_clevis(
            PLACA_PISTONES_X, y_pos, base_z=0.0, pin_z=50.0
        )
        piezas_pistones_2[f"horquilla_2_{i}"] = horquilla_base
        piezas_pistones_2[f"horquilla_ojo_2_{i}"] = horquilla_ojo
        piezas_pistones_2[f"horquilla_pin_2_{i}"] = horquilla_pin

        punto_fijo = (PLACA_PISTONES_X, y_pos, 50.0)
        anclaje_movil = triangulo.punto_anclaje_piston(puntos_t, PISTON_ANCLAJE_DIST)
        piezas_pistones_2[f"piston_2_{i}"] = make_rod_between(
            punto_fijo, anclaje_movil, PISTON_DIAMETRO
        )

    todas_las_piezas = {}
    todas_las_piezas.update(piezas_marco)
    todas_las_piezas.update(piezas_marco_2)
    todas_las_piezas.update(piezas_triangulo)
    todas_las_piezas.update(piezas_triangulo_2)
    todas_las_piezas.update(piezas_triangulo_3)
    todas_las_piezas.update(piezas_triangulo_4)
    todas_las_piezas.update(piezas_triangulo_5)
    todas_las_piezas.update(piezas_triangulo_6)
    todas_las_piezas.update(piezas_pistones)
    todas_las_piezas.update(piezas_pistones_2)


    piezas_vidrio_1, _ = panel_vidrio.build(
        x_poste_a=-2700.0, x_poste_b=-1800.0,
        z_abajo_cara=60.0, z_arriba_cara=1940.0,
    )
    todas_las_piezas.update(piezas_vidrio_1)

    # --- Vidrio restante en marco_lateral (el hueco entre vertical y vertical_centro_1) ---
    piezas_vidrio_2, _ = panel_vidrio.build(
        x_poste_a=0.0, x_poste_b=-900.0,
        z_abajo_cara=60.0, z_arriba_cara=1940.0,
    )
    todas_las_piezas.update({f"{n}_2": p for n, p in piezas_vidrio_2.items()})

    # --- Los 3 huecos de marco_lateral_2 (mismas X, trasladado a Y=4000) ---
    huecos_marco_2 = [
        (0.0, -900.0, "a"),
        (-900.0, -1800.0, "b"),
        (-1800.0, -2700.0, "c"),
    ]
    for x_a, x_b, sufijo in huecos_marco_2:
        piezas_v, _ = panel_vidrio.build(
            x_poste_a=x_a, x_poste_b=x_b,
            z_abajo_cara=60.0, z_arriba_cara=1940.0,
            signo_exterior=1.0,
        )
        piezas_v = {f"{n}_m2_{sufijo}": p.translate(OFFSET_MARCO_2) for n, p in piezas_v.items()}
        todas_las_piezas.update(piezas_v)

    # ============================================================
    # LADO DERECHO: replica completa del mecanismo, ahora anclado a
    # inclinado_der / inclinado_der_2 (x=0) en vez de inclinado_izq (x=-2700)
    # ============================================================
    OFFSET_TRIANGULO_7 = (0.0, 70.0, 50.0)
    OFFSET_TRIANGULO_8 = (0.0, 140.0, 50.0)
    OFFSET_TRIANGULO_9 = (0.0, 210.0, 50.0)
    OFFSET_TRIANGULO_10 = (0.0, 4000.0 - 70.0, 50.0)
    OFFSET_TRIANGULO_11 = (0.0, 4000.0 - 140.0, 50.0)
    OFFSET_TRIANGULO_12 = (0.0, 4000.0 - 210.0, 50.0)

    triangulos_der_config = [
        (7, OFFSET_TRIANGULO_7, 1840.0, 67.5, 45.0, FOLD_MAX[1]),
        (8, OFFSET_TRIANGULO_8, 1760.0, 45.0, 22.5, FOLD_MAX[2]),
        (9, OFFSET_TRIANGULO_9, 1680.0, 22.5, 0.0, FOLD_MAX[5]),
        (10, OFFSET_TRIANGULO_10, 1840.0, 67.5, 45.0, FOLD_MAX[1]),
        (11, OFFSET_TRIANGULO_11, 1760.0, 45.0, 22.5, FOLD_MAX[2]),
        (12, OFFSET_TRIANGULO_12, 1680.0, 22.5, 0.0, FOLD_MAX[5]),
    ]

    puntos_triangulos_der = {}
    puntos_triangulos_der_local = {}
    for num, offset_t, lado_largo, ang_a, ang_b, fold_max in triangulos_der_config:
        piezas_t, puntos_t = triangulo.build(
            lado_largo=lado_largo, angulo_a_deg=ang_a, angulo_b_deg=ang_b,
            fold_angle=APERTURA * fold_max, signo_x=1.0,
        )
        puntos_triangulos_der_local[num] = puntos_t   # sin offset, para el vidrio
        piezas_t = {f"{n}_{num}": p.translate(offset_t) for n, p in piezas_t.items()}
        puntos_t = {n: tuple(a + b for a, b in zip(p, offset_t)) for n, p in puntos_t.items()}
        todas_las_piezas.update(piezas_t)
        puntos_triangulos_der[num] = puntos_t

    # --- Conectores entre pares (7-10, 8-11, 9-12), igual que izq ---
    for a, b in [(7, 10), (8, 11), (9, 12)]:
        pa, pb = puntos_triangulos_der[a], puntos_triangulos_der[b]
        for lado in ["punta_lado_a", "punta_lado_b"]:
            dir_lado = tuple(x - y for x, y in zip(pa[lado], pa["vertice_base"]))
            nombre_conector = f"conector_lado_{lado.split('_')[-1]}_{a}"
            todas_las_piezas[nombre_conector] = make_tube_between(
                pa[lado], pb[lado], x_dir=dir_lado
            )

    # --- Soportes de pivote (der, ambos marcos) ---
    piezas_soporte_der, puntos_soporte_der = soporte_pivote.build(
        p_base_vertical_final=puntos_marco["base_vertical_inicio"],
        y_triangulos=[puntos_triangulos_der[7]["vertice_base"][1],
                      puntos_triangulos_der[8]["vertice_base"][1],
                      puntos_triangulos_der[9]["vertice_base"][1]],
        x_pivote=puntos_triangulos_der[7]["vertice_base"][0],
        z_pivote=puntos_triangulos_der[7]["vertice_base"][2],
    )
    piezas_soporte_der = {f"{n}_der": p for n, p in piezas_soporte_der.items()}
    todas_las_piezas.update(piezas_soporte_der)

    piezas_soporte_der_2, puntos_soporte_der_2 = soporte_pivote.build(
        p_base_vertical_final=puntos_marco_2["base_vertical_inicio"],
        y_triangulos=[puntos_triangulos_der[10]["vertice_base"][1],
                      puntos_triangulos_der[11]["vertice_base"][1],
                      puntos_triangulos_der[12]["vertice_base"][1]],
        x_pivote=puntos_triangulos_der[10]["vertice_base"][0],
        z_pivote=puntos_triangulos_der[10]["vertice_base"][2],
    )
    piezas_soporte_der_2 = {f"{n}_der_2": p for n, p in piezas_soporte_der_2.items()}
    todas_las_piezas.update(piezas_soporte_der_2)

    # --- Placas y pistones (der, ambos marcos) ---
    placa_pistones_der = make_plate(
        width_x=150.0, depth_y=240.0, thickness_z=10.0,
        center_x=PLACA_PISTONES_X_DER, center_y=150.0, top_z=0.0,
    )
    todas_las_piezas["placa_pistones_der"] = placa_pistones_der

    placa_pistones_der_2 = make_plate(
        width_x=150.0, depth_y=240.0, thickness_z=10.0,
        center_x=PLACA_PISTONES_X_DER, center_y=3860.0, top_z=0.0,
    )
    todas_las_piezas["placa_pistones_der_2"] = placa_pistones_der_2

    for num in [7, 8, 9, 10, 11, 12]:
        puntos_t = puntos_triangulos_der[num]
        y_pos = puntos_t["vertice_base"][1]
        horquilla_base, horquilla_ojo, horquilla_pin = make_clevis(
            PLACA_PISTONES_X_DER, y_pos, base_z=0.0, pin_z=50.0
        )
        todas_las_piezas[f"horquilla_der_{num}"] = horquilla_base
        todas_las_piezas[f"horquilla_ojo_der_{num}"] = horquilla_ojo
        todas_las_piezas[f"horquilla_pin_der_{num}"] = horquilla_pin

        punto_fijo = (PLACA_PISTONES_X_DER, y_pos, 50.0)
        anclaje_movil = triangulo.punto_anclaje_piston(puntos_t, PISTON_ANCLAJE_DIST)
        todas_las_piezas[f"piston_der_{num}"] = make_rod_between(
            punto_fijo, anclaje_movil, PISTON_DIAMETRO
        )


    # --- conector longitudinal entre las puntas superiores de
    # inclinado_izq (marco 1) e inclinado_izq_2 (marco 2), rotado sobre
    # su propio eje para coincidir con la inclinacion de inclinado_izq.
    p_base_inclinado_izq = puntos_marco["base_vertical_final"]
    p_punta_inclinado_izq = puntos_marco["punta_inclinado_izq"]
    dir_inclinado_izq = tuple(
        a - b for a, b in zip(p_punta_inclinado_izq, p_base_inclinado_izq)
    )

    conector_longitudinal_izq = make_tube_between(
        puntos_marco["punta_inclinado_izq"],
        puntos_marco_2["punta_inclinado_izq"],
        x_dir=dir_inclinado_izq,
    )
    todas_las_piezas["conector_longitudinal_izq"] = conector_longitudinal_izq

    # --- Nuevos conectores "por arriba" entre marco_lateral y marco_lateral_2 ---
    conectores_top = {
        "conector_top_vertical": ("top_cl_vertical", None),
        "conector_top_vertical_centro_1": ("top_cl_vertical_centro_1", None),
        "conector_top_vertical_centro_2": ("top_cl_vertical_centro_2", None),
        "conector_top_vertical_final": ("top_cl_vertical_final", None),
    }
    for nombre_pieza, (nombre_punto, _) in conectores_top.items():
        p1 = puntos_marco[nombre_punto]
        p2 = puntos_marco_2[nombre_punto]
        todas_las_piezas[nombre_pieza] = make_tube_between(p1, p2, x_dir=(1, 0, 0))

    # inclinado_der tambien se conecta "por arriba" (su propia punta),
    # rotado sobre su eje para coincidir con la inclinacion de inclinado_der
    p_base_inclinado_der = puntos_marco["base_vertical_inicio"]
    p_punta_inclinado_der = puntos_marco["punta_inclinado_der"]
    dir_inclinado_der = tuple(
        a - b for a, b in zip(p_punta_inclinado_der, p_base_inclinado_der)
    )
    conector_longitudinal_der = make_tube_between(
        puntos_marco["punta_inclinado_der"],
        puntos_marco_2["punta_inclinado_der"],
        x_dir=dir_inclinado_der,
    )
    todas_las_piezas["conector_longitudinal_der"] = conector_longitudinal_der

    # --- Conector entre lado_a_67.5 (triangulo) y lado_a_67.5_3 (triangulo_3) ---
    p_vertice_lado_a = puntos_triangulo["vertice_base"]
    p_punta_lado_a = puntos_triangulo["punta_lado_a"]
    dir_lado_a = tuple(
        a - b for a, b in zip(p_punta_lado_a, p_vertice_lado_a)
    )
    conector_lado_a = make_tube_between(
        puntos_triangulo["punta_lado_a"],
        puntos_triangulo_3["punta_lado_a"],
        x_dir=dir_lado_a,
    )
    todas_las_piezas["conector_lado_a"] = conector_lado_a

    # --- Conector entre lado_b_45 (triangulo) y lado_b_45_3 (triangulo_3) ---
    dir_lado_b = tuple(
        a - b for a, b in zip(puntos_triangulo["punta_lado_b"], puntos_triangulo["vertice_base"])
    )
    conector_lado_b = make_tube_between(
        puntos_triangulo["punta_lado_b"],
        puntos_triangulo_3["punta_lado_b"],
        x_dir=dir_lado_b,
    )
    todas_las_piezas["conector_lado_b"] = conector_lado_b

    # --- Conector entre lado_a_67.5_2 (triangulo_2) y lado_a_67.5_4 (triangulo_4) ---
    dir_lado_a_2 = tuple(
        a - b for a, b in zip(puntos_triangulo_2["punta_lado_a"], puntos_triangulo_2["vertice_base"])
    )
    conector_lado_a_2 = make_tube_between(
        puntos_triangulo_2["punta_lado_a"],
        puntos_triangulo_4["punta_lado_a"],
        x_dir=dir_lado_a_2,
    )
    todas_las_piezas["conector_lado_a_2"] = conector_lado_a_2

    # --- Conector entre lado_b_45_2 (triangulo_2) y lado_b_45_4 (triangulo_4) ---
    dir_lado_b_2 = tuple(
        a - b for a, b in zip(puntos_triangulo_2["punta_lado_b"], puntos_triangulo_2["vertice_base"])
    )
    conector_lado_b_2 = make_tube_between(
        puntos_triangulo_2["punta_lado_b"],
        puntos_triangulo_4["punta_lado_b"],
        x_dir=dir_lado_b_2,
    )
    todas_las_piezas["conector_lado_b_2"] = conector_lado_b_2

    # --- Conector entre lado_a_67.5_5 (triangulo_5) y lado_a_67.5_6 (triangulo_6) ---
    dir_lado_a_5 = tuple(
        a - b for a, b in zip(puntos_triangulo_5["punta_lado_a"], puntos_triangulo_5["vertice_base"])
    )
    conector_lado_a_5 = make_tube_between(
        puntos_triangulo_5["punta_lado_a"],
        puntos_triangulo_6["punta_lado_a"],
        x_dir=dir_lado_a_5,
    )
    todas_las_piezas["conector_lado_a_5"] = conector_lado_a_5

    # --- Conector entre lado_b_45_5 (triangulo_5) y lado_b_45_6 (triangulo_6) ---
    dir_lado_b_5 = tuple(
        a - b for a, b in zip(puntos_triangulo_5["punta_lado_b"], puntos_triangulo_5["vertice_base"])
    )
    conector_lado_b_5 = make_tube_between(
        puntos_triangulo_5["punta_lado_b"],
        puntos_triangulo_6["punta_lado_b"],
        x_dir=dir_lado_b_5,
    )
    todas_las_piezas["conector_lado_b_5"] = conector_lado_b_5

    # --- Soporte del eje de pivote para los triangulos (abanico) ---
    piezas_soporte, puntos_soporte = soporte_pivote.build(
        p_base_vertical_final=puntos_marco["base_vertical_final"],
        y_triangulos=[
            puntos_triangulo["vertice_base"][1],
            puntos_triangulo_2["vertice_base"][1],
            puntos_triangulo_5["vertice_base"][1],
        ],
        x_pivote=puntos_triangulo["vertice_base"][0],
        z_pivote=puntos_triangulo["vertice_base"][2],
    )
    todas_las_piezas.update(piezas_soporte)

    # --- Soporte del eje de pivote espejo (para triangulo_3 y triangulo_4,
    # anclado a marco_lateral_2 en vez de marco_lateral) ---
    piezas_soporte_2, puntos_soporte_2 = soporte_pivote.build(
        p_base_vertical_final=puntos_marco_2["base_vertical_final"],
        y_triangulos=[
            puntos_triangulo_3["vertice_base"][1],
            puntos_triangulo_4["vertice_base"][1],
            puntos_triangulo_6["vertice_base"][1],
        ],
        x_pivote=puntos_triangulo_3["vertice_base"][0],
        z_pivote=puntos_triangulo_3["vertice_base"][2],
    )
    piezas_soporte_2 = {f"{n}_2": p for n, p in piezas_soporte_2.items()}
    todas_las_piezas.update(piezas_soporte_2)

    # bbox_horiz_top = piezas_marco["horiz_top"].val().BoundingBox()

    piezas_puerta, puntos_puerta = puerta_bisagra.build(
        x_poste_bisagra=-1800.0, x_poste_otro=-900.0,
        z_abajo=60.0, z_arriba=1940.0,
        angulo_apertura=PUERTA_ANGULO,
    )
    todas_las_piezas.update(piezas_puerta)

    # --- Techo: 3 paneles, uno por cada vano entre postes ---
    Y_TECHO_MIN, Y_TECHO_MAX = 32.0, 3968.0
    Z_TECHO_CENTRO = 1970.0
    vanos_techo = [(0.0, -900.0, "a"), (-900.0, -1800.0, "b"), (-1800.0, -2700.0, "c")]
    for x_a, x_b, sufijo in vanos_techo:
        piezas_t, _ = panel_vidrio_techo.build(
            x_poste_a=x_a, x_poste_b=x_b,
            y_min=Y_TECHO_MIN, y_max=Y_TECHO_MAX, z_centro=Z_TECHO_CENTRO,
        )
        todas_las_piezas.update({f"{n}_{sufijo}": p for n, p in piezas_t.items()})



    piezas_vidrio_fijo1, _ = panel_vidrio_triangulo_fijo.build(
        v_abajo=(-2700.0, 30.0), v_arriba=(-2700.0, 1970.0),
        v_punta=(puntos_marco["punta_inclinado_izq"][0], puntos_marco["punta_inclinado_izq"][2]),
        y_pos=0.0, signo_exterior=-1.0,
    )
    todas_las_piezas.update({f"{n}_fijo1": p for n, p in piezas_vidrio_fijo1.items()})

    # --- Triangulo fijo DER, marco_lateral (vertical, inclinado_der, conector_der) ---
    piezas_vidrio_fijo2, _ = panel_vidrio_triangulo_fijo.build(
        v_abajo=(0.0, 30.0), v_arriba=(0.0, 1970.0),
        v_punta=(puntos_marco["punta_inclinado_der"][0], puntos_marco["punta_inclinado_der"][2]),
        y_pos=0.0, signo_exterior=-1.0,
    )
    todas_las_piezas.update({f"{n}_fijo2": p for n, p in piezas_vidrio_fijo2.items()})

    # --- Triangulo fijo IZQ, marco_lateral_2 (vertical_final_2, inclinado_izq_2, conector_izq_2) ---
    piezas_vidrio_fijo3, _ = panel_vidrio_triangulo_fijo.build(
        v_abajo=(-2700.0, 30.0), v_arriba=(-2700.0, 1970.0),
        v_punta=(puntos_marco_2["punta_inclinado_izq"][0], puntos_marco_2["punta_inclinado_izq"][2]),
        y_pos=4000.0, signo_exterior=1.0,
    )
    todas_las_piezas.update({f"{n}_fijo3": p for n, p in piezas_vidrio_fijo3.items()})

    # --- Triangulo fijo DER, marco_lateral_2 (vertical_2, inclinado_der_2, conector_der_2) ---
    piezas_vidrio_fijo4, _ = panel_vidrio_triangulo_fijo.build(
        v_abajo=(0.0, 30.0), v_arriba=(0.0, 1970.0),
        v_punta=(puntos_marco_2["punta_inclinado_der"][0], puntos_marco_2["punta_inclinado_der"][2]),
        y_pos=4000.0, signo_exterior=1.0,
    )
    todas_las_piezas.update({f"{n}_fijo4": p for n, p in piezas_vidrio_fijo4.items()})

    # --- Vidrio superior entre marco_lateral y marco_lateral_2, lado izq ---
    piezas_vidrio_sup1, _ = panel_vidrio_superior.build(
        pa1=puntos_marco["top_cl_vertical_final"], pa3=puntos_marco_2["top_cl_vertical_final"],
        pb1=puntos_marco["punta_inclinado_izq"], pb3=puntos_marco_2["punta_inclinado_izq"],
        tubo_pa=todas_las_piezas["conector_top_vertical_final"].val(),
        tubo_pb=todas_las_piezas["conector_longitudinal_izq"].val(),
    )
    todas_las_piezas.update({f"{n}_sup1": p for n, p in piezas_vidrio_sup1.items()})

    # --- Vidrio superior entre marco_lateral y marco_lateral_2, lado der
    # (espejo de vidrio_sup1: conector_top_vertical / conector_longitudinal_der /
    # conector_der / conector_der_2) ---
    piezas_vidrio_sup2, _ = panel_vidrio_superior.build(
        pa1=puntos_marco["top_cl_vertical"], pa3=puntos_marco_2["top_cl_vertical"],
        pb1=puntos_marco["punta_inclinado_der"], pb3=puntos_marco_2["punta_inclinado_der"],
        tubo_pa=todas_las_piezas["conector_top_vertical"].val(),
        tubo_pb=todas_las_piezas["conector_longitudinal_der"].val(),
    )
    todas_las_piezas.update({f"{n}_sup2": p for n, p in piezas_vidrio_sup2.items()})

    # --- Vidrio de los triangulos moviles del abanico (6 parejas: 3 en el
    # lado izq, 3 espejadas en el lado der) - cada pareja usa
    # panel_vidrio_triangulo.build(), que arma 1 panel "vientre" + 2
    # "tapas" (una por triangulo) + sus beads. ---
    def _y_exterior(offset):
        # cara exterior de la tapa: el extremo MAS ALEJADO del centro del
        # garage (Y=2000) - 30mm mas alla del propio offset en Y.
        return offset[1] - 30.0 if offset[1] < 2000.0 else offset[1] + 30.0

    parejas_triangulo = [
        ("1_3", puntos_triangulo_local, OFFSET_TRIANGULO, puntos_triangulo_3_local, OFFSET_TRIANGULO_3,
         "conector_lado_a", "conector_lado_b"),
        ("2_4", puntos_triangulo_2_local, OFFSET_TRIANGULO_2, puntos_triangulo_4_local, OFFSET_TRIANGULO_4,
         "conector_lado_a_2", "conector_lado_b_2"),
        ("5_6", puntos_triangulo_5_local, OFFSET_TRIANGULO_5, puntos_triangulo_6_local, OFFSET_TRIANGULO_6,
         "conector_lado_a_5", "conector_lado_b_5"),
        ("7_10", puntos_triangulos_der_local[7], OFFSET_TRIANGULO_7, puntos_triangulos_der_local[10], OFFSET_TRIANGULO_10,
         "conector_lado_a_7", "conector_lado_b_7"),
        ("8_11", puntos_triangulos_der_local[8], OFFSET_TRIANGULO_8, puntos_triangulos_der_local[11], OFFSET_TRIANGULO_11,
         "conector_lado_a_8", "conector_lado_b_8"),
        ("9_12", puntos_triangulos_der_local[9], OFFSET_TRIANGULO_9, puntos_triangulos_der_local[12], OFFSET_TRIANGULO_12,
         "conector_lado_a_9", "conector_lado_b_9"),
    ]
    for sufijo, puntos_1, offset_1, puntos_3, offset_3, nombre_conector_a, nombre_conector_b in parejas_triangulo:
        piezas_vt, _ = panel_vidrio_triangulo.build(
            puntos_1=puntos_1, puntos_3=puntos_3,
            offset_1=offset_1, offset_3=offset_3,
            y_exterior_1=_y_exterior(offset_1), y_exterior_3=_y_exterior(offset_3),
            tubo_conector_a=todas_las_piezas[nombre_conector_a].val(),
            tubo_conector_b=todas_las_piezas[nombre_conector_b].val(),
        )
        todas_las_piezas.update({f"{n}_{sufijo}": p for n, p in piezas_vt.items()})

    todos_los_puntos = {
        "marco_lateral": puntos_marco,
        "marco_lateral_2": puntos_marco_2,
        "triangulo": puntos_triangulo,
        "triangulo_2": puntos_triangulo_2,
        "triangulo_3": puntos_triangulo_3,
        "triangulo_4": puntos_triangulo_4,
        "soporte_pivote": puntos_soporte,
        "soporte_pivote_2": puntos_soporte_2,
        "triangulo_5": puntos_triangulo_5,
        "triangulo_6": puntos_triangulo_6,
    }

    return todas_las_piezas, todos_los_puntos