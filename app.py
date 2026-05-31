"""
GC Canva - Servidor Flask
Puerto: 5050
"""
import base64
import io
import json
import os
from flask import Flask, render_template, request, jsonify, send_file
from engine import generate_from_spec, export_image, list_available_fonts, get_font, LOCAL_FONTS_DIR
from PIL import Image, ImageEnhance, ImageFilter

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64MB

CANVAS_PRESETS = [
    {"name": "Post Cuadrado",          "w": 1080, "h": 1080, "cat": "Social"},
    {"name": "Instagram Story",         "w": 1080, "h": 1920, "cat": "Social"},
    {"name": "Twitter/X Post",          "w": 1200, "h": 675,  "cat": "Social"},
    {"name": "Twitter/X Header",        "w": 1500, "h": 500,  "cat": "Social"},
    {"name": "Facebook Cover",          "w": 820,  "h": 312,  "cat": "Social"},
    {"name": "Facebook Post",           "w": 1200, "h": 630,  "cat": "Social"},
    {"name": "LinkedIn Cover",          "w": 1584, "h": 396,  "cat": "Social"},
    {"name": "LinkedIn Post",           "w": 1200, "h": 627,  "cat": "Social"},
    {"name": "Pinterest Pin",           "w": 1000, "h": 1500, "cat": "Social"},
    {"name": "TikTok Video",            "w": 1080, "h": 1920, "cat": "Video"},
    {"name": "YouTube Thumbnail",       "w": 1280, "h": 720,  "cat": "Video"},
    {"name": "YouTube Banner",          "w": 2560, "h": 1440, "cat": "Video"},
    {"name": "YouTube Short",           "w": 1080, "h": 1920, "cat": "Video"},
    {"name": "Presentacion 16:9",       "w": 1920, "h": 1080, "cat": "Presentacion"},
    {"name": "Presentacion 4:3",        "w": 1024, "h": 768,  "cat": "Presentacion"},
    {"name": "Presentacion Cuadrada",   "w": 1080, "h": 1080, "cat": "Presentacion"},
    {"name": "OG Image / Blog",         "w": 1200, "h": 630,  "cat": "Web"},
    {"name": "Banner Web 728x90",       "w": 728,  "h": 90,   "cat": "Web"},
    {"name": "Banner Web 300x250",      "w": 300,  "h": 250,  "cat": "Web"},
    {"name": "Banner Web 970x250",      "w": 970,  "h": 250,  "cat": "Web"},
    {"name": "Hero Web",                "w": 1440, "h": 500,  "cat": "Web"},
    {"name": "Tarjeta Personal",        "w": 1050, "h": 600,  "cat": "Print"},
    {"name": "Flyer A5 Vertical",       "w": 1748, "h": 2480, "cat": "Print"},
    {"name": "Flyer A5 Horizontal",     "w": 2480, "h": 1748, "cat": "Print"},
    {"name": "A4 Vertical",             "w": 1754, "h": 2480, "cat": "Print"},
    {"name": "A4 Horizontal",           "w": 2480, "h": 1754, "cat": "Print"},
    {"name": "Etsy Listing Photo",      "w": 2000, "h": 2000, "cat": "Etsy"},
    {"name": "Etsy Banner",             "w": 3360, "h": 840,  "cat": "Etsy"},
    {"name": "Etsy Shop Icon",          "w": 500,  "h": 500,  "cat": "Etsy"},
    {"name": "Blog Header",             "w": 1600, "h": 840,  "cat": "Blog"},
    {"name": "Blog Featured Image",     "w": 1200, "h": 628,  "cat": "Blog"},
    {"name": "Email Header",            "w": 600,  "h": 200,  "cat": "Email"},
    {"name": "Personalizado",           "w": 800,  "h": 600,  "cat": ""},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/presets")
def presets():
    return jsonify(CANVAS_PRESETS)


@app.route("/api/fonts")
def fonts():
    """Lista todas las fuentes disponibles en el proyecto."""
    available = list_available_fonts()
    return jsonify(available)


@app.route("/api/preview", methods=["POST"])
def preview():
    """Genera preview base64 desde JSON spec."""
    spec = request.get_json(force=True)
    if not spec:
        return jsonify({"error": "JSON invalido"}), 400
    try:
        img = generate_from_spec(spec)
        fmt = spec.get("format", "webp")
        quality = int(spec.get("quality", 85))
        buf, mime, _ = export_image(img, fmt, quality)
        b64 = base64.b64encode(buf.read()).decode()
        return jsonify({"image": b64, "mime": mime})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/download", methods=["POST"])
def download():
    """Descarga imagen desde JSON spec con alta calidad."""
    spec = request.get_json(force=True)
    if not spec:
        return jsonify({"error": "JSON invalido"}), 400
    try:
        img = generate_from_spec(spec)
        fmt = spec.get("format", "webp")
        quality = int(spec.get("quality", 92))
        buf, mime, ext = export_image(img, fmt, quality)
        name = (spec.get("filename") or "diseno").strip() or "diseno"
        return send_file(buf, mimetype=mime, as_attachment=True,
                         download_name=f"{name}.{ext}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/qr", methods=["POST"])
def qr_code():
    try:
        import qrcode
    except ImportError:
        return jsonify({"error": "qrcode no disponible"}), 501

    data = request.get_json(force=True)
    text = str(data.get("text", ""))
    size = max(100, min(1000, int(data.get("size", 300))))
    fg = str(data.get("color", "#000000"))
    bg = str(data.get("bg_color", "#ffffff"))

    if not text:
        return jsonify({"error": "Texto vacio"}), 400

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10, border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg)
    img = img.resize((size, size), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    return jsonify({"image": b64, "mime": "image/png"})


@app.route("/api/remove-bg", methods=["POST"])
def remove_bg():
    try:
        from rembg import remove as rembg_remove
    except ImportError:
        return jsonify({
            "error": "rembg no instalado. Ejecuta: venv\\Scripts\\pip install rembg"
        }), 501

    if "image" not in request.files:
        return jsonify({"error": "No se encontro imagen"}), 400

    try:
        input_bytes = request.files["image"].read()
        output_bytes = rembg_remove(input_bytes)
        b64 = base64.b64encode(output_bytes).decode()
        return jsonify({"image": b64, "mime": "image/png"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/filter", methods=["POST"])
def apply_filter():
    data = request.get_json(force=True)
    image_b64 = data.get("image", "")
    filters = data.get("filters", {})

    if not image_b64:
        return jsonify({"error": "No se recibio imagen"}), 400

    try:
        raw = base64.b64decode(image_b64.split(",")[-1])
        img = Image.open(io.BytesIO(raw)).convert("RGBA")
        alpha = img.split()[3]
        rgb = img.convert("RGB")

        if "brightness" in filters:
            rgb = ImageEnhance.Brightness(rgb).enhance(float(filters["brightness"]))
        if "contrast" in filters:
            rgb = ImageEnhance.Contrast(rgb).enhance(float(filters["contrast"]))
        if "saturation" in filters:
            rgb = ImageEnhance.Color(rgb).enhance(float(filters["saturation"]))
        if "sharpness" in filters:
            rgb = ImageEnhance.Sharpness(rgb).enhance(float(filters["sharpness"]))
        if float(filters.get("blur", 0)) > 0:
            rgb = rgb.filter(ImageFilter.GaussianBlur(radius=float(filters["blur"])))
        if filters.get("grayscale"):
            rgb = rgb.convert("L").convert("RGB")
        if filters.get("sepia"):
            pixels = list(rgb.getdata())
            sepia = [(min(255, int(p[0]*.393+p[1]*.769+p[2]*.189)),
                      min(255, int(p[0]*.349+p[1]*.686+p[2]*.168)),
                      min(255, int(p[0]*.272+p[1]*.534+p[2]*.131))) for p in pixels]
            rgb2 = Image.new("RGB", rgb.size)
            rgb2.putdata(sepia)
            rgb = rgb2
        if filters.get("invert"):
            from PIL import ImageOps
            rgb = ImageOps.invert(rgb)

        out = rgb.convert("RGBA")
        out.putalpha(alpha)
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()
        return jsonify({"image": b64, "mime": "image/png"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 55)
    print("  GC Canva - http://localhost:5050")
    print(f"  Fuentes disponibles: {len(list_available_fonts())}")
    print("=" * 55)
    app.run(debug=True, port=5050, host="0.0.0.0")
