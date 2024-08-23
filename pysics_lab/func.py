import numpy as np
from .objects import Measure
from . import units

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
    x = Measure(x)

    if not (np.isclose(x.units.si,  units.rad.si)).all():
        print("WARNING: the value passed is not an angle")
    else:
        x = x.si()

    value = np.sin(x._value)
    error = np.abs(np.cos(x._value))*x._error

    nullvalues = [i for i, v in enumerate(value) if v==1 or v==-1]
    for i in nullvalues:
        error[i] = np.abs(np.sin(x._value[i]+x._error[i])-np.sin(x._value[i]))

    return Measure(value, error, aproximate = False)

def cos(x: Measure) -> Measure:
    """
    Calculate the cosine of a value
    """
    x = Measure(x)


    if not (np.isclose(x.units.si,  units.rad.si)).all():
        print("WARNING: the value passed is not an angle")
    else:
        x = x.si()

    value = np.cos(x._value)
    error = np.abs(np.sin(x._value))*x._error

    nullvalues = [i for i, v in enumerate(value) if v==1 or v==-1]

    for i in nullvalues:
        error[i] = np.abs(np.cos(x._value[i]+x._error[i])-np.cos(x._value[i]))

    return Measure(value, error, aproximate = False)

def tan(x):
    x = Measure(x)

    if not (np.isclose(x.units.si,  units.rad.si)).all():
        print("WARNING: the value passed is not an angle")
    else:
        x = x.si()

    value = np.tan(x._value)
    error = (1+value**2) * x._error
    return Measure(value, error, aproximate=False)


def asin(x):
    x = Measure(x)

    x = x.si()
    if not (np.isclose(x.units.si,  0)).all(): print("WARNING: the value passed is not adimensional")

    value = np.arcsin(x._value)
    error = x._error/np.sqrt(1-np.power(x._value, 2)) if (x._value != 1).any() else np.abs(np.arcsin(x._value-x._error) - value)

    return Measure(value, error, aproximate=False, units=units.rad)


def acos(x):
    x = Measure(x)

    x = x.si()
    if not (np.isclose(x.units.si,  0)).all(): print("WARNING: the value passed is not adimensional")

    value = np.arccos(x._value)
    error = x._error/np.sqrt(1-np.power(x._value, 2)) if (x._value != 1).any() else np.abs(np.arcsin(x._value-x._error) - value)

    return Measure(value, error, aproximate=False, units=units.rad)


def atan(x):
    x = Measure(x)

    x = x.si()
    if not (np.isclose(x.units.si,  0)).all(): print("WARNING: the value passed is not adimensional")

    value = np.arctan(x._value)
    error = x.error/(1+np.power(x._value, 2))
    return Measure(value, error, aproximate=False, units=units.rad)

def atan2(x: Measure, y: Measure):
    """
    Angle of a point in polar coordinates
    """
    x = Measure(x)
    y = Measure(y)


    if not (np.isclose(x.units.si,  y.units.si)).all():
        print("WARNING: x and y don't have the same units")
    else:
        x = x.si()
        y = y.si()

    angles = [np.arctan2(x, y) for x, y in zip(x._value, y._value)]

    error = np.sqrt((y._value*x._error)**2+(x._value*y._error)**2)/np.abs(x**2+y**2)

    return Measure(angles, error, aproximate=False, units=units.rad)

def ln(x: Measure) -> Measure:
    """
    Calculate the natural logarithm of a value
    """
    x = Measure(x)

    if not (np.isclose(x.units.si, 0)).all():
        print("WARNING: the value passed is not adimensional")
    else:
        x = x.si()

    value = np.log(x._value)
    error = abs(1/x._value)*x._error
    return Measure(value, error, aproximate = False)

def sqrt(x: Measure) -> Measure:
    """
    Calculate the square root of a value
    """
    return x**(1/2)

def exp(x: Measure) -> Measure:
    """
    Calculate the exponential of a value
    """
    x = Measure(x)

    if not (np.isclose(x.units.si, 0)).all():
        print("WARNING: the value passed is not adimensional")
    else:
        x = x.si()

    value = np.exp(x._value)
    error = abs(value)*x._error
    return Measure(value, error, aproximate=False)

def delta(x: Measure) -> Measure:
    """
    Calculate the difference between consecutive values in a measure
    """
    x = Measure(x)

    values = []
    errors = []
    for i, j in zip(x[1:].list_of_measures(), x[:-1].list_of_measures()):
        v = i-j
        values.append(v._value[0])
        errors.append(v._error[0])
    return Measure(values, errors, units = x.units, aproximate=False)

if __name__ == '__main__':
    print(cos(acos(Measure(1, 0.1))))
