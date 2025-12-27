"""
Script para preparar la carpeta para desplegar en Vercel.
Copia el HTML estático a una carpeta lista para subir.
"""

import os
import shutil

# Rutas
ORIGEN = "static/descuento.html"
DESTINO_DIR = "vercel-deploy"
DESTINO_HTML = os.path.join(DESTINO_DIR, "index.html")

# Crear carpeta de destino
if not os.path.exists(DESTINO_DIR):
    os.makedirs(DESTINO_DIR)
    print(f"[OK] Carpeta '{DESTINO_DIR}' creada")

# Copiar HTML
if os.path.exists(ORIGEN):
    shutil.copy2(ORIGEN, DESTINO_HTML)
    print(f"[OK] HTML copiado a '{DESTINO_HTML}'")
    print(f"\nCarpeta lista para Vercel: {os.path.abspath(DESTINO_DIR)}")
    print(f"   Contiene: index.html")
    print(f"\nSiguiente paso:")
    print(f"   1. Sube la carpeta '{DESTINO_DIR}' a un repo de GitHub")
    print(f"   2. O arrastrala directamente a Vercel")
    print(f"   3. Tu URL sera: https://tu-proyecto.vercel.app/")
else:
    print(f"[ERROR] No se encontro {ORIGEN}")

