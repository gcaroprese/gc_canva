"""
Biblioteca de templates profesionales reutilizables.
Cada template es una funcion que acepta parametros y retorna un spec.
El usuario solo cambia titulo, subtitulo, colores, imagen.
"""
import os

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "assets", "images")


def blog_dark_split(title="Title", subtitle="Subtitle", accent="#7c6bf5",
                    bg_photo=None, brand="brand.com", w=1200, h=675):
    """Blog OG con split: contenido izquierda + foto fondo derecha."""
    elements = [
        # Fondo
        {"type":"gradient","x":0,"y":0,"w":w,"h":h,
         "stops":[[0,"#03030a"],[0.3,"#0a0820"],[0.6,"#0e0c30"],[1,"#03030a"]],"angle":145},
        {"type":"rect","x":0,"y":0,"w":w,"h":2,"color":accent},
    ]
    # Foto de fondo derecha con overlay
    if bg_photo and os.path.exists(bg_photo):
        elements += [
            {"type":"image","src":bg_photo,"x":w//2,"y":0,"w":w//2,"h":h,"opacity":0.2},
            {"type":"gradient","x":w//2,"y":0,"w":w//2,"h":h,"color1":"#03030aEE","color2":"#03030a40","direction":"horizontal"},
        ]
    # Calcular posiciones dinamicas basadas en el titulo
    title_size = min(62, w // 18)
    title_lines = title.count('\n') + 1
    # Estimar lineas extra por wrap (max_width = w//2-120)
    avg_char_w = title_size * 0.55
    max_chars = int((w // 2 - 120) / max(avg_char_w, 1))
    for line in title.split('\n'):
        if len(line) > max_chars:
            title_lines += len(line) // max_chars
    title_end_y = 110 + title_lines * (title_size + 12)
    sep_y = title_end_y + 25
    sub_y = sep_y + 30
    cta_y = min(sub_y + 70, h - 110)

    # Glass card
    elements += [
        {"type":"rect","x":40,"y":35,"w":w//2-20,"h":h-70,"color":accent,"opacity":0.03,"radius":20},
        # Categoria pill
        {"type":"pill","x":65,"y":60,"text":subtitle.split()[0].upper() if subtitle else "BLOG","color":accent,"size":12,"py":8},
        # Titulo
        {"type":"text","text":title,"x":65,"y":110,"size":title_size,"bold":True,"font":"mukta",
         "color":"#ffffff","shadow":True,"shadow_blur":10,"shadow_color":accent+"20","max_width":w//2-120},
        # Separador
        {"type":"divider","x":65,"y":sep_y,"w":w//5,"color":accent,"thickness":2},
        # Subtitulo
        {"type":"text","text":subtitle,"x":65,"y":sub_y,"size":18,"color":"#8888b0","font":"segoe ui","max_width":w//2-120},
        # CTA
        {"type":"rect","x":65,"y":cta_y,"w":200,"h":46,"color":accent,"radius":23,
         "shadow":True,"shadow_color":accent+"50","shadow_blur":16,"shadow_y":4},
        {"type":"text","text":"Leer mas","x":165,"y":cta_y+14,"size":14,"color":"white","align":"center","bold":True,"font":"segoe ui"},
        # Brand
        {"type":"text","text":brand,"x":65,"y":h-50,"size":13,"color":"#4a4a6a","font":"consolas"},
        {"type":"rect","x":0,"y":h-2,"w":w,"h":2,"color":accent+"30"},
    ]
    return {"width":w,"height":h,"background":"dark","antialias":2,
            "post":{"vignette":True,"vignette_strength":0.3,"tint":accent,"tint_strength":0.03},
            "elements":elements}


def blog_photo_hero(title="Title", subtitle="Subtitle", accent="#c8956c",
                    photo=None, brand="brand.com", w=1200, h=675):
    """Blog OG con foto como hero de fondo completo + texto superpuesto."""
    elements = []
    # Foto de fondo completa
    if photo and os.path.exists(photo):
        elements.append({"type":"image","src":photo,"x":0,"y":0,"w":w,"h":h,"opacity":0.35})
    # Overlay oscuro para legibilidad
    elements += [
        {"type":"gradient","x":0,"y":0,"w":w,"h":h,
         "stops":[[0,"#000000CC"],[0.4,"#000000AA"],[1,"#00000088"]],"direction":"vertical"},
        {"type":"rect","x":0,"y":0,"w":w,"h":3,"color":accent},
        # Titulo centrado
        {"type":"text","text":title,"x":w//2,"y":h//3,"size":min(72, w//15),"color":"#ffffff","align":"center","valign":"center",
         "bold":True,"font":"mukta","shadow":True,"shadow_blur":12,"max_width":w*3//4},
        # Separador centrado
        {"type":"rect","x":w//2-60,"y":h//2+20,"w":120,"h":3,"color":accent},
        # Subtitulo
        {"type":"text","text":subtitle,"x":w//2,"y":h//2+60,"size":20,"color":"#cccccc","align":"center","font":"segoe ui","max_width":w*2//3},
        # Brand
        {"type":"text","text":brand,"x":w//2,"y":h-40,"size":14,"color":"#888888","align":"center","font":"consolas"},
        {"type":"rect","x":0,"y":h-2,"w":w,"h":2,"color":accent+"40"},
    ]
    return {"width":w,"height":h,"background":"#000000","antialias":2,
            "post":{"vignette":True,"vignette_strength":0.4,"grain":True,"grain_strength":4},
            "elements":elements}


def dashboard_card(accent="#7c6bf5", w=1200, h=675):
    """Dashboard analytics sin texto - solo graficos."""
    return {
        "width":w,"height":h,"background":"#030308","antialias":2,
        "post":{"vignette":True,"vignette_strength":0.35,"tint":accent,"tint_strength":0.03,"grain":True,"grain_strength":4},
        "elements":[
            {"type":"gradient","x":0,"y":0,"w":w,"h":h,
             "stops":[[0,"#03030a"],[0.25,"#08061a"],[0.5,"#0e0c30"],[0.75,"#08061a"],[1,"#03030a"]],"angle":145},
            {"type":"circle","x":w//2,"y":h//2,"r":int(w*0.3),"color":accent,"opacity":0.025},
            {"type":"circle","x":w//2,"y":h//2,"r":int(w*0.15),"color":accent,"opacity":0.04},
            # Surface
            {"type":"gradient","x":0,"y":int(h*0.72),"w":w,"h":int(h*0.28),"color1":"#06050f","color2":"#030308","direction":"vertical"},
            # Main card
            {"type":"rect","x":int(w*0.07),"y":int(h*0.09),"w":int(w*0.52),"h":int(h*0.6),"color":"#0a0a1a","radius":20,
             "shadow":True,"shadow_color":accent+"10","shadow_blur":30,"shadow_y":10},
            # Bars
            {"type":"rect","x":int(w*0.10),"y":int(h*0.52),"w":int(w*0.03),"h":int(h*0.08),"color":accent+"25","radius":4},
            {"type":"rect","x":int(w*0.14),"y":int(h*0.47),"w":int(w*0.03),"h":int(h*0.13),"color":accent+"38","radius":4},
            {"type":"rect","x":int(w*0.18),"y":int(h*0.42),"w":int(w*0.03),"h":int(h*0.18),"color":accent+"50","radius":4},
            {"type":"rect","x":int(w*0.22),"y":int(h*0.36),"w":int(w*0.03),"h":int(h*0.24),"color":accent+"65","radius":4},
            {"type":"rect","x":int(w*0.26),"y":int(h*0.30),"w":int(w*0.03),"h":int(h*0.30),"color":accent+"80","radius":4},
            {"type":"rect","x":int(w*0.30),"y":int(h*0.24),"w":int(w*0.03),"h":int(h*0.36),"color":accent,"radius":4},
            {"type":"rect","x":int(w*0.34),"y":int(h*0.27),"w":int(w*0.03),"h":int(h*0.33),"color":"#22c55e","radius":4},
            # Glow on tallest
            {"type":"circle","x":int(w*0.315),"y":int(h*0.23),"r":5,"color":accent,
             "shadow":True,"shadow_color":accent+"60","shadow_blur":10},
            # Donut
            {"type":"ring","x":int(w*0.48),"y":int(h*0.40),"r":int(h*0.12),"thickness":int(h*0.03),"color":accent,"start":0,"end":210},
            {"type":"ring","x":int(w*0.48),"y":int(h*0.40),"r":int(h*0.12),"thickness":int(h*0.03),"color":"#22c55e","start":210,"end":300},
            {"type":"ring","x":int(w*0.48),"y":int(h*0.40),"r":int(h*0.12),"thickness":int(h*0.03),"color":"#f59e0b","start":300,"end":360},
            {"type":"circle","x":int(w*0.48),"y":int(h*0.40),"r":int(h*0.07),"color":"#0a0a1a"},
            # Secondary card
            {"type":"rect","x":int(w*0.62),"y":int(h*0.09),"w":int(w*0.35),"h":int(h*0.27),"color":"#0a0a1a","radius":18,
             "shadow":True,"shadow_color":accent+"10","shadow_blur":20,"shadow_y":8},
            # Mini bars
            {"type":"rect","x":int(w*0.65),"y":int(h*0.27),"w":int(w*0.02),"h":int(h*0.05),"color":accent+"40","radius":3},
            {"type":"rect","x":int(w*0.68),"y":int(h*0.24),"w":int(w*0.02),"h":int(h*0.08),"color":accent+"60","radius":3},
            {"type":"rect","x":int(w*0.71),"y":int(h*0.21),"w":int(w*0.02),"h":int(h*0.11),"color":accent+"80","radius":3},
            {"type":"rect","x":int(w*0.74),"y":int(h*0.18),"w":int(w*0.02),"h":int(h*0.14),"color":accent,"radius":3},
            {"type":"rect","x":int(w*0.77),"y":int(h*0.20),"w":int(w*0.02),"h":int(h*0.12),"color":"#22c55e","radius":3},
            # Mini donut
            {"type":"ring","x":int(w*0.88),"y":int(h*0.22),"r":int(h*0.06),"thickness":int(h*0.016),"color":"#f59e0b","start":0,"end":250},
            {"type":"ring","x":int(w*0.88),"y":int(h*0.22),"r":int(h*0.06),"thickness":int(h*0.016),"color":"#ef4444","start":250,"end":360},
            {"type":"circle","x":int(w*0.88),"y":int(h*0.22),"r":int(h*0.035),"color":"#0a0a1a"},
            # Scatter card
            {"type":"rect","x":int(w*0.62),"y":int(h*0.40),"w":int(w*0.35),"h":int(h*0.29),"color":"#0a0a1a","radius":18,
             "shadow":True,"shadow_color":accent+"10","shadow_blur":20,"shadow_y":8},
            # Dots
            {"type":"circle","x":int(w*0.67),"y":int(h*0.53),"r":6,"color":accent,"opacity":0.6},
            {"type":"circle","x":int(w*0.71),"y":int(h*0.58),"r":8,"color":"#22c55e","opacity":0.7},
            {"type":"circle","x":int(w*0.76),"y":int(h*0.52),"r":5,"color":accent,"opacity":0.5},
            {"type":"circle","x":int(w*0.80),"y":int(h*0.55),"r":9,"color":"#22c55e","opacity":0.8,
             "shadow":True,"shadow_color":"#22c55e40","shadow_blur":6},
            {"type":"circle","x":int(w*0.84),"y":int(h*0.49),"r":7,"color":accent,"opacity":0.6},
            {"type":"circle","x":int(w*0.88),"y":int(h*0.46),"r":10,"color":accent,"opacity":0.9,
             "shadow":True,"shadow_color":accent+"40","shadow_blur":8},
            {"type":"circle","x":int(w*0.92),"y":int(h*0.52),"r":6,"color":"#f59e0b","opacity":0.5},
            # Particles
            {"type":"circle","x":int(w*0.35),"y":int(h*0.04),"r":7,"color":accent,"opacity":0.3,
             "shadow":True,"shadow_color":accent+"40","shadow_blur":10},
            {"type":"circle","x":int(w*0.45),"y":int(h*0.02),"r":9,"color":"#22c55e","opacity":0.2,
             "shadow":True,"shadow_color":"#22c55e40","shadow_blur":12},
            {"type":"circle","x":int(w*0.55),"y":int(h*0.01),"r":5,"color":"#f59e0b","opacity":0.15},
            # Accent
            {"type":"rect","x":0,"y":0,"w":w,"h":2,"color":accent},
        ]
    }


def product_showcase(product_image=None, accent="#5d8a5e", bg_tint="#0a0e0a", w=1200, h=675):
    """Producto con fondo oscuro y glow - sin texto."""
    elements = [
        {"type":"gradient","x":0,"y":0,"w":w,"h":h,
         "stops":[[0,bg_tint],[0.4,"#060806"],[1,"#030403"]],"direction":"radial"},
        {"type":"circle","x":w//2,"y":h//2-30,"r":int(w*0.28),"color":accent,"opacity":0.035},
        {"type":"circle","x":w//2,"y":h//2-30,"r":int(w*0.16),"color":accent,"opacity":0.05},
        # Surface
        {"type":"gradient","x":0,"y":int(h*0.65),"w":w,"h":int(h*0.35),
         "color1":"#0c100c","color2":"#060806","direction":"vertical"},
        {"type":"rect","x":0,"y":int(h*0.65),"w":w,"h":1,"color":accent+"08"},
    ]
    if product_image and os.path.exists(product_image):
        # Contact shadow
        elements.append({"type":"ellipse","x":int(w*0.3),"y":int(h*0.72),"w":int(w*0.4),"h":int(h*0.04),"color":"#000000","opacity":0.3})
        # Product centered
        elements.append({"type":"image","src":product_image,"x":int(w*0.2),"y":int(h*0.05),"w":int(w*0.6),"h":int(h*0.7)})
    # Particles
    elements += [
        # Sombra de contacto realista
        {"type":"contact_shadow","x":int(w*0.28),"y":int(h*0.72),"w":int(w*0.44),"h":int(h*0.04),
         "color":"#00000050","blur":20},
        {"type":"circle","x":int(w*0.15),"y":int(h*0.3),"r":4,"color":accent,"opacity":0.12},
        {"type":"circle","x":int(w*0.85),"y":int(h*0.2),"r":3,"color":accent,"opacity":0.08},
        {"type":"circle","x":int(w*0.8),"y":int(h*0.7),"r":5,"color":accent,"opacity":0.06},
    ]
    return {"width":w,"height":h,"background":"#060806","antialias":2,
            "post":{"vignette":True,"vignette_strength":0.45,"tint":accent,"tint_strength":0.04,"grain":True,"grain_strength":4},
            "elements":elements}


def church_post(title="Title", verse="", reference="", accent="#c9a227",
                bg_photo=None, church_name="", w=1080, h=1080):
    """Post de iglesia - elegante, oscuro, espiritual."""
    elements = [
        {"type":"gradient","x":0,"y":0,"w":w,"h":h,
         "stops":[[0,"#1a1200"],[0.3,"#0a0800"],[0.7,"#050400"],[1,"#020200"]],"direction":"radial"},
    ]
    if bg_photo and os.path.exists(bg_photo):
        elements.append({"type":"image","src":bg_photo,"x":0,"y":0,"w":w,"h":h,"opacity":0.1})
    elements += [
        # Cruz dorada
        {"type":"rect","x":w//2-3,"y":int(h*0.08),"w":6,"h":int(h*0.15),"color":accent},
        {"type":"rect","x":w//2-int(h*0.05),"y":int(h*0.12),"w":int(h*0.1),"h":5,"color":accent},
        # Glow detras de la cruz
        {"type":"circle","x":w//2,"y":int(h*0.15),"r":int(h*0.08),"color":accent,"opacity":0.06},
        # Texto
        {"type":"text","text":verse,"x":w//2,"y":int(h*0.38),"size":min(60, w//16),"color":"#ffffff","align":"center","valign":"center",
         "bold":True,"font":"optimus princeps","shadow":True,"shadow_blur":15,"shadow_color":accent+"30","max_width":int(w*0.8)},
        {"type":"text","text":reference,"x":w//2,"y":int(h*0.62),"size":24,"color":accent,"align":"center","font":"gabriola"},
        {"type":"divider","x":int(w*0.3),"y":int(h*0.70),"w":int(w*0.4),"color":accent+"40","thickness":1},
        {"type":"text","text":church_name,"x":w//2,"y":int(h*0.76),"size":26,"color":"#8a7040","align":"center","bold":True,"font":"roboto slab"},
        {"type":"text","text":"Todos son bienvenidos","x":w//2,"y":int(h*0.83),"size":18,"color":"#5a5040","align":"center","font":"segoe ui"},
    ]
    return {"width":w,"height":h,"background":"#020200","antialias":2,
            "post":{"vignette":True,"vignette_strength":0.5,"tint":accent,"tint_strength":0.03},
            "elements":elements}


def etsy_listing(title_lines=None, price="$24.99", accent="#8b4513",
                 product_image=None, w=2000, h=2000):
    """Listing de Etsy - producto centrado, tipografia grande."""
    if title_lines is None:
        title_lines = ["BEST", "DOG MOM", "EVER"]
    elements = [
        {"type":"gradient","x":0,"y":0,"w":w,"h":h,
         "stops":[[0,"#fdf9f3"],[0.5,"#f5ece0"],[1,"#ebe0d0"]],"direction":"radial"},
        {"type":"circle","x":w//2,"y":int(h*0.35),"r":int(w*0.35),"color":accent,"opacity":0.04},
    ]
    if product_image and os.path.exists(product_image):
        elements.append({"type":"image","src":product_image,"x":int(w*0.15),"y":int(h*0.02),"w":int(w*0.7),"h":int(h*0.5),"opacity":0.2})
    # Titulo grande con colores degradados
    colors = [accent, "#" + hex(int(accent.lstrip("#"), 16) + 0x303030)[2:].zfill(6), "#d4956a"]
    y_start = int(h * 0.22)
    for i, line in enumerate(title_lines):
        col = colors[i % len(colors)] if i < len(colors) else accent
        elements.append({"type":"text","text":line,"x":w//2,"y":y_start + i * int(h*0.12),
                         "size":min(200, w//9),"color":col,"align":"center","bold":True,"font":"impact"})
    elements += [
        {"type":"divider","x":int(w*0.25),"y":int(h*0.60),"w":int(w*0.5),"color":accent+"60","thickness":2},
        {"type":"text","text":"Premium Unisex T-Shirt","x":w//2,"y":int(h*0.65),"size":int(w*0.022),
         "color":"#6b4423","align":"center","font":"bahnschrift"},
        {"type":"text","text":"S  M  L  XL  2XL","x":w//2,"y":int(h*0.70),"size":int(w*0.018),
         "color":"#a08060","align":"center","font":"segoe ui"},
        {"type":"text","text":price,"x":w//2,"y":int(h*0.78),"size":int(w*0.045),
         "color":accent,"align":"center","bold":True,"font":"roboto slab bold"},
        {"type":"pill","x":w//2,"y":int(h*0.86),"text":"FREE SHIPPING","color":"#5d8a5e","align":"center",
         "size":int(w*0.012),"py":int(w*0.008)},
    ]
    return {"width":w,"height":h,"background":"#faf8f5","antialias":2,
            "post":{"vignette":True,"vignette_strength":0.2,"grain":True,"grain_strength":3},
            "elements":elements}
