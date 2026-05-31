"""
GC Canva - Test de calidad y comparacion de formatos.
Genera imagenes con features complejos y compara WebP vs PNG vs JPG.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

# ─── Test 1: Sombras con blur, text stroke, opacidad superpuesta ───
spec_complex = {
    "width": 1200, "height": 630, "background": "#0f0f1a",
    "elements": [
        # Gradiente de fondo radial
        {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"color1":"#1a1040","color2":"#0a0510","direction":"radial"},
        # Rectangulos semi-transparentes superpuestos
        {"type":"rect","x":50,"y":50,"w":500,"h":530,"color":"#7c6bf5","opacity":0.08,"radius":24},
        {"type":"rect","x":650,"y":50,"w":500,"h":530,"color":"#f59e0b","opacity":0.06,"radius":24},
        # Circulo decorativo con opacity
        {"type":"circle","x":600,"y":315,"r":180,"color":"#ffffff","opacity":0.03},
        {"type":"circle","x":600,"y":315,"r":120,"color":"#ffffff","opacity":0.04},
        # Linea separadora
        {"type":"line","x1":80,"y1":400,"x2":520,"y2":400,"color":"#7c6bf5","width":2},
        # Texto con sombra blur
        {"type":"text","text":"SHADOWS","x":300,"y":120,"size":72,"color":"#ffffff","align":"center","bold":True,"font":"impact","shadow":True,"shadow_color":"#7c6bf580","shadow_x":0,"shadow_y":0,"shadow_blur":20},
        # Texto con text_stroke (outline)
        {"type":"text","text":"OUTLINED","x":300,"y":240,"size":56,"color":"#0f0f1a","align":"center","bold":True,"font":"impact","text_stroke":True,"text_stroke_color":"#7c6bf5","text_stroke_width":2},
        # Texto regular
        {"type":"text","text":"Subtitulo con sombra suave","x":300,"y":330,"size":22,"color":"#a0a0c0","align":"center","font":"segoe ui","shadow":True,"shadow_color":"#00000080","shadow_blur":4},
        # Texto derecha con align right
        {"type":"text","text":"Align Right Test","x":1120,"y":120,"size":28,"color":"#f59e0b","align":"right","font":"roboto slab bold"},
        # Texto multilinea centrado
        {"type":"text","text":"Multilinea\nCentrado\nPerfecto","x":900,"y":250,"size":36,"color":"#ffffff","align":"center","font":"mukta","shadow":True,"shadow_blur":6},
        # Estrella decorativa
        {"type":"star","x":900,"y":480,"r":40,"inner_r":16,"points":5,"color":"#f59e0b"},
        # Triangulo
        {"type":"triangle","x":100,"y":450,"w":120,"h":100,"color":"#7c6bf530"},
        # Poligono hexagonal
        {"type":"polygon","x":400,"y":500,"r":40,"sides":6,"color":"#7c6bf520"},
    ]
}

# ─── Test 2: Diseño realista complejo (tarjeta de presentacion premium) ───
spec_card = {
    "width": 1050, "height": 600, "background": "#0c0c14",
    "elements": [
        {"type":"gradient","x":0,"y":0,"w":1050,"h":600,"color1":"#0c0c14","color2":"#14142a","direction":"horizontal"},
        # Barra lateral dorada
        {"type":"rect","x":0,"y":0,"w":5,"h":600,"color":"#c9a227"},
        {"type":"rect","x":0,"y":595,"w":1050,"h":5,"color":"#c9a22740"},
        # Rectangulo decorativo sutil
        {"type":"rect","x":40,"y":40,"w":400,"h":520,"color":"#c9a227","opacity":0.04,"radius":16},
        # Logo area
        {"type":"text","text":"GC","x":160,"y":100,"size":80,"color":"#c9a227","align":"center","bold":True,"font":"impact"},
        {"type":"rect","x":100,"y":200,"w":120,"h":2,"color":"#c9a227"},
        {"type":"text","text":"STUDIOS","x":160,"y":218,"size":20,"color":"#c9a22780","align":"center","font":"bahnschrift"},
        # Nombre
        {"type":"text","text":"Gabriel","x":160,"y":290,"size":36,"color":"#ffffff","align":"center","bold":True,"font":"roboto slab"},
        {"type":"text","text":"Caroprese","x":160,"y":340,"size":36,"color":"#c9a227","align":"center","bold":True,"font":"roboto slab"},
        {"type":"text","text":"Creative Director","x":160,"y":400,"size":16,"color":"#6a6a8a","align":"center","font":"segoe ui"},
        # Info derecha
        {"type":"text","text":"contacto@gcstudios.com","x":560,"y":180,"size":20,"color":"#c9a227","font":"segoe ui"},
        {"type":"text","text":"+54 11 5555-1234","x":560,"y":220,"size":20,"color":"#8a8aa0","font":"segoe ui"},
        {"type":"text","text":"www.gcstudios.com","x":560,"y":260,"size":20,"color":"#8a8aa0","font":"segoe ui"},
        {"type":"text","text":"Buenos Aires, Argentina","x":560,"y":300,"size":20,"color":"#5a5a74","font":"segoe ui"},
        # Linea separadora
        {"type":"rect","x":560,"y":350,"w":400,"h":1,"color":"#c9a22730"},
        # Tagline
        {"type":"text","text":"Diseno Digital\ny Marketing Creativo","x":560,"y":380,"size":28,"color":"#ffffff","font":"mukta","bold":True,"shadow":True,"shadow_blur":6,"shadow_color":"#c9a22730"},
    ]
}

# ─── Test 3: Comparacion de fuentes ───
spec_fonts = {
    "width": 1200, "height": 1400, "background": "#ffffff",
    "elements": [
        {"type":"rect","x":0,"y":0,"w":1200,"h":80,"color":"#1a1a2e"},
        {"type":"text","text":"GC Canva - Font Showcase","x":30,"y":20,"size":32,"color":"#ffffff","bold":True,"font":"mukta"},
    ] + [
        {"type":"text","text":f"{font}","x":30,"y":120+i*50,"size":28,"color":"#1a1a2e","font":font}
        for i, font in enumerate([
            "arial","impact","georgia","verdana","times",
            "trebuchet","calibri","tahoma","segoe ui","consolas",
            "courier","comic sans","cooper black","roboto slab",
            "roboto slab bold","mukta","mukta bold","moon bold",
            "moon light","narnia","optimus princeps","rakoon",
            "rockwell","gabriola","bahnschrift",
        ])
    ]
}

# ─── Generar y comparar formatos ───
print("=" * 65)
print("  GC CANVA - TEST DE CALIDAD")
print("=" * 65)

tests = [
    ("complex_features", spec_complex),
    ("premium_card", spec_card),
    ("font_showcase", spec_fonts),
]

for name, spec in tests:
    print(f"\n  {name}:")
    img = generate_from_spec(spec)

    for fmt in ["webp", "png", "jpg"]:
        q = 92 if fmt != "png" else 0
        t0 = time.time()
        buf, mime, ext = export_image(img, fmt, q)
        dt = time.time() - t0
        data = buf.read()
        fpath = os.path.join(OUT, f"{name}.{ext}")
        with open(fpath, "wb") as f:
            f.write(data)
        print(f"    {ext:4s}  {len(data)/1024:7.1f}KB  {dt*1000:6.0f}ms")

print("\n" + "=" * 65)
print("  Archivos en:", OUT)
print("=" * 65)
