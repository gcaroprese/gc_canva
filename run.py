"""
GC Canva - Lanzador con ventana nativa (pywebview)
Abre el editor como una aplicacion de escritorio.
"""
import os
import threading
import webview
from app import app

ICON_PATH = os.path.join(os.path.dirname(__file__), "static", "icon.ico")

def start_flask():
    app.run(debug=False, port=5050, host="127.0.0.1", use_reloader=False)

if __name__ == "__main__":
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()

    webview.create_window(
        "GC Canva",
        "http://127.0.0.1:5050",
        width=1400,
        height=900,
        resizable=True,
        min_size=(900, 600),
    )
    webview.start(icon=ICON_PATH)
