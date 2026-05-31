"""Stress test - usa TODAS las features del engine."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")

spec = {
    "width":1200,"height":800,"background":"dark",
    "elements":[
        {"type":"gradient","x":0,"y":0,"w":1200,"h":800,"stops":[[0,"#050510"],[0.3,"#0f0a30"],[0.6,"#1a1050"],[1,"#050510"]],"angle":120},
        {"type":"rect","x":0,"y":0,"w":1200,"h":4,"color":"accent"},
        {"type":"rect","x":0,"y":796,"w":1200,"h":4,"color":"accent"},
        {"type":"rect","x":900,"y":50,"w":250,"h":250,"color":"accent","opacity":0.04,"radius":30,"rotate":20},
        {"type":"circle","x":1050,"y":200,"r":120,"color":"gold","opacity":0.03,"shadow":True,"shadow_color":"#c9a22720","shadow_blur":30},
        {"type":"rect","x":50,"y":50,"w":500,"h":700,"color":"#12122a","radius":20,"shadow":True,"shadow_color":"#00000060","shadow_blur":24,"shadow_y":8},
        {"type":"pill","x":80,"y":80,"text":"STRESS TEST","color":"accent","size":11},
        {"type":"text","text":"GC Canva","x":80,"y":130,"size":64,"bold":True,"font":"mukta",
         "text_gradient":{"color1":"#ff6b6b","color2":"#7c6bf5"},"shadow":True,"shadow_blur":10},
        {"type":"text","text":"Motor de imagenes","x":80,"y":220,"size":28,"color":"white","font":"roboto slab","shadow":True,"shadow_blur":6},
        {"type":"text","text":"v3.2","x":80,"y":270,"size":16,"color":"white","font":"consolas","bg_color":"accent","bg_padding":6,"bg_radius":4},
        {"type":"rect","x":80,"y":310,"w":120,"h":3,"color":"accent"},
        {"type":"text","text":"Este motor genera imagenes profesionales de alta calidad usando solo JSON. Soporta 84 fuentes, gradientes multi-stop, sombras, rotacion, y mucho mas.","x":80,"y":340,"size":16,"color":"#8888b0","font":"segoe ui","max_width":420},
        {"type":"star","x":150,"y":560,"r":40,"inner_r":16,"points":5,"color":"gold","shadow":True,"shadow_color":"#c9a22740","shadow_blur":12},
        {"type":"triangle","x":220,"y":530,"w":60,"h":60,"color":"green","opacity":0.6},
        {"type":"polygon","x":340,"y":560,"r":30,"sides":6,"color":"accent","opacity":0.4},
        {"type":"circle","x":420,"y":560,"r":25,"color":"red","opacity":0.5},
        {"type":"text","text":"star","x":150,"y":610,"size":11,"color":"#666","align":"center","font":"consolas"},
        {"type":"text","text":"tri","x":250,"y":610,"size":11,"color":"#666","align":"center","font":"consolas"},
        {"type":"text","text":"hex","x":340,"y":610,"size":11,"color":"#666","align":"center","font":"consolas"},
        {"type":"text","text":"circle","x":420,"y":610,"size":11,"color":"#666","align":"center","font":"consolas"},
        {"type":"rect","x":620,"y":100,"w":250,"h":130,"color":"#14142a","radius":14,"shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":6},
        {"type":"pill","x":640,"y":116,"text":"FUENTES","color":"green","size":10},
        {"type":"text","text":"84","x":640,"y":150,"size":52,"color":"green","bold":True,"font":"impact"},
        {"type":"rect","x":900,"y":100,"w":250,"h":130,"color":"#14142a","radius":14,"shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":6},
        {"type":"pill","x":920,"y":116,"text":"ICONOS","color":"orange","size":10},
        {"type":"text","text":"80+","x":920,"y":150,"size":52,"color":"orange","bold":True,"font":"impact"},
        {"type":"rect","x":620,"y":260,"w":250,"h":130,"color":"#14142a","radius":14,"shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":6},
        {"type":"pill","x":640,"y":276,"text":"PRESETS","color":"blue","size":10},
        {"type":"text","text":"32","x":640,"y":310,"size":52,"color":"blue","bold":True,"font":"impact"},
        {"type":"rect","x":900,"y":260,"w":250,"h":130,"color":"#14142a","radius":14,"shadow":True,"shadow_color":"#00000050","shadow_blur":16,"shadow_y":6},
        {"type":"pill","x":920,"y":276,"text":"TEMPLATES","color":"purple","size":10},
        {"type":"text","text":"12","x":920,"y":310,"size":52,"color":"purple","bold":True,"font":"impact"},
        {"type":"gradient","x":620,"y":440,"w":160,"h":80,"color1":"red","color2":"orange","direction":"horizontal"},
        {"type":"gradient","x":800,"y":440,"w":160,"h":80,"stops":[[0,"cyan"],[0.5,"blue"],[1,"purple"]],"direction":"horizontal"},
        {"type":"gradient","x":980,"y":440,"w":160,"h":80,"stops":[[0,"green"],[0.5,"yellow"],[1,"red"]],"angle":45},
        {"type":"text","text":"RAINBOW","x":860,"y":560,"size":48,"align":"center","bold":True,"font":"impact",
         "text_gradient":{"stops":[[0,"#ff0000"],[0.17,"#ff8800"],[0.33,"#ffff00"],[0.5,"#00ff00"],[0.67,"#0088ff"],[0.83,"#8800ff"],[1,"#ff00ff"]]}},
        {"type":"text","text":"valign: center","x":860,"y":650,"size":14,"color":"#666","align":"center","valign":"center","font":"consolas"},
        {"type":"line","x1":50,"y1":750,"x2":1150,"y2":750,"color":"#333","width":1},
        {"type":"text","text":"github.com/gcaroprese/gc_canva","x":80,"y":760,"size":13,"color":"#5a5a80","font":"consolas"},
        {"type":"text","text":"WebP q92 | Pillow","x":1120,"y":760,"size":13,"color":"#5a5a80","align":"right","font":"consolas"},
    ]
}

t0 = time.time()
img = generate_from_spec(spec)
dt = time.time() - t0
buf, _, _ = export_image(img, "webp", 92)
data = buf.read()
path = os.path.join(OUT, "stress_test.webp")
with open(path, "wb") as f:
    f.write(data)
print(f"Gen: {dt*1000:.0f}ms | Size: {len(data)/1024:.1f}KB | Elements: {len(spec['elements'])}")
