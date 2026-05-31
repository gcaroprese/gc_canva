# GC Canva - Documentacion

## Inicio rapido

```bash
# Ventana nativa
start.bat

# En browser
venv\Scripts\python app.py
# → http://localhost:5050
```

## Dos modos de uso

### 1. Editor Visual (Fabric.js)
Canvas interactivo: seleccionar, texto, rect, circulo, triangulo, linea, flecha, estrella, poligono, diamante. Panel de propiedades, iconos SVG, backgrounds, exportacion.

### 2. Claude JSON Mode (Pillow)
JSON spec compacto → imagen server-side de alta calidad. Bajo consumo de tokens. 84 fuentes. Sombras con blur, gradientes multi-stop, opacidades, rotacion.

## JSON Spec - Referencia

```json
{
  "width": 1200, "height": 630,
  "background": "dark",
  "format": "webp", "quality": 92,
  "elements": [
    {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"color1":"accent","color2":"dark","direction":"diagonal"},
    {"type":"pill","x":60,"y":60,"text":"NUEVO","color":"accent"},
    {"type":"text","text":"Titulo","x":600,"y":280,"size":72,"color":"white","align":"center","bold":true,"font":"mukta","shadow":true,"shadow_blur":8}
  ]
}
```

### Elementos

| Tipo | Props |
|------|-------|
| rect | x,y,w,h,color,radius,opacity,stroke,stroke_width,rotate,**shadow**,shadow_color,shadow_blur,shadow_x,shadow_y |
| circle | x,y,r,color,opacity,**shadow**,shadow_color,shadow_blur |
| ellipse | x,y,w,h,color,opacity,**shadow** |
| triangle | x,y,w,h,color,rotate |
| polygon | x,y,r,sides,angle,color,rotate |
| star | x,y,r,inner_r,points,color,rotate,**shadow** |
| line | x1,y1,x2,y2,color,width |
| gradient | x,y,w,h,color1,color2,direction,stops,**angle** |
| pill | x,y,text,color,text_color,size,font,px,py,radius,align,**shadow** |
| text | x,y,text,size,color,font,bold,italic,align,valign,shadow,shadow_blur,text_stroke,max_width,bg_color,bg_padding,bg_radius,spacing |
| image | src(base64 o path local),x,y,w,h,rotate |

### Shadow universal

Todas las formas aceptan shadow:
```json
{"type":"rect","x":60,"y":80,"w":320,"h":200,"color":"#1a1a30","radius":16,
 "shadow":true,"shadow_color":"#00000060","shadow_blur":20,"shadow_x":0,"shadow_y":8}
```
Para efecto glow usar shadow_color con el color del acento: `"shadow_color":"#7c6bf540"`

### Gradiente con angulo

```json
{"type":"gradient","x":0,"y":0,"w":1200,"h":630,
 "stops":[[0,"cyan"],[0.33,"blue"],[0.66,"purple"],[1,"pink"]],
 "angle":135}
```
Angulo en grados (0=derecha, 90=abajo, 135=diagonal inferior-derecha). Compatible con multi-stop.

### Gradientes multi-stop

```json
{"type":"gradient","x":0,"y":0,"w":1200,"h":630,
 "stops":[[0,"#0f0524"],[0.4,"#1e1b4b"],[0.7,"#312e81"],[1,"#1e1b4b"]],
 "direction":"diagonal"}
```
Direcciones: horizontal, vertical, diagonal, radial. Soporta 2+ colores con posiciones 0.0-1.0.

### Pill / Badge

```json
{"type":"pill","x":60,"y":60,"text":"NUEVO","color":"accent","text_color":"white","size":14,"font":"bahnschrift"}
```
Auto-sizing: calcula ancho segun texto. Padding y radio configurables.

### Text features

```json
{"type":"text","text":"Titulo","x":600,"y":300,"size":72,"color":"white",
 "align":"center","valign":"center",
 "shadow":true,"shadow_blur":12,"shadow_color":"#7c6bf540",
 "bg_color":"#7c6bf530","bg_padding":8,"bg_radius":6,
 "max_width":500,
 "text_stroke":true,"text_stroke_color":"accent","text_stroke_width":2}
```

### Rotacion

Cualquier forma acepta `"rotate": 15` (grados). Se rota alrededor del centro del elemento.

### Colores con nombre

white, black, red, green, blue, yellow, orange, purple, pink, gold, silver, brown, navy, teal, cyan, lime, indigo, violet, accent(#7c6bf5), dark(#0c0c14), light(#f8f9fa), transparent

### Fuentes

**Sans:** arial, calibri, mukta, segoe ui, tahoma, verdana, bahnschrift, candara, corbel, trebuchet ms
**Serif:** georgia, times, roboto slab, optimus princeps, rockwell
**Display:** impact, cooper black, moon bold, moon light, narnia, rakoon
**Mono:** consolas, courier new
**Script:** gabriola

## API

| Ruta | Metodo | Uso |
|------|--------|-----|
| /api/preview | POST | Preview base64 desde JSON spec |
| /api/download | POST | Descarga imagen desde JSON spec |
| /api/qr | POST | QR code (text,size,color,bg_color) |
| /api/remove-bg | POST | Quitar fondo (requiere rembg) |
| /api/filter | POST | Filtros (brightness,contrast,saturation,blur,grayscale,sepia) |
| /api/fonts | GET | Fuentes disponibles |
| /api/presets | GET | Presets de canvas |

## Presets (32)

Social (Post, Story, Twitter, Facebook, LinkedIn, Pinterest), Video (TikTok, YouTube, Shorts), Presentacion (16:9, 4:3), Web (OG, Banners, Hero), Print (Tarjeta, Flyer, A4), Etsy, Blog, Email

## Plantillas AI (12)

Social Elegante, YouTube Thumb, Blog Inforket, Blog Gabriel, Hatton Naturals, Pawsitive Brews, Etsy Perros, Etsy Remera, Iglesia Post, Real Estate, Banner Tech, Tarjeta Personal

## Shortcuts

V=Select T=Texto R=Rect C=Circulo L=Linea Del=Borrar
Ctrl+Z/Y Ctrl+C/V Ctrl+D Ctrl+G Ctrl+A
Flechas=1px Shift+Flechas=10px Alt+Drag=Pan Scroll=Zoom

## Performance

~250ms generacion, ~650ms export WebP. ~42KB promedio por imagen 1200x630.
WebP q92: 50% menor que PNG, 40% menor que JPG, calidad identica.

## Instalacion

```bash
python -m venv venv
venv\Scripts\pip install flask pillow "qrcode[pil]" pywebview
python setup_fonts.py  # copiar fuentes de Windows
```
