# GC Canva - Instrucciones para Claude

## Reglas obligatorias

1. **pawsitivebrews.com es de TE, NO cafe**
2. **Las imagenes de blog NO llevan texto** — los sitios son bilingues, la misma imagen se usa en varios idiomas
3. **Verificar CADA imagen** antes de mostrarla al usuario
4. **NO usar assets < 400px** — correr `python quality_check.py` si hay dudas
5. **NO dibujar objetos con Pillow** (tazas, perros, etc) — usar fotos reales con transparencia
6. **Las fotos tienen que VERSE** — opacity minimo 0.7, no tapar con overlays negros

## Como generar imagenes

### Para blog posts (sin texto):
```python
# Foto protagonista, sin texto, 1200x675
spec = {
    "width":1200,"height":675,"background":"dark","antialias":2,
    "post":{"vignette":True,"vignette_strength":0.25,"tint":"#7c6bf5","tint_strength":0.02,"grain":True,"grain_strength":3},
    "elements":[
        {"type":"image","src":"static/assets/images/FOTO.jpg","x":0,"y":0,"w":1200,"h":675,"opacity":0.85},
        {"type":"rect","x":0,"y":0,"w":1200,"h":3,"color":"#7c6bf5"},
    ]
}
```

### Para social/marketing (con texto):
```python
from templates_lib import blog_dark_split, stats_banner, quote_card, minimal_brand
spec = blog_dark_split(title="Titulo", subtitle="Sub", accent="#7c6bf5", brand="site.com")
```

### Para productos (sin texto):
```python
from templates_lib import product_showcase
spec = product_showcase(product_image="static/assets/images/green_tea_nobg.webp", accent="#8fbc8f")
```

## Templates disponibles (templates_lib.py)
- `blog_dark_split` — split texto/foto con glass card
- `blog_photo_hero` — foto fullscreen + texto centrado
- `dashboard_card` — analytics sin texto
- `product_showcase` — producto centrado con glow y contact_shadow
- `church_post` — verso + cruz dorada
- `etsy_listing` — producto tipografico con precios
- `quote_card` — cita/testimonial elegante
- `stats_banner` — metricas con glow coloreado
- `feature_grid` — grid de servicios
- `minimal_brand` — identidad de marca minimalista

## Sitios del usuario
- **inforket.com** — marketing digital (accent: #7c6bf5)
- **gabrielcaroprese.com** — marca personal (accent: #c9a227)
- **hattonnaturals.com** — productos naturales (accent: #5d8a5e)
- **pawsitivebrews.com** — TE + perros (accent: #8fbc8f) **NO ES CAFE**
- **Etsy** — remeras, productos para perros
- **Iglesias** (accent: #c9a227)
- **Real Estate** (accent: #c9a227)

## Buenos assets (static/assets/images/)
### Fotos de fondo (JPG, 1200x675):
coding_screen2, analytics_screen, team_meeting, seo_graph, social_media, content_writing, ecommerce_shop, startup_work, tea_dark_bg, tea_ceremony, dog_park, church_light, church_interior, house_full

### Con transparencia (_nobg.webp, _png.webp):
- Perros: dog_beagle_png (1903x3000), dog_happy2_png, dog_walk_png
- Te: green_tea_nobg (1000x1000)
- Tech: macbook_png (1327x716)
- Tazas: teacup2_hires_png (1600x1200)

## Engine features
- 17 elementos: rect, circle, ellipse, triangle, polygon, star, line, gradient, pill, divider, text, image, asset, arc, ring, grid, repeat, contact_shadow
- `"antialias": 2` — render 2x + LANCZOS downscale
- Post-processing: `"post": {"vignette":true, "tint":"#color", "grain":true}`
- `"contact_shadow"` — sombra realista con blur gaussiano
- `{"type":"asset","name":"nombre"}` — carga de static/assets/images/

## Herramientas de calidad
```bash
python quality_check.py          # auditar assets
python tests/blog_notext.py      # generar 15 blog images sin texto
python tests/full_test.py        # generar 12 templates con texto
python tests/auto_review.py      # analizar brillo/contraste/score
```

## NO hacer
- No poner texto en imagenes de blog (son bilingues)
- No usar fotos con opacity < 0.7 (se ven invisibles)
- No dibujar formas de Pillow para representar objetos reales
- No usar assets de baja resolucion
- No inventar que un asset es algo que no es (verificar visualmente)
