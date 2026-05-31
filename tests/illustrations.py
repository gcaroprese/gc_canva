"""Ilustraciones sin texto para pawsitivebrews e inforket."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")

# ═══════════════════════════════════════════════════════════
# PAWSITIVE BREWS - Taza de cafe + huella de perro
# ═══════════════════════════════════════════════════════════
pawsitive = {
    "width":1080,"height":1080,"background":"#1a0d08",
    "elements":[
        # Fondo atmosferico
        {"type":"gradient","x":0,"y":0,"w":1080,"h":1080,
         "stops":[[0,"#2a1508"],[0.3,"#1a0d08"],[0.7,"#0d0604"],[1,"#050202"]],
         "direction":"radial"},

        # Glow central calido
        {"type":"circle","x":540,"y":500,"r":350,"color":"#d4956a","opacity":0.04},
        {"type":"circle","x":540,"y":500,"r":250,"color":"#d4956a","opacity":0.05},
        {"type":"circle","x":540,"y":500,"r":150,"color":"#d4956a","opacity":0.04},

        # === TAZA DE CAFE ===
        # Cuerpo de la taza (rect redondeado)
        {"type":"rect","x":340,"y":420,"w":300,"h":280,"color":"#c8956c","radius":30,
         "shadow":True,"shadow_color":"#00000080","shadow_blur":30,"shadow_y":15},
        # Interior de la taza (elipse oscura = cafe)
        {"type":"ellipse","x":350,"y":400,"w":280,"h":60,"color":"#3d1e0a"},
        # Superficie del cafe (elipse marron)
        {"type":"ellipse","x":355,"y":405,"w":270,"h":50,"color":"#6b3a1a"},
        # Reflejo en el cafe
        {"type":"ellipse","x":400,"y":415,"w":100,"h":20,"color":"#8b5030","opacity":0.6},
        # Handle derecho (arco)
        {"type":"arc","x":620,"y":480,"w":100,"h":150,"start":-60,"end":60,"color":"#c8956c","width":18},

        # === VAPOR ===
        # 3 lineas de vapor curvas (usando circulos delgados)
        {"type":"arc","x":400,"y":300,"w":40,"h":100,"start":180,"end":360,"color":"#ffffff","width":3},
        {"type":"arc","x":420,"y":250,"w":40,"h":80,"start":0,"end":180,"color":"#ffffff","width":3,"opacity":0.7},
        {"type":"arc","x":470,"y":280,"w":35,"h":110,"start":180,"end":360,"color":"#ffffff","width":3,"opacity":0.8},
        {"type":"arc","x":490,"y":230,"w":35,"h":80,"start":0,"end":180,"color":"#ffffff","width":3,"opacity":0.5},
        {"type":"arc","x":540,"y":290,"w":30,"h":100,"start":180,"end":360,"color":"#ffffff","width":3,"opacity":0.6},
        {"type":"arc","x":555,"y":240,"w":30,"h":80,"start":0,"end":180,"color":"#ffffff","width":3,"opacity":0.4},

        # Plato debajo de la taza
        {"type":"ellipse","x":310,"y":680,"w":360,"h":40,"color":"#a07050",
         "shadow":True,"shadow_color":"#00000060","shadow_blur":10,"shadow_y":5},

        # === HUELLA DE PERRO (arriba a la derecha) ===
        # Pad principal
        {"type":"circle","x":800,"y":230,"r":55,"color":"#d4a574","opacity":0.9,
         "shadow":True,"shadow_color":"#d4956a40","shadow_blur":15},
        # Dedos (4 circulos)
        {"type":"circle","x":745,"y":145,"r":25,"color":"#d4a574","opacity":0.85},
        {"type":"circle","x":800,"y":120,"r":28,"color":"#d4a574","opacity":0.85},
        {"type":"circle","x":855,"y":130,"r":25,"color":"#d4a574","opacity":0.85},
        {"type":"circle","x":885,"y":175,"r":22,"color":"#d4a574","opacity":0.85},

        # === HUELLA DE PERRO PEQUEÑA (abajo a la izquierda) ===
        {"type":"circle","x":200,"y":800,"r":30,"color":"#8b6040","opacity":0.4},
        {"type":"circle","x":170,"y":750,"r":14,"color":"#8b6040","opacity":0.35},
        {"type":"circle","x":200,"y":738,"r":15,"color":"#8b6040","opacity":0.35},
        {"type":"circle","x":230,"y":745,"r":14,"color":"#8b6040","opacity":0.35},
        {"type":"circle","x":248,"y":770,"r":12,"color":"#8b6040","opacity":0.35},

        # Granos de cafe decorativos (ellipses pequenos)
        {"type":"ellipse","x":150,"y":920,"w":25,"h":18,"color":"#5a3018","opacity":0.6,"rotate":30},
        {"type":"ellipse","x":880,"y":850,"w":22,"h":16,"color":"#5a3018","opacity":0.5,"rotate":-20},
        {"type":"ellipse","x":120,"y":350,"w":20,"h":14,"color":"#5a3018","opacity":0.4,"rotate":45},

        # Estrellas decorativas
        {"type":"star","x":900,"y":500,"r":12,"inner_r":5,"points":4,"color":"#ffd700","opacity":0.3},
        {"type":"star","x":180,"y":200,"r":10,"inner_r":4,"points":4,"color":"#ffd700","opacity":0.2},
        {"type":"star","x":850,"y":900,"r":8,"inner_r":3,"points":4,"color":"#ffd700","opacity":0.25},
    ]
}

# ═══════════════════════════════════════════════════════════
# INFORKET - Visualizacion de datos / dashboard abstracto
# ═══════════════════════════════════════════════════════════
inforket = {
    "width":1200,"height":630,"background":"dark",
    "elements":[
        # Fondo
        {"type":"gradient","x":0,"y":0,"w":1200,"h":630,
         "stops":[[0,"#02020a"],[0.3,"#0a0825"],[0.6,"#141040"],[1,"#02020a"]],
         "angle":140},

        # Grid de puntos decorativos (repeat)
        {"type":"repeat","count":8,"dx":80,"dy":0,
         "element":{"type":"repeat","count":5,"dx":0,"dy":80,
                    "element":{"type":"circle","x":200,"y":80,"r":2,"color":"#7c6bf5","opacity":0.15}}},

        # Linea accent top
        {"type":"rect","x":0,"y":0,"w":1200,"h":2,"color":"accent"},

        # === CHART DE BARRAS PRINCIPAL ===
        # Background del chart
        {"type":"rect","x":60,"y":80,"w":500,"h":420,"color":"#0d0d20","radius":20,
         "shadow":True,"shadow_color":"#00000060","shadow_blur":24,"shadow_y":8},

        # Grid lines horizontales
        {"type":"line","x1":100,"y1":180,"x2":520,"y2":180,"color":"#1a1a35","width":1},
        {"type":"line","x1":100,"y1":260,"x2":520,"y2":260,"color":"#1a1a35","width":1},
        {"type":"line","x1":100,"y1":340,"x2":520,"y2":340,"color":"#1a1a35","width":1},
        {"type":"line","x1":100,"y1":420,"x2":520,"y2":420,"color":"#1a1a35","width":1},

        # Barras con gradiente de color (de pequeno a grande)
        {"type":"rect","x":110,"y":380,"w":35,"h":60,"color":"#7c6bf525","radius":4},
        {"type":"rect","x":158,"y":340,"w":35,"h":100,"color":"#7c6bf535","radius":4},
        {"type":"rect","x":206,"y":360,"w":35,"h":80,"color":"#7c6bf540","radius":4},
        {"type":"rect","x":254,"y":310,"w":35,"h":130,"color":"#7c6bf550","radius":4},
        {"type":"rect","x":302,"y":280,"w":35,"h":160,"color":"#7c6bf560","radius":4},
        {"type":"rect","x":350,"y":300,"w":35,"h":140,"color":"#7c6bf570","radius":4},
        {"type":"rect","x":398,"y":250,"w":35,"h":190,"color":"#7c6bf580","radius":4},
        {"type":"rect","x":446,"y":200,"w":35,"h":240,"color":"accent","radius":4},
        {"type":"rect","x":494,"y":220,"w":35,"h":220,"color":"#22c55e","radius":4},

        # Punto highlight en la barra mas alta
        {"type":"circle","x":463,"y":195,"r":6,"color":"accent",
         "shadow":True,"shadow_color":"#7c6bf560","shadow_blur":10},

        # Linea de tendencia (diagonal ascendente)
        {"type":"line","x1":120,"y1":400,"x2":510,"y2":200,"color":"#22c55e50","width":2},

        # === PIE CHART (donut) ===
        {"type":"rect","x":620,"y":80,"w":280,"h":280,"color":"#0d0d20","radius":20,
         "shadow":True,"shadow_color":"#00000060","shadow_blur":24,"shadow_y":8},
        # Ring segments
        {"type":"ring","x":760,"y":220,"r":90,"thickness":20,"color":"accent","start":0,"end":200},
        {"type":"ring","x":760,"y":220,"r":90,"thickness":20,"color":"#22c55e","start":200,"end":290},
        {"type":"ring","x":760,"y":220,"r":90,"thickness":20,"color":"#f59e0b","start":290,"end":340},
        {"type":"ring","x":760,"y":220,"r":90,"thickness":20,"color":"#ef4444","start":340,"end":360},
        # Centro del donut
        {"type":"circle","x":760,"y":220,"r":55,"color":"#0d0d20"},

        # === MINI CARDS DE METRICAS ===
        {"type":"rect","x":940,"y":80,"w":220,"h":120,"color":"#0d0d20","radius":14,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":14,"shadow_y":4},
        # Icono: flecha arriba (triangulo)
        {"type":"triangle","x":970,"y":115,"w":30,"h":25,"color":"#22c55e"},
        # Mini sparkline
        {"type":"line","x1":1020,"y1":155,"x2":1040,"y2":135,"color":"#22c55e","width":2},
        {"type":"line","x1":1040,"y1":135,"x2":1060,"y2":145,"color":"#22c55e","width":2},
        {"type":"line","x1":1060,"y1":145,"x2":1080,"y2":120,"color":"#22c55e","width":2},
        {"type":"line","x1":1080,"y1":120,"x2":1100,"y2":110,"color":"#22c55e","width":2},
        {"type":"line","x1":1100,"y1":110,"x2":1130,"y2":100,"color":"#22c55e","width":2},

        {"type":"rect","x":940,"y":220,"w":220,"h":120,"color":"#0d0d20","radius":14,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":14,"shadow_y":4},
        # Icono: circulo con punto
        {"type":"ring","x":985,"y":280,"r":15,"thickness":3,"color":"#f59e0b"},
        {"type":"circle","x":985,"y":280,"r":5,"color":"#f59e0b"},
        # Mini bars
        {"type":"rect","x":1020,"y":290,"w":12,"h":30,"color":"#f59e0b40","radius":2},
        {"type":"rect","x":1040,"y":280,"w":12,"h":40,"color":"#f59e0b60","radius":2},
        {"type":"rect","x":1060,"y":270,"w":12,"h":50,"color":"#f59e0b80","radius":2},
        {"type":"rect","x":1080,"y":260,"w":12,"h":60,"color":"#f59e0b","radius":2},

        # === SCATTER PLOT ABAJO ===
        {"type":"rect","x":620,"y":400,"w":540,"h":190,"color":"#0d0d20","radius":14,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":14,"shadow_y":4},
        # Grid
        {"type":"line","x1":660,"y1":450,"x2":1120,"y2":450,"color":"#1a1a35","width":1},
        {"type":"line","x1":660,"y1":500,"x2":1120,"y2":500,"color":"#1a1a35","width":1},
        {"type":"line","x1":660,"y1":550,"x2":1120,"y2":550,"color":"#1a1a35","width":1},
        # Puntos scatter
        {"type":"circle","x":700,"y":530,"r":6,"color":"accent","opacity":0.7},
        {"type":"circle","x":750,"y":510,"r":8,"color":"accent","opacity":0.8},
        {"type":"circle","x":810,"y":490,"r":5,"color":"accent","opacity":0.6},
        {"type":"circle","x":850,"y":520,"r":7,"color":"#22c55e","opacity":0.7},
        {"type":"circle","x":900,"y":470,"r":9,"color":"accent","opacity":0.9},
        {"type":"circle","x":940,"y":480,"r":6,"color":"#22c55e","opacity":0.8},
        {"type":"circle","x":980,"y":460,"r":8,"color":"accent","opacity":0.7},
        {"type":"circle","x":1020,"y":440,"r":10,"color":"#22c55e","opacity":0.9,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":8},
        {"type":"circle","x":1060,"y":450,"r":7,"color":"accent","opacity":0.8},
        {"type":"circle","x":1100,"y":430,"r":11,"color":"accent",
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":8},
        # Linea de tendencia
        {"type":"line","x1":680,"y1":540,"x2":1110,"y2":430,"color":"#ffffff15","width":1},

        # Decorativo: anillo grande sutil
        {"type":"ring","x":100,"y":550,"r":200,"thickness":1,"color":"#7c6bf510"},
    ]
}

for name, spec in [("pawsitive_illustration", pawsitive), ("inforket_illustration", inforket)]:
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 95)  # quality 95 para max calidad
    data = buf.read()
    path = os.path.join(OUT, f"{name}.webp")
    with open(path, "wb") as f:
        f.write(data)
    print(f"  {name}: {len(data)/1024:.1f}KB ({img.width}x{img.height})")
