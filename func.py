import numpy as np
from pysics.objetos import Medida, Number
from mpmath import atan2 as mpatan2
from mpmath import mp


def rad(grados: Medida) -> Medida:
    """Transforma un ángulo a radianes"""
    if isinstance(grados, (Number, Medida)):
        return grados.rad()
    return grados * np.pi/180

def grad(radianes: Medida):
    """Transforma un ángulo a grados"""
    if isinstance(radianes, (Number, Medida)):
        return radianes.grad()
    return radianes * 180/np.pi

def sen(x: Medida) -> Medida:
    """Calcula el seno de una medida"""
    if not isinstance(x, Medida):
        return np.sin(x)
    
    valor = np.sin(x._medida)
    error = np.abs(np.cos(x._medida))*x._error
    
    
    null_values = [i for i, v in enumerate(valor) if v==1 or v==-1]
    for i in null_values:
        error[i] = np.abs(np.sin(x._medida[i]+x._error[i])-np.sin(x._medida[i]))
        
    return Medida(valor, error, aproximar = False)

sin = sen

def cos(x: Medida) -> Medida:
    """Calcula el coseno de una medida"""
    if not isinstance(x, Medida):
        return np.cos(x)
    
    valor = np.cos(x._medida)
    error = np.abs(np.sin(x._medida))*x._error
    
    null_values = [i for i, v in enumerate(valor) if v==1 or v==-1]
    
    for i in null_values:
        error[i] = np.abs(np.cos(x._medida[i]+x._error[i])-np.cos(x._medida[i]))
    
    return Medida(valor, error, aproximar = False)

def tan(x):
    
    if not isinstance(x, Medida):
        x = Medida(x)
    valor = np.tan(x._medida)
    error = (1+valor**2) * x._error
    return Medida(valor, error, aproximar=False)


def asin(x):
    
    if not isinstance(x, Medida):
        x = Medida(x)
        
    valor = np.arcsin(x._medida)
    error = x._error/np.sqrt(1-np.power(valor, 2))
            
    return Medida(valor, error, aproximar=False)


def acos(x):
    
    if not isinstance(x, Medida):
        x = Medida(x)
        
    if not (1 in x._medida or -1 in x._medida):
        valor = np.arccos(x._medida)
        error = x._error/np.sqrt(1-np.power(valor, 2))

    return Medida(valor, error, aproximar=False)


def atan(x):

    if not isinstance(x, Medida):
        x = Medida(x)
    valor = np.arctan(x._medida)
    error = x._error/(1+np.power(valor, 2))

    return Medida(valor, error, aproximar=False)

def atan2(x: Medida, y: Medida):
    """Angulo de un punto en coordenadas polares"""
    if not isinstance(x, Medida):
        x = Medida(x)
    if not isinstance(y, Medida):
        y = Medida(y)
    angulos = [mpatan2(x.value, y.value, prec=mp.prec+2) for x, y in zip(x._medida, y._medida)]
    
    error = np.sqrt((y._medida*x._error)**2+(x._medida*y._error)**2)/np.abs(x**2+y**2)
    
    return Medida(angulos, error, aproximar=False)

def ln(x: Medida) -> Medida:
    """Logaritmo natural"""
    if not isinstance(x, Medida):
        return np.log(x)
    
    valor = np.log(x._medida)
    error = abs(1/x._medida)*x._error
    return Medida(valor, error, aproximar = False)

def sqrt(x: Medida) -> Medida:
    """Raiz cuadrada"""
    if not isinstance(x, (Medida, Number)):
        return x**(1/2)
    return x.sqrt()
    
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

if __name__ == '__main__':
    print(cos(acos(Medida(1, 0.1))))
    