"""
Script para crear una carpeta limpia solo con los archivos para Vercel.
Esta carpeta se puede subir directamente a un repo nuevo de GitHub.
"""

import os
import shutil

# Rutas
ORIGEN_HTML = "static/descuento.html"
DESTINO_DIR = "repo-vercel"
DESTINO_HTML = os.path.join(DESTINO_DIR, "index.html")
DESTINO_VERCEL_JSON = os.path.join(DESTINO_DIR, "vercel.json")

# Limpiar carpeta anterior si existe
if os.path.exists(DESTINO_DIR):
    shutil.rmtree(DESTINO_DIR)
    print(f"[OK] Carpeta anterior eliminada")

# Crear carpeta nueva
os.makedirs(DESTINO_DIR)
print(f"[OK] Carpeta '{DESTINO_DIR}' creada")

# Copiar HTML como index.html
if os.path.exists(ORIGEN_HTML):
    shutil.copy2(ORIGEN_HTML, DESTINO_HTML)
    print(f"[OK] HTML copiado como index.html")
else:
    print(f"[ERROR] No se encontro {ORIGEN_HTML}")
    exit(1)

# Crear vercel.json
vercel_config = """{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}"""
with open(DESTINO_VERCEL_JSON, 'w', encoding='utf-8') as f:
    f.write(vercel_config)
print(f"[OK] vercel.json creado")

# Crear README para el repo
readme_content = """# Calculadora de Descuento QR

HTML estático para calcular descuentos del 5%.

## Despliegue en Vercel

Este proyecto se despliega automáticamente en Vercel.

URL: https://tu-proyecto.vercel.app/
"""
with open(os.path.join(DESTINO_DIR, "README.md"), 'w', encoding='utf-8') as f:
    f.write(readme_content)
print(f"[OK] README.md creado")

print(f"\n" + "="*60)
print(f"Carpeta lista: {os.path.abspath(DESTINO_DIR)}")
print(f"="*60)
print(f"\nContenido:")
print(f"  - index.html")
print(f"  - vercel.json")
print(f"  - README.md")
print(f"\nSiguiente paso:")
print(f"  1. Crea un repositorio NUEVO en GitHub")
print(f"  2. Sube SOLO el contenido de la carpeta '{DESTINO_DIR}'")
print(f"  3. Conecta el repo a Vercel")
print(f"  4. Deploy automatico!")
print(f"\nIMPORTANTE: Sube solo estos 3 archivos, NO la carpeta completa")

