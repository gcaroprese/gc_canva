"""Imagen de produccion final para inforket.com"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")

spec = {
    "width":1200,"height":630,"background":"dark",
    "elements":[
        {"type":"gradient","x":0,"y":0,"w":1200,"h":630,
         "stops":[[0,"#03030a"],[0.3,"#0d0a25"],[0.6,"#1a1450"],[1,"#03030a"]],"angle":140},
        {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"accent"},
        {"type":"rect","x":0,"y":627,"w":1200,"h":3,"color":"#7c6bf530"},
        {"type":"repeat","count":3,"dx":0,"dy":0,"d_scale":50,"d_opacity":-0.015,
         "element":{"type":"circle","x":950,"y":315,"r":80,"color":"accent","opacity":0.05}},
        {"type":"rect","x":40,"y":35,"w":580,"h":560,"color":"#7c6bf5","opacity":0.03,"radius":24},
        {"type":"pill","x":65,"y":60,"text":"MARKETING DIGITAL","color":"accent","size":12,"py":8,"px":16},
        {"type":"text","text":"Como Triplicar\ntu Trafico\nOrganico","x":65,"y":110,"size":62,"bold":True,"font":"mukta",
         "text_gradient":{"color1":"#ffffff","color2":"#c4b5fd"},
         "shadow":True,"shadow_blur":12,"shadow_color":"#7c6bf520"},
        {"type":"divider","x":65,"y":370,"w":250,"color":"accent","thickness":2},
        {"type":"text","text":"Guia paso a paso con estrategias\nprobadas para 2026","x":65,"y":400,"size":18,"color":"#8888b0","font":"segoe ui","line_spacing":6},
        {"type":"rect","x":65,"y":480,"w":200,"h":48,"color":"accent","radius":24,
         "shadow":True,"shadow_color":"#7c6bf550","shadow_blur":20,"shadow_y":4},
        {"type":"text","text":"Leer Articulo","x":165,"y":492,"size":15,"color":"white","align":"center","bold":True,"font":"segoe ui"},
        {"type":"text","text":"inforket.com","x":65,"y":555,"size":14,"color":"#4a4a6a","font":"consolas"},
        {"type":"rect","x":670,"y":60,"w":240,"h":130,"color":"#0d0d20","radius":16,
         "shadow":True,"shadow_color":"#00000060","shadow_blur":18,"shadow_y":6},
        {"type":"pill","x":690,"y":78,"text":"TRAFICO","color":"green","size":10},
        {"type":"text","text":"+340%","x":690,"y":115,"size":48,"color":"green","bold":True,"font":"impact"},
        {"type":"rect","x":935,"y":60,"w":220,"h":130,"color":"#0d0d20","radius":16,
         "shadow":True,"shadow_color":"#00000060","shadow_blur":18,"shadow_y":6},
        {"type":"pill","x":955,"y":78,"text":"LEADS","color":"gold","size":10},
        {"type":"text","text":"2.4K","x":955,"y":115,"size":48,"color":"gold","bold":True,"font":"impact"},
        {"type":"rect","x":670,"y":220,"w":485,"h":220,"color":"#0d0d20","radius":16,
         "shadow":True,"shadow_color":"#00000060","shadow_blur":18,"shadow_y":6},
        {"type":"text","text":"Crecimiento Mensual","x":695,"y":240,"size":13,"color":"#5a5a80","font":"segoe ui"},
        {"type":"rect","x":700,"y":370,"w":36,"h":50,"color":"#7c6bf530","radius":3},
        {"type":"rect","x":750,"y":340,"w":36,"h":80,"color":"#7c6bf540","radius":3},
        {"type":"rect","x":800,"y":355,"w":36,"h":65,"color":"#7c6bf545","radius":3},
        {"type":"rect","x":850,"y":320,"w":36,"h":100,"color":"#7c6bf550","radius":3},
        {"type":"rect","x":900,"y":300,"w":36,"h":120,"color":"#7c6bf560","radius":3},
        {"type":"rect","x":950,"y":330,"w":36,"h":90,"color":"#7c6bf570","radius":3},
        {"type":"rect","x":1000,"y":290,"w":36,"h":130,"color":"#7c6bf580","radius":3},
        {"type":"rect","x":1050,"y":270,"w":36,"h":150,"color":"accent","radius":3},
        {"type":"rect","x":1100,"y":280,"w":36,"h":140,"color":"green","radius":3},
        {"type":"text","text":"E  F  M  A  M  J  J  A  S","x":700,"y":425,"size":10,"color":"#4a4a6a","font":"consolas"},
        {"type":"rect","x":670,"y":470,"w":485,"h":120,"color":"#0d0d20","radius":16,
         "shadow":True,"shadow_color":"#00000060","shadow_blur":18,"shadow_y":6},
        {"type":"text","text":"Top Keywords","x":695,"y":490,"size":13,"color":"#5a5a80","font":"segoe ui"},
        {"type":"text","text":"SEO","x":695,"y":520,"size":13,"color":"white","font":"segoe ui","bg_color":"#7c6bf530","bg_padding":6,"bg_radius":4},
        {"type":"text","text":"Marketing","x":750,"y":520,"size":13,"color":"white","font":"segoe ui","bg_color":"#22c55e30","bg_padding":6,"bg_radius":4},
        {"type":"text","text":"Contenido","x":850,"y":520,"size":13,"color":"white","font":"segoe ui","bg_color":"#f59e0b30","bg_padding":6,"bg_radius":4},
        {"type":"text","text":"Growth","x":950,"y":520,"size":13,"color":"white","font":"segoe ui","bg_color":"#ef444430","bg_padding":6,"bg_radius":4},
        {"type":"text","text":"Analytics","x":695,"y":555,"size":13,"color":"white","font":"segoe ui","bg_color":"#06b6d430","bg_padding":6,"bg_radius":4},
        {"type":"text","text":"Conversion","x":795,"y":555,"size":13,"color":"white","font":"segoe ui","bg_color":"#a855f730","bg_padding":6,"bg_radius":4},
    ]
}

img = generate_from_spec(spec)
for fmt in ["webp", "png"]:
    buf, _, ext = export_image(img, fmt, 92)
    data = buf.read()
    path = os.path.join(OUT, f"inforket_final.{ext}")
    with open(path, "wb") as f:
        f.write(data)
    print(f"  {ext}: {len(data)/1024:.1f}KB")
print("  OK")
