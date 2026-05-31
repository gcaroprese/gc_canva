"""Inforket - composicion limpia sin errores de posicionamiento."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), "output")
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

# PASO 1: Generar el dashboard como imagen separada
dashboard_spec = {
    "width": 960, "height": 540, "background": "#080818",
    "elements": [
        # Grid lines horizontales sutiles
        {"type":"line","x1":60,"y1":150,"x2":500,"y2":150,"color":"#1a1a35","width":1},
        {"type":"line","x1":60,"y1":260,"x2":500,"y2":260,"color":"#1a1a35","width":1},
        {"type":"line","x1":60,"y1":370,"x2":500,"y2":370,"color":"#1a1a35","width":1},

        # Chart de barras creciente
        {"type":"rect","x":80,"y":340,"w":40,"h":60,"color":"#7c6bf530","radius":4},
        {"type":"rect","x":135,"y":310,"w":40,"h":90,"color":"#7c6bf540","radius":4},
        {"type":"rect","x":190,"y":280,"w":40,"h":120,"color":"#7c6bf555","radius":4},
        {"type":"rect","x":245,"y":240,"w":40,"h":160,"color":"#7c6bf570","radius":4},
        {"type":"rect","x":300,"y":210,"w":40,"h":190,"color":"#7c6bf585","radius":4},
        {"type":"rect","x":355,"y":170,"w":40,"h":230,"color":"#7c6bf5","radius":4},
        {"type":"rect","x":410,"y":190,"w":40,"h":210,"color":"#22c55e","radius":4},

        # Punto highlight en la barra mas alta
        {"type":"circle","x":375,"y":165,"r":5,"color":"#7c6bf5",
         "shadow":True,"shadow_color":"#7c6bf560","shadow_blur":8},

        # Linea de tendencia
        {"type":"line","x1":90,"y1":380,"x2":440,"y2":180,"color":"#22c55e40","width":2},

        # Donut chart derecho
        {"type":"ring","x":680,"y":260,"r":90,"thickness":22,"color":"#7c6bf5","start":0,"end":210},
        {"type":"ring","x":680,"y":260,"r":90,"thickness":22,"color":"#22c55e","start":210,"end":300},
        {"type":"ring","x":680,"y":260,"r":90,"thickness":22,"color":"#f59e0b","start":300,"end":360},
        {"type":"circle","x":680,"y":260,"r":55,"color":"#080818"},

        # Mini metrics arriba
        {"type":"rect","x":540,"y":40,"w":180,"h":80,"color":"#0d0d25","radius":10},
        {"type":"text","text":"+340%","x":570,"y":55,"size":32,"color":"#22c55e","bold":True,"font":"impact"},
        {"type":"text","text":"traffic","x":570,"y":95,"size":12,"color":"#5a5a80","font":"segoe ui"},

        {"type":"rect","x":740,"y":40,"w":180,"h":80,"color":"#0d0d25","radius":10},
        {"type":"text","text":"2.4K","x":770,"y":55,"size":32,"color":"#f59e0b","bold":True,"font":"impact"},
        {"type":"text","text":"leads","x":770,"y":95,"size":12,"color":"#5a5a80","font":"segoe ui"},

        # Labels del chart
        {"type":"text","text":"Growth","x":60,"y":430,"size":14,"color":"#5a5a80","font":"segoe ui"},
        {"type":"text","text":"Revenue","x":580,"y":430,"size":14,"color":"#5a5a80","font":"segoe ui"},
    ]
}

# Generar dashboard
dashboard_img = generate_from_spec(dashboard_spec)

# PASO 2: Cargar el macbook y pegar el dashboard en la pantalla
macbook = Image.open(os.path.join(A, "macbook_png.webp")).convert("RGBA")

# Coordenadas EXACTAS de la pantalla del macbook (medidas del asset 1327x716)
# Pantalla: aprox x=168, y=28 hasta x=1160, y=615
screen_x, screen_y = 168, 28
screen_w, screen_h = 992, 587
dashboard_resized = dashboard_img.resize((screen_w, screen_h), Image.LANCZOS)
macbook.paste(dashboard_resized, (screen_x, screen_y))

# PASO 3: Componer macbook+dashboard sobre fondo
final_spec = {
    "width": 1200, "height": 675, "background": "#030308",
    "elements": [
        # Fondo
        {"type":"gradient","x":0,"y":0,"w":1200,"h":675,
         "stops":[[0,"#03030a"],[0.3,"#0a0820"],[0.5,"#10103a"],[0.75,"#0a0820"],[1,"#03030a"]],
         "angle":150},
        {"type":"rect","x":0,"y":0,"w":1200,"h":2,"color":"accent"},

        # Glow desde la laptop
        {"type":"circle","x":600,"y":400,"r":350,"color":"accent","opacity":0.025},
        {"type":"circle","x":600,"y":400,"r":200,"color":"accent","opacity":0.04},

        # Mesa
        {"type":"rect","x":0,"y":530,"w":1200,"h":145,"color":"#05050f","opacity":0.8},
        {"type":"line","x1":0,"y1":530,"x2":1200,"y2":530,"color":"#7c6bf508","width":1},

        # Datos saliendo de la pantalla
        {"type":"circle","x":500,"y":100,"r":7,"color":"accent","opacity":0.4,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":10},
        {"type":"circle","x":600,"y":60,"r":9,"color":"green","opacity":0.35,
         "shadow":True,"shadow_color":"#22c55e40","shadow_blur":12},
        {"type":"circle","x":700,"y":80,"r":5,"color":"gold","opacity":0.3},
        {"type":"circle","x":550,"y":40,"r":11,"color":"accent","opacity":0.2,
         "shadow":True,"shadow_color":"#7c6bf540","shadow_blur":14},
        {"type":"circle","x":650,"y":30,"r":6,"color":"green","opacity":0.15},
        {"type":"circle","x":450,"y":70,"r":4,"color":"accent","opacity":0.25},

        {"type":"rect","x":0,"y":673,"w":1200,"h":2,"color":"#7c6bf520"},
    ]
}

final_img = generate_from_spec(final_spec)

# Pegar macbook con dashboard en la composicion final
# Escalar macbook para que quepa bien (ancho ~850px)
mac_w = 850
mac_h = int(macbook.height * mac_w / macbook.width)
macbook_scaled = macbook.resize((mac_w, mac_h), Image.LANCZOS)
mac_x = (1200 - mac_w) // 2  # centrado
mac_y = 530 - mac_h + 20  # apoyado sobre la mesa
final_img.paste(macbook_scaled, (mac_x, mac_y), macbook_scaled)

# Exportar
buf, _, _ = export_image(final_img, "webp", 95)
d = buf.read()
with open(os.path.join(OUT, "inforket_clean.webp"), "wb") as f:
    f.write(d)
print(f"OK: {len(d)//1024}KB")
