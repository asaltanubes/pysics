import numpy as np
from .objetos import Measure

def rad(grados: Measure) -> Measure:
    """Transforma un ángulo a radianes"""
    return grados * np.pi/180

def grad(radianes: Measure):
    """Transforma un ángulo a grados"""
    return radianes * 180/np.pi

def sen(x: Measure) -> Measure:
    """Calcula el seno de una value"""
    if not isinstance(x, Measure):
        return np.sin(x)
    
    valor = np.sin(x._value)
    error = np.abs(np.cos(x._value))*x._error
    
    
    null_values = [i for i, v in enumerate(valor) if v==1 or v==-1]
    for i in null_values:
        error[i] = np.abs(np.sin(x._value[i]+x._error[i])-np.sin(x._value[i]))
        
    return Measure(valor, error, aproximar = False)

def cos(x: Measure) -> Measure:
    """Calcula el coseno de una value"""
    if not isinstance(x, Measure):
        return np.cos(x)
    
    valor = np.cos(x._value)
    error = np.abs(np.sin(x._value))*x._error
    
    null_values = [i for i, v in enumerate(valor) if v==1 or v==-1]
    
    for i in null_values:
        error[i] = np.abs(np.cos(x._value[i]+x._error[i])-np.cos(x._value[i]))
    
    return Measure(valor, error, aproximar = False)

def tan(x):
    
    if not isinstance(x, Measure):
        x = Measure(x)
    valor = np.tan(x._value)
    error = (1+valor**2) * x._error
    return Measure(valor, error, aproximar=False)


def asin(x):
    
    x = Measure(x)
        
    if not (1 in x._value or -1 in x._value):
        valor = np.arcsin(x._value)
        error = x._error/np.sqrt(1-np.power(x._value, 2))
    else: 
        valor = np.zeros(len(x._value))
        error = np.zeros(len(x._error))
        for i, (v, e) in enumerate(zip(x._value, x._error)):
            if v != 1 and v != -1:
                valor[i] = np.arcsin(v)
                error[i] = e/np.sqrt(1-np.power(v, 2))
            else:
                valor[i] = np.arcsin(v)
                error[i] = np.abs(np.arcsin(v-e)-v)
            
    return Measure(valor, error, aproximar=False)


def acos(x):
    
    x = Measure(x)
        
    if not (1 in x._value or -1 in x._value):
        valor = np.arccos(x._value)
        error = x._error/np.sqrt(1-np.power(x._value, 2))
    else:
        valor = np.zeros(len(x._value))
        error = np.zeros(len(x._error))
        for i, (v, e) in enumerate(zip(x._value, x._error)):
            if v != 1 and v != -1:
                valor[i] = np.arccos(v)
                error[i] = e/np.sqrt(1-np.power(v, 2))
            else:
                valor[i] = np.arccos(v)
                d = v-e if v>0 else v+e
                error[i] = np.abs(np.arccos(d)-np.arccos(v))
    return Measure(valor, error, aproximar=False)


def atan(x):
    x = Measure(x)
    valor = np.arctan(x._value)
    error = x._error/(1+np.power(x._value, 2))
    return Measure(valor, error, aproximar=False)

def atan2(x: Measure, y: Measure):
    """Angulo de un punto en coordenadas polares"""
    x = Measure(x)
    y = Measure(y)
    
    angulos = [np.arctan2(x, y) for x, y in zip(x._value, y._value)]
    
    error = np.sqrt((y._value*x._error)**2+(x._value*y._error)**2)/np.abs(x**2+y**2)
    
    return Measure(angulos, error, aproximar=False)

def ln(x: Measure) -> Measure:
    """Logaritmo natural"""
    if not isinstance(x, Measure):
        return np.log(x)
    
    valor = np.log(x._value)
    error = abs(1/x._value)*x._error
    return Measure(valor, error, aproximar = False)

def sqrt(x: Measure) -> Measure:
    """Raiz cuadrada"""
    if not isinstance(x, Measure):
        return x**(1/2)
    return x.sqrt()
    
def exp(x: Measure) -> Measure:
    """Función exponencial (e**x)"""
    if not isinstance(x, Measure):
        return np.exp(x)
    
    valor = np.exp(x._value)
    error = abs(valor)*x._error
    return Measure(valor, error, aproximar=False)

def delta(x: Measure) -> Measure:
    """Devuelve x[n+1]-x[n] en una value"""
    if not isinstance(x, Measure):
        x = Measure(x)

    valores = []
    errores = []
    for i, j in zip(x[1:].list_of_values(), x[:-1].list_of_values()):
        v = i-j
        valores.append(v._value[0])
        errores.append(v._error[0])
    return Measure(valores, errores, aproximar=False)

if __name__ == '__main__':
    print(cos(acos(Measure(1, 0.1))))
    