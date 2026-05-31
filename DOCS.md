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
| circle | x,y,r,color,opacity,shadow,antialias(default true, 2x supersampled) |
| divider | x,y,w,color,thickness,text,text_color,font,size,direction(horizontal/vertical) |
| ellipse | x,y,w,h,color,opacity,**shadow** |
| triangle | x,y,w,h,color,rotate |
| polygon | x,y,r,sides,angle,color,rotate |
| star | x,y,r,inner_r,points,color,rotate,**shadow** |
| line | x1,y1,x2,y2,color,width |
| gradient | x,y,w,h,color1,color2,direction,stops,**angle** |
| pill | x,y,text,color,text_color,size,font,px,py,radius,align,shadow,**outline**,stroke,stroke_width |
| text | x,y,text,size,color,font,bold,italic,align,valign,shadow,shadow_blur,text_stroke,max_width,bg_color,bg_padding,bg_radius,spacing,text_gradient,**letter_spacing**,**uppercase** |
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

### Texto con gradiente

```json
{"type":"text","text":"TITULO","x":600,"y":100,"size":72,"align":"center","bold":true,"font":"impact",
 "text_gradient":{"color1":"#ff6b6b","color2":"#ffd93d"}}
```
Multi-stop: `"text_gradient":{"stops":[[0,"red"],[0.5,"yellow"],[1,"blue"]]}`
Con angulo: `"text_gradient":{"color1":"accent","color2":"cyan","angle":30}`
Compatible con shadow (la sombra se dibuja atras del gradiente).

### Image clip (recortar en forma)

```json
{"type":"image","src":"foto.jpg","x":100,"y":100,"w":300,"h":300,
 "clip":"circle"}
```
Valores de clip: `circle`, `rounded` (+ `clip_radius`), `ellipse`

### Auto-centrado

```json
{"type":"rect","w":200,"h":100,"color":"accent","center_x":true,"center_y":true}
```
`center_x` y `center_y` auto-calculan x/y para centrar el elemento en el canvas.

### Grid layout

```json
{"type":"grid","x":50,"y":50,"cols":4,"rows":1,"gap":20,"item_w":260,"item_h":140,
 "template":{"type":"rect","color":"#14142a","radius":14,"shadow":true},
 "items":[{"color":"#14142a"},{"color":"#1a1a30"}]}
```
Genera N elementos en grilla. `template` define la forma base, `items` override por posicion.

### Repeat

```json
{"type":"repeat","count":6,"dx":60,"dy":0,"d_opacity":-0.15,
 "element":{"type":"circle","x":100,"y":300,"r":20,"color":"accent","opacity":0.9}}
```
Repite un elemento N veces con offset incremental. `d_opacity` y `d_scale` para degradado.

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
