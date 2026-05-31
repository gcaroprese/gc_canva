"""Test de imagenes de produccion para los sitios del usuario."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

specs = {
    "inforket_hero": {
        "width":1440,"height":500,"background":"dark",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1440,"h":500,"stops":[[0,"#0a0518"],[0.5,"#1e1b4b"],[1,"#0a0518"]],"direction":"horizontal"},
            {"type":"rect","x":0,"y":0,"w":1440,"h":3,"color":"accent"},
            {"type":"circle","x":1200,"y":250,"r":200,"color":"accent","opacity":0.04},
            {"type":"circle","x":1200,"y":250,"r":120,"color":"accent","opacity":0.06},
            {"type":"pill","x":80,"y":80,"text":"MARKETING DIGITAL","color":"accent","size":13},
            {"type":"text","text":"Estrategias que\ngeneran resultados","x":80,"y":140,"size":62,"color":"white","bold":True,"font":"mukta","shadow":True,"shadow_blur":10,"shadow_color":"#7c6bf530"},
            {"type":"rect","x":80,"y":330,"w":100,"h":3,"color":"accent"},
            {"type":"text","text":"SEO  |  Contenido  |  Redes Sociales  |  Email","x":80,"y":360,"size":18,"color":"#8888b0","font":"segoe ui"},
            {"type":"rect","x":80,"y":410,"w":180,"h":44,"color":"accent","radius":22},
            {"type":"text","text":"Empezar","x":170,"y":420,"size":16,"color":"white","align":"center","bold":True,"font":"segoe ui"},
            {"type":"text","text":"inforket.com","x":80,"y":465,"size":13,"color":"#5a5a80","font":"consolas"},
        ]
    },
    "pawsitive_story": {
        "width":1080,"height":1920,"background":"#1a0d08",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1080,"h":1920,"stops":[[0,"#2a1508"],[0.3,"#1a0d08"],[0.7,"#1a0d08"],[1,"#2a1508"]],"direction":"vertical"},
            {"type":"ellipse","x":90,"y":400,"w":900,"h":900,"color":"#8b4513","opacity":0.08},
            {"type":"text","text":"PAWSITIVE","x":540,"y":500,"size":96,"color":"#d4a574","align":"center","bold":True,"font":"cooper black","shadow":True,"shadow_blur":15},
            {"type":"text","text":"BREWS","x":540,"y":630,"size":96,"color":"#ff9a3c","align":"center","bold":True,"font":"cooper black"},
            {"type":"rect","x":340,"y":780,"w":400,"h":2,"color":"#8b4513"},
            {"type":"text","text":"Cafe Artesanal","x":540,"y":830,"size":36,"color":"#c8956c","align":"center","font":"roboto slab"},
            {"type":"pill","x":540,"y":1000,"text":"PROMO DEL MES","color":"#d4956a","align":"center","size":16},
            {"type":"text","text":"2x1","x":540,"y":1100,"size":140,"color":"white","align":"center","bold":True,"font":"impact","shadow":True,"shadow_blur":20,"shadow_color":"#d4956a60"},
            {"type":"text","text":"en todos los lattes","x":540,"y":1280,"size":28,"color":"#c8956c","align":"center","font":"segoe ui"},
            {"type":"text","text":"pawsitivebrews.com","x":540,"y":1700,"size":18,"color":"#5a3020","align":"center","font":"consolas"},
        ]
    },
    "hatton_etsy": {
        "width":2000,"height":2000,"background":"#f5f0e8",
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":2000,"h":2000,"stops":[[0,"#fdf8f0"],[0.5,"#f0e8d8"],[1,"#e8dcc8"]],"direction":"radial"},
            {"type":"ellipse","x":300,"y":300,"w":1400,"h":1400,"color":"#8fbc8f","opacity":0.06},
            {"type":"rect","x":150,"y":150,"w":1700,"h":1700,"color":"#5d8a5e","opacity":0.03,"radius":40},
            {"type":"text","text":"HATTON","x":1000,"y":400,"size":120,"color":"#2d5a2e","align":"center","bold":True,"font":"optimus princeps"},
            {"type":"text","text":"NATURALS","x":1000,"y":560,"size":120,"color":"#5d8a5e","align":"center","bold":True,"font":"optimus princeps"},
            {"type":"rect","x":600,"y":720,"w":800,"h":3,"color":"#8fbc8f"},
            {"type":"text","text":"Pure  |  Natural  |  Authentic","x":1000,"y":780,"size":48,"color":"#5d8a5e","align":"center","font":"gabriola"},
            {"type":"text","text":"Organic Lavender\nEssential Oil","x":1000,"y":920,"size":72,"color":"#2d5a2e","align":"center","bold":True,"font":"roboto slab"},
            {"type":"pill","x":1000,"y":1130,"text":"100% ORGANIC","color":"#5d8a5e","align":"center","size":18,"py":12,"px":24},
            {"type":"text","text":"10ml | Cold Pressed | Vegan","x":1000,"y":1260,"size":28,"color":"#6b8a5e","align":"center","font":"segoe ui"},
            {"type":"text","text":"$18.99","x":1000,"y":1400,"size":80,"color":"#2d5a2e","align":"center","bold":True,"font":"roboto slab bold"},
            {"type":"text","text":"hattonnaturals.com","x":1000,"y":1650,"size":24,"color":"#8a9e6a","align":"center","font":"consolas"},
        ]
    },
}

print("=" * 60)
print("  PRODUCTION TEST")
print("=" * 60)
for name, spec in specs.items():
    t0 = time.time()
    img = generate_from_spec(spec)
    dt = time.time() - t0
    buf, _, _ = export_image(img, "webp", 92)
    data = buf.read()
    path = os.path.join(OUT, f"{name}.webp")
    with open(path, "wb") as f:
        f.write(data)
    print(f"  {name:20s} {img.width}x{img.height}  {dt*1000:5.0f}ms  {len(data)/1024:5.1f}KB")
print("=" * 60)
