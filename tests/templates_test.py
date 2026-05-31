"""Testea todos los templates con validacion de calidad."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates_lib import blog_dark_split, blog_photo_hero, dashboard_card, product_showcase
from engine import generate_from_spec, export_image

OUT = os.path.join(os.path.dirname(__file__), "output")
A = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "assets", "images")

tests = {
    # Inforket - blog post dark split
    "tpl_inforket_split": blog_dark_split(
        title="10 Estrategias SEO\nque Funcionan Hoy",
        subtitle="Guia completa para posicionar tu sitio en los primeros resultados",
        accent="#7c6bf5",
        bg_photo=os.path.join(A, "coding_screen2.jpg"),
        brand="inforket.com",
    ),
    # Pawsitive - blog photo hero
    "tpl_pawsitive_hero": blog_photo_hero(
        title="5 Organic Teas\nYour Dog Will Love",
        subtitle="Discover the best natural blends that are safe and healthy for your pup",
        accent="#8fbc8f",
        photo=os.path.join(A, "tea_herbs.jpg"),
        brand="pawsitivebrews.com",
    ),
    # Inforket - dashboard sin texto
    "tpl_inforket_dash": dashboard_card(accent="#7c6bf5"),
    # Pawsitive - producto showcase sin texto
    "tpl_pawsitive_product": product_showcase(
        product_image=os.path.join(A, "green_tea_nobg.webp"),
        accent="#8fbc8f",
        bg_tint="#0a100a",
    ),
    # Hatton Naturals - producto
    "tpl_hatton_product": product_showcase(
        product_image=os.path.join(A, "lavender_bunch_nobg.webp"),
        accent="#5d8a5e",
        bg_tint="#0a0e0a",
    ),
    # Gabriel - blog dark split
    "tpl_gabriel_split": blog_dark_split(
        title="Diseno Digital\ny Marketing Creativo",
        subtitle="Estrategias probadas para hacer crecer tu marca en 2026",
        accent="#c9a227",
        brand="gabrielcaroprese.com",
    ),
    # Real Estate - photo hero
    "tpl_realestate_hero": blog_photo_hero(
        title="Departamento Premium\nen Palermo",
        subtitle="3 ambientes | 95m2 | Balcon con vista | USD 245,000",
        accent="#c9a227",
        photo=os.path.join(A, "house_full.jpg"),
        brand="Premium Properties",
    ),
}

print("=" * 55)
for name, spec in tests.items():
    img = generate_from_spec(spec)
    buf, _, _ = export_image(img, "webp", 95)
    d = buf.read()
    with open(os.path.join(OUT, f"{name}.webp"), "wb") as f:
        f.write(d)
    print(f"  {name:30s} {len(d)//1024:4d}KB")
print("=" * 55)
