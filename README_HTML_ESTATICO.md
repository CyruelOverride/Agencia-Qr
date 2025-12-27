# Uso del HTML Estático (Sin Backend)

## 📄 Archivo: `static/descuento.html`

Este es un archivo HTML estático que funciona **sin necesidad de backend**. Puedes alojarlo en:

- **GitHub Pages** (gratis)
- **Netlify** (gratis)
- **Vercel** (gratis)
- **Cualquier servidor web estático**
- **Incluso abrirlo directamente desde el archivo** (file://)

## 🚀 Cómo usar

### Opción 1: Sin servidor (archivo local)

1. Copia `static/descuento.html` a donde quieras
2. Abre el archivo directamente en el navegador
3. Los QRs deben apuntar a la ruta del archivo (ej: `file:///C:/ruta/al/archivo/descuento.html`)

### Opción 2: Con servidor estático (recomendado)

1. Sube `static/descuento.html` a tu servidor
2. Accede desde: `https://tu-dominio.com/descuento.html`
3. Al generar QRs, usa esa URL como `base_url`

### Opción 3: GitHub Pages (gratis)

1. Crea un repositorio en GitHub
2. Sube `descuento.html` a la carpeta raíz
3. Activa GitHub Pages en la configuración del repositorio
4. Tu URL será: `https://tu-usuario.github.io/repo/descuento.html`
5. Usa esa URL al generar los QRs

## 🔧 Configuración de QRs

Cuando generes los QRs desde AGENCIA, puedes configurar la URL base:

```python
# En qr_helper.py o al generar QRs
base_url = "https://tu-dominio.com"  # O la URL donde esté tu HTML
```

O usar variable de entorno:
```bash
export QR_BASE_URL="https://tu-dominio.com"
```

## ✨ Características

- ✅ **Funciona sin backend**: Todo el cálculo se hace en JavaScript
- ✅ **Descuento del 5%**: Calculado automáticamente
- ✅ **Responsive**: Se ve bien en móviles y desktop
- ✅ **Sin dependencias**: Solo HTML, CSS y JavaScript puro

## 📱 Cómo funciona

1. Usuario escanea el QR
2. Se abre `descuento.html` en el navegador
3. Usuario ingresa el monto de compra
4. JavaScript calcula el descuento del 5% automáticamente
5. Muestra el resultado sin necesidad de servidor

## 🔄 Si quieres usar el backend

Si más adelante quieres usar el backend con contador de visitas:

1. Cambia `usar_html_estatico=False` en `qr_helper.py`
2. Asegúrate de tener el servidor FastAPI corriendo
3. Los QRs apuntarán a `http://tu-servidor:8000/{restaurant_id}`

