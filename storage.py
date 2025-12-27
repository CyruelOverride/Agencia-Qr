"""
Módulo de almacenamiento para gestionar visitas de restaurantes/comercios.
Maneja lectura/escritura de data.json y operaciones sobre contadores.
"""

import json
import os
from typing import Dict

# Ruta del archivo de datos
DATA_FILE = "data.json"

# Estado en memoria (cache)
_memoria_cache: Dict = None


def cargar_datos() -> Dict:
    """
    Carga los datos desde data.json.
    Si el archivo no existe, crea una estructura vacía.
    Si no hay datos en memoria, los carga desde el archivo.
    
    Returns:
        dict: Diccionario con los datos de restaurantes y sus visitas
    """
    global _memoria_cache
    
    # Si ya están en memoria, retornar cache
    if _memoria_cache is not None:
        return _memoria_cache
    
    # Si el archivo existe, cargarlo
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                _memoria_cache = json.load(f)
                return _memoria_cache
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar {DATA_FILE}: {e}")
            # Si hay error, inicializar estructura vacía
            _memoria_cache = {"restaurantes": {}}
            return _memoria_cache
    else:
        # Archivo no existe, crear estructura vacía
        _memoria_cache = {"restaurantes": {}}
        guardar_datos(_memoria_cache)
        return _memoria_cache


def guardar_datos(data: Dict) -> None:
    """
    Guarda los datos en data.json.
    También actualiza el cache en memoria.
    
    Args:
        data: Diccionario con los datos a guardar
    """
    global _memoria_cache
    
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        _memoria_cache = data
    except IOError as e:
        print(f"Error al guardar {DATA_FILE}: {e}")
        raise


def inicializar_restaurante(restaurant_id: str) -> None:
    """
    Crea una entrada para un restaurante/comercio si no existe.
    
    Args:
        restaurant_id: ID del restaurante/comercio (ej: "rest_001", "com_001")
    """
    data = cargar_datos()
    
    if "restaurantes" not in data:
        data["restaurantes"] = {}
    
    if restaurant_id not in data["restaurantes"]:
        data["restaurantes"][restaurant_id] = {"visitas": 0}
        guardar_datos(data)


def get_visitas(restaurant_id: str) -> int:
    """
    Obtiene el número de visitas actuales de un restaurante/comercio.
    
    Args:
        restaurant_id: ID del restaurante/comercio
        
    Returns:
        int: Número de visitas (0 si no existe)
    """
    data = cargar_datos()
    
    if "restaurantes" not in data:
        return 0
    
    if restaurant_id not in data["restaurantes"]:
        inicializar_restaurante(restaurant_id)
        return 0
    
    return data["restaurantes"][restaurant_id].get("visitas", 0)


def incrementar_visita(restaurant_id: str) -> int:
    """
    Incrementa el contador de visitas de un restaurante/comercio.
    Si no existe, lo crea con 1 visita.
    
    Args:
        restaurant_id: ID del restaurante/comercio
        
    Returns:
        int: Nuevo número total de visitas
    """
    data = cargar_datos()
    
    # Asegurar estructura
    if "restaurantes" not in data:
        data["restaurantes"] = {}
    
    # Inicializar si no existe
    if restaurant_id not in data["restaurantes"]:
        data["restaurantes"][restaurant_id] = {"visitas": 0}
    
    # Incrementar
    data["restaurantes"][restaurant_id]["visitas"] += 1
    
    # Guardar y retornar
    nuevo_total = data["restaurantes"][restaurant_id]["visitas"]
    guardar_datos(data)
    
    return nuevo_total

