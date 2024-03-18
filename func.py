import numpy as np
from .objects import Measure

def rad(degrees: Measure) -> Measure:
    """
    Transform an angle to radians
    """
    return degrees * np.pi/180

def grad(radians: Measure):
    """
    Transform an angle to degrees
    """
    return radians * 180/np.pi

def sin(x: Measure) -> Measure:
    """
    Calculate the sine of a value
    """
    if not isinstance(x, Measure):
        return np.sin(x)
    
    value = np.sin(x.value)
    error = np.abs(np.cos(x.value))*x.error
    
    nullvalues = [i for i, v in enumerate(value) if v==1 or v==-1]
    for i in nullvalues:
        error[i] = np.abs(np.sin(x.value[i]+x.error[i])-np.sin(x.value[i]))
        
    return Measure(value, error, aproximate = False)

def cos(x: Measure) -> Measure:
    """
    Calculate the cosine of a value
    """
    if not isinstance(x, Measure):
        return np.cos(x)
    
    value = np.cos(x.value)
    error = np.abs(np.sin(x.value))*x.error
    
    nullvalues = [i for i, v in enumerate(value) if v==1 or v==-1]
    
    for i in nullvalues:
        error[i] = np.abs(np.cos(x.value[i]+x.error[i])-np.cos(x.value[i]))
    
    return Measure(value, error, aproximate = False)

def tan(x):
    if not isinstance(x, Measure):
        x = Measure(x)
    value = np.tan(x.value)
    error = (1+value**2) * x.error
    return Measure(value, error, aproximate=False)


def asin(x):
    x = Measure(x)
        
    value = np.arcsin(x.value)
    error = x.error/np.sqrt(1-np.power(value, 2))

    return Measure(value, error, aproximate=False)


def acos(x):
    
    x = Measure(x)
        
    value = np.arccos(x.value)
    error = x.error/np.sqrt(1-np.power(value, 2))

    return Measure(value, error, aproximate=False)


def atan(x):
    x = Measure(x)
    value = np.arctan(x.value)
    error = x.error/(1+np.power(value, 2))
    return Measure(value, error, aproximate=False)

def atan2(x: Measure, y: Measure):
    """
    Angle of a point in polar coordinates
    """
    x = Measure(x)
    y = Measure(y)
    
    angles = [np.arctan2(x, y) for x, y in zip(x.value, y.value)]
    
    error = np.sqrt((y.value*x.error)**2+(x.value*y.error)**2)/np.abs(x**2+y**2)
    
    return Measure(angles, error, aproximate=False)

def ln(x: Measure) -> Measure:
    """
    Calculate the natural logarithm of a value
    """
    if not isinstance(x, Measure):
        return np.log(x)
    
    value = np.log(x.value)
    error = abs(1/x.value)*x.error
    return Measure(value, error, aproximate = False)

def sqrt(x: Measure) -> Measure:
    """
    Calculate the square root of a value
    """
    if not isinstance(x, Measure):
        return x**(1/2)
    return x.sqrt()
    
def exp(x: Measure) -> Measure:
    """
    Calculate the exponential of a value
    """
    if not isinstance(x, Measure):
        return np.exp(x)
    
    value = np.exp(x.value)
    error = abs(value)*x.error
    return Measure(value, error, aproximate=False)

def delta(x: Measure) -> Measure:
    """
    Calculate the difference between consecutive values in a measure
    """
    if not isinstance(x, Measure):
        x = Measure(x)

    values = []
    errors = []
    for i, j in zip(x[1:].list_of_values(), x[:-1].list_of_values()):
        v = i-j
        values.append(v.value[0])
        errors.append(v.error[0])
    return Measure(values, errors, aproximate=False)

if __name__ == '__main__':
    print(cos(acos(Measure(1, 0.1))))
    