"""
Featured images para blog posts - FOTO protagonista, poco texto.
La foto tiene que verse, no estar tapada por un overlay negro.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output", "blog")
os.makedirs(OUT, exist_ok=True)
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

specs = {
    # ─── INFORKET: foto de codigo visible + titulo en franja ───
    "inforket_seo": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"grain":True,"grain_strength":3},
        "elements":[
            # Foto de codigo VISIBLE - protagonista
            {"type":"image","src":os.path.join(A,"coding_screen2.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.75},
            # Franja inferior para texto (no cubre toda la foto)
            {"type":"gradient","x":0,"y":400,"w":1200,"h":275,
             "color1":"#0a0a1400","color2":"#0a0a14EE","direction":"vertical"},
            {"type":"rect","x":0,"y":580,"w":1200,"h":95,"color":"#0a0a14DD"},
            # Titulo sobre la franja
            {"type":"text","text":"10 Estrategias SEO que Funcionan en 2026","x":60,"y":595,
             "size":36,"color":"#ffffff","bold":True,"font":"mukta","shadow":True,"shadow_blur":6,"max_width":900},
            # Pill + brand
            {"type":"pill","x":60,"y":560,"text":"SEO","color":"#7c6bf5","size":11},
            {"type":"text","text":"inforket.com","x":1140,"y":640,"size":14,"color":"#7c6bf5","align":"right","font":"consolas"},
        ]
    },

    # ─── INFORKET: analytics screen visible ───
    "inforket_analytics": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"grain":True,"grain_strength":3},
        "elements":[
            # Foto analytics VISIBLE
            {"type":"image","src":os.path.join(A,"analytics_screen.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.8},
            # Franja inferior sutil
            {"type":"gradient","x":0,"y":450,"w":1200,"h":225,
             "color1":"#00000000","color2":"#000000DD","direction":"vertical"},
            {"type":"text","text":"Como Triplicar tu Trafico Organico","x":60,"y":590,
             "size":38,"color":"#ffffff","bold":True,"font":"mukta","shadow":True,"shadow_blur":8,"max_width":900},
            {"type":"pill","x":60,"y":555,"text":"MARKETING","color":"#22c55e","size":11},
            {"type":"text","text":"inforket.com","x":1140,"y":640,"size":14,"color":"#22c55e","align":"right","font":"consolas"},
        ]
    },

    # ─── PAWSITIVE: te verde protagonista + perro ───
    "pawsitive_tea": {
        "width":1200,"height":675,"background":"#0a100a","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.25,"tint":"#8fbc8f","tint_strength":0.03,"grain":True,"grain_strength":3},
        "elements":[
            # Fondo oscuro verde
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
             "stops":[[0,"#141e14"],[0.5,"#0c140c"],[1,"#060a06"]],"direction":"radial"},
            # Glow verde calido
            {"type":"circle","x":500,"y":340,"r":350,"color":"#8fbc8f","opacity":0.04},
            # Superficie
            {"type":"gradient","x":0,"y":440,"w":1200,"h":235,"color1":"#0c100c","color2":"#060a06","direction":"vertical"},
            # Sombra de contacto del vaso
            {"type":"contact_shadow","x":250,"y":480,"w":350,"h":20,"color":"#00000060","blur":18},
            # Vaso de te GRANDE y protagonista
            {"type":"image","src":os.path.join(A,"green_tea_nobg.webp"),"x":220,"y":20,"w":500,"h":470},
            # Perro a la derecha
            {"type":"image","src":os.path.join(A,"dog_beagle_png.webp"),"x":720,"y":40,"w":400,"h":580},
            # Sombra de contacto perro
            {"type":"contact_shadow","x":750,"y":570,"w":340,"h":18,"color":"#00000050","blur":15},
            # Solo marca minima abajo
            {"type":"rect","x":0,"y":640,"w":1200,"h":35,"color":"#0a100aCC"},
            {"type":"text","text":"pawsitivebrews.com","x":600,"y":648,"size":14,"color":"#8fbc8f80","align":"center","font":"consolas"},
        ]
    },

    # ─── PAWSITIVE: foto de te herbs como fondo VISIBLE ───
    "pawsitive_blog": {
        "width":1200,"height":675,"background":"#0a100a","antialias":2,
        "post":{"grain":True,"grain_strength":3},
        "elements":[
            # Foto de te como fondo VISIBLE (0.7 opacity, no 0.25)
            {"type":"image","src":os.path.join(A,"tea_dark_bg.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.7},
            # Solo franja inferior para texto
            {"type":"gradient","x":0,"y":420,"w":1200,"h":255,
             "color1":"#00000000","color2":"#000000DD","direction":"vertical"},
            {"type":"text","text":"5 Organic Teas Your Dog Will Love","x":60,"y":585,
             "size":36,"color":"#ffffff","bold":True,"font":"roboto slab","shadow":True,"shadow_blur":8,"max_width":900},
            {"type":"pill","x":60,"y":550,"text":"ORGANIC TEA","color":"#5d8a5e","size":11},
            {"type":"text","text":"pawsitivebrews.com","x":1140,"y":640,"size":14,"color":"#8fbc8f","align":"right","font":"consolas"},
        ]
    },

    # ─── GABRIEL: sin foto, pero con visual interesante ───
    "gabriel_brand": {
        "width":1200,"height":675,"background":"dark","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.3,"grain":True,"grain_strength":4},
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
             "stops":[[0,"#0a0810"],[0.3,"#14102a"],[0.6,"#0a0810"]],"angle":135},
            # Circulos decorativos grandes (visual interest)
            {"type":"circle","x":900,"y":200,"r":300,"color":"#c9a227","opacity":0.04},
            {"type":"circle","x":900,"y":200,"r":180,"color":"#c9a227","opacity":0.06},
            {"type":"circle","x":900,"y":200,"r":80,"color":"#c9a227","opacity":0.08},
            # Lineas decorativas
            {"type":"rect","x":800,"y":100,"w":2,"h":400,"color":"#c9a22720"},
            {"type":"rect","x":850,"y":150,"w":2,"h":300,"color":"#c9a22715"},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#c9a227"},
            # Contenido izquierda
            {"type":"text","text":"Gabriel","x":80,"y":200,"size":72,"color":"#ffffff","bold":True,"font":"roboto slab"},
            {"type":"text","text":"Caroprese","x":80,"y":290,"size":72,"color":"#c9a227","bold":True,"font":"roboto slab"},
            {"type":"rect","x":80,"y":390,"w":100,"h":3,"color":"#c9a227"},
            {"type":"text","text":"Diseno Digital y Marketing Creativo","x":80,"y":420,"size":22,"color":"#8888a0","font":"segoe ui"},
            {"type":"text","text":"gabrielcaroprese.com","x":80,"y":610,"size":14,"color":"#5a5070","font":"consolas"},
        ]
    },

    # ─── REAL ESTATE: foto de casa VISIBLE ───
    "realestate_listing": {
        "width":1200,"height":675,"background":"#0f1923","antialias":2,
        "post":{"grain":True,"grain_strength":3},
        "elements":[
            # Casa VISIBLE como protagonista
            {"type":"image","src":os.path.join(A,"house_full.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.7},
            # Franja inferior
            {"type":"gradient","x":0,"y":400,"w":1200,"h":275,
             "color1":"#0f192300","color2":"#0f1923EE","direction":"vertical"},
            {"type":"rect","x":0,"y":0,"w":5,"h":675,"color":"#c9a227"},
            {"type":"pill","x":30,"y":560,"text":"EXCLUSIVO","color":"#c9a227","size":12,"text_color":"#0f1923"},
            {"type":"text","text":"Departamento Premium en Palermo","x":30,"y":590,
             "size":34,"color":"#ffffff","bold":True,"font":"roboto slab","shadow":True,"shadow_blur":6,"max_width":800},
            {"type":"text","text":"3 Amb | 95m2 | USD 245,000","x":30,"y":640,"size":18,"color":"#c9a227","font":"segoe ui"},
        ]
    },
}

print("=" * 55)
for name, spec in specs.items():
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    with open(os.path.join(OUT, f"{name}.webp"), "wb") as f:
        f.write(d)
    print(f"  {name:25s} {len(d)//1024:4d}KB")
print("=" * 55)
