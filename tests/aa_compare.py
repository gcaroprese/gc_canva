"""Comparar calidad con y sin anti-aliasing global."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")

# Spec con lineas, formas, barras - lo que se ve mal sin AA
elements = [
    {"type":"gradient","x":0,"y":0,"w":600,"h":400,"color1":"#0a0825","color2":"#030310","angle":135},
    # Lineas finas
    {"type":"line","x1":40,"y1":60,"x2":560,"y2":60,"color":"#333355","width":1},
    {"type":"line","x1":40,"y1":140,"x2":560,"y2":140,"color":"#333355","width":1},
    {"type":"line","x1":40,"y1":220,"x2":560,"y2":220,"color":"#333355","width":1},
    # Linea diagonal (trend)
    {"type":"line","x1":50,"y1":300,"x2":350,"y2":80,"color":"#22c55e60","width":2},
    # Barras
    {"type":"rect","x":60,"y":260,"w":30,"h":40,"color":"#7c6bf540","radius":4},
    {"type":"rect","x":100,"y":230,"w":30,"h":70,"color":"#7c6bf560","radius":4},
    {"type":"rect","x":140,"y":200,"w":30,"h":100,"color":"#7c6bf580","radius":4},
    {"type":"rect","x":180,"y":160,"w":30,"h":140,"color":"accent","radius":4},
    {"type":"rect","x":220,"y":140,"w":30,"h":160,"color":"green","radius":4},
    # Donut
    {"type":"ring","x":450,"y":180,"r":70,"thickness":16,"color":"accent","start":0,"end":210},
    {"type":"ring","x":450,"y":180,"r":70,"thickness":16,"color":"green","start":210,"end":300},
    {"type":"ring","x":450,"y":180,"r":70,"thickness":16,"color":"gold","start":300,"end":360},
    # Circulo
    {"type":"circle","x":450,"y":340,"r":30,"color":"accent","opacity":0.5},
    # Pill
    {"type":"pill","x":300,"y":330,"text":"QUALITY TEST","color":"accent","size":12},
]

# Sin AA
spec_noaa = {"width":600,"height":400,"background":"dark","elements":elements}
img1 = generate_from_spec(spec_noaa)
buf1, _, _ = export_image(img1, "webp", 95)
d1 = buf1.read()
with open(os.path.join(OUT, "compare_noaa.webp"), "wb") as f:
    f.write(d1)

# Con AA 2x
spec_aa = {"width":600,"height":400,"background":"dark","antialias":2,"elements":elements}
img2 = generate_from_spec(spec_aa)
buf2, _, _ = export_image(img2, "webp", 95)
d2 = buf2.read()
with open(os.path.join(OUT, "compare_aa2x.webp"), "wb") as f:
    f.write(d2)

print(f"  Sin AA:  {len(d1)//1024}KB")
print(f"  Con AA:  {len(d2)//1024}KB")
