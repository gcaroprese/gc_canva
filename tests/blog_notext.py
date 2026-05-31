"""
Featured images para blog - SIN TEXTO, pura imagen visual.
Para sitios bilingues donde la misma imagen se usa en varios idiomas.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output", "blog_notext")
os.makedirs(OUT, exist_ok=True)
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

def no_text_check(spec):
    for el in spec.get("elements", []):
        if el.get("type") in ("text", "pill") and el.get("text"):
            print(f"  ERROR: tiene texto '{el['text']}'")
            return False
    return True

specs = {
    # ─── INFORKET: codigo/tech ───
    "inforket_code": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.3,"tint":"#7c6bf5","tint_strength":0.03,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"coding_screen2.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.8},
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
             "stops":[[0,"#7c6bf510"],[0.5,"#00000010"],[1,"#7c6bf515"]],"angle":135},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#7c6bf5"},
            {"type":"rect","x":0,"y":672,"w":1200,"h":3,"color":"#7c6bf530"},
        ]
    },

    # ─── INFORKET: analytics/data ───
    "inforket_data": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.3,"tint":"#7c6bf5","tint_strength":0.03,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"analytics_screen.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.75},
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
             "stops":[[0,"#0a0a1440"],[0.5,"#0a0a1420"],[1,"#0a0a1450"]],"direction":"radial"},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#22c55e"},
        ]
    },

    # ─── INFORKET: dashboard abstracto (sin texto) ───
    "inforket_dashboard": {
        "width":1200,"height":675,"background":"#030308","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.35,"tint":"#7c6bf5","tint_strength":0.03,"grain":True,"grain_strength":4},
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
             "stops":[[0,"#03030a"],[0.25,"#08061a"],[0.5,"#0e0c30"],[0.75,"#08061a"],[1,"#03030a"]],"angle":145},
            {"type":"circle","x":600,"y":340,"r":350,"color":"#7c6bf5","opacity":0.025},
            {"type":"circle","x":600,"y":340,"r":180,"color":"#7c6bf5","opacity":0.04},
            {"type":"gradient","x":0,"y":480,"w":1200,"h":195,"color1":"#06050f","color2":"#030308","direction":"vertical"},
            # Card principal con barras
            {"type":"rect","x":80,"y":60,"w":620,"h":400,"color":"#0a0a1a","radius":20,
             "shadow":True,"shadow_color":"#7c6bf510","shadow_blur":30,"shadow_y":10},
            {"type":"rect","x":120,"y":340,"w":35,"h":50,"color":"#7c6bf525","radius":4},
            {"type":"rect","x":168,"y":310,"w":35,"h":80,"color":"#7c6bf535","radius":4},
            {"type":"rect","x":216,"y":275,"w":35,"h":115,"color":"#7c6bf548","radius":4},
            {"type":"rect","x":264,"y":240,"w":35,"h":150,"color":"#7c6bf560","radius":4},
            {"type":"rect","x":312,"y":200,"w":35,"h":190,"color":"#7c6bf578","radius":4},
            {"type":"rect","x":360,"y":160,"w":35,"h":230,"color":"#7c6bf5","radius":4},
            {"type":"rect","x":408,"y":180,"w":35,"h":210,"color":"#22c55e","radius":4},
            {"type":"circle","x":377,"y":155,"r":5,"color":"#7c6bf5",
             "shadow":True,"shadow_color":"#7c6bf560","shadow_blur":10},
            # Donut
            {"type":"ring","x":580,"y":260,"r":78,"thickness":19,"color":"#7c6bf5","start":0,"end":210},
            {"type":"ring","x":580,"y":260,"r":78,"thickness":19,"color":"#22c55e","start":210,"end":300},
            {"type":"ring","x":580,"y":260,"r":78,"thickness":19,"color":"#f59e0b","start":300,"end":360},
            {"type":"circle","x":580,"y":260,"r":46,"color":"#0a0a1a"},
            # Card derecha
            {"type":"rect","x":740,"y":60,"w":420,"h":180,"color":"#0a0a1a","radius":18,
             "shadow":True,"shadow_color":"#7c6bf510","shadow_blur":20,"shadow_y":8},
            {"type":"rect","x":780,"y":170,"w":24,"h":30,"color":"#7c6bf540","radius":3},
            {"type":"rect","x":815,"y":155,"w":24,"h":45,"color":"#7c6bf560","radius":3},
            {"type":"rect","x":850,"y":138,"w":24,"h":62,"color":"#7c6bf580","radius":3},
            {"type":"rect","x":885,"y":122,"w":24,"h":78,"color":"#7c6bf5","radius":3},
            {"type":"rect","x":920,"y":132,"w":24,"h":68,"color":"#22c55e","radius":3},
            {"type":"ring","x":1050,"y":140,"r":42,"thickness":11,"color":"#f59e0b","start":0,"end":250},
            {"type":"ring","x":1050,"y":140,"r":42,"thickness":11,"color":"#ef4444","start":250,"end":360},
            {"type":"circle","x":1050,"y":140,"r":23,"color":"#0a0a1a"},
            # Scatter
            {"type":"rect","x":740,"y":270,"w":420,"h":190,"color":"#0a0a1a","radius":18,
             "shadow":True,"shadow_color":"#7c6bf510","shadow_blur":20,"shadow_y":8},
            {"type":"circle","x":790,"y":350,"r":6,"color":"#7c6bf5","opacity":0.6},
            {"type":"circle","x":830,"y":380,"r":8,"color":"#22c55e","opacity":0.7},
            {"type":"circle","x":875,"y":340,"r":5,"color":"#7c6bf5","opacity":0.5},
            {"type":"circle","x":920,"y":360,"r":9,"color":"#22c55e","opacity":0.8,
             "shadow":True,"shadow_color":"#22c55e40","shadow_blur":6},
            {"type":"circle","x":965,"y":325,"r":7,"color":"#7c6bf5","opacity":0.6},
            {"type":"circle","x":1010,"y":305,"r":10,"color":"#7c6bf5","opacity":0.9,
             "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":8},
            {"type":"circle","x":1050,"y":340,"r":6,"color":"#f59e0b","opacity":0.5},
            # Particulas
            {"type":"circle","x":400,"y":35,"r":7,"color":"#7c6bf5","opacity":0.3,
             "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":10},
            {"type":"circle","x":520,"y":20,"r":9,"color":"#22c55e","opacity":0.2,
             "shadow":True,"shadow_color":"#22c55e40","shadow_blur":12},
            {"type":"circle","x":300,"y":25,"r":5,"color":"#f59e0b","opacity":0.15},
            {"type":"rect","x":0,"y":0,"w":1200,"h":2,"color":"#7c6bf5"},
        ]
    },

    # ─── INFORKET: laptop + team meeting ───
    "inforket_team": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.25,"tint":"#7c6bf5","tint_strength":0.02,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"team_meeting.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.8},
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,"color1":"#7c6bf508","color2":"#00000008","direction":"diagonal"},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#7c6bf5"},
        ]
    },

    # ─── PAWSITIVE: te + perro sin texto ───
    "pawsitive_product": {
        "width":1200,"height":675,"background":"#060a06","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.3,"tint":"#8fbc8f","tint_strength":0.03,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
             "stops":[[0,"#141e14"],[0.5,"#0c140c"],[1,"#060a06"]],"direction":"radial"},
            {"type":"circle","x":400,"y":340,"r":350,"color":"#8fbc8f","opacity":0.04},
            {"type":"gradient","x":0,"y":440,"w":1200,"h":235,"color1":"#0c100c","color2":"#060a06","direction":"vertical"},
            {"type":"contact_shadow","x":220,"y":480,"w":380,"h":22,"color":"#00000060","blur":18},
            {"type":"contact_shadow","x":720,"y":570,"w":360,"h":20,"color":"#00000050","blur":15},
            {"type":"image","src":os.path.join(A,"green_tea_nobg.webp"),"x":200,"y":20,"w":480,"h":470},
            {"type":"image","src":os.path.join(A,"dog_beagle_png.webp"),"x":700,"y":30,"w":420,"h":580},
        ]
    },

    # ─── PAWSITIVE: foto de te fondo ───
    "pawsitive_herbs": {
        "width":1200,"height":675,"background":"#0a100a","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.3,"tint":"#8fbc8f","tint_strength":0.03,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"tea_dark_bg.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.8},
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,"color1":"#0a100a10","color2":"#0a100a20","direction":"radial"},
        ]
    },

    # ─── INFORKET: SEO grafico ───
    "inforket_seo": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.25,"tint":"#7c6bf5","tint_strength":0.02,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"seo_graph.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#7c6bf5"},
        ]
    },

    # ─── INFORKET: social media ───
    "inforket_social": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.2,"tint":"#7c6bf5","tint_strength":0.02,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"social_media.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#ec4899"},
        ]
    },

    # ─── INFORKET: content writing ───
    "inforket_content": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.25,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"content_writing.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#f59e0b"},
        ]
    },

    # ─── INFORKET: ecommerce ───
    "inforket_ecommerce": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.2,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"ecommerce_shop.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#22c55e"},
        ]
    },

    # ─── INFORKET: startup/trabajo ───
    "inforket_startup": {
        "width":1200,"height":675,"background":"#0a0a14","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.2,"tint":"#7c6bf5","tint_strength":0.02,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"startup_work.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#7c6bf5"},
        ]
    },

    # ─── PAWSITIVE: perro en parque ───
    "pawsitive_park": {
        "width":1200,"height":675,"background":"#0a100a","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.2,"tint":"#8fbc8f","tint_strength":0.02,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"dog_park.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#8fbc8f"},
        ]
    },

    # ─── PAWSITIVE: ceremonia de te ───
    "pawsitive_ceremony": {
        "width":1200,"height":675,"background":"#0a100a","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.2,"tint":"#d4a574","tint_strength":0.02,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"tea_ceremony.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#d4a574"},
        ]
    },

    # ─── IGLESIA: interior ───
    "iglesia_interior": {
        "width":1200,"height":675,"background":"#0a0806","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.3,"tint":"#c9a227","tint_strength":0.02,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"church_interior.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#c9a227"},
        ]
    },

    # ─── REAL ESTATE: casa visible ───
    "realestate_house": {
        "width":1200,"height":675,"background":"#0f1923","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.25,"grain":True,"grain_strength":3},
        "elements":[
            {"type":"image","src":os.path.join(A,"house_full.jpg"),"x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
            {"type":"gradient","x":0,"y":0,"w":1200,"h":675,"color1":"#0f192310","color2":"#0f192320","direction":"diagonal"},
            {"type":"rect","x":0,"y":0,"w":5,"h":675,"color":"#c9a227"},
            {"type":"rect","x":0,"y":672,"w":1200,"h":3,"color":"#c9a22740"},
        ]
    },
}

print("=" * 55)
for name, spec in specs.items():
    if not no_text_check(spec):
        continue
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    with open(os.path.join(OUT, f"{name}.webp"), "wb") as f:
        f.write(d)
    print(f"  OK {name:25s} {len(d)//1024:4d}KB")
print("=" * 55)
