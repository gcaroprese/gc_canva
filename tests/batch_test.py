"""
GC Canva - Test batch de generacion de imagenes
Genera varias imagenes de prueba y reporta calidad/tiempos.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

TESTS = [
    # 1. Blog OG - pawsitivebrews.com
    ("blog_pawsitive", {
        "width": 1200, "height": 630, "background": "#0a0505",
        "elements": [
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"color1":"#3d2314","color2":"#0a0505","direction":"diagonal"},
            {"type":"rect","x":0,"y":0,"w":1200,"h":4,"color":"#d4956a"},
            {"type":"rect","x":0,"y":626,"w":1200,"h":4,"color":"#d4956a"},
            {"type":"ellipse","x":300,"y":80,"w":600,"h":470,"color":"#8b4513","opacity":0.1},
            {"type":"text","text":"PAWSITIVE BREWS","x":600,"y":140,"size":68,"color":"#d4a574","align":"center","bold":True,"font":"cooper black","shadow":True,"shadow_blur":10},
            {"type":"text","text":"Coffee for Dog Lovers","x":600,"y":250,"size":28,"color":"#c8956c","align":"center","font":"roboto slab"},
            {"type":"rect","x":400,"y":310,"w":400,"h":2,"color":"#8b4513"},
            {"type":"text","text":"NEW BLOG POST","x":600,"y":340,"size":16,"color":"#ff9a3c","align":"center","bold":True,"font":"bahnschrift"},
            {"type":"text","text":"5 Ways to Enjoy Coffee\nWith Your Dog","x":600,"y":380,"size":40,"color":"#ffffff","align":"center","bold":True,"font":"roboto slab bold","shadow":True,"shadow_blur":6},
            {"type":"text","text":"pawsitivebrews.com","x":600,"y":560,"size":16,"color":"#6b4423","align":"center","font":"segoe ui"},
        ]
    }),

    # 2. Blog OG - inforket.com (tech/marketing)
    ("blog_inforket", {
        "width": 1200, "height": 630, "background": "#0a0a14",
        "elements": [
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"color1":"#0d0d20","color2":"#1a0a2e","direction":"diagonal"},
            {"type":"rect","x":0,"y":0,"w":5,"h":630,"color":"#7c6bf5"},
            {"type":"rect","x":0,"y":626,"w":1200,"h":4,"color":"#7c6bf5"},
            {"type":"text","text":"MARKETING DIGITAL","x":60,"y":80,"size":16,"color":"#7c6bf5","font":"consolas","bold":True},
            {"type":"text","text":"10 Estrategias SEO\nque Funcionan en 2026","x":60,"y":140,"size":64,"color":"#ffffff","bold":True,"font":"mukta","shadow":True,"shadow_blur":8},
            {"type":"rect","x":60,"y":370,"w":100,"h":3,"color":"#7c6bf5"},
            {"type":"text","text":"Guia completa para posicionar tu sitio web","x":60,"y":400,"size":22,"color":"#8888b0","font":"segoe ui"},
            {"type":"text","text":"inforket.com","x":60,"y":560,"size":16,"color":"#5a5a80","font":"segoe ui"},
        ]
    }),

    # 3. Etsy listing - Dog product
    ("etsy_dog_product", {
        "width": 2000, "height": 2000, "background": "#faf8f5",
        "elements": [
            {"type":"gradient","x":0,"y":0,"w":2000,"h":2000,"color1":"#fdf9f3","color2":"#f0e8d8","direction":"radial"},
            {"type":"ellipse","x":300,"y":300,"w":1400,"h":1400,"color":"#d4a06a","opacity":0.06},
            {"type":"text","text":"DOG MOM","x":1000,"y":500,"size":220,"color":"#3d2314","align":"center","bold":True,"font":"impact","shadow":True,"shadow_color":"#d4956a40","shadow_blur":20},
            {"type":"text","text":"LIFE","x":1000,"y":760,"size":220,"color":"#8b4513","align":"center","bold":True,"font":"impact"},
            {"type":"star","x":1000,"y":1050,"r":35,"inner_r":14,"points":5,"color":"#d4956a"},
            {"type":"text","text":"Proudly Obsessed","x":1000,"y":1150,"size":52,"color":"#6b4423","align":"center","font":"gabriola"},
            {"type":"rect","x":600,"y":1270,"w":800,"h":2,"color":"#d4a06a80"},
            {"type":"text","text":"Premium Unisex T-Shirt","x":1000,"y":1320,"size":36,"color":"#8b6040","align":"center","font":"bahnschrift"},
        ]
    }),

    # 4. Instagram Story - Hatton Naturals
    ("story_hatton", {
        "width": 1080, "height": 1920, "background": "#f5f0e8",
        "elements": [
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1920,"color1":"#fdf8f0","color2":"#e8dcc8","direction":"vertical"},
            {"type":"rect","x":60,"y":60,"w":960,"h":1800,"color":"#5d8a5e","opacity":0.04,"radius":30},
            {"type":"text","text":"HATTON","x":540,"y":300,"size":72,"color":"#2d5a2e","align":"center","bold":True,"font":"optimus princeps"},
            {"type":"text","text":"NATURALS","x":540,"y":395,"size":72,"color":"#5d8a5e","align":"center","bold":True,"font":"optimus princeps"},
            {"type":"rect","x":340,"y":500,"w":400,"h":2,"color":"#8fbc8f"},
            {"type":"text","text":"100% Natural","x":540,"y":560,"size":36,"color":"#3d6b3e","align":"center","font":"gabriola"},
            {"type":"ellipse","x":190,"y":700,"w":700,"h":700,"color":"#8fbc8f","opacity":0.08},
            {"type":"text","text":"NUEVO","x":540,"y":800,"size":24,"color":"#ffffff","align":"center","bold":True,"font":"bahnschrift"},
            {"type":"rect","x":460,"y":780,"w":160,"h":38,"color":"#5d8a5e","radius":20},
            {"type":"text","text":"NUEVO","x":540,"y":785,"size":20,"color":"#ffffff","align":"center","bold":True,"font":"bahnschrift"},
            {"type":"text","text":"Aceite Esencial\nde Lavanda","x":540,"y":900,"size":56,"color":"#2d5a2e","align":"center","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Relajacion y bienestar\npara cuerpo y mente","x":540,"y":1100,"size":28,"color":"#5d7a4e","align":"center","font":"segoe ui"},
            {"type":"text","text":"$24.99","x":540,"y":1300,"size":64,"color":"#2d5a2e","align":"center","bold":True,"font":"roboto slab bold"},
            {"type":"text","text":"hattonnaturals.com","x":540,"y":1650,"size":22,"color":"#8a9e6a","align":"center","font":"segoe ui"},
        ]
    }),

    # 5. Real Estate listing
    ("real_estate", {
        "width": 1200, "height": 630, "background": "#0f1923",
        "elements": [
            {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"color1":"#0f1923","color2":"#1a2535","direction":"diagonal"},
            {"type":"rect","x":0,"y":0,"w":5,"h":630,"color":"#c9a227"},
            {"type":"rect","x":0,"y":622,"w":1200,"h":8,"color":"#c9a227"},
            {"type":"text","text":"EXCLUSIVO","x":60,"y":60,"size":15,"color":"#c9a227","bold":True,"font":"bahnschrift"},
            {"type":"text","text":"Casa Moderna\nen Palermo","x":60,"y":100,"size":72,"color":"#ffffff","bold":True,"font":"roboto slab","shadow":True,"shadow_blur":8},
            {"type":"text","text":"4 Hab  |  3 Banos  |  280 m2  |  Jardin","x":60,"y":300,"size":22,"color":"#8090a0","font":"segoe ui"},
            {"type":"rect","x":60,"y":350,"w":180,"h":3,"color":"#c9a227"},
            {"type":"text","text":"USD 385,000","x":60,"y":380,"size":52,"color":"#c9a227","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Premium Properties","x":1050,"y":560,"size":20,"color":"#4a5a6d","align":"right","font":"segoe ui"},
        ]
    }),

    # 6. Church post
    ("iglesia_post", {
        "width": 1080, "height": 1080, "background": "#080808",
        "elements": [
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1080,"color1":"#1a1200","color2":"#080808","direction":"radial"},
            {"type":"text","text":"+","x":540,"y":120,"size":140,"color":"#ffd700","align":"center","font":"times"},
            {"type":"text","text":"DOMINGO 10:00 AM","x":540,"y":300,"size":18,"color":"#ffd700","align":"center","bold":True,"font":"bahnschrift"},
            {"type":"text","text":"La fe mueve\nmontanas","x":540,"y":380,"size":72,"color":"#ffffff","align":"center","font":"optimus princeps","shadow":True,"shadow_blur":15},
            {"type":"text","text":"Mateo 17:20","x":540,"y":600,"size":26,"color":"#ffd700","align":"center","font":"gabriola"},
            {"type":"rect","x":340,"y":680,"w":400,"h":2,"color":"#ffd70040"},
            {"type":"text","text":"Iglesia de la Gracia","x":540,"y":720,"size":28,"color":"#8a7040","align":"center","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Todos son bienvenidos","x":540,"y":790,"size":20,"color":"#5a5040","align":"center","font":"segoe ui"},
        ]
    }),

    # 7. Presentation slide
    ("presentacion", {
        "width": 1920, "height": 1080, "background": "#0c0c18",
        "elements": [
            {"type":"gradient","x":0,"y":0,"w":1920,"h":1080,"color1":"#12122a","color2":"#0c0c18","direction":"horizontal"},
            {"type":"rect","x":0,"y":0,"w":1920,"h":6,"color":"#7c6bf5"},
            {"type":"rect","x":80,"y":80,"w":800,"h":920,"color":"#7c6bf5","opacity":0.04,"radius":20},
            {"type":"text","text":"01","x":120,"y":120,"size":80,"color":"#7c6bf5","font":"impact","opacity":0.3},
            {"type":"text","text":"Transformacion\nDigital","x":120,"y":250,"size":72,"color":"#ffffff","bold":True,"font":"mukta","shadow":True,"shadow_blur":6},
            {"type":"rect","x":120,"y":480,"w":120,"h":3,"color":"#7c6bf5"},
            {"type":"text","text":"Las empresas que adoptan\ntecnologia crecen 3x mas rapido","x":120,"y":520,"size":26,"color":"#8888b0","font":"segoe ui"},
            {"type":"text","text":"3x","x":1400,"y":300,"size":200,"color":"#7c6bf5","align":"center","bold":True,"font":"impact","opacity":0.15},
            {"type":"text","text":"crecimiento","x":1400,"y":520,"size":32,"color":"#7c6bf5","align":"center","font":"segoe ui"},
        ]
    }),
]

print("=" * 60)
print("  GC CANVA - BATCH TEST")
print("=" * 60)

results = []
for name, spec in TESTS:
    t0 = time.time()
    img = generate_from_spec(spec)
    t_gen = time.time() - t0

    t1 = time.time()
    buf, mime, ext = export_image(img, "webp", 92)
    t_exp = time.time() - t1

    data = buf.read()
    fpath = os.path.join(OUT, f"{name}.webp")
    with open(fpath, "wb") as f:
        f.write(data)

    sz_kb = len(data) / 1024
    results.append({
        "name": name,
        "size": f"{img.width}x{img.height}",
        "gen_ms": round(t_gen * 1000),
        "exp_ms": round(t_exp * 1000),
        "file_kb": round(sz_kb, 1),
    })
    print(f"  {name:25s}  {img.width}x{img.height}  gen={t_gen*1000:6.0f}ms  exp={t_exp*1000:5.0f}ms  {sz_kb:6.1f}KB")

print("-" * 60)
avg_gen = sum(r["gen_ms"] for r in results) / len(results)
avg_exp = sum(r["exp_ms"] for r in results) / len(results)
total_kb = sum(r["file_kb"] for r in results)
print(f"  PROMEDIO:  gen={avg_gen:.0f}ms  exp={avg_exp:.0f}ms")
print(f"  TOTAL:     {len(results)} imagenes, {total_kb:.1f}KB")
print(f"  OUTPUT:    {OUT}")
print("=" * 60)
