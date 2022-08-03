import numpy as np
from pysics.objetos import Medida


def rad(med: Medida) -> Medida:
    """Transforma un ángulo a radianes"""
    if not isinstance(med, Medida):
        return med * np.pi/180
    valores = med._medida*np.pi/180
    error = np.pi/180 * med._error
    return Medida(valores, error, aproximar = False)

def sen(x: Medida) -> Medida:
    if not isinstance(x, Medida):
        return np.sin(x)
    valor = np.sin(x._medida)
    if 1 in valor:
        raise RuntimeWarning("Uno de los valores tiene un error de 0, sin embargo esto puede ser poco preciso")

    error = abs(np.cos(x._medida))*x._error
    return Medida(valor, error, aproximar = False)

def cos(x: Medida) -> Medida:
    if not isinstance(x, Medida):
        return np.sin(x)
    valor = np.cos(x._medida)
    if 1 in valor:
        raise RuntimeWarning("Uno de los valores tiene un error de 0, sin embargo esto puede ser poco preciso")

    error = abs(np.sin(x._medida))*x._error
    return Medida(valor, error, aproximar = False)

def log(x: Medida) -> Medida:
    """Logaritmo natural"""
    if not isinstance(x, Medida):
        return np.log(x)
    valor = np.log(x._medida)
    error = abs(1/x._medida)*x._error
    return Medida(valor, error, aproximar = False)

def sqrt(x: Medida) -> Medida:
    """Raiz cuadrada"""
    if isinstance(x, Medida):
        x = x.copy()
    return x**(1/2)

def exp(x: Medida) -> Medida:
    """Función exponencial (e**x)"""
    if not isinstance(x, Medida):
        return np.exp(x)
    valor = np.exp(x._medida)
    error = abs(valor)*x._error
    return Medida(valor, error, aproximar=False)
