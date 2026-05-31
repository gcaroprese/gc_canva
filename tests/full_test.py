"""Test completo de TODOS los templates - verifica cada uno."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates_lib import *
from engine import generate_from_spec, export_image
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), "output", "final")
os.makedirs(OUT, exist_ok=True)
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

tests = {
    "01_inforket_blog": blog_dark_split(
        title="10 Estrategias SEO\nque Funcionan en 2026",
        subtitle="Guia completa para posicionar tu sitio web",
        accent="#7c6bf5", bg_photo=os.path.join(A,"coding_screen2.jpg"),
        brand="inforket.com"),

    "02_pawsitive_blog": blog_photo_hero(
        title="5 Organic Teas\nYour Dog Will Love",
        subtitle="Natural blends safe and healthy for your pup",
        accent="#8fbc8f", photo=os.path.join(A,"tea_dark_bg.jpg"),
        brand="pawsitivebrews.com"),

    "03_gabriel_blog": blog_dark_split(
        title="Diseno Digital\ny Marketing Creativo",
        subtitle="Estrategias para hacer crecer tu marca",
        accent="#c9a227", brand="gabrielcaroprese.com"),

    "04_realestate": blog_photo_hero(
        title="Departamento Premium\nen Palermo",
        subtitle="3 ambientes | 95m2 | USD 245,000",
        accent="#c9a227", photo=os.path.join(A,"house_full.jpg"),
        brand="Premium Properties"),

    "05_inforket_dashboard": dashboard_card(accent="#7c6bf5"),

    "06_pawsitive_product": product_showcase(
        product_image=os.path.join(A,"green_tea_nobg.webp"),
        accent="#8fbc8f", bg_tint="#0a100a"),

    "07_iglesia": church_post(
        verse="La fe mueve\nmontanas",
        reference="Mateo 17:20",
        church_name="Iglesia de la Gracia",
        accent="#c9a227",
        bg_photo=os.path.join(A,"church_light.jpg")),

    "08_etsy_dogs": etsy_listing(
        title_lines=["BEST","DOG MOM","EVER"],
        price="$24.99", accent="#3d2314"),

    "09_quote": quote_card(
        quote="El marketing no es sobre\nlo que vendes, es sobre\nla historia que contas",
        author="Gabriel Caroprese",
        accent="#c9a227"),

    "10_stats": stats_banner(
        stats=[
            {"value":"+340%","label":"Trafico","color":"#22c55e"},
            {"value":"2.4K","label":"Leads","color":"#f59e0b"},
            {"value":"98%","label":"Satisfaccion","color":"#7c6bf5"},
            {"value":"24/7","label":"Soporte","color":"#ef4444"},
        ], accent="#7c6bf5"),

    "11_features": feature_grid(accent="#7c6bf5"),

    "12_brand": minimal_brand(
        name="INFORKET",
        tagline="Marketing Digital que Funciona",
        accent="#7c6bf5"),
}

print("=" * 55)
for name, spec in tests.items():
    img = generate_from_spec(spec)
    # Verificar que no es solido
    ex = img.getextrema()
    if all(e[0] == e[1] for e in ex[:3]):
        print(f"  FAIL {name}: color solido")
        continue
    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    with open(os.path.join(OUT, f"{name}.webp"), "wb") as f:
        f.write(d)
    print(f"  OK   {name:30s} {len(d)//1024:4d}KB  {spec['width']}x{spec['height']}")
print("=" * 55)
