"""Composiciones con fotos reales + engine para todos los sitios del usuario."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

specs = {
    # ─── PAWSITIVE BREWS - Cafe con foto real ────────────
    "pawsitive_photo": {
        "width":1080,"height":1080,"background":"#1a0d08",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1080,
             "stops":[[0,"#2a1508"],[0.4,"#1a0d08"],[1,"#050202"]],"direction":"radial"},
            # Foto de cafe con clip circular
            {"type":"image","src":os.path.join(ASSETS,"coffee_photo.jpg"),
             "x":190,"y":140,"w":700,"h":700,"clip":"circle","opacity":0.9},
            # Overlay oscuro sobre la foto para que el texto se lea
            {"type":"circle","x":540,"y":490,"r":350,"color":"#1a0d08","opacity":0.3},
            # Branding
            {"type":"text","text":"PAWSITIVE","x":540,"y":350,"size":72,"color":"#d4a574","align":"center","bold":True,"font":"cooper black","shadow":True,"shadow_blur":12},
            {"type":"text","text":"BREWS","x":540,"y":440,"size":72,"color":"#ff9a3c","align":"center","bold":True,"font":"cooper black"},
            {"type":"divider","x":340,"y":540,"w":400,"color":"#8b4513","thickness":2},
            {"type":"text","text":"Coffee for Dog Lovers","x":540,"y":570,"size":28,"color":"#c8956c","align":"center","font":"roboto slab"},
            # Foto de perro en esquina
            {"type":"image","src":os.path.join(ASSETS,"dog_happy.jpg"),
             "x":780,"y":780,"w":250,"h":250,"clip":"circle","opacity":0.8},
            # Borde decorativo
            {"type":"ring","x":905,"y":905,"r":127,"thickness":3,"color":"#d4a574"},
            {"type":"text","text":"pawsitivebrews.com","x":540,"y":980,"size":16,"color":"#5a3020","align":"center","font":"consolas"},
        ]
    },

    # ─── INFORKET - Marketing con foto real ──────────────
    "inforket_photo": {
        "width":1200,"height":630,"background":"dark",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,
             "stops":[[0,"#02020a"],[0.3,"#0a0825"],[0.6,"#161245"],[1,"#02020a"]],"angle":140},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"accent"},
            # Foto analytics con clip redondeado
            {"type":"image","src":os.path.join(ASSETS,"analytics_screen.jpg"),
             "x":620,"y":60,"w":540,"h":340,"clip":"rounded","clip_radius":20,"opacity":0.7},
            # Overlay gradiente sobre la foto
            {"type":"gradient","x":620,"y":60,"w":540,"h":340,"color1":"#02020a00","color2":"#02020aCC","direction":"horizontal"},
            # Contenido izquierdo
            {"type":"rect","x":35,"y":35,"w":550,"h":560,"color":"accent","opacity":0.025,"radius":20},
            {"type":"pill","x":60,"y":60,"text":"MARKETING DIGITAL","color":"accent","size":12,"py":8},
            {"type":"text","text":"Estrategias\nSEO 2026","x":60,"y":110,"size":72,"bold":True,"font":"mukta",
             "text_gradient":{"color1":"#ffffff","color2":"#c4b5fd"},
             "shadow":True,"shadow_blur":10},
            {"type":"divider","x":60,"y":330,"w":200,"color":"accent","thickness":2},
            {"type":"text","text":"Guia completa para triplicar\ntu trafico organico","x":60,"y":360,"size":20,"color":"#8888b0","font":"segoe ui"},
            {"type":"rect","x":60,"y":440,"w":200,"h":46,"color":"accent","radius":23,
             "shadow":True,"shadow_color":"#7c6bf550","shadow_blur":16},
            {"type":"text","text":"Leer Articulo","x":160,"y":452,"size":14,"color":"white","align":"center","bold":True,"font":"segoe ui"},
            {"type":"text","text":"inforket.com","x":60,"y":550,"size":14,"color":"#4a4a6a","font":"consolas"},
            # Foto laptop abajo derecha
            {"type":"image","src":os.path.join(ASSETS,"laptop_desk.jpg"),
             "x":620,"y":430,"w":540,"h":170,"clip":"rounded","clip_radius":16,"opacity":0.5},
            {"type":"gradient","x":620,"y":430,"w":540,"h":170,"color1":"#02020a80","color2":"#02020aDD","direction":"vertical"},
        ]
    },

    # ─── HATTON NATURALS - Productos naturales ───────────
    "hatton_photo": {
        "width":1080,"height":1080,"background":"#f5f0e8",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1080,
             "stops":[[0,"#fdf8f0"],[0.5,"#f0e8d8"],[1,"#e8dcc8"]],"direction":"radial"},
            # Foto lavanda con clip circular
            {"type":"image","src":os.path.join(ASSETS,"lavender.jpg"),
             "x":190,"y":50,"w":700,"h":700,"clip":"circle","opacity":0.85},
            # Overlay claro
            {"type":"circle","x":540,"y":400,"r":350,"color":"#f5f0e8","opacity":0.3},
            # Branding sobre la foto
            {"type":"text","text":"HATTON","x":540,"y":250,"size":64,"color":"#2d5a2e","align":"center","bold":True,"font":"optimus princeps","shadow":True,"shadow_color":"#ffffff80","shadow_blur":8},
            {"type":"text","text":"NATURALS","x":540,"y":340,"size":64,"color":"#5d8a5e","align":"center","bold":True,"font":"optimus princeps"},
            # Producto
            {"type":"rect","x":240,"y":750,"w":600,"h":250,"color":"#ffffff","opacity":0.7,"radius":20,
             "shadow":True,"shadow_color":"#00000015","shadow_blur":20},
            {"type":"image","src":os.path.join(ASSETS,"essential_oil.jpg"),
             "x":270,"y":770,"w":180,"h":210,"clip":"rounded","clip_radius":12},
            {"type":"text","text":"Aceite Esencial\nde Lavanda","x":500,"y":790,"size":28,"color":"#2d5a2e","bold":True,"font":"roboto slab"},
            {"type":"pill","x":500,"y":870,"text":"100% ORGANIC","color":"#5d8a5e","size":12},
            {"type":"text","text":"$18.99","x":500,"y":920,"size":36,"color":"#2d5a2e","bold":True,"font":"roboto slab bold"},
        ]
    },

    # ─── YOUTUBE THUMB con foto ──────────────────────────
    "youtube_photo": {
        "width":1280,"height":720,"background":"dark",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1280,"h":720,
             "stops":[[0,"#0a0510"],[0.5,"#1a0a30"],[1,"#0a0510"]],"angle":135},
            # Foto de fondo con overlay
            {"type":"image","src":os.path.join(ASSETS,"laptop_desk.jpg"),
             "x":0,"y":0,"w":1280,"h":720,"opacity":0.15},
            # Accent bars
            {"type":"rect","x":0,"y":0,"w":8,"h":720,"color":"red"},
            {"type":"rect","x":0,"y":714,"w":1280,"h":6,"color":"red"},
            # Titulo con gradient
            {"type":"text","text":"5 ERRORES","x":60,"y":140,"size":110,"bold":True,"font":"impact",
             "text_gradient":{"color1":"#ffffff","color2":"#ff8888"},
             "shadow":True,"shadow_blur":12},
            {"type":"text","text":"DE SEO","x":60,"y":280,"size":110,"color":"red","bold":True,"font":"impact",
             "shadow":True,"shadow_blur":8},
            {"type":"text","text":"que destruyen tu trafico","x":60,"y":420,"size":38,"color":"#cccccc","font":"mukta"},
            {"type":"pill","x":60,"y":500,"text":"GUIA 2026","color":"red","size":18,"py":12},
            # Foto analytics en esquina
            {"type":"image","src":os.path.join(ASSETS,"analytics_screen.jpg"),
             "x":850,"y":100,"w":380,"h":250,"clip":"rounded","clip_radius":16,"opacity":0.6},
            {"type":"rect","x":850,"y":100,"w":380,"h":250,"color":"dark","opacity":0.3,"radius":16},
            {"type":"text","text":"INFORKET","x":60,"y":630,"size":26,"color":"#ff6666","bold":True,"font":"bahnschrift","letter_spacing":4},
        ]
    },

    # ─── REAL ESTATE con foto ────────────────────────────
    "realestate_photo": {
        "width":1200,"height":630,"background":"#0f1923",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,
             "stops":[[0,"#0f1923"],[0.5,"#152030"],[1,"#0f1923"]],"angle":135},
            {"type":"rect","x":0,"y":0,"w":5,"h":630,"color":"gold"},
            {"type":"rect","x":0,"y":624,"w":1200,"h":6,"color":"gold"},
            # Foto laptop como fondo sutil
            {"type":"image","src":os.path.join(ASSETS,"laptop_desk.jpg"),
             "x":500,"y":0,"w":700,"h":630,"opacity":0.08},
            {"type":"pill","x":50,"y":50,"text":"EXCLUSIVO","color":"gold","size":13,"text_color":"#0f1923"},
            {"type":"text","text":"Departamento\nPremium","x":50,"y":100,"size":68,"color":"white","bold":True,"font":"roboto slab",
             "shadow":True,"shadow_blur":8},
            {"type":"text","text":"3 Amb  |  2 Banos  |  95 m2","x":50,"y":300,"size":22,"color":"#8090a0","font":"segoe ui"},
            {"type":"divider","x":50,"y":350,"w":200,"color":"gold","thickness":2},
            {"type":"text","text":"USD 245,000","x":50,"y":380,"size":56,"color":"gold","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Palermo, Buenos Aires","x":50,"y":460,"size":20,"color":"#607080","font":"segoe ui"},
            {"type":"text","text":"Premium Properties","x":1100,"y":570,"size":18,"color":"#4a5a6d","align":"right","font":"segoe ui"},
        ]
    },

    # ─── ETSY - Dog merch con foto ───────────────────────
    "etsy_photo": {
        "width":2000,"height":2000,"background":"#faf8f5",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":2000,"h":2000,
             "stops":[[0,"#fdf9f3"],[0.5,"#f5ece0"],[1,"#ebe0d0"]],"direction":"radial"},
            # Foto de perro grande
            {"type":"image","src":os.path.join(ASSETS,"dog_happy.jpg"),
             "x":400,"y":100,"w":1200,"h":1200,"clip":"circle","opacity":0.25},
            # Texto principal
            {"type":"text","text":"BEST","x":1000,"y":400,"size":220,"color":"#3d2314","align":"center","bold":True,"font":"impact"},
            {"type":"text","text":"DOG MOM","x":1000,"y":650,"size":220,"color":"#8b4513","align":"center","bold":True,"font":"impact"},
            {"type":"text","text":"EVER","x":1000,"y":900,"size":220,"color":"#d4956a","align":"center","bold":True,"font":"impact"},
            {"type":"divider","x":500,"y":1150,"w":1000,"color":"#d4a06a60","thickness":2},
            {"type":"text","text":"Premium Unisex T-Shirt","x":1000,"y":1220,"size":44,"color":"#6b4423","align":"center","font":"bahnschrift"},
            {"type":"text","text":"S  M  L  XL  2XL","x":1000,"y":1320,"size":36,"color":"#a08060","align":"center","font":"segoe ui"},
            {"type":"text","text":"$24.99","x":1000,"y":1460,"size":90,"color":"#3d2314","align":"center","bold":True,"font":"roboto slab bold"},
            {"type":"pill","x":1000,"y":1620,"text":"FREE SHIPPING","color":"#5d8a5e","align":"center","size":22,"py":14},
        ]
    },
}

print("=" * 60)
for name, spec in specs.items():
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 92)
    data = buf.read()
    path = os.path.join(OUT, f"{name}.webp")
    with open(path, "wb") as f:
        f.write(data)
    print(f"  {name:22s} {img.width}x{img.height:4d}  {len(data)/1024:5.1f}KB")
print("=" * 60)
