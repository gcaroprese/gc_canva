"""Composiciones con post-processing para calidad Canva."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

# ══════════════════════════════════════════════════════
# PAWSITIVE BREWS - con post-processing completo
# ══════════════════════════════════════════════════════
pw = {
    "width":1200, "height":675, "background":"#060806", "antialias":2,
    "post": {
        "vignette": True, "vignette_strength": 0.5,
        "tint": "#d4a574", "tint_strength": 0.04,
        "grain": True, "grain_strength": 5,
    },
    "elements": [
        # Fondo verde oscuro calido
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#161e16"],[0.25,"#0e140e"],[0.6,"#080c08"],[1,"#040604"]],
         "angle":150},

        # Glow central verde (donde va el te)
        {"type":"circle","x":350,"y":320,"r":400,"color":"#5d8a5e","opacity":0.03},
        {"type":"circle","x":350,"y":320,"r":220,"color":"#8fbc8f","opacity":0.04},

        # Superficie de mesa
        {"type":"gradient","x":0,"y":420,"w":1200,"h":255,
         "color1":"#0c100c","color2":"#060806","direction":"vertical"},
        {"type":"rect","x":0,"y":420,"w":1200,"h":1,"color":"#8fbc8f08"},

        # Sombra de contacto del vaso
        {"type":"ellipse","x":180,"y":500,"w":340,"h":25,"color":"#000000","opacity":0.3},

        # Sombra de contacto del perro
        {"type":"ellipse","x":680,"y":590,"w":400,"h":30,"color":"#000000","opacity":0.25},

        # Vaso de te verde - protagonista izquierda
        {"type":"image","src":os.path.join(A,"green_tea_nobg.webp"),
         "x":140,"y":30,"w":460,"h":480},

        # Perro beagle sentado - derecha, mirando al frente
        {"type":"image","src":os.path.join(A,"dog_beagle_png.webp"),
         "x":660,"y":10,"w":450,"h":610},

        # Particulas organicas sutiles (conexion visual)
        {"type":"circle","x":530,"y":180,"r":4,"color":"#8fbc8f","opacity":0.15},
        {"type":"circle","x":590,"y":280,"r":3,"color":"#a0d0a0","opacity":0.1},
        {"type":"circle","x":620,"y":120,"r":3,"color":"#5d8a5e","opacity":0.07},
        {"type":"circle","x":480,"y":350,"r":2,"color":"#a0d0a0","opacity":0.06},
    ]
}

# ══════════════════════════════════════════════════════
# INFORKET - Dashboard con post-processing
# ══════════════════════════════════════════════════════
ink = {
    "width":1200, "height":675, "background":"#030308", "antialias":2,
    "post": {
        "vignette": True, "vignette_strength": 0.35,
        "tint": "#7c6bf5", "tint_strength": 0.03,
        "grain": True, "grain_strength": 4,
    },
    "elements": [
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#03030a"],[0.25,"#08061a"],[0.5,"#0e0c30"],[0.75,"#08061a"],[1,"#03030a"]],
         "angle":145},

        # Glow
        {"type":"circle","x":600,"y":340,"r":350,"color":"#7c6bf5","opacity":0.025},
        {"type":"circle","x":600,"y":340,"r":180,"color":"#7c6bf5","opacity":0.04},

        # Mesa
        {"type":"gradient","x":0,"y":480,"w":1200,"h":195,
         "color1":"#06050f","color2":"#030308","direction":"vertical"},

        # Card principal
        {"type":"rect","x":80,"y":60,"w":620,"h":400,"color":"#0a0a1a","radius":20,
         "shadow":True,"shadow_color":"#7c6bf510","shadow_blur":30,"shadow_y":10},

        # Barras crecientes
        {"type":"rect","x":120,"y":340,"w":35,"h":50,"color":"#7c6bf525","radius":4},
        {"type":"rect","x":168,"y":310,"w":35,"h":80,"color":"#7c6bf535","radius":4},
        {"type":"rect","x":216,"y":275,"w":35,"h":115,"color":"#7c6bf548","radius":4},
        {"type":"rect","x":264,"y":240,"w":35,"h":150,"color":"#7c6bf560","radius":4},
        {"type":"rect","x":312,"y":200,"w":35,"h":190,"color":"#7c6bf578","radius":4},
        {"type":"rect","x":360,"y":160,"w":35,"h":230,"color":"#7c6bf5","radius":4},
        {"type":"rect","x":408,"y":180,"w":35,"h":210,"color":"#22c55e","radius":4},

        # Glow en barra mas alta
        {"type":"circle","x":377,"y":155,"r":5,"color":"#7c6bf5",
         "shadow":True,"shadow_color":"#7c6bf560","shadow_blur":10},

        # Donut
        {"type":"ring","x":580,"y":260,"r":78,"thickness":19,"color":"#7c6bf5","start":0,"end":210},
        {"type":"ring","x":580,"y":260,"r":78,"thickness":19,"color":"#22c55e","start":210,"end":300},
        {"type":"ring","x":580,"y":260,"r":78,"thickness":19,"color":"#f59e0b","start":300,"end":360},
        {"type":"circle","x":580,"y":260,"r":46,"color":"#0a0a1a"},

        # Card secundaria
        {"type":"rect","x":740,"y":60,"w":420,"h":180,"color":"#0a0a1a","radius":18,
         "shadow":True,"shadow_color":"#7c6bf510","shadow_blur":20,"shadow_y":8},

        # Mini barras
        {"type":"rect","x":780,"y":170,"w":24,"h":30,"color":"#7c6bf540","radius":3},
        {"type":"rect","x":815,"y":155,"w":24,"h":45,"color":"#7c6bf560","radius":3},
        {"type":"rect","x":850,"y":138,"w":24,"h":62,"color":"#7c6bf580","radius":3},
        {"type":"rect","x":885,"y":122,"w":24,"h":78,"color":"#7c6bf5","radius":3},
        {"type":"rect","x":920,"y":132,"w":24,"h":68,"color":"#22c55e","radius":3},

        # Mini donut
        {"type":"ring","x":1050,"y":140,"r":42,"thickness":11,"color":"#f59e0b","start":0,"end":250},
        {"type":"ring","x":1050,"y":140,"r":42,"thickness":11,"color":"#ef4444","start":250,"end":360},
        {"type":"circle","x":1050,"y":140,"r":23,"color":"#0a0a1a"},

        # Card scatter
        {"type":"rect","x":740,"y":270,"w":420,"h":190,"color":"#0a0a1a","radius":18,
         "shadow":True,"shadow_color":"#7c6bf510","shadow_blur":20,"shadow_y":8},

        # Scatter dots con glows
        {"type":"circle","x":790,"y":350,"r":6,"color":"#7c6bf5","opacity":0.6},
        {"type":"circle","x":830,"y":380,"r":8,"color":"#22c55e","opacity":0.7},
        {"type":"circle","x":875,"y":340,"r":5,"color":"#7c6bf5","opacity":0.5},
        {"type":"circle","x":920,"y":360,"r":9,"color":"#22c55e","opacity":0.8,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":6},
        {"type":"circle","x":965,"y":325,"r":7,"color":"#7c6bf5","opacity":0.6},
        {"type":"circle","x":1010,"y":305,"r":10,"color":"#7c6bf5","opacity":0.9,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":8},
        {"type":"circle","x":1050,"y":340,"r":6,"color":"#f59e0b","opacity":0.5},
        {"type":"circle","x":1090,"y":310,"r":8,"color":"#22c55e","opacity":0.7},

        # Particulas ascendentes
        {"type":"circle","x":400,"y":35,"r":7,"color":"#7c6bf5","opacity":0.3,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":10},
        {"type":"circle","x":520,"y":20,"r":9,"color":"#22c55e","opacity":0.2,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":12},
        {"type":"circle","x":300,"y":25,"r":5,"color":"#f59e0b","opacity":0.15},
        {"type":"circle","x":650,"y":15,"r":6,"color":"#7c6bf5","opacity":0.12},

        # Accent lines
        {"type":"rect","x":0,"y":0,"w":1200,"h":2,"color":"#7c6bf5"},
    ]
}

for name, spec in [("pawsitive_postfx", pw), ("inforket_postfx", ink)]:
    # Validar no-text
    has_text = any(el.get("type") in ("text","pill") and el.get("text") for el in spec["elements"])
    if has_text:
        print(f"  FAIL {name}: contiene texto!")
        continue
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    with open(os.path.join(OUT, f"{name}.webp"), "wb") as f:
        f.write(d)
    print(f"  OK {name}: {len(d)//1024}KB")
