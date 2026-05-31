"""Copia fuentes de Windows al proyecto (correr una sola vez)."""
import os, shutil

SRC_DIRS = [
    "C:/Windows/Fonts",
    os.path.expandvars("%LOCALAPPDATA%/Microsoft/Windows/Fonts"),
]
DST = os.path.join(os.path.dirname(__file__), "static", "fonts")
os.makedirs(DST, exist_ok=True)

FONTS = [
    "arial.ttf","arialbd.ttf","ariali.ttf","arialbi.ttf","ariblk.ttf",
    "bahnschrift.ttf","calibri.ttf","calibrib.ttf","calibrii.ttf","calibril.ttf",
    "Candara.ttf","Candarab.ttf","Candarai.ttf","cambriab.ttf","cambriai.ttf",
    "comic.ttf","comicbd.ttf","consola.ttf","consolab.ttf","consolai.ttf",
    "corbel.ttf","corbelb.ttf","corbeli.ttf","cour.ttf","courbd.ttf",
    "framd.ttf","framdit.ttf","Gabriola.ttf",
    "georgia.ttf","georgiab.ttf","georgiai.ttf","georgiaz.ttf",
    "impact.ttf","tahoma.ttf","tahomabd.ttf",
    "trebuc.ttf","trebucbd.ttf","trebucbi.ttf","trebucit.ttf",
    "verdana.ttf","verdanab.ttf","verdanai.ttf","verdanaz.ttf",
    "times.ttf","timesbd.ttf","timesbi.ttf","timesi.ttf",
    "segoeui.ttf","segoeuib.ttf","segoeuii.ttf","segoeuil.ttf","segoeuiz.ttf",
    "ROCK.TTF","Rockwell-Bold.ttf",
]

copied = 0
for fname in FONTS:
    if os.path.exists(os.path.join(DST, fname)):
        continue
    for src_dir in SRC_DIRS:
        src = os.path.join(src_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DST, fname))
            copied += 1
            break

print(f"Copiadas {copied} fuentes a {DST}")
print(f"Total: {len([f for f in os.listdir(DST) if f.endswith(('.ttf','.otf'))])} fuentes")
