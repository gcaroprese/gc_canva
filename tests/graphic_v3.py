"""Composiciones graficas SIN TEXTO con assets de calidad."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

# Pawsitive Brews - solo grafica, 1200x675
pw = {
    "width":1200,"height":675,"background":"#0a0806",
    "elements":[
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#1e1610"],[0.4,"#120e08"],[0.8,"#060402"]],"direction":"radial"},
        {"type":"rect","x":0,"y":0,"w":1200,"h":4,"color":"#c8956c"},
        {"type":"circle","x":380,"y":340,"r":300,"color":"#d4956a","opacity":0.04},
        {"type":"circle","x":380,"y":340,"r":180,"color":"#d4956a","opacity":0.05},
        # Perro border collie completo - protagonista derecha
        {"type":"image","src":os.path.join(A,"dog_happy2_png.webp"),"x":620,"y":30,"w":560,"h":640},
        # Taza de te izquierda
        {"type":"image","src":os.path.join(A,"cup_tea_png.webp"),"x":120,"y":150,"w":360,"h":400},
        # Burbujas doradas
        {"type":"circle","x":250,"y":100,"r":18,"color":"#d4a574","opacity":0.12},
        {"type":"circle","x":380,"y":60,"r":11,"color":"#d4a574","opacity":0.1},
        {"type":"circle","x":160,"y":200,"r":7,"color":"#ffd700","opacity":0.08},
        {"type":"circle","x":520,"y":120,"r":13,"color":"#c8956c","opacity":0.07},
        {"type":"star","x":560,"y":50,"r":9,"inner_r":3,"points":4,"color":"#ffd700","opacity":0.12},
        {"type":"star","x":100,"y":590,"r":7,"inner_r":2,"points":4,"color":"#ffd700","opacity":0.08},
        {"type":"rect","x":0,"y":671,"w":1200,"h":4,"color":"#c8956c30"},
    ]
}

# Inforket - solo grafica, 1200x675
ink = {
    "width":1200,"height":675,"background":"#050510",
    "elements":[
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#03030a"],[0.3,"#0a0825"],[0.6,"#141050"],[1,"#03030a"]],"angle":140},
        {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"accent"},
        {"type":"circle","x":480,"y":380,"r":280,"color":"accent","opacity":0.04},
        {"type":"circle","x":480,"y":380,"r":160,"color":"accent","opacity":0.05},
        # Macbook con dashboard dentro
        {"type":"image","src":os.path.join(A,"macbook_png.webp"),"x":80,"y":80,"w":850,"h":458},
        # Dashboard dentro de la pantalla
        {"type":"rect","x":220,"y":120,"w":570,"h":360,"color":"#0d0d20"},
        # Barras
        {"type":"rect","x":250,"y":380,"w":28,"h":50,"color":"#7c6bf530","radius":2},
        {"type":"rect","x":288,"y":360,"w":28,"h":70,"color":"#7c6bf540","radius":2},
        {"type":"rect","x":326,"y":335,"w":28,"h":95,"color":"#7c6bf555","radius":2},
        {"type":"rect","x":364,"y":305,"w":28,"h":125,"color":"#7c6bf570","radius":2},
        {"type":"rect","x":402,"y":280,"w":28,"h":150,"color":"#7c6bf585","radius":2},
        {"type":"rect","x":440,"y":260,"w":28,"h":170,"color":"accent","radius":2},
        {"type":"rect","x":478,"y":270,"w":28,"h":160,"color":"green","radius":2},
        # Donut
        {"type":"ring","x":650,"y":310,"r":60,"thickness":14,"color":"accent","start":0,"end":220},
        {"type":"ring","x":650,"y":310,"r":60,"thickness":14,"color":"green","start":220,"end":310},
        {"type":"ring","x":650,"y":310,"r":60,"thickness":14,"color":"gold","start":310,"end":360},
        # Trend line
        {"type":"line","x1":250,"y1":390,"x2":510,"y2":270,"color":"#22c55e40","width":2},
        # Tablet derecha
        {"type":"image","src":os.path.join(A,"tablet_png.webp"),"x":920,"y":170,"w":270,"h":200},
        {"type":"rect","x":947,"y":193,"w":215,"h":148,"color":"#0d0d20"},
        {"type":"rect","x":965,"y":295,"w":14,"h":35,"color":"#7c6bf560","radius":2},
        {"type":"rect","x":988,"y":280,"w":14,"h":50,"color":"#7c6bf580","radius":2},
        {"type":"rect","x":1011,"y":268,"w":14,"h":62,"color":"accent","radius":2},
        {"type":"rect","x":1034,"y":285,"w":14,"h":45,"color":"green","radius":2},
        # Scatter dots
        {"type":"circle","x":100,"y":580,"r":5,"color":"accent","opacity":0.5},
        {"type":"circle","x":140,"y":560,"r":7,"color":"accent","opacity":0.4},
        {"type":"circle","x":185,"y":540,"r":9,"color":"green","opacity":0.5},
        {"type":"circle","x":235,"y":550,"r":6,"color":"accent","opacity":0.3},
        {"type":"circle","x":280,"y":520,"r":11,"color":"green","opacity":0.6,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":8},
        {"type":"ring","x":1100,"y":80,"r":30,"thickness":2,"color":"#7c6bf520"},
        {"type":"rect","x":0,"y":672,"w":1200,"h":3,"color":"#7c6bf530"},
    ]
}

# Test pills
pill_test = {
    "width":800,"height":200,"background":"dark",
    "elements":[
        {"type":"gradient","x":0,"y":0,"w":800,"h":200,"color1":"#0a0825","color2":"dark","direction":"diagonal"},
        {"type":"pill","x":40,"y":40,"text":"ORGANIC TEA","color":"#5d8a5e","size":16,"py":10,"px":24},
        {"type":"pill","x":250,"y":40,"text":"SEO 2026","color":"accent","size":16,"py":10,"px":24},
        {"type":"pill","x":430,"y":40,"text":"BLOG POST","color":"red","size":16,"py":10,"px":24},
        {"type":"pill","x":40,"y":110,"text":"OUTLINED","color":"green","size":16,"py":10,"px":24,"outline":True},
        {"type":"pill","x":250,"y":110,"text":"MARKETING","color":"gold","size":16,"py":10,"px":24,"outline":True},
        {"type":"pill","x":480,"y":110,"text":"SMALL","color":"accent","size":12,"py":7,"px":16},
        {"type":"pill","x":580,"y":110,"text":"LARGE","color":"accent","size":20,"py":12,"px":28},
    ]
}

for name, spec in [("pawsitive_g3", pw), ("inforket_g3", ink), ("pill_test", pill_test)]:
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    with open(os.path.join(OUT, f"{name}.webp"), "wb") as f:
        f.write(d)
    print(f"  {name}: {len(d)//1024}KB")
