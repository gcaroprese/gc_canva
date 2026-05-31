"""
Composiciones de CALIDAD - sin texto, solo visual.
Cada imagen se valida antes de guardar.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image
from quality_check import check_asset
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), "output")
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

def verify_and_save(name, spec, no_text=True):
    """Genera, valida, y guarda."""
    # Validar que no hay texto si se pide
    if no_text:
        for el in spec.get("elements", []):
            if el.get("type") in ("text", "pill") and el.get("text"):
                print(f"  FAIL {name}: contiene texto '{el.get('text')}' (se pidio sin texto)")
                return False

    # Validar assets usados
    for el in spec.get("elements", []):
        if el.get("type") == "asset":
            ok, issues = check_asset(el.get("name", ""))
            if not ok:
                print(f"  FAIL {name}: asset malo - {issues}")
                return False

    # Generar
    img = generate_from_spec(spec)

    # Verificar que la imagen no esta vacia/corrupta
    extrema = img.getextrema()
    if all(e[0] == e[1] for e in extrema[:3]):
        print(f"  FAIL {name}: imagen es un color solido")
        return False

    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    path = os.path.join(OUT, f"{name}.webp")
    with open(path, "wb") as f:
        f.write(d)
    print(f"  OK   {name}: {len(d)//1024}KB ({spec['width']}x{spec['height']})")
    return True


# ══════════════════════════════════════════════════════
# 1. PAWSITIVE BREWS - Perro + te, atmosfera calida
#    1200x675 blog OG, sin texto
# ══════════════════════════════════════════════════════
# Verificar assets primero
for asset in ["dog_beagle_png", "teacup2_hires_png"]:
    ok, issues = check_asset(asset)
    if not ok:
        print(f"  SKIP: {asset} - {issues}")

pawsitive = {
    "width":1200, "height":675, "background":"#080604", "antialias":2,
    "elements":[
        # Fondo calido atmosferico
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#1c1410"],[0.3,"#120c08"],[0.7,"#080604"],[1,"#040302"]],
         "angle":160},

        # Luz calida central-izquierda (donde va la taza)
        {"type":"circle","x":400,"y":350,"r":380,"color":"#c8956c","opacity":0.03},
        {"type":"circle","x":400,"y":350,"r":220,"color":"#d4a574","opacity":0.04},

        # Superficie de mesa
        {"type":"gradient","x":0,"y":460,"w":1200,"h":215,
         "color1":"#0d090680","color2":"#04030200","direction":"vertical"},

        # Taza de te (asset hi-res 1600x1200) - izquierda, sobre la mesa
        {"type":"image","src":os.path.join(A,"teacup2_hires_png.webp"),
         "x":80,"y":160,"w":500,"h":375},

        # Perro beagle (asset 1903x3000) - derecha, mirando la taza
        {"type":"image","src":os.path.join(A,"dog_beagle_png.webp"),
         "x":680,"y":30,"w":440,"h":640},

        # Particulas doradas conectando perro y taza
        {"type":"circle","x":520,"y":200,"r":5,"color":"#d4a574","opacity":0.18},
        {"type":"circle","x":580,"y":280,"r":3,"color":"#ffd700","opacity":0.12},
        {"type":"circle","x":620,"y":150,"r":4,"color":"#c8956c","opacity":0.1},
        {"type":"circle","x":560,"y":350,"r":3,"color":"#ffd700","opacity":0.08},

        # Estrellas decorativas
        {"type":"star","x":180,"y":80,"r":6,"inner_r":2,"points":4,"color":"#ffd700","opacity":0.08},
        {"type":"star","x":1100,"y":120,"r":5,"inner_r":2,"points":4,"color":"#ffd700","opacity":0.06},
    ]
}

# ══════════════════════════════════════════════════════
# 2. INFORKET - Dashboard tech, datos visuales
#    1200x675 blog OG, sin texto
# ══════════════════════════════════════════════════════
# Approach: render dashboard por separado, componer en macbook
inforket = {
    "width":1200, "height":675, "background":"#030308", "antialias":2,
    "elements":[
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#03030a"],[0.25,"#08061a"],[0.5,"#0e0c30"],[0.75,"#08061a"],[1,"#03030a"]],
         "angle":145},

        # Glow central
        {"type":"circle","x":600,"y":340,"r":350,"color":"#7c6bf5","opacity":0.025},
        {"type":"circle","x":600,"y":340,"r":180,"color":"#7c6bf5","opacity":0.04},

        # Mesa/superficie
        {"type":"gradient","x":0,"y":480,"w":1200,"h":195,
         "color1":"#06050f80","color2":"#02020500","direction":"vertical"},

        # Dashboard card principal (en vez de mockup de laptop)
        {"type":"rect","x":80,"y":60,"w":620,"h":400,"color":"#0a0a1a","radius":20,
         "shadow":True,"shadow_color":"#00000060","shadow_blur":30,"shadow_y":10},

        # Barras del chart
        {"type":"rect","x":120,"y":340,"w":35,"h":50,"color":"#7c6bf525","radius":4},
        {"type":"rect","x":168,"y":310,"w":35,"h":80,"color":"#7c6bf535","radius":4},
        {"type":"rect","x":216,"y":280,"w":35,"h":110,"color":"#7c6bf545","radius":4},
        {"type":"rect","x":264,"y":240,"w":35,"h":150,"color":"#7c6bf560","radius":4},
        {"type":"rect","x":312,"y":210,"w":35,"h":180,"color":"#7c6bf578","radius":4},
        {"type":"rect","x":360,"y":170,"w":35,"h":220,"color":"#7c6bf5","radius":4},
        {"type":"rect","x":408,"y":190,"w":35,"h":200,"color":"#22c55e","radius":4},

        # Punto glow en la barra mas alta
        {"type":"circle","x":377,"y":166,"r":5,"color":"#7c6bf5",
         "shadow":True,"shadow_color":"#7c6bf560","shadow_blur":10},

        # Donut chart
        {"type":"ring","x":580,"y":270,"r":75,"thickness":18,"color":"#7c6bf5","start":0,"end":210},
        {"type":"ring","x":580,"y":270,"r":75,"thickness":18,"color":"#22c55e","start":210,"end":300},
        {"type":"ring","x":580,"y":270,"r":75,"thickness":18,"color":"#f59e0b","start":300,"end":360},
        {"type":"circle","x":580,"y":270,"r":45,"color":"#0a0a1a"},

        # Card secundaria derecha-arriba
        {"type":"rect","x":740,"y":60,"w":420,"h":180,"color":"#0a0a1a","radius":18,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":20,"shadow_y":8},

        # Mini barras en card secundaria
        {"type":"rect","x":780,"y":170,"w":24,"h":30,"color":"#7c6bf540","radius":3},
        {"type":"rect","x":815,"y":155,"w":24,"h":45,"color":"#7c6bf560","radius":3},
        {"type":"rect","x":850,"y":140,"w":24,"h":60,"color":"#7c6bf580","radius":3},
        {"type":"rect","x":885,"y":125,"w":24,"h":75,"color":"#7c6bf5","radius":3},
        {"type":"rect","x":920,"y":135,"w":24,"h":65,"color":"#22c55e","radius":3},

        # Mini donut en card secundaria
        {"type":"ring","x":1050,"y":140,"r":40,"thickness":10,"color":"#f59e0b","start":0,"end":250},
        {"type":"ring","x":1050,"y":140,"r":40,"thickness":10,"color":"#ef4444","start":250,"end":360},
        {"type":"circle","x":1050,"y":140,"r":22,"color":"#0a0a1a"},

        # Card tercera derecha-abajo
        {"type":"rect","x":740,"y":270,"w":420,"h":190,"color":"#0a0a1a","radius":18,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":20,"shadow_y":8},

        # Scatter dots en card tercera
        {"type":"circle","x":790,"y":350,"r":6,"color":"#7c6bf5","opacity":0.6},
        {"type":"circle","x":830,"y":380,"r":8,"color":"#22c55e","opacity":0.7},
        {"type":"circle","x":880,"y":340,"r":5,"color":"#7c6bf5","opacity":0.5},
        {"type":"circle","x":920,"y":360,"r":9,"color":"#22c55e","opacity":0.8,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":6},
        {"type":"circle","x":960,"y":330,"r":7,"color":"#7c6bf5","opacity":0.6},
        {"type":"circle","x":1000,"y":310,"r":10,"color":"#7c6bf5","opacity":0.9,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":8},
        {"type":"circle","x":1040,"y":340,"r":6,"color":"#f59e0b","opacity":0.5},
        {"type":"circle","x":1080,"y":300,"r":8,"color":"#22c55e","opacity":0.7},
        {"type":"circle","x":1110,"y":350,"r":5,"color":"#7c6bf5","opacity":0.4},

        # Particulas flotando arriba (datos ascendiendo)
        {"type":"circle","x":400,"y":40,"r":7,"color":"#7c6bf5","opacity":0.35,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":10},
        {"type":"circle","x":500,"y":25,"r":9,"color":"#22c55e","opacity":0.25,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":12},
        {"type":"circle","x":600,"y":15,"r":5,"color":"#f59e0b","opacity":0.2},
        {"type":"circle","x":300,"y":30,"r":4,"color":"#7c6bf5","opacity":0.15},
        {"type":"circle","x":700,"y":20,"r":6,"color":"#7c6bf5","opacity":0.18},

        # Lineas accent
        {"type":"rect","x":0,"y":0,"w":1200,"h":2,"color":"#7c6bf5"},
        {"type":"rect","x":0,"y":673,"w":1200,"h":2,"color":"#7c6bf520"},
    ]
}

print("=" * 50)
verify_and_save("pawsitive_quality", pawsitive, no_text=True)
verify_and_save("inforket_quality", inforket, no_text=True)
print("=" * 50)
