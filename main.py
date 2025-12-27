"""
Aplicación FastAPI principal para el sistema QR de descuentos.
Maneja endpoints para visitas, cálculo de descuentos y generación de QRs.
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from storage import incrementar_visita, get_visitas, inicializar_restaurante
from discounts import calcular_descuento, calcular_montos
from qr_generator import generar_qr, generar_todos_los_qr, RESTAURANTES_COMERCIOS

# Inicializar FastAPI
app = FastAPI(title="Sistema QR Descuentos", version="1.0.0")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Montar carpeta estática para QRs (opcional, para servir imágenes)
if os.path.exists("qr_codes"):
    app.mount("/qr_codes", StaticFiles(directory="qr_codes"), name="qr_codes")

# URL base (configurable)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Página de inicio con información del sistema."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema QR Descuentos</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🎯 Sistema QR Descuentos</h1>
        <p>Sistema de conteo de visitas y cálculo de descuentos para restaurantes y comercios.</p>
        <h2>Endpoints disponibles:</h2>
        <div class="endpoint">
            <strong>GET /{restaurant_id}</strong> - Escanear QR (incrementa visitas y muestra página de descuento)
        </div>
        <div class="endpoint">
            <strong>POST /calcular</strong> - Calcular descuento del 5%
        </div>
        <div class="endpoint">
            <strong>GET /qr/{restaurant_id}</strong> - Generar QR para un restaurante
        </div>
        <div class="endpoint">
            <strong>GET /qr/generar-todos</strong> - Generar todos los QRs
        </div>
        <h2>Restaurantes y Comercios:</h2>
        <ul>
            <li>rest_001, rest_002, rest_003, rest_004, rest_005</li>
            <li>com_001, com_002, com_003</li>
        </ul>
    </body>
    </html>
    """


@app.get("/{restaurant_id}", response_class=HTMLResponse)
async def visitar_restaurante(restaurant_id: str, request: Request):
    """
    Endpoint principal cuando se escanea un QR.
    Incrementa el contador de visitas y muestra la página de cálculo de descuento.
    
    Args:
        restaurant_id: ID del restaurante/comercio
        request: Request de FastAPI para el template
    """
    # Validar que el restaurante existe en la lista
    if restaurant_id not in RESTAURANTES_COMERCIOS:
        raise HTTPException(status_code=404, detail=f"Restaurante/comercio '{restaurant_id}' no encontrado")
    
    # Inicializar si no existe
    inicializar_restaurante(restaurant_id)
    
    # Incrementar visita
    visitas = incrementar_visita(restaurant_id)
    
    # Obtener porcentaje de descuento
    descuento_pct = calcular_descuento()
    
    # Renderizar template
    return templates.TemplateResponse("index.html", {
        "request": request,
        "restaurant_id": restaurant_id,
        "visitas": visitas,
        "descuento_pct": descuento_pct
    })


@app.post("/calcular")
async def calcular_descuento_endpoint(
    restaurant_id: str = Form(...),
    monto_compra: float = Form(...)
):
    """
    Calcula el descuento del 5% sobre el monto de compra.
    
    Args:
        restaurant_id: ID del restaurante/comercio
        monto_compra: Monto de la compra
        
    Returns:
        JSON con los montos calculados
    """
    # Validar restaurante
    if restaurant_id not in RESTAURANTES_COMERCIOS:
        raise HTTPException(status_code=404, detail=f"Restaurante/comercio '{restaurant_id}' no encontrado")
    
    # Validar monto
    if monto_compra < 0:
        raise HTTPException(status_code=400, detail="El monto debe ser positivo")
    
    # Calcular descuento
    resultado = calcular_montos(monto_compra)
    
    # Agregar información adicional
    resultado["restaurant_id"] = restaurant_id
    resultado["visitas"] = get_visitas(restaurant_id)
    
    return JSONResponse(content=resultado)


@app.get("/qr/{restaurant_id}")
async def obtener_qr(restaurant_id: str):
    """
    Genera y retorna el código QR para un restaurante/comercio.
    
    Args:
        restaurant_id: ID del restaurante/comercio
        
    Returns:
        Archivo de imagen PNG del QR
    """
    # Validar restaurante
    if restaurant_id not in RESTAURANTES_COMERCIOS:
        raise HTTPException(status_code=404, detail=f"Restaurante/comercio '{restaurant_id}' no encontrado")
    
    # Generar QR
    filepath = generar_qr(restaurant_id, BASE_URL)
    
    # Verificar que se generó
    if not os.path.exists(filepath):
        raise HTTPException(status_code=500, detail="Error al generar QR")
    
    # Retornar archivo
    return FileResponse(
        filepath,
        media_type="image/png",
        filename=f"{restaurant_id}_qr.png"
    )


@app.get("/qr/generar-todos")
async def generar_todos_qr():
    """
    Genera códigos QR para todos los restaurantes y comercios.
    
    Returns:
        JSON con el resultado de la generación
    """
    try:
        rutas = generar_todos_los_qr(BASE_URL)
        return JSONResponse(content={
            "status": "success",
            "message": f"Se generaron {len(rutas)} códigos QR",
            "rutas": rutas,
            "total": len(rutas)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar QRs: {str(e)}")


@app.get("/api/visitas/{restaurant_id}")
async def obtener_visitas(restaurant_id: str):
    """
    Endpoint API para obtener el número de visitas de un restaurante/comercio.
    
    Args:
        restaurant_id: ID del restaurante/comercio
        
    Returns:
        JSON con el número de visitas
    """
    if restaurant_id not in RESTAURANTES_COMERCIOS:
        raise HTTPException(status_code=404, detail=f"Restaurante/comercio '{restaurant_id}' no encontrado")
    
    visitas = get_visitas(restaurant_id)
    
    return JSONResponse(content={
        "restaurant_id": restaurant_id,
        "visitas": visitas
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

