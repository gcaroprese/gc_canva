"""Test v3.6: AA stars, letter-spacing, pill outline, uppercase"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")

spec = {
    "width":1200,"height":500,"background":"dark",
    "elements":[
        {"type":"gradient","x":0,"y":0,"w":1200,"h":500,"stops":[[0,"#050510"],[0.5,"#12103a"],[1,"#050510"]],"angle":135},
        {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"accent"},

        # Letter spacing test
        {"type":"text","text":"LETTER SPACING","x":100,"y":40,"size":48,"color":"white","bold":True,"font":"bahnschrift","letter_spacing":12},
        {"type":"text","text":"Normal spacing","x":100,"y":110,"size":32,"color":"#888","font":"segoe ui","letter_spacing":0},
        {"type":"text","text":"Wide spacing","x":100,"y":160,"size":32,"color":"#888","font":"segoe ui","letter_spacing":8},

        # Uppercase auto
        {"type":"text","text":"auto uppercase test","x":100,"y":220,"size":20,"color":"accent","font":"bahnschrift","uppercase":True,"letter_spacing":4},

        # Anti-aliased stars (comparar)
        {"type":"star","x":800,"y":120,"r":80,"inner_r":32,"points":5,"color":"gold"},
        {"type":"text","text":"AA Star","x":800,"y":210,"size":13,"color":"#666","align":"center","font":"consolas"},

        {"type":"star","x":1000,"y":120,"r":80,"inner_r":32,"points":7,"color":"accent","stroke":"white","stroke_width":2},
        {"type":"text","text":"7-point + stroke","x":1000,"y":210,"size":13,"color":"#666","align":"center","font":"consolas"},

        # Pill variants
        {"type":"pill","x":100,"y":290,"text":"SOLID PILL","color":"accent","size":14},
        {"type":"pill","x":300,"y":290,"text":"OUTLINE PILL","color":"green","size":14,"outline":True},
        {"type":"pill","x":520,"y":290,"text":"OUTLINE RED","color":"red","size":14,"outline":True},

        # Pill con shadow
        {"type":"pill","x":100,"y":350,"text":"GLOW PILL","color":"accent","size":14,
         "shadow":True,"shadow_color":"#7c6bf560","shadow_blur":16},

        # Mixed features
        {"type":"text","text":"GC CANVA V3.6","x":600,"y":420,"size":36,"align":"center","bold":True,"font":"impact",
         "text_gradient":{"color1":"gold","color2":"orange"},"letter_spacing":6},

        {"type":"text","text":"v3.6","x":1140,"y":460,"size":14,"color":"#5a5a80","align":"right","font":"consolas"},
    ]
}

img = generate_from_spec(spec)
buf, _, _ = export_image(img, "webp", 92)
data = buf.read()
with open(os.path.join(OUT, "v36_features.webp"), "wb") as f:
    f.write(data)
print(f"OK: {len(data)/1024:.1f}KB")
