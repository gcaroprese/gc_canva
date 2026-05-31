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

def make_gradient(w, h, c1, c2, direction="horizontal"):
    """Gradiente lineal eficiente. c1/c2 son tuplas RGBA."""
    w, h = max(1, int(w)), max(1, int(h))
    if direction == "horizontal":
        base = Image.new("RGBA", (w, 1))
        d = ImageDraw.Draw(base)
        for x in range(w):
            t = x / max(w-1, 1)
            col = tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(4))
            d.point((x, 0), fill=col)
        return base.resize((w, h), Image.NEAREST)
    elif direction == "vertical":
        base = Image.new("RGBA", (1, h))
        d = ImageDraw.Draw(base)
        for y in range(h):
            t = y / max(h-1, 1)
            col = tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(4))
            d.point((0, y), fill=col)
        return base.resize((w, h), Image.NEAREST)
    elif direction == "radial":
        import math
        img = Image.new("RGBA", (w, h), c2)
        draw = ImageDraw.Draw(img)
        cx, cy = w / 2, h / 2
        maxR = math.sqrt(cx ** 2 + cy ** 2)
        steps = min(512, max(100, int(maxR / 2)))
        for i in range(steps, -1, -1):
            t = i / steps
            r = maxR * t
            col = tuple(int(c1[j] * (1 - t) + c2[j] * t) for j in range(4))
            if r > 0:
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        return img
    else:  # diagonal - verdadero gradiente esquina a esquina
        total = w + h - 1
        colors = []
        for i in range(total):
            t = i / max(total - 1, 1)
            colors.append(tuple(int(c1[j] * (1 - t) + c2[j] * t) for j in range(4)))
        img = Image.new("RGBA", (w, h))
        pixels = []
        for y in range(h):
            for x in range(w):
                pixels.append(colors[x + y])
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
        draw.ellipse(box, fill=fill, outline=stroke, width=sw if stroke else 0)

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
        pts = []
        for i in range(points*2):
            a = math.radians(-90 + 180*i/points)
            r_i = outer if i % 2 == 0 else inner
            pts.append((cx + r_i*math.cos(a), cy + r_i*math.sin(a)))
        draw.polygon(pts, fill=fill)

    elif etype == "line":
        x1,y1 = int(el.get("x1",0)), int(el.get("y1",0))
        x2,y2 = int(el.get("x2",100)), int(el.get("y2",0))
        col   = c("color", "#000000")
        w_    = int(el.get("width", el.get("stroke_width", 2)))
        draw.line([(x1,y1),(x2,y2)], fill=col, width=w_)

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
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pw, ph = tw + pad_x * 2, th + pad_y * 2
        radius = int(el.get("radius", ph // 2))
        # Si align=center, centrar el pill en x
        pill_x = x - pw // 2 if el.get("align") == "center" else x
        pill_y = y
        draw_rounded_rect(draw, pill_x, pill_y, pw, ph, radius, bg)
        draw.text((pill_x + pad_x, pill_y + pad_y), text, font=font, fill=tc)

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
        max_width = el.get("max_width")  # auto-wrap si se especifica

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

        # Stroke/outline on text (circular para suavidad)
        if el.get("text_stroke"):
            import math
            tcol   = parse_color(el.get("text_stroke_color", "#000000"))
            t_sw   = int(el.get("text_stroke_width", 2))
            steps  = max(12, t_sw * 8)
            for i in range(steps):
                angle = 2 * math.pi * i / steps
                dx = t_sw * math.cos(angle)
                dy = t_sw * math.sin(angle)
                draw.multiline_text((draw_x + dx, draw_y + dy), text, font=font, fill=tcol,
                                    align=align, spacing=spacing)

        draw.multiline_text((draw_x, draw_y), text, font=font, fill=col, align=align, spacing=spacing)

    elif etype == "gradient":
        gx, gy = int(el.get("x",0)), int(el.get("y",0))
        gw = int(el.get("w", img.width))
        gh = int(el.get("h", img.height))
        c1 = parse_color(el.get("color1", "#000000"))
        c2 = parse_color(el.get("color2", "#ffffff"))
        direction = el.get("direction", "horizontal")
        grad = make_gradient(gw, gh, c1, c2, direction)
        if opacity_factor < 1.0:
            a = grad.split()[3].point(lambda p: int(p*opacity_factor))
            grad.putalpha(a)
        img.paste(grad, (gx, gy), grad)

    elif etype == "image":
        # Embed external/base64 image into the spec (for server-side use)
        src = el.get("src", "")
        if src.startswith("data:"):
            import base64
            header, b64data = src.split(",", 1)
            raw = base64.b64decode(b64data)
            try:
                src_img = Image.open(io.BytesIO(raw)).convert("RGBA")
                x, y = int(el.get("x",0)), int(el.get("y",0))
                w = int(el.get("w", src_img.width))
                h = int(el.get("h", src_img.height))
                if w != src_img.width or h != src_img.height:
                    src_img = src_img.resize((w, h), Image.LANCZOS)
                if opacity_factor < 1.0:
                    alpha = src_img.split()[3].point(lambda p: int(p*opacity_factor))
                    src_img.putalpha(alpha)
                img.paste(src_img, (x, y), src_img)
            except Exception as e:
                print(f"[engine] Error cargando imagen embebida: {e}")


def draw_element(img, draw, el):
    opacity = float(el.get("opacity", 1.0))
    if opacity <= 0:
        return draw

    etype = el.get("type","")
    if opacity < 1.0 and etype not in ("gradient", "image"):
        layer = Image.new("RGBA", img.size, (0,0,0,0))
        ld = ImageDraw.Draw(layer)
        _apply_element(img, ld, el, opacity_factor=opacity)
        img.paste(layer, (0,0), layer)
    else:
        _apply_element(img, draw, el, opacity_factor=opacity)

    return ImageDraw.Draw(img)  # draw might be invalidated after paste


# ------------------------------------------------------------------ #
# GENERATE & EXPORT                                                    #
# ------------------------------------------------------------------ #

def generate_from_spec(spec):
    """Genera imagen PIL de alta calidad desde JSON spec."""
    width  = max(1, int(spec.get("width",  800)))
    height = max(1, int(spec.get("height", 600)))
    bg_raw = spec.get("background", "#ffffff")

    img  = Image.new("RGBA", (width, height), parse_color(bg_raw, (255,255,255,255)))
    draw = ImageDraw.Draw(img)

    for el in spec.get("elements", []):
        try:
            draw = draw_element(img, draw, el)
        except Exception as e:
            print(f"[engine] Error en elemento {el.get('type')}: {e}")

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
