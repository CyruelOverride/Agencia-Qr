"""
Módulo para calcular descuentos.
Implementa lógica de descuento fijo del 5%.
"""


def calcular_descuento() -> int:
    """
    Retorna el porcentaje de descuento aplicable.
    Actualmente es un descuento fijo del 5%.
    
    Returns:
        int: Porcentaje de descuento (5)
    """
    return 5


def calcular_montos(monto: float, porcentaje: int = None) -> dict:
    """
    Calcula el descuento y el total final a pagar.
    
    Args:
        monto: Monto original de la compra
        porcentaje: Porcentaje de descuento (opcional, por defecto usa calcular_descuento())
        
    Returns:
        dict: Diccionario con:
            - descuento_pct: Porcentaje de descuento aplicado
            - descuento_monto: Monto descontado
            - total_final: Monto final a pagar
    """
    if porcentaje is None:
        porcentaje = calcular_descuento()
    
    # Validar monto
    if monto < 0:
        monto = 0
    
    # Calcular descuento
    descuento_monto = (monto * porcentaje) / 100
    
    # Calcular total final
    total_final = monto - descuento_monto
    
    return {
        "descuento_pct": porcentaje,
        "descuento_monto": round(descuento_monto, 2),
        "total_final": round(total_final, 2),
        "monto_original": round(monto, 2)
    }

