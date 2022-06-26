import numpy as np
from pysics.objetos import Medida


def rad(med):
    """Transforma un ángulo a radianes"""
    if not isinstance(med, Medida):
        return med * np.pi/180
    valores = med.medida*np.pi/180
    error = np.pi/180 * med.error
    return Medida(valores, error, aproximar = False)

def sen(x):
    if not isinstance(x, Medida):
        return np.sin(x)
    valor = np.sin(x.medida)
    if 1 in valor:
        raise RuntimeWarning("Uno de los valores tiene un error de 0, sin embargo esto puede ser poco preciso")

    error = abs(np.cos(x.medida))*x.error
    return Medida(valor, error, aproximar = False)

def cos(x: Medida) -> Medida:
    if not isinstance(x, Medida):
        return np.sin(x)
    valor = np.cos(x.medida)
    if 1 in valor:
        raise RuntimeWarning("Uno de los valores tiene un error de 0, sin embargo esto puede ser poco preciso")

    error = abs(np.sin(x.medida))*x.error
    return Medida(valor, error, aproximar = False)

def log(x):
    """Logaritmo natural"""
    if not isinstance(x, Medida):
        return np.log(x)
    valor = np.log(x.medida)
    error = abs(1/x.medida)*x.error
    return Medida(valor, error, aproximar = False)

def sqrt(x):
    if isinstance(x, Medida):
        x = x.copy()
    return x**(1/2)
