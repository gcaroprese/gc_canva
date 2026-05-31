"""Genera imagenes demo de produccion para cada sitio del usuario."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output", "demos")
os.makedirs(OUT, exist_ok=True)

DEMOS = {
    # ─── inforket.com ───────────────────────────
    "inforket_og": {
        "width":1200,"height":630,"background":"dark",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"stops":[[0,"#050510"],[0.4,"#12103a"],[1,"#050510"]],"angle":135},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"accent"},
            {"type":"rect","x":0,"y":627,"w":1200,"h":3,"color":"accent"},
            {"type":"rect","x":40,"y":40,"w":520,"h":550,"color":"accent","opacity":0.04,"radius":20},
            {"type":"pill","x":60,"y":65,"text":"MARKETING DIGITAL","color":"accent","size":12},
            {"type":"text","text":"Titulo del\nArticulo","x":60,"y":120,"size":72,"color":"white","bold":True,"font":"mukta","shadow":True,"shadow_blur":10},
            {"type":"divider","x":60,"y":330,"w":200,"color":"accent","thickness":2},
            {"type":"text","text":"Descripcion breve del contenido\nque aporta valor al lector","x":60,"y":360,"size":20,"color":"#8888b0","font":"segoe ui"},
            {"type":"rect","x":60,"y":440,"w":160,"h":42,"color":"accent","radius":21},
            {"type":"text","text":"Leer mas","x":140,"y":450,"size":14,"color":"white","align":"center","bold":True,"font":"segoe ui"},
            {"type":"text","text":"inforket.com","x":60,"y":540,"size":14,"color":"#5a5a80","font":"consolas"},
            {"type":"rect","x":620,"y":80,"w":530,"h":460,"color":"#ffffff","opacity":0.02,"radius":16},
            {"type":"text","text":"+340%","x":885,"y":220,"size":120,"color":"green","align":"center","bold":True,"font":"impact","opacity":0.15},
            {"type":"text","text":"trafico organico","x":885,"y":360,"size":20,"color":"#5a5a80","align":"center","font":"segoe ui"},
        ]
    },

    # ─── gabrielcaroprese.com ────────────────────
    "gabriel_og": {
        "width":1200,"height":630,"background":"dark",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"stops":[[0,"#0a0510"],[0.5,"#141030"],[1,"#0a0510"]],"angle":120},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"gold"},
            {"type":"rect","x":0,"y":627,"w":1200,"h":3,"color":"#c9a22740"},
            {"type":"circle","x":1000,"y":180,"r":160,"color":"gold","opacity":0.03},
            {"type":"rect","x":40,"y":40,"w":500,"h":550,"color":"gold","opacity":0.03,"radius":20},
            {"type":"pill","x":60,"y":65,"text":"CREATIVE DIRECTOR","color":"gold","size":11,"text_color":"#1a1040"},
            {"type":"text","text":"Gabriel","x":60,"y":120,"size":68,"color":"white","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Caroprese","x":60,"y":210,"size":68,"color":"gold","bold":True,"font":"roboto slab"},
            {"type":"divider","x":60,"y":310,"w":140,"color":"gold","thickness":2},
            {"type":"text","text":"Diseno digital y marketing\ncreativo con resultados","x":60,"y":340,"size":20,"color":"#9090b0","font":"segoe ui"},
            {"type":"rect","x":60,"y":430,"w":160,"h":42,"color":"gold","radius":21,"shadow":True,"shadow_color":"#c9a22730","shadow_blur":12},
            {"type":"text","text":"Contactar","x":140,"y":440,"size":14,"color":"#1a1040","align":"center","bold":True,"font":"segoe ui"},
            {"type":"text","text":"gabrielcaroprese.com","x":60,"y":540,"size":14,"color":"#5a5070","font":"consolas"},
            {"type":"rect","x":600,"y":80,"w":260,"h":120,"color":"#14142a","radius":14,"shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":6},
            {"type":"pill","x":620,"y":96,"text":"PROYECTOS","color":"green","size":10},
            {"type":"text","text":"120+","x":620,"y":130,"size":44,"color":"green","bold":True,"font":"impact"},
            {"type":"rect","x":890,"y":80,"w":260,"h":120,"color":"#14142a","radius":14,"shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":6},
            {"type":"pill","x":910,"y":96,"text":"CLIENTES","color":"gold","size":10},
            {"type":"text","text":"45+","x":910,"y":130,"size":44,"color":"gold","bold":True,"font":"impact"},
        ]
    },

    # ─── hattonnaturals.com ──────────────────────
    "hatton_post": {
        "width":1080,"height":1080,"background":"#f5f0e8",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1080,"stops":[[0,"#fdf8f0"],[0.5,"#f0e8d8"],[1,"#e8dcc8"]],"direction":"radial"},
            {"type":"ellipse","x":140,"y":140,"w":800,"h":800,"color":"#8fbc8f","opacity":0.08},
            {"type":"rect","x":60,"y":60,"w":960,"h":960,"color":"#5d8a5e","opacity":0.03,"radius":30},
            {"type":"text","text":"HATTON\nNATURALS","x":540,"y":180,"size":80,"color":"#2d5a2e","align":"center","bold":True,"font":"optimus princeps"},
            {"type":"divider","x":340,"y":400,"w":400,"color":"#8fbc8f","thickness":2},
            {"type":"text","text":"Pure  |  Natural  |  Authentic","x":540,"y":440,"size":30,"color":"#5d8a5e","align":"center","font":"gabriola"},
            {"type":"text","text":"Aceite Esencial\nde Lavanda","x":540,"y":530,"size":52,"color":"#2d5a2e","align":"center","bold":True,"font":"roboto slab"},
            {"type":"pill","x":540,"y":690,"text":"100% ORGANIC","color":"#5d8a5e","align":"center","size":16,"py":10},
            {"type":"text","text":"$18.99","x":540,"y":780,"size":64,"color":"#2d5a2e","align":"center","bold":True,"font":"roboto slab bold"},
            {"type":"text","text":"hattonnaturals.com","x":540,"y":920,"size":18,"color":"#8a9e6a","align":"center","font":"consolas"},
        ]
    },

    # ─── pawsitivebrews.com ──────────────────────
    "pawsitive_promo": {
        "width":1080,"height":1080,"background":"#1a0d08",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1080,"stops":[[0,"#2a1508"],[0.4,"#1a0d08"],[1,"#0a0504"]],"direction":"radial"},
            {"type":"ellipse","x":140,"y":140,"w":800,"h":800,"color":"#8b4513","opacity":0.08},
            {"type":"text","text":"PAWSITIVE\nBREWS","x":540,"y":180,"size":84,"color":"#d4a574","align":"center","bold":True,"font":"cooper black","shadow":True,"shadow_blur":12},
            {"type":"divider","x":290,"y":420,"w":500,"color":"#8b4513","thickness":2},
            {"type":"text","text":"Cafe Artesanal","x":540,"y":460,"size":32,"color":"#c8956c","align":"center","font":"roboto slab"},
            {"type":"pill","x":540,"y":550,"text":"PROMO","color":"#d4956a","align":"center","size":18,"py":10},
            {"type":"text","text":"2x1","x":540,"y":640,"size":160,"color":"white","align":"center","bold":True,"font":"impact","shadow":True,"shadow_blur":24,"shadow_color":"#d4956a50"},
            {"type":"text","text":"en todos los lattes","x":540,"y":830,"size":26,"color":"#c8956c","align":"center","font":"segoe ui"},
            {"type":"text","text":"pawsitivebrews.com","x":540,"y":980,"size":16,"color":"#5a3020","align":"center","font":"consolas"},
        ]
    },

    # ─── YouTube Thumbnail ───────────────────────
    "youtube_thumb": {
        "width":1280,"height":720,"background":"dark",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1280,"h":720,"stops":[[0,"#0a0510"],[0.5,"#1a0a2e"],[1,"#0a0510"]],"angle":135},
            {"type":"rect","x":0,"y":0,"w":8,"h":720,"color":"red"},
            {"type":"rect","x":0,"y":712,"w":1280,"h":8,"color":"red"},
            {"type":"text","text":"5 ERRORES","x":50,"y":120,"size":100,"color":"white","bold":True,"font":"impact",
             "text_gradient":{"color1":"#ffffff","color2":"#ff6666"},"shadow":True,"shadow_blur":10},
            {"type":"text","text":"DE SEO","x":50,"y":250,"size":100,"color":"red","bold":True,"font":"impact","shadow":True,"shadow_blur":8},
            {"type":"text","text":"que arruinan tu trafico","x":50,"y":380,"size":36,"color":"#cccccc","font":"mukta"},
            {"type":"pill","x":50,"y":460,"text":"2026 EDITION","color":"red","size":16,"py":10},
            {"type":"text","text":"INFORKET","x":50,"y":600,"size":24,"color":"#ff6666","bold":True,"font":"bahnschrift"},
            {"type":"circle","x":1100,"y":360,"r":200,"color":"red","opacity":0.04},
            {"type":"text","text":"?","x":1100,"y":250,"size":220,"color":"red","align":"center","bold":True,"font":"impact","opacity":0.08},
        ]
    },

    # ─── Etsy Listing ────────────────────────────
    "etsy_listing": {
        "width":2000,"height":2000,"background":"#faf8f5",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":2000,"h":2000,"stops":[[0,"#fdf9f3"],[0.5,"#f5ece0"],[1,"#ebe0d0"]],"direction":"radial"},
            {"type":"ellipse","x":250,"y":250,"w":1500,"h":1500,"color":"#d4a06a","opacity":0.05},
            {"type":"text","text":"BEST","x":1000,"y":380,"size":200,"color":"#3d2314","align":"center","bold":True,"font":"impact"},
            {"type":"text","text":"DOG MOM","x":1000,"y":620,"size":200,"color":"#8b4513","align":"center","bold":True,"font":"impact"},
            {"type":"text","text":"EVER","x":1000,"y":860,"size":200,"color":"#d4956a","align":"center","bold":True,"font":"impact"},
            {"type":"divider","x":500,"y":1100,"w":1000,"color":"#d4a06a80","text":"","thickness":2},
            {"type":"text","text":"Premium Unisex T-Shirt","x":1000,"y":1180,"size":40,"color":"#6b4423","align":"center","font":"bahnschrift"},
            {"type":"text","text":"S  M  L  XL  2XL","x":1000,"y":1280,"size":32,"color":"#a08060","align":"center","font":"segoe ui"},
            {"type":"text","text":"$24.99","x":1000,"y":1420,"size":80,"color":"#3d2314","align":"center","bold":True,"font":"roboto slab bold"},
            {"type":"pill","x":1000,"y":1560,"text":"FREE SHIPPING","color":"#5d8a5e","align":"center","size":20,"py":12},
        ]
    },

    # ─── Iglesia ─────────────────────────────────
    "iglesia_domingo": {
        "width":1080,"height":1080,"background":"#080808",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1080,"stops":[[0,"#1a1200"],[0.4,"#080808"],[1,"#000000"]],"direction":"radial"},
            {"type":"text","text":"+","x":540,"y":80,"size":120,"color":"#ffd700","align":"center","font":"times"},
            {"type":"pill","x":540,"y":260,"text":"DOMINGO 10:00 AM","color":"#ffd700","align":"center","size":14,"text_color":"#1a1200","py":10},
            {"type":"text","text":"La fe mueve\nmontanas","x":540,"y":350,"size":72,"color":"white","align":"center","font":"optimus princeps","shadow":True,"shadow_blur":20,"shadow_color":"#ffd70030"},
            {"type":"text","text":"Mateo 17:20","x":540,"y":580,"size":28,"color":"#ffd700","align":"center","font":"gabriola"},
            {"type":"divider","x":290,"y":660,"w":500,"color":"#ffd70030","thickness":1},
            {"type":"text","text":"Iglesia de la Gracia","x":540,"y":700,"size":28,"color":"#8a7040","align":"center","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Todos son bienvenidos","x":540,"y":770,"size":20,"color":"#5a5040","align":"center","font":"segoe ui"},
        ]
    },

    # ─── Real Estate ─────────────────────────────
    "realestate_listing": {
        "width":1200,"height":630,"background":"#0f1923",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"stops":[[0,"#0f1923"],[0.5,"#152030"],[1,"#0f1923"]],"angle":135},
            {"type":"rect","x":0,"y":0,"w":5,"h":630,"color":"gold"},
            {"type":"rect","x":0,"y":622,"w":1200,"h":8,"color":"gold"},
            {"type":"pill","x":60,"y":50,"text":"EXCLUSIVO","color":"gold","size":12,"text_color":"#0f1923"},
            {"type":"text","text":"Departamento\nPremium","x":60,"y":100,"size":68,"color":"white","bold":True,"font":"roboto slab","shadow":True,"shadow_blur":8},
            {"type":"text","text":"3 Amb  |  2 Banos  |  95 m2  |  Balcon","x":60,"y":290,"size":20,"color":"#8090a0","font":"segoe ui"},
            {"type":"divider","x":60,"y":340,"w":180,"color":"gold","thickness":2},
            {"type":"text","text":"USD 245,000","x":60,"y":370,"size":52,"color":"gold","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Palermo, Buenos Aires","x":60,"y":450,"size":20,"color":"#607080","font":"segoe ui"},
            {"type":"text","text":"Premium Properties","x":1100,"y":560,"size":18,"color":"#4a5a6d","align":"right","font":"segoe ui"},
        ]
    },
}

print("=" * 60)
print("  DEMO SITES - Produccion")
print("=" * 60)
total_time = 0
total_size = 0
for name, spec in DEMOS.items():
    t0 = time.time()
    img = generate_from_spec(spec)
    dt = time.time() - t0
    buf, _, _ = export_image(img, "webp", 92)
    data = buf.read()
    path = os.path.join(OUT, f"{name}.webp")
    with open(path, "wb") as f:
        f.write(data)
    kb = len(data) / 1024
    total_time += dt
    total_size += kb
    print(f"  {name:22s} {img.width}x{img.height:4d}  {dt*1000:5.0f}ms  {kb:5.1f}KB")

print("-" * 60)
print(f"  TOTAL: {len(DEMOS)} imagenes | {total_time*1000:.0f}ms | {total_size:.0f}KB")
print(f"  OUTPUT: {OUT}")
print("=" * 60)
