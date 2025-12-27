# Sistema QR de Descuentos

Sistema de conteo de visitas y cálculo de descuentos para restaurantes y comercios mediante códigos QR.

## 🚀 Características

- Generación de códigos QR únicos por restaurante/comercio
- Conteo automático de visitas al escanear QR
- Cálculo de descuento del 5% sobre el monto de compra
- Interfaz web responsive y moderna
- Almacenamiento en archivo JSON (sin base de datos)

## 📦 Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

Iniciar el servidor:
```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## 🔗 Endpoints

### GET `/`
Página de inicio con información del sistema.

### GET `/{restaurant_id}`
Endpoint principal cuando se escanea un QR. Incrementa el contador de visitas y muestra la página de cálculo de descuento.

**Ejemplo**: `http://localhost:8000/rest_001`

### POST `/calcular`
Calcula el descuento del 5% sobre el monto de compra.

**Parámetros**:
- `restaurant_id`: ID del restaurante/comercio
- `monto_compra`: Monto de la compra (número)

### GET `/qr/{restaurant_id}`
Genera y retorna el código QR para un restaurante/comercio específico.

**Ejemplo**: `http://localhost:8000/qr/rest_001`

### GET `/qr/generar-todos`
Genera códigos QR para todos los restaurantes y comercios de una vez.

**Ejemplo**: `http://localhost:8000/qr/generar-todos`

### GET `/api/visitas/{restaurant_id}`
Obtiene el número de visitas de un restaurante/comercio (API JSON).

## 🏪 Restaurantes y Comercios

El sistema incluye los siguientes restaurantes y comercios de AGENCIA:

**Restaurantes**:
- `rest_001` - El Buen Suspiro
- `rest_002` - Charco Bistró
- `rest_003` - La Bodeguita
- `rest_004` - Parrillada El Portón
- `rest_005` - Viejo Barrio

**Comercios**:
- `com_001` - Manos del Uruguay
- `com_002` - Mercado Artesanal
- `com_003` - Feria de Emprendedores

## 📁 Estructura del Proyecto

```
AGENCIA QR BACK/
├── main.py              # Aplicación FastAPI principal
├── storage.py           # Gestión de data.json
├── discounts.py         # Cálculo de descuentos (5% fijo)
├── qr_generator.py      # Generación de códigos QR
├── templates/
│   └── index.html       # Página de cálculo de descuento
├── qr_codes/            # Carpeta para imágenes QR generadas
├── data.json            # Persistencia de visitas
└── requirements.txt     # Dependencias
```

## 💾 Almacenamiento

Los datos se guardan en `data.json` con la siguiente estructura:

```json
{
  "restaurantes": {
    "rest_001": {"visitas": 0},
    "rest_002": {"visitas": 0},
    ...
  }
}
```

## 🎯 Flujo de Uso

1. **Generar QRs**: Visitar `/qr/generar-todos` para generar todos los códigos QR
2. **Escanear QR**: El usuario escanea el QR del restaurante/comercio
3. **Incremento automático**: El sistema incrementa el contador de visitas
4. **Página de descuento**: Se muestra la página con el formulario de cálculo
5. **Calcular**: El usuario ingresa el monto y calcula el descuento del 5%

## ⚙️ Configuración

La URL base se puede configurar mediante variable de entorno:

```bash
export BASE_URL="https://tu-dominio.com"
```

Por defecto es `http://localhost:8000`.

## 📝 Notas

- El descuento es fijo del 5% para todos los restaurantes/comercios
- Cada escaneo de QR incrementa el contador de visitas
- No hay validación de doble escaneo (cada escaneo cuenta como nueva visita)
- Los datos se persisten en `data.json` y se mantienen en memoria para mejor rendimiento

