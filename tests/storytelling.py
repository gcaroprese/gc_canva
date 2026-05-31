"""Composiciones que CUENTAN UNA HISTORIA visual - sin texto."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

# ══════════════════════════════════════════════════════════
# PAWSITIVE BREWS - Historia: perro mira la taza de te
# El perro (puppy) esta a la derecha mirando hacia la izquierda
# donde esta la taza. La composicion crea tension/deseo visual.
# Fondo calido, iluminacion desde la taza.
# ══════════════════════════════════════════════════════════
pw = {
    "width":1200,"height":675,"background":"#080604",
    "elements":[
        # Fondo base
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#18120c"],[0.35,"#100a06"],[1,"#040302"]],
         "direction":"radial"},

        # Luz calida emanando de la taza (como si el te brillara)
        {"type":"circle","x":320,"y":380,"r":350,"color":"#d4956a","opacity":0.035},
        {"type":"circle","x":320,"y":380,"r":220,"color":"#d4956a","opacity":0.04},
        {"type":"circle","x":320,"y":380,"r":120,"color":"#ffd700","opacity":0.03},

        # Superficie/mesa sutil
        {"type":"rect","x":0,"y":500,"w":1200,"h":175,"color":"#0d0906","opacity":0.8},
        {"type":"line","x1":0,"y1":500,"x2":1200,"y2":500,"color":"#c8956c15","width":1},

        # Taza de te - posicion izquierda-centro, sobre la mesa
        {"type":"image","src":os.path.join(A,"teacup2_hires_png.webp"),
         "x":100,"y":200,"w":480,"h":360},

        # Vapor sutil sobre la taza (arcos)
        {"type":"arc","x":250,"y":140,"w":60,"h":70,"start":180,"end":360,
         "color":"#ffffff","width":2,"opacity":0.12},
        {"type":"arc","x":310,"y":110,"w":50,"h":60,"start":0,"end":180,
         "color":"#ffffff","width":2,"opacity":0.08},
        {"type":"arc","x":350,"y":130,"w":45,"h":65,"start":180,"end":360,
         "color":"#ffffff","width":2,"opacity":0.06},

        # Perro puppy - derecha, mirando hacia la taza (hacia la izquierda)
        # El puppy PNG mira hacia la izquierda naturalmente
        {"type":"image","src":os.path.join(A,"dog_puppy_png.webp"),
         "x":680,"y":80,"w":480,"h":580},

        # Reflejo de luz en los ojos del perro (punto brillante sutil)
        {"type":"circle","x":830,"y":310,"r":3,"color":"#ffd700","opacity":0.2},

        # Particulas doradas flotando (conectan perro y taza)
        {"type":"circle","x":550,"y":250,"r":4,"color":"#d4a574","opacity":0.2},
        {"type":"circle","x":600,"y":180,"r":3,"color":"#ffd700","opacity":0.15},
        {"type":"circle","x":650,"y":300,"r":5,"color":"#d4a574","opacity":0.12},
        {"type":"circle","x":500,"y":150,"r":3,"color":"#c8956c","opacity":0.1},
        {"type":"circle","x":580,"y":350,"r":2,"color":"#ffd700","opacity":0.18},

        # Accent lines
        {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#c8956c60"},
        {"type":"rect","x":0,"y":672,"w":1200,"h":3,"color":"#c8956c30"},
    ]
}

# ══════════════════════════════════════════════════════════
# INFORKET - Historia: datos cobrando vida desde la laptop
# La laptop muestra un dashboard, y los datos "salen" de la
# pantalla como particulas/puntos que flotan hacia arriba.
# Sensacion de crecimiento, data-driven.
# ══════════════════════════════════════════════════════════
ink = {
    "width":1200,"height":675,"background":"#030308",
    "elements":[
        # Fondo tech profundo
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#03030a"],[0.25,"#0a0820"],[0.5,"#10103a"],[0.75,"#0a0820"],[1,"#03030a"]],
         "angle":150},

        # Glow desde la pantalla (la laptop ilumina la escena)
        {"type":"circle","x":500,"y":350,"r":350,"color":"accent","opacity":0.025},
        {"type":"circle","x":500,"y":350,"r":200,"color":"accent","opacity":0.035},

        # Mesa/superficie
        {"type":"rect","x":0,"y":520,"w":1200,"h":155,"color":"#05050f","opacity":0.8},
        {"type":"line","x1":0,"y1":520,"x2":1200,"y2":520,"color":"#7c6bf510","width":1},

        # Macbook con dashboard
        {"type":"image","src":os.path.join(A,"macbook_png.webp"),
         "x":150,"y":120,"w":750,"h":405},

        # Dashboard DENTRO de la pantalla
        {"type":"rect","x":275,"y":155,"w":500,"h":320,"color":"#080818"},

        # Chart de barras creciente
        {"type":"rect","x":300,"y":380,"w":24,"h":40,"color":"#7c6bf530","radius":2},
        {"type":"rect","x":334,"y":365,"w":24,"h":55,"color":"#7c6bf540","radius":2},
        {"type":"rect","x":368,"y":345,"w":24,"h":75,"color":"#7c6bf555","radius":2},
        {"type":"rect","x":402,"y":320,"w":24,"h":100,"color":"#7c6bf570","radius":2},
        {"type":"rect","x":436,"y":295,"w":24,"h":125,"color":"#7c6bf585","radius":2},
        {"type":"rect","x":470,"y":265,"w":24,"h":155,"color":"accent","radius":2},
        {"type":"rect","x":504,"y":250,"w":24,"h":170,"color":"green","radius":2},

        # Donut chart
        {"type":"ring","x":650,"y":320,"r":50,"thickness":12,"color":"accent","start":0,"end":210},
        {"type":"ring","x":650,"y":320,"r":50,"thickness":12,"color":"green","start":210,"end":300},
        {"type":"ring","x":650,"y":320,"r":50,"thickness":12,"color":"gold","start":300,"end":360},

        # Trend line
        {"type":"line","x1":300,"y1":395,"x2":530,"y2":260,"color":"#22c55e50","width":2},

        # DATOS SALIENDO de la pantalla (la magia visual)
        # Particulas que ascienden desde la laptop
        {"type":"circle","x":450,"y":140,"r":6,"color":"accent","opacity":0.5,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":8},
        {"type":"circle","x":500,"y":100,"r":8,"color":"green","opacity":0.4,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":10},
        {"type":"circle","x":550,"y":80,"r":5,"color":"gold","opacity":0.35},
        {"type":"circle","x":400,"y":110,"r":4,"color":"accent","opacity":0.3},
        {"type":"circle","x":520,"y":60,"r":10,"color":"accent","opacity":0.25,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":12},
        {"type":"circle","x":480,"y":40,"r":6,"color":"green","opacity":0.2},
        {"type":"circle","x":560,"y":50,"r":3,"color":"gold","opacity":0.3},
        {"type":"circle","x":430,"y":70,"r":7,"color":"accent","opacity":0.15},

        # Tablet mostrando datos secundarios
        {"type":"image","src":os.path.join(A,"tablet_png.webp"),
         "x":930,"y":240,"w":230,"h":170},
        {"type":"rect","x":955,"y":260,"w":180,"h":120,"color":"#080818"},
        {"type":"rect","x":975,"y":340,"w":12,"h":28,"color":"#7c6bf560","radius":2},
        {"type":"rect","x":996,"y":328,"w":12,"h":40,"color":"#7c6bf580","radius":2},
        {"type":"rect","x":1017,"y":318,"w":12,"h":50,"color":"accent","radius":2},
        {"type":"rect","x":1038,"y":330,"w":12,"h":38,"color":"green","radius":2},

        # Particulas desde la tablet tambien
        {"type":"circle","x":1000,"y":220,"r":4,"color":"accent","opacity":0.3},
        {"type":"circle","x":1040,"y":200,"r":3,"color":"green","opacity":0.25},

        # Lines
        {"type":"rect","x":0,"y":0,"w":1200,"h":2,"color":"accent"},
        {"type":"rect","x":0,"y":673,"w":1200,"h":2,"color":"#7c6bf520"},
    ]
}

for name, spec in [("pawsitive_story", pw), ("inforket_story", ink)]:
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    with open(os.path.join(OUT, f"{name}.webp"), "wb") as f:
        f.write(d)
    print(f"  {name}: {len(d)//1024}KB")
