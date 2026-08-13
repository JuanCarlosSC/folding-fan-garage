from ocp_vscode import show
from assembly import build_all

piezas, puntos = build_all()

# Vidrio con transparencia (color celeste translucido, alpha ~50%),
# el resto de las piezas con su color por defecto.
colores = []
for nombre in piezas.keys():
    if "_bead_" in nombre:
        colores.append("#000000FF")   # negro, opaco (las tiras de sujecion)
    elif "vidrio" in nombre:
        colores.append("#AEE3F080")   # celeste, ~50% transparente (el vidrio)
    else:
        colores.append("#C9A227")     # el amarillo/dorado que ya veniamos usando

show(
    *piezas.values(),
    names=list(piezas.keys()),
    colors=colores,
)

print("Piezas mostradas:", list(piezas.keys()))
print("Puntos de conexion disponibles:")
for estructura, pts in puntos.items():
    print(f"  {estructura}:")
    for nombre, coord in pts.items():
        print(f"    {nombre}: {coord}")