import re
import base64
import os

# Nombre del archivo HTML de entrada
INPUT_FILE = "studio-atik-34-9.html"
OUTPUT_FILE = "studio-atik-limpio.html"
IMG_FOLDER = "img"

# Crear carpeta de imágenes si no existe
os.makedirs(IMG_FOLDER, exist_ok=True)

# Leer el HTML
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    html = f.read()

counter = 0

def replace_base64(match):
    global counter
    mime_type = match.group(1)  # jpeg, png, webp, etc.
    data = match.group(2)

    # Determinar extensión
    ext_map = {
        "jpeg": "jpg",
        "jpg": "jpg",
        "png": "png",
        "webp": "webp",
        "gif": "gif",
        "svg+xml": "svg"
    }
    ext = ext_map.get(mime_type, "jpg")

    # Nombre del archivo
    counter += 1
    filename = f"img_{counter:03d}.{ext}"
    filepath = os.path.join(IMG_FOLDER, filename)

    # Guardar imagen
    try:
        img_data = base64.b64decode(data)
        with open(filepath, "wb") as f:
            f.write(img_data)
        print(f"  Guardada: {filepath}")
    except Exception as e:
        print(f"  Error en imagen {counter}: {e}")
        return match.group(0)  # dejar el original si falla

    return f"img/{filename}"

# Buscar y reemplazar todos los base64 de imágenes
pattern = r'data:image/([a-zA-Z+]+);base64,([A-Za-z0-9+/=]+)'
html_nuevo = re.sub(pattern, replace_base64, html)

# Guardar HTML limpio
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_nuevo)

print(f"\n✅ Listo. {counter} imágenes extraídas a la carpeta /{IMG_FOLDER}")
print(f"✅ HTML limpio guardado como: {OUTPUT_FILE}")
