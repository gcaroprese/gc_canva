"""Inforket.com - imagen OG con todas las features v3.6"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")

spec = {
    "width":1200,"height":630,"background":"dark",
    "elements":[
        # Fondo multi-stop + angle
        {"type":"gradient","x":0,"y":0,"w":1200,"h":630,
         "stops":[[0,"#02020a"],[0.25,"#0a0825"],[0.5,"#161245"],[0.75,"#0a0825"],[1,"#02020a"]],
         "angle":140},
        {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"accent"},
        {"type":"rect","x":0,"y":627,"w":1200,"h":3,"color":"#7c6bf520"},

        # Glow circles decorativos
        {"type":"repeat","count":3,"dx":0,"dy":0,"d_scale":60,"d_opacity":-0.012,
         "element":{"type":"circle","x":1000,"y":315,"r":60,"color":"accent","opacity":0.04}},

        # Glass card
        {"type":"rect","x":35,"y":30,"w":600,"h":570,"color":"#7c6bf5","opacity":0.025,"radius":24},

        # Categoria con letter spacing
        {"type":"text","text":"marketing digital","x":65,"y":55,"size":12,"color":"accent","font":"consolas",
         "uppercase":True,"letter_spacing":6},

        # Titulo con gradient text
        {"type":"text","text":"Guia SEO\n2026","x":65,"y":95,"size":82,"bold":True,"font":"mukta",
         "text_gradient":{"color1":"#ffffff","color2":"#b4a5fd"},
         "shadow":True,"shadow_blur":14,"shadow_color":"#7c6bf518"},

        # Subtitulo
        {"type":"text","text":"Estrategias probadas para\ntriplicar tu trafico organico","x":65,"y":340,"size":22,"color":"#8888b0","font":"segoe ui","line_spacing":8},

        # Divider
        {"type":"divider","x":65,"y":430,"w":200,"color":"accent","thickness":2},

        # Tags con bg_color
        {"type":"text","text":"SEO","x":65,"y":455,"size":14,"color":"white","font":"segoe ui","bg_color":"#7c6bf535","bg_padding":7,"bg_radius":5},
        {"type":"text","text":"Contenido","x":120,"y":455,"size":14,"color":"white","font":"segoe ui","bg_color":"#22c55e30","bg_padding":7,"bg_radius":5},
        {"type":"text","text":"Growth","x":225,"y":455,"size":14,"color":"white","font":"segoe ui","bg_color":"#f59e0b30","bg_padding":7,"bg_radius":5},

        # CTA con glow
        {"type":"rect","x":65,"y":510,"w":210,"h":48,"color":"accent","radius":24,
         "shadow":True,"shadow_color":"#7c6bf560","shadow_blur":18,"shadow_y":4},
        {"type":"text","text":"Leer Guia Completa","x":170,"y":522,"size":14,"color":"white","align":"center","bold":True,"font":"segoe ui"},

        # URL
        {"type":"text","text":"inforket.com","x":65,"y":580,"size":13,"color":"#3a3a5a","font":"consolas"},

        # Dashboard derecho
        # Metric 1
        {"type":"rect","x":690,"y":55,"w":230,"h":125,"color":"#0a0a1a","radius":14,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":5},
        {"type":"pill","x":710,"y":72,"text":"TRAFICO","color":"green","size":9},
        {"type":"text","text":"+340%","x":710,"y":105,"size":50,"color":"green","bold":True,"font":"impact"},

        # Metric 2
        {"type":"rect","x":940,"y":55,"w":220,"h":125,"color":"#0a0a1a","radius":14,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":5},
        {"type":"pill","x":960,"y":72,"text":"LEADS","color":"gold","size":9},
        {"type":"text","text":"2.4K","x":960,"y":105,"size":50,"color":"gold","bold":True,"font":"impact"},

        # Chart card
        {"type":"rect","x":690,"y":200,"w":470,"h":230,"color":"#0a0a1a","radius":14,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":5},
        {"type":"text","text":"CRECIMIENTO MENSUAL","x":715,"y":220,"size":11,"color":"#4a4a6a","font":"consolas",
         "letter_spacing":3,"uppercase":True},

        # Barras del chart
        {"type":"rect","x":720,"y":370,"w":34,"h":40,"color":"#7c6bf525","radius":3},
        {"type":"rect","x":766,"y":345,"w":34,"h":65,"color":"#7c6bf535","radius":3},
        {"type":"rect","x":812,"y":355,"w":34,"h":55,"color":"#7c6bf540","radius":3},
        {"type":"rect","x":858,"y":325,"w":34,"h":85,"color":"#7c6bf550","radius":3},
        {"type":"rect","x":904,"y":310,"w":34,"h":100,"color":"#7c6bf560","radius":3},
        {"type":"rect","x":950,"y":330,"w":34,"h":80,"color":"#7c6bf570","radius":3},
        {"type":"rect","x":996,"y":300,"w":34,"h":110,"color":"#7c6bf580","radius":3},
        {"type":"rect","x":1042,"y":280,"w":34,"h":130,"color":"accent","radius":3},
        {"type":"rect","x":1088,"y":290,"w":34,"h":120,"color":"green","radius":3},

        # Keywords card
        {"type":"rect","x":690,"y":450,"w":470,"h":140,"color":"#0a0a1a","radius":14,
         "shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":5},
        {"type":"text","text":"TOP KEYWORDS","x":715,"y":470,"size":11,"color":"#4a4a6a","font":"consolas",
         "letter_spacing":3,"uppercase":True},

        {"type":"pill","x":715,"y":500,"text":"SEO","color":"accent","size":11,"outline":True},
        {"type":"pill","x":775,"y":500,"text":"Marketing","color":"green","size":11,"outline":True},
        {"type":"pill","x":880,"y":500,"text":"Analytics","color":"gold","size":11,"outline":True},
        {"type":"pill","x":985,"y":500,"text":"Growth","color":"red","size":11,"outline":True},
        {"type":"pill","x":715,"y":540,"text":"Conversion","color":"cyan","size":11,"outline":True},
        {"type":"pill","x":835,"y":540,"text":"Content","color":"purple","size":11,"outline":True},
    ]
}

img = generate_from_spec(spec)
buf, _, _ = export_image(img, "webp", 92)
data = buf.read()
with open(os.path.join(OUT, "inforket_v2.webp"), "wb") as f:
    f.write(data)
print(f"OK: {len(data)/1024:.1f}KB")
