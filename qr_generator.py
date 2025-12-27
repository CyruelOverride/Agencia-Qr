"""
Módulo para generar códigos QR para restaurantes/comercios.
Genera imágenes QR que apuntan a URLs dinámicas.
"""

import qrcode
import os
from typing import List

# Carpeta donde se guardan los QRs
QR_CODES_DIR = "qr_codes"

# IDs de todos los restaurantes y comercios de AGENCIA
RESTAURANTES_COMERCIOS = [
    "rest_001", "rest_002", "rest_003", "rest_004", "rest_005",
    "com_001", "com_002", "com_003"
]


def generar_qr(restaurant_id: str, base_url: str = None, usar_html_estatico: bool = True) -> str:
   
    if not os.path.exists(QR_CODES_DIR):
        os.makedirs(QR_CODES_DIR)
    
    if usar_html_estatico:
        if base_url:
            url = f"{base_url}/descuento.html" if base_url.endswith('/') else f"{base_url}/descuento.html"
        else:
            url = "./descuento.html"
    else:
        if base_url is None:
            base_url = "http://localhost:8000"
        url = f"{base_url}/{restaurant_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"{restaurant_id}.png"
    filepath = os.path.join(QR_CODES_DIR, filename)
    img.save(filepath)
    
    return filepath


def generar_todos_los_qr(base_url: str = "http://localhost:8000") -> List[str]:
    
    rutas_generadas = []
    
    for restaurant_id in RESTAURANTES_COMERCIOS:
        try:
            ruta = generar_qr(restaurant_id, base_url)
            rutas_generadas.append(ruta)
            print(f"✓ QR generado para {restaurant_id}: {ruta}")
        except Exception as e:
            print(f"✗ Error al generar QR para {restaurant_id}: {e}")
    
    return rutas_generadas

