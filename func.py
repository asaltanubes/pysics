import numpy as np
from pysics.objetos import Medida


def rad(grados: Medida) -> Medida:
    """Transforma un ángulo a radianes"""
    if not isinstance(grados, Medida):
        return grados * np.pi/180
    
    valores = grados._medida*np.pi/180
    error = np.pi/180 * grados._error
    return Medida(valores, error, aproximar = False)

def sen(x: Medida) -> Medida:
    if not isinstance(x, Medida):
        return np.sin(x)
    
    valor = np.sin(x._medida)

    error = abs(np.cos(x._medida))*x._error
    return Medida(valor, error, aproximar = False)

def cos(x: Medida) -> Medida:
    if not isinstance(x, Medida):
        return np.cos(x)
    
    valor = np.cos(x._medida)

    error = abs(np.sin(x._medida))*x._error
    return Medida(valor, error, aproximar = False)

def ln(x: Medida) -> Medida:
    """Logaritmo natural"""
    if not isinstance(x, Medida):
        return np.log(x)
    
    valor = np.log(x._medida)
    error = abs(1/x._medida)*x._error
    return Medida(valor, error, aproximar = False)

def sqrt(x: Medida) -> Medida:
    """Raiz cuadrada"""
    if not isinstance(x, Medida):
        x = x.copy()
    return x**(1/2)
    
def exp(x: Medida) -> Medida:
    """Función exponencial (e**x)"""
    if not isinstance(x, Medida):
        return np.exp(x)
    
    valor = np.exp(x._medida)
    error = abs(valor)*x._error
    return Medida(valor, error, aproximar=False)

def delta(x: Medida) -> Medida:
    """Devuelve x[n+1]-x[n] en una medida"""
    if not isinstance(x, Medida):
        x = Medida(x)

    valores = []
    errores = []
    for i, j in zip(x[1:].lista_de_medidas(), x[:-1].lista_de_medidas()):
        v = i-j
        valores.append(v._medida[0])
        errores.append(v._error[0])
    return Medida(valores, errores, aproximar=False)