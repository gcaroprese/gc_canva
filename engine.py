"""
GC Canva - Motor de generacion de imagenes (Pillow)
Soporta fuentes locales del proyecto + Windows.
Alta calidad: LANCZOS para resize, RGBA siempre.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os

# ------------------------------------------------------------------ #
# FUENTES                                                             #
# ------------------------------------------------------------------ #

# Directorio de fuentes del proyecto (viajan con el repo)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOCAL_FONTS_DIR = os.path.join(PROJECT_ROOT, "static", "fonts")

# Mapeo de nombre legible → archivo (buscado en LOCAL_FONTS_DIR primero, luego Windows)
FONT_MAP = {
    # Arial family
    "arial":              ["arial.ttf"],
    "arial bold":         ["arialbd.ttf"],
    "arial italic":       ["ariali.ttf"],
    "arial black":        ["ariblk.ttf"],
    # Calibri
    "calibri":            ["calibri.ttf"],
    "calibri bold":       ["calibrib.ttf"],
    "calibri light":      ["calibril.ttf"],
    # Cambria
    "cambria bold":       ["cambriab.ttf"],
    "cambria italic":     ["cambriai.ttf"],
    # Candara
    "candara":            ["Candara.ttf"],
    "candara bold":       ["Candarab.ttf"],
    # Comic Sans
    "comic sans":         ["comic.ttf"],
    "comic sans bold":    ["comicbd.ttf"],
    # Consolas
    "consolas":           ["consola.ttf"],
    "consolas bold":      ["consolab.ttf"],
    # Cooper
    "cooper black":       ["Cooper Std Black.ttf"],
    # Corbel
    "corbel":             ["corbel.ttf"],
    "corbel bold":        ["corbelb.ttf"],
    # Courier New
    "courier new":        ["cour.ttf"],
    "courier new bold":   ["courbd.ttf"],
    "courier":            ["cour.ttf"],
    # Franklin Gothic
    "franklin gothic":    ["framd.ttf"],
    "franklin gothic italic": ["framdit.ttf"],
    # Gabriola
    "gabriola":           ["Gabriola.ttf"],
    # Georgia
    "georgia":            ["georgia.ttf"],
    "georgia bold":       ["georgiab.ttf"],
    "georgia italic":     ["georgiai.ttf"],
    # Impact
    "impact":             ["impact.ttf"],
    # Moon
    "moon bold":          ["Moon Bold.otf"],
    "moon light":         ["Moon Light.otf"],
    "moon":               ["Moon Bold.otf"],
    # Mukta
    "mukta":              ["Mukta-Regular.ttf"],
    "mukta bold":         ["Mukta-Bold.ttf"],
    "mukta light":        ["Mukta-Light.ttf"],
    "mukta medium":       ["Mukta-Medium.ttf"],
    "mukta semibold":     ["Mukta-SemiBold.ttf"],
    "mukta extrabold":    ["Mukta-ExtraBold.ttf"],
    "mukta extralight":   ["Mukta-ExtraLight.ttf"],
    # Narnia
    "narnia":             ["Narnia.otf"],
    # Optimus Princeps
    "optimus princeps":   ["OptimusPrinceps.ttf"],
    "optimus princeps semibold": ["OptimusPrincepsSemiBold.ttf"],
    "optimus":            ["OptimusPrinceps.ttf"],
    # Rakoon
    "rakoon":             ["Rakoon_PersonalUse.ttf"],
    # Roboto Slab
    "roboto slab":        ["RobotoSlab-Regular.ttf"],
    "roboto slab bold":   ["RobotoSlab-Bold.ttf"],
    "roboto slab light":  ["RobotoSlab-Light.ttf"],
    "roboto slab thin":   ["RobotoSlab-Thin.ttf"],
    "roboto slab black":  ["RobotoSlab-Black.ttf"],
    "roboto slab medium": ["RobotoSlab-Medium.ttf"],
    "roboto slab semibold": ["RobotoSlab-SemiBold.ttf"],
    "roboto slab extrabold": ["RobotoSlab-ExtraBold.ttf"],
    "roboto slab extralight": ["RobotoSlab-ExtraLight.ttf"],
    "roboto":             ["RobotoSlab-Regular.ttf"],
    # Rockwell
    "rockwell":           ["ROCK.TTF", "Rockwell-Bold.ttf"],
    "rockwell bold":      ["Rockwell-Bold.ttf"],
    # Segoe UI
    "segoe ui":           ["segoeui.ttf"],
    "segoe ui bold":      ["segoeuib.ttf"],
    "segoe ui italic":    ["segoeuii.ttf"],
    "segoe ui light":     ["segoeuil.ttf"],
    "segoe":              ["segoeui.ttf"],
    # Tahoma
    "tahoma":             ["tahoma.ttf"],
    "tahoma bold":        ["tahomabd.ttf"],
    # Times New Roman
    "times new roman":    ["times.ttf"],
    "times new roman bold": ["timesbd.ttf"],
    "times":              ["times.ttf"],
    # Trebuchet MS
    "trebuchet ms":       ["trebuc.ttf"],
    "trebuchet ms bold":  ["trebucbd.ttf"],
    "trebuchet":          ["trebuc.ttf"],
    # Verdana
    "verdana":            ["verdana.ttf"],
    "verdana bold":       ["verdanab.ttf"],
    "verdana italic":     ["verdanai.ttf"],
    # Bahnschrift
    "bahnschrift":        ["bahnschrift.ttf"],
    # Bananas
    "bananas":            ["Bananas_VF_Light_Condensed (1).otf"],
}

# Aliases para el motor (shortcuts)
FONT_ALIASES = {
    "sans": "arial", "sans-serif": "arial", "monospace": "consolas",
    "mono": "consolas", "code": "consolas", "serif": "georgia",
    "display": "impact", "slab": "roboto slab", "fancy": "gabriola",
    "elegant": "optimus princeps", "modern": "mukta", "tech": "bahnschrift",
    "cafe": "rockwell", "script": "gabriola",
}

_font_cache = {}

def resolve_font_path(names_list):
    """Busca el archivo de fuente en fonts locales, luego Windows."""
    search_dirs = [LOCAL_FONTS_DIR]
    if os.name == 'nt':
        search_dirs += [
            "C:/Windows/Fonts",
            os.path.expandvars("%LOCALAPPDATA%/Microsoft/Windows/Fonts"),
        ]
    for name in names_list:
        for d in search_dirs:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None

def get_font(name="arial", size=24, bold=False, italic=False):
    """Carga fuente por nombre. Soporta nombres como 'roboto slab bold'."""
    size = max(6, int(size))
    name_clean = str(name or "arial").lower().strip()
    name_clean = FONT_ALIASES.get(name_clean, name_clean)

    # Construir variante
    key_base = name_clean
    key_bold = name_clean + " bold" if bold and "bold" not in name_clean else None
    key_italic = name_clean + " italic" if italic and "italic" not in name_clean else None

    # Orden de preferencia
    candidates = []
    if bold and key_bold: candidates.append(key_bold)
    if italic and key_italic: candidates.append(key_italic)
    candidates.append(key_base)

    cache_key = (tuple(candidates), size)
    if cache_key in _font_cache:
        return _font_cache[cache_key]

    for candidate in candidates:
        files = FONT_MAP.get(candidate)
        if files:
            path = resolve_font_path(files)
            if path:
                try:
                    f = ImageFont.truetype(path, size)
                    _font_cache[cache_key] = f
                    return f
                except Exception:
                    pass

    # Fallback: scan LOCAL_FONTS_DIR for partial name match
    try:
        if os.path.isdir(LOCAL_FONTS_DIR):
            for fname in os.listdir(LOCAL_FONTS_DIR):
                if fname.lower().endswith(('.ttf', '.otf')):
                    fname_key = os.path.splitext(fname)[0].lower().replace('-', ' ').replace('_', ' ')
                    if name_clean in fname_key:
                        path = os.path.join(LOCAL_FONTS_DIR, fname)
                        f = ImageFont.truetype(path, size)
                        _font_cache[cache_key] = f
                        return f
    except Exception:
        pass

    # Last resort: default
    try:
        fallback = resolve_font_path(["arial.ttf"])
        if fallback:
            f = ImageFont.truetype(fallback, size)
        else:
            f = ImageFont.load_default(size=size)
        _font_cache[cache_key] = f
        return f
    except Exception:
        return ImageFont.load_default()


def list_available_fonts():
    """Retorna lista de fuentes disponibles en el proyecto."""
    fonts = []
    if os.path.isdir(LOCAL_FONTS_DIR):
        for fname in sorted(os.listdir(LOCAL_FONTS_DIR)):
            if fname.lower().endswith(('.ttf', '.otf')):
                display_name = os.path.splitext(fname)[0]
                display_name = display_name.replace('-', ' ').replace('_', ' ')
                fonts.append({"name": display_name, "file": fname})
    return fonts


# ------------------------------------------------------------------ #
# COLORES                                                             #
# ------------------------------------------------------------------ #

NAMED_COLORS = {
    "white":"#ffffff","black":"#000000","red":"#ef4444","green":"#22c55e",
    "blue":"#3b82f6","yellow":"#eab308","orange":"#f97316","purple":"#a855f7",
    "pink":"#ec4899","gray":"#6b7280","grey":"#6b7280","gold":"#c9a227",
    "silver":"#9ca3af","brown":"#92400e","navy":"#1e3a5f","teal":"#14b8a6",
    "cyan":"#06b6d4","lime":"#84cc16","indigo":"#6366f1","violet":"#8b5cf6",
    "accent":"#7c6bf5","dark":"#0c0c14","light":"#f8f9fa",
    "transparent":"#00000000",
}

def parse_color(color, default=(0, 0, 0, 255)):
    if not color:
        return default
    c = str(color).strip().lower()
    if c in NAMED_COLORS:
        c = NAMED_COLORS[c]
    if c.startswith('#'):
        h = c.lstrip('#')
        try:
            if len(h) == 3:
                r, g, b = (int(x*2, 16) for x in h)
                return (r, g, b, 255)
            if len(h) == 6:
                return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), 255)
            if len(h) == 8:
                return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), int(h[6:8],16))
        except Exception:
            pass
    if c.startswith('rgba'):
        try:
            pts = c[5:-1].split(',')
            return (int(pts[0]), int(pts[1]), int(pts[2]), int(float(pts[3])*255))
        except Exception:
            pass
    if c.startswith('rgb'):
        try:
            pts = c[4:-1].split(',')
            return (int(pts[0]), int(pts[1]), int(pts[2]), 255)
        except Exception:
            pass
    return default


# ------------------------------------------------------------------ #
# GRADIENTES                                                           #
# ------------------------------------------------------------------ #

def _lerp_color(c1, c2, t):
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(4))


def _multi_stop_color(stops, t):
    """Interpola color en gradiente multi-stop. stops = [(pos, color), ...]"""
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1s = stops[i + 1]
        if p0 <= t <= p1:
            local_t = (t - p0) / max(p1 - p0, 0.001)
            return _lerp_color(c0, c1s, local_t)
    return stops[-1][1]


def make_gradient(w, h, c1, c2, direction="horizontal", stops=None, angle=None):
    """Gradiente lineal/radial/diagonal/angled. Soporta multi-stop con 'stops'."""
    w, h = max(1, int(w)), max(1, int(h))
    # Build stop list: [(0.0, color), ..., (1.0, color)]
    if stops:
        stop_list = [(s[0], parse_color(s[1])) for s in stops]
    else:
        stop_list = [(0.0, c1), (1.0, c2)]

    def color_at(t):
        return _multi_stop_color(stop_list, t) if len(stop_list) > 2 else _lerp_color(c1, c2, t)

    if direction == "horizontal":
        base = Image.new("RGBA", (w, 1))
        d = ImageDraw.Draw(base)
        for x in range(w):
            d.point((x, 0), fill=color_at(x / max(w - 1, 1)))
        return base.resize((w, h), Image.NEAREST)
    elif direction == "vertical":
        base = Image.new("RGBA", (1, h))
        d = ImageDraw.Draw(base)
        for y in range(h):
            d.point((0, y), fill=color_at(y / max(h - 1, 1)))
        return base.resize((w, h), Image.NEAREST)
    elif direction == "radial":
        import math
        img = Image.new("RGBA", (w, h), color_at(1.0))
        draw = ImageDraw.Draw(img)
        cx, cy = w / 2, h / 2
        maxR = math.sqrt(cx ** 2 + cy ** 2)
        steps = min(512, max(100, int(maxR / 2)))
        for i in range(steps, -1, -1):
            t = i / steps
            r = maxR * t
            if r > 0:
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color_at(t))
        return img
    elif angle is not None:
        # Gradiente con angulo libre (0=derecha, 90=abajo, etc)
        import math
        rad = math.radians(float(angle))
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        # Calcular proyeccion maxima para normalizar t
        corners = [(0, 0), (w, 0), (0, h), (w, h)]
        projs = [x * cos_a + y * sin_a for x, y in corners]
        min_p, max_p = min(projs), max(projs)
        rng = max_p - min_p
        img = Image.new("RGBA", (w, h))
        pixels = []
        for y in range(h):
            for x in range(w):
                proj = x * cos_a + y * sin_a
                t = (proj - min_p) / max(rng, 1)
                pixels.append(color_at(t))
        img.putdata(pixels)
        return img
    else:  # diagonal - verdadero gradiente esquina a esquina
        total = w + h - 1
        colors = [color_at(i / max(total - 1, 1)) for i in range(total)]
        img = Image.new("RGBA", (w, h))
        pixels = [colors[x + y] for y in range(h) for x in range(w)]
        img.putdata(pixels)
        return img


# ------------------------------------------------------------------ #
# DRAW HELPERS                                                        #
# ------------------------------------------------------------------ #

def draw_rounded_rect(draw, x, y, w, h, radius, fill, stroke=None, sw=0):
    r = max(0, min(int(radius), w//2, h//2))
    if r > 0:
        draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill,
                                outline=stroke if stroke else None, width=sw if stroke else 0)
    else:
        draw.rectangle([x, y, x+w, y+h], fill=fill,
                        outline=stroke if stroke else None, width=sw if stroke else 0)


def _draw_text_spaced(draw, pos, text, font, fill, spacing=4, letter_spacing=0, align="left"):
    """Dibuja texto con letter-spacing custom. Si letter_spacing=0, usa multiline_text normal."""
    if letter_spacing == 0:
        draw.multiline_text(pos, text, font=font, fill=fill, align=align, spacing=spacing)
        return
    x0, y0 = pos
    for line_idx, line in enumerate(text.split('\n')):
        cx = x0
        for ch in line:
            draw.text((cx, y0), ch, font=font, fill=fill)
            bbox = draw.textbbox((0, 0), ch, font=font)
            cx += (bbox[2] - bbox[0]) + letter_spacing
        y0 += font.size + spacing


def _apply_element(img, draw, el, opacity_factor=1.0):
    etype = el.get("type", "")

    def c(key, default="#000000"):
        col = parse_color(el.get(key, default))
        if opacity_factor < 1.0:
            col = col[:3] + (int(col[3] * opacity_factor),)
        return col

    def ci(key):
        v = el.get(key)
        return parse_color(v)[:3] + (int(parse_color(v)[3] * opacity_factor),) if v else None

    if etype == "rect":
        x, y = int(el.get("x",0)), int(el.get("y",0))
        w, h = max(1,int(el.get("w",100))), max(1,int(el.get("h",100)))
        fill   = c("color", "#cccccc")
        stroke = ci("stroke")
        sw     = int(el.get("stroke_width", el.get("strokeWidth", 0)))
        radius = int(el.get("radius", el.get("rx", 0)))
        draw_rounded_rect(draw, x, y, w, h, radius, fill, stroke, sw)

    elif etype in ("circle", "ellipse"):
        x, y = int(el.get("x",0)), int(el.get("y",0))
        if etype == "circle":
            r = int(el.get("r", 50))
            box = [x-r, y-r, x+r, y+r]
        else:
            w, h = max(1,int(el.get("w",100))), max(1,int(el.get("h",60)))
            box = [x, y, x+w, y+h]
        fill   = c("color", "#cccccc")
        stroke = ci("stroke")
        sw     = int(el.get("stroke_width", 0))
        # Anti-aliasing: render 2x y downscale para bordes suaves
        aa = el.get("antialias", True)
        if aa and etype == "circle":
            ss = 2
            aa_size = (r*2*ss, r*2*ss)
            aa_img = Image.new("RGBA", aa_size, (0,0,0,0))
            aa_d = ImageDraw.Draw(aa_img)
            aa_d.ellipse([0, 0, aa_size[0]-1, aa_size[1]-1], fill=fill,
                         outline=stroke, width=sw*ss if stroke else 0)
            aa_img = aa_img.resize((r*2, r*2), Image.LANCZOS)
            img.paste(aa_img, (x-r, y-r), aa_img)
        else:
            draw.ellipse(box, fill=fill, outline=stroke, width=sw if stroke else 0)

    elif etype == "divider":
        # Linea decorativa con label opcional (ahorra tokens)
        x = int(el.get("x", 0))
        y = int(el.get("y", 0))
        w = int(el.get("w", img.width))
        color = c("color", "#33334850")
        thickness = int(el.get("thickness", 1))
        label = el.get("text", "")
        direction = el.get("direction", "horizontal")
        if direction == "horizontal":
            if label:
                font_name = el.get("font", "segoe ui")
                size = int(el.get("size", 12))
                font = get_font(font_name, size)
                lbox = draw.textbbox((0,0), label, font=font)
                lw = lbox[2] - lbox[0]
                gap = 16
                mid = x + w // 2
                draw.line([(x, y), (mid - lw//2 - gap, y)], fill=color, width=thickness)
                draw.line([(mid + lw//2 + gap, y), (x + w, y)], fill=color, width=thickness)
                tc = c("text_color", "#666666")
                draw.text((mid - lw//2, y - size//2), label, font=font, fill=tc)
            else:
                draw.line([(x, y), (x + w, y)], fill=color, width=thickness)
        else:  # vertical
            h = int(el.get("h", img.height))
            draw.line([(x, y), (x, y + h)], fill=color, width=thickness)

    elif etype == "triangle":
        x, y = int(el.get("x",0)), int(el.get("y",0))
        w, h = max(1,int(el.get("w",100))), max(1,int(el.get("h",80)))
        fill = c("color", "#cccccc")
        pts  = [(x+w//2, y), (x, y+h), (x+w, y+h)]
        draw.polygon(pts, fill=fill)

    elif etype == "polygon":
        import math
        cx, cy = int(el.get("x",0)), int(el.get("y",0))
        r      = int(el.get("r", 60))
        sides  = int(el.get("sides", 6))
        angle  = float(el.get("angle", -90))
        fill   = c("color", "#cccccc")
        pts    = [(cx + r*math.cos(math.radians(angle + 360/sides*i)),
                   cy + r*math.sin(math.radians(angle + 360/sides*i))) for i in range(sides)]
        draw.polygon(pts, fill=fill)

    elif etype == "star":
        import math
        cx, cy   = int(el.get("x",0)), int(el.get("y",0))
        outer    = int(el.get("r", 60))
        inner    = int(el.get("inner_r", outer//2))
        points   = int(el.get("points", 5))
        fill     = c("color", "#ffcc00")
        stroke_c = ci("stroke")
        stroke_w = int(el.get("stroke_width", 0))
        pts = []
        for i in range(points*2):
            a = math.radians(-90 + 180*i/points)
            r_i = outer if i % 2 == 0 else inner
            pts.append((cx + r_i*math.cos(a), cy + r_i*math.sin(a)))
        # Anti-alias: render 2x y downscale
        ss = 2
        ss_sz = (outer*2*ss+4, outer*2*ss+4)
        aa = Image.new("RGBA", ss_sz, (0,0,0,0))
        ad = ImageDraw.Draw(aa)
        offset_pts = [(int((px-cx+outer)*ss+2), int((py-cy+outer)*ss+2)) for px,py in pts]
        ad.polygon(offset_pts, fill=fill, outline=stroke_c, width=stroke_w*ss if stroke_c else 0)
        aa = aa.resize((outer*2+2, outer*2+2), Image.LANCZOS)
        img.paste(aa, (cx-outer-1, cy-outer-1), aa)

    elif etype == "line":
        x1,y1 = int(el.get("x1",0)), int(el.get("y1",0))
        x2,y2 = int(el.get("x2",100)), int(el.get("y2",0))
        col   = c("color", "#000000")
        w_    = int(el.get("width", el.get("stroke_width", 2)))
        draw.line([(x1,y1),(x2,y2)], fill=col, width=w_)

    elif etype == "arc":
        # Arco: para semicirculos, curvas, handle de taza, etc.
        x, y = int(el.get("x",0)), int(el.get("y",0))
        w, h = max(1,int(el.get("w",100))), max(1,int(el.get("h",100)))
        start = float(el.get("start", 0))
        end = float(el.get("end", 180))
        col = c("color", "#cccccc")
        sw = int(el.get("width", el.get("stroke_width", 3)))
        fill_c = ci("fill")
        if fill_c:
            draw.pieslice([x, y, x+w, y+h], start, end, fill=fill_c, outline=col, width=sw)
        else:
            draw.arc([x, y, x+w, y+h], start, end, fill=col, width=sw)

    elif etype == "ring":
        # Anillo: circulo hueco (para donas, progress rings, etc)
        cx, cy = int(el.get("x",0)), int(el.get("y",0))
        r = int(el.get("r", 50))
        thickness = int(el.get("thickness", 8))
        col = c("color", "#cccccc")
        start = float(el.get("start", 0))
        end = float(el.get("end", 360))
        # Render anti-aliased
        ss = 2
        sz = (r*2*ss+4, r*2*ss+4)
        aa = Image.new("RGBA", sz, (0,0,0,0))
        ad = ImageDraw.Draw(aa)
        margin = 2
        box = [margin, margin, r*2*ss+margin, r*2*ss+margin]
        if end - start >= 360:
            ad.ellipse(box, outline=col, width=thickness*ss)
        else:
            ad.arc(box, start, end, fill=col, width=thickness*ss)
        aa = aa.resize((r*2+2, r*2+2), Image.LANCZOS)
        img.paste(aa, (cx-r-1, cy-r-1), aa)

    elif etype == "pill":
        # Pill/badge: rect redondeado con texto centrado adentro (ahorra tokens)
        x, y = int(el.get("x", 0)), int(el.get("y", 0))
        text = str(el.get("text", ""))
        size = int(el.get("size", el.get("fontSize", 16)))
        bg = c("color", "#7c6bf5")
        tc = parse_color(el.get("text_color", "#ffffff"))
        font_name = el.get("font", el.get("fontFamily", "segoe ui"))
        bold = el.get("bold", True)
        font = get_font(font_name, size, bold)
        pad_x = int(el.get("padding_x", el.get("px", 20)))
        pad_y = int(el.get("padding_y", el.get("py", 8)))
        bbox = draw.textbbox((0, 0), text, font=font)
        text_y_offset = bbox[1]  # offset real del ascender
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pw, ph = tw + pad_x * 2, th + pad_y * 2
        radius = int(el.get("radius", ph // 2))
        pill_x = x - pw // 2 if el.get("align") == "center" else x
        pill_y = y
        # Centrado vertical real: compensar offset del ascender
        text_draw_x = pill_x + pad_x - bbox[0]
        text_draw_y = pill_y + pad_y - text_y_offset
        stroke_c = ci("stroke")
        stroke_w = int(el.get("stroke_width", 0))
        # Anti-alias: render pill a 2x y downscale
        ss = 2
        pill_img = Image.new("RGBA", (pw * ss, ph * ss), (0, 0, 0, 0))
        pill_d = ImageDraw.Draw(pill_img)
        if el.get("outline"):
            r2 = min(radius * ss, pw * ss // 2, ph * ss // 2)
            pill_d.rounded_rectangle([0, 0, pw * ss - 1, ph * ss - 1], radius=r2,
                                      outline=bg, width=(stroke_w or 2) * ss)
            pill_d.text(((pad_x - bbox[0]) * ss, (pad_y - text_y_offset) * ss),
                        text, font=get_font(font_name, size * ss, bold), fill=bg)
        else:
            r2 = min(radius * ss, pw * ss // 2, ph * ss // 2)
            pill_d.rounded_rectangle([0, 0, pw * ss - 1, ph * ss - 1], radius=r2, fill=bg)
            if stroke_c and stroke_w:
                pill_d.rounded_rectangle([0, 0, pw * ss - 1, ph * ss - 1], radius=r2,
                                          outline=stroke_c, width=stroke_w * ss)
            pill_d.text(((pad_x - bbox[0]) * ss, (pad_y - text_y_offset) * ss),
                        text, font=get_font(font_name, size * ss, bold), fill=tc)
        pill_img = pill_img.resize((pw, ph), Image.LANCZOS)
        img.paste(pill_img, (pill_x, pill_y), pill_img)

    elif etype == "text":
        text = str(el.get("text",""))
        if not text: return
        x, y   = int(el.get("x",0)), int(el.get("y",0))
        size   = int(el.get("size", el.get("fontSize", 24)))
        col    = c("color", "#000000")
        align  = el.get("align", "left")
        valign = el.get("valign", "top")  # top, center, bottom
        bold   = el.get("bold", False)
        italic = el.get("italic", False)
        font_name = el.get("font", el.get("fontFamily", "arial"))
        font   = get_font(font_name, size, bold, italic)
        spacing = int(el.get("line_spacing", el.get("spacing", 4)))
        letter_spacing = int(el.get("letter_spacing", 0))  # px extra entre letras
        uppercase = el.get("uppercase", False)
        max_width = el.get("max_width")  # auto-wrap si se especifica

        if uppercase:
            text = text.upper()

        # Auto-wrap text si max_width especificado
        if max_width:
            wrapped_lines = []
            for line in text.split('\n'):
                words = line.split(' ')
                current = words[0] if words else ''
                for word in words[1:]:
                    test = current + ' ' + word
                    bbox_test = draw.textbbox((0, 0), test, font=font)
                    if bbox_test[2] - bbox_test[0] > int(max_width):
                        wrapped_lines.append(current)
                        current = word
                    else:
                        current = test
                wrapped_lines.append(current)
            text = '\n'.join(wrapped_lines)

        # Calcular bounding box total del texto
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        # Ajustar ancho si hay letter_spacing
        if letter_spacing:
            lines = text.split('\n')
            max_chars = max(len(l) for l in lines) if lines else 0
            tw += letter_spacing * (max_chars - 1) if max_chars > 1 else 0

        # Background color behind text (highlight)
        bg_color = el.get("bg_color")
        bg_pad = int(el.get("bg_padding", 6))
        bg_radius = int(el.get("bg_radius", 4))

        # Offset X segun alineacion horizontal
        draw_x = x
        if align == "center":
            draw_x = x - tw // 2
        elif align == "right":
            draw_x = x - tw

        # Offset Y segun alineacion vertical
        draw_y = y
        if valign == "center":
            draw_y = y - th // 2
        elif valign == "bottom":
            draw_y = y - th

        # Dibujar background highlight si se especifica
        if bg_color:
            bg_fill = parse_color(bg_color)
            if opacity_factor < 1.0:
                bg_fill = bg_fill[:3] + (int(bg_fill[3] * opacity_factor),)
            draw_rounded_rect(draw, draw_x - bg_pad, draw_y - bg_pad,
                              tw + bg_pad * 2, th + bg_pad * 2,
                              bg_radius, bg_fill)

        # Shadow
        if el.get("shadow"):
            sh_color = parse_color(el.get("shadow_color", "#00000080"))
            sh_x = int(el.get("shadow_x", 3))
            sh_y = int(el.get("shadow_y", 3))
            sh_blur_r = int(el.get("shadow_blur", 4))
            if sh_blur_r > 0:
                shadow_layer = Image.new("RGBA", img.size, (0,0,0,0))
                sd = ImageDraw.Draw(shadow_layer)
                sd.multiline_text((draw_x+sh_x, draw_y+sh_y), text, font=font, fill=sh_color,
                                  align=align, spacing=spacing)
                shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=sh_blur_r))
                img.paste(shadow_layer, (0,0), shadow_layer)
                draw = ImageDraw.Draw(img)
            else:
                draw.multiline_text((draw_x+sh_x, draw_y+sh_y), text, font=font, fill=sh_color,
                                    align=align, spacing=spacing)

        # Gradient text o texto solido
        text_grad = el.get("text_gradient")
        if text_grad and isinstance(text_grad, dict):
            # Texto con relleno gradiente (con margen de seguridad)
            gc1 = parse_color(text_grad.get("color1", "#ff0000"))
            gc2 = parse_color(text_grad.get("color2", "#0000ff"))
            g_dir = text_grad.get("direction", "horizontal")
            g_stops = text_grad.get("stops")
            g_angle = text_grad.get("angle")
            mask = Image.new("L", img.size, 0)
            md = ImageDraw.Draw(mask)
            md.multiline_text((draw_x, draw_y), text, font=font, fill=255, align=align, spacing=spacing)
            pad = size // 4  # margen para descenders y kerning
            gw = max(tw + pad * 2, 1)
            gh = max(th + pad * 2, 1)
            grad = make_gradient(gw, gh, gc1, gc2, g_dir, stops=g_stops, angle=g_angle)
            grad_full = Image.new("RGBA", img.size, (0, 0, 0, 0))
            grad_full.paste(grad.resize((gw, gh), Image.LANCZOS), (draw_x - pad, draw_y - pad))
            grad_full.putalpha(mask)
            img.paste(grad_full, (0, 0), grad_full)
        else:
            # Stroke/outline (solo para texto solido)
            if el.get("text_stroke"):
                import math
                tcol   = parse_color(el.get("text_stroke_color", "#000000"))
                t_sw   = int(el.get("text_stroke_width", 2))
                steps  = max(12, t_sw * 8)
                for i in range(steps):
                    a = 2 * math.pi * i / steps
                    dx = t_sw * math.cos(a)
                    dy = t_sw * math.sin(a)
                    _draw_text_spaced(draw, (draw_x + dx, draw_y + dy), text, font=font, fill=tcol,
                                      spacing=spacing, letter_spacing=letter_spacing, align=align)
            _draw_text_spaced(draw, (draw_x, draw_y), text, font=font, fill=col,
                              spacing=spacing, letter_spacing=letter_spacing, align=align)

    elif etype == "gradient":
        gx, gy = int(el.get("x",0)), int(el.get("y",0))
        gw = int(el.get("w", img.width))
        gh = int(el.get("h", img.height))
        c1 = parse_color(el.get("color1", "#000000"))
        c2 = parse_color(el.get("color2", "#ffffff"))
        direction = el.get("direction", "horizontal")
        stops = el.get("stops")  # [[0,"#c1"],[0.5,"#c2"],[1,"#c3"]]
        angle = el.get("angle")  # angulo libre en grados
        grad = make_gradient(gw, gh, c1, c2, direction, stops=stops, angle=angle)
        if opacity_factor < 1.0:
            a = grad.split()[3].point(lambda p: int(p*opacity_factor))
            grad.putalpha(a)
        img.paste(grad, (gx, gy), grad)

    elif etype == "asset":
        # Shortcut para cargar assets del proyecto: {"type":"asset","name":"coffee_cup","x":100,"y":100,"w":300}
        name = el.get("name", "")
        asset_dir = os.path.join(PROJECT_ROOT, "static", "assets", "images")
        # Buscar en orden: .webp, .png
        src_path = None
        for ext in [".webp", ".png", ".jpg"]:
            p = os.path.join(asset_dir, name + ext)
            if os.path.exists(p):
                src_path = p
                break
        if src_path:
            el_copy = dict(el)
            el_copy["type"] = "image"
            el_copy["src"] = src_path
            _apply_element(img, draw, el_copy, opacity_factor)

    elif etype == "image":
        src = el.get("src", "")
        src_img = None
        if src.startswith("data:"):
            import base64
            try:
                _, b64data = src.split(",", 1)
                src_img = Image.open(io.BytesIO(base64.b64decode(b64data))).convert("RGBA")
            except Exception as e:
                print(f"[engine] Error imagen base64: {e}")
        elif src and os.path.exists(src):
            try:
                src_img = Image.open(src).convert("RGBA")
            except Exception as e:
                print(f"[engine] Error imagen local: {e}")
        if src_img:
            x, y = int(el.get("x", 0)), int(el.get("y", 0))
            w = int(el.get("w", src_img.width))
            h = int(el.get("h", src_img.height))
            if w != src_img.width or h != src_img.height:
                src_img = src_img.resize((w, h), Image.LANCZOS)
            # Clip: recortar imagen en forma (circle, rounded)
            clip = el.get("clip")
            if clip:
                mask = Image.new("L", (w, h), 0)
                md = ImageDraw.Draw(mask)
                if clip == "circle":
                    r = min(w, h) // 2
                    md.ellipse([w//2-r, h//2-r, w//2+r, h//2+r], fill=255)
                elif clip == "rounded":
                    clip_r = int(el.get("clip_radius", min(w, h) // 8))
                    md.rounded_rectangle([0, 0, w, h], radius=clip_r, fill=255)
                elif clip == "ellipse":
                    md.ellipse([0, 0, w, h], fill=255)
                src_img.putalpha(mask)
            rot = float(el.get("rotate", 0))
            if rot:
                src_img = src_img.rotate(-rot, expand=True, resample=Image.BICUBIC)
            if opacity_factor < 1.0:
                alpha = src_img.split()[3].point(lambda p: int(p * opacity_factor))
                src_img.putalpha(alpha)
            img.paste(src_img, (x, y), src_img)


def _draw_element_shadow(img, el):
    """Dibuja sombra para formas (rect, circle, ellipse, pill). Text maneja su propia sombra."""
    etype = el.get("type", "")
    if etype in ("text", "gradient", "line", "image"):
        return  # text maneja su propia sombra

    shadow = el.get("shadow")
    if not shadow:
        return

    sh_color = parse_color(el.get("shadow_color", "#00000040"))
    sh_x = int(el.get("shadow_x", 4))
    sh_y = int(el.get("shadow_y", 4))
    sh_blur = int(el.get("shadow_blur", 12))

    # Crear copia del elemento desplazada para la sombra
    shadow_el = dict(el)
    shadow_el.pop("shadow", None)
    shadow_el.pop("shadow_color", None)
    shadow_el.pop("shadow_x", None)
    shadow_el.pop("shadow_y", None)
    shadow_el.pop("shadow_blur", None)
    shadow_el.pop("stroke", None)
    shadow_el.pop("stroke_width", None)
    shadow_el.pop("opacity", None)
    shadow_el.pop("rotate", None)
    shadow_el["color"] = "#000000"

    # Desplazar posicion
    if "x" in shadow_el:
        shadow_el["x"] = int(shadow_el["x"]) + sh_x
    if "y" in shadow_el:
        shadow_el["y"] = int(shadow_el["y"]) + sh_y

    # Renderizar sombra en capa separada
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    _apply_element(layer, ld, shadow_el, opacity_factor=1.0)

    # Aplicar color de sombra (reemplazar negro con sh_color)
    r, g, b, a = layer.split()
    colored = Image.new("RGBA", img.size, sh_color[:3])
    colored.putalpha(a)

    # Blur
    if sh_blur > 0:
        colored = colored.filter(ImageFilter.GaussianBlur(radius=sh_blur))

    img.paste(colored, (0, 0), colored)


def draw_element(img, draw, el):
    opacity = float(el.get("opacity", 1.0))
    if opacity <= 0:
        return draw

    etype = el.get("type", "")
    rotate = float(el.get("rotate", 0))

    # Sombra universal (antes del elemento)
    if el.get("shadow") and etype not in ("text", "gradient", "image"):
        _draw_element_shadow(img, el)
        draw = ImageDraw.Draw(img)

    # Rotacion a nivel de elemento
    if rotate and etype not in ("gradient", "text", "image", "pill"):
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        el_copy = dict(el)
        el_copy.pop("rotate", None)
        el_copy.pop("opacity", None)
        el_copy.pop("shadow", None)
        _apply_element(layer, layer_draw, el_copy, opacity_factor=opacity)
        cx = int(el.get("x", 0)) + int(el.get("w", el.get("r", 50))) // 2
        cy = int(el.get("y", 0)) + int(el.get("h", el.get("r", 50))) // 2
        layer = layer.rotate(-rotate, center=(cx, cy), resample=Image.BICUBIC)
        img.paste(layer, (0, 0), layer)
        return ImageDraw.Draw(img)

    if opacity < 1.0 and etype not in ("gradient", "image"):
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        _apply_element(layer, ld, el, opacity_factor=opacity)
        img.paste(layer, (0, 0), layer)
    else:
        _apply_element(img, draw, el, opacity_factor=opacity)

    return ImageDraw.Draw(img)


# ------------------------------------------------------------------ #
# GENERATE & EXPORT                                                    #
# ------------------------------------------------------------------ #

def generate_from_spec(spec):
    """Genera imagen PIL de alta calidad desde JSON spec.
    Soporta supersampling global con 'antialias': 2 (render a 2x y downscale).
    """
    width  = max(1, int(spec.get("width",  800)))
    height = max(1, int(spec.get("height", 600)))
    bg_raw = spec.get("background", "#ffffff")
    ss = max(1, int(spec.get("antialias", 1)))  # 1=normal, 2=supersampled

    render_w, render_h = width * ss, height * ss
    img  = Image.new("RGBA", (render_w, render_h), parse_color(bg_raw, (255,255,255,255)))
    draw = ImageDraw.Draw(img)

    # Si supersampling, escalar todas las coordenadas y tamaños
    def scale_el(el):
        if ss == 1:
            return el
        scaled = dict(el)
        for k in ["x","y","w","h","r","x1","y1","x2","y2","size","fontSize",
                   "radius","rx","stroke_width","strokeWidth","width","thickness",
                   "padding_x","padding_y","px","py","shadow_x","shadow_y","shadow_blur",
                   "bg_padding","bg_radius","inner_r","letter_spacing","max_width",
                   "clip_radius","item_w","item_h","gap","gap_x","gap_y"]:
            if k in scaled:
                scaled[k] = int(float(scaled[k]) * ss)
        if "line_spacing" in scaled:
            scaled["line_spacing"] = int(float(scaled["line_spacing"]) * ss)
        if "spacing" in scaled and isinstance(scaled["spacing"], (int, float)):
            scaled["spacing"] = int(float(scaled["spacing"]) * ss)
        # Escalar stops de gradiente (no posiciones, solo colores)
        # Escalar text_gradient sizes si los tiene
        return scaled

    for el in spec.get("elements", []):
        try:
            etype = el.get("type", "")

            # ── Meta: grid ──────────────────────────────
            # Repite un template de elemento en grilla NxM
            if etype == "grid":
                cols = int(el.get("cols", 3))
                rows = int(el.get("rows", 1))
                x0 = int(el.get("x", 0))
                y0 = int(el.get("y", 0))
                gap_x = int(el.get("gap_x", el.get("gap", 10)))
                gap_y = int(el.get("gap_y", el.get("gap", 10)))
                items = el.get("items", [])
                item_w = int(el.get("item_w", 100))
                item_h = int(el.get("item_h", 100))
                template = el.get("template", {})
                idx = 0
                for row in range(rows):
                    for col in range(cols):
                        child = dict(template)
                        child["x"] = x0 + col * (item_w + gap_x)
                        child["y"] = y0 + row * (item_h + gap_y)
                        child["w"] = item_w
                        child["h"] = item_h
                        # Override con item-specific props si hay items
                        if idx < len(items):
                            child.update(items[idx])
                        draw = draw_element(img, draw, child)
                        idx += 1
                continue

            # ── Meta: repeat ────────────────────────────
            # Repite un elemento N veces con offset incremental
            if etype == "repeat":
                count = int(el.get("count", 5))
                dx = int(el.get("dx", 0))
                dy = int(el.get("dy", 0))
                d_opacity = float(el.get("d_opacity", 0))
                d_scale = float(el.get("d_scale", 0))
                child_tpl = el.get("element", {})
                for i in range(count):
                    child = dict(child_tpl)
                    child["x"] = int(child.get("x", 0)) + dx * i
                    child["y"] = int(child.get("y", 0)) + dy * i
                    if d_opacity:
                        child["opacity"] = max(0, min(1, float(child.get("opacity", 1)) + d_opacity * i))
                    if d_scale and "r" in child:
                        child["r"] = max(1, int(int(child["r"]) + d_scale * i))
                    draw = draw_element(img, draw, child)
                continue

            # ── Convenience: center_x / center_y ────────
            if el.get("center_x"):
                ew = int(el.get("w", el.get("r", 0)) * 2 if el.get("r") else el.get("w", 0))
                el["x"] = (width - ew) // 2
            if el.get("center_y"):
                eh = int(el.get("h", el.get("r", 0)) * 2 if el.get("r") else el.get("h", 0))
                el["y"] = (height - eh) // 2

            draw = draw_element(img, draw, scale_el(el))
        except Exception as e:
            print(f"[engine] Error en elemento {el.get('type')}: {e}")

    # Downscale si supersampling
    if ss > 1:
        img = img.resize((width, height), Image.LANCZOS)

    return img


def export_image(img, fmt="webp", quality=92):
    """
    Exporta imagen PIL a buffer.
    Siempre renderiza en RGBA → convierte según formato.
    quality 1-100, default 92 para buena calidad.
    """
    buf = io.BytesIO()
    fmt = (fmt or "webp").lower().strip()

    quality = max(1, min(100, int(quality)))

    if fmt in ("jpg", "jpeg"):
        out = img.convert("RGB")
        out.save(buf, format="JPEG", quality=quality, optimize=True,
                 subsampling=0 if quality >= 90 else 2)  # subsampling=0 = mejor calidad
        mime, ext = "image/jpeg", "jpg"
    elif fmt == "png":
        img.save(buf, format="PNG", optimize=True)
        mime, ext = "image/png", "png"
    else:  # webp (default)
        img.save(buf, format="WEBP", quality=quality, method=4,
                 lossless=(quality == 100))
        mime, ext = "image/webp", "webp"

    buf.seek(0)
    return buf, mime, ext
