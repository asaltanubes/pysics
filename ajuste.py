from .objetos import Medida, Recta
from .type_alias import elementos, Opcional
import numpy as np
from scipy.optimize import curve_fit




def curva(funcion, x: elementos, y: elementos, sigma = None, initial_guess: list[float] = None, aproximar: bool = False):
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        if sigma is not None:
            sigma = y._error
        y = y._medida
    
    if initial_guess is not None and not hasattr(initial_guess, '__iter__'):
        from inspect import signature
        if len(signature(funcion).parameters) == 2:
            initial_guess = (initial_guess, )
    popt, error = curve_fit(funcion, x, y, p0=initial_guess) if sigma is None else curve_fit(funcion, x, y, p0=initial_guess, sigma = sigma)
    return tuple((Medida(v, e, aproximar=aproximar) for v, e in zip(popt, np.sqrt(np.diag(error)))))

def minimos_cuadrados(x: elementos, y: elementos, aproximar: bool = False) -> Recta:
    """
    Calcula la recta de ajuste por mínimos cuadrados para dos medidas.

    return tuple(Medida, Medida)
    (pen, n_0)
    pen: pendiente de la recta de ajuste
    n_0: ordenada en el origen de la recta de ajuste
    """
    p, n = calc_line(x, y)
    dp, dn = sigma_calc_line(x, y)
    pen: Medida = Medida(p, dp, aproximar=aproximar)
    n_0: Medida = Medida(n, dn, aproximar=aproximar)
    if isinstance(x, Medida):
        x = x.medida
    return Recta(pen, n_0, x)

def minimos_pesados(x: Medida, y: Medida, yerr: Opcional[[float, ...]] = None, aproximar: bool = False) -> Recta:
    """
    Calcula la recta de ajuste por mínimos cuadrados pesados para dos medidas.
    El error del eje y se extrae de la Medida \"y\" y el error del eje x se
    desprecia

    return tuple(Medida, Medida)
    (pen, n_0)
    pen: pendiente de la recta de ajuste
    n_0: ordenada en el origen de la recta de ajuste
    """
    p, n = wcalc_line(x=x, y=y, yerr=yerr)
    dp, dn = wsigma_calc_line(x=x, y=y, yerr=yerr)
    pen: Medida = Medida(p, dp, aproximar=aproximar)
    n_0: Medida = Medida(n, dn, aproximar=aproximar)
    if isinstance(x, Medida):
        x = x.medida
    return Recta(pen, n_0, x)

def line(x: elementos , pen: float, n_0: float=0) -> list[float]:
    if isinstance(x, Medida):
        x = x._medida

    if isinstance(pen, Recta):
        n_0 = pen.n_0
        pen = pen.pendiente

    if isinstance(pen, Medida):
        pen = pen._medida
    if isinstance(n_0, Medida):
        n_0 = n_0._medida

    return x*pen + n_0

def calc_line(x: elementos, y: elementos) -> tuple[float, float]:
    """Dadas 2 listas con los valores x e y de un conjunto de puntos devuelve el ajuste por mínimos cuadrados de esta"""
    return pen(x, y), n_0(x, y)

def sigma_calc_line(x: float, y: float) -> tuple[float, float]:
    """Dadas 2 listas con los valores x e y de un conjunto de puntos devuelve los errores de la pendiente y la ordenada en el origen"""
    return sigma_pen(x, y), sigma_n_0(x, y)

def pen(x : elementos, y : elementos) -> float:
    """Calcula la pendiente de la recta de ajuste"""
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)

    return float((x.size*np.sum(x*y) - np.sum(x)*np.sum(y))/(x.size*np.sum(x**2) - np.sum(x)**2))

def n_0 (x : elementos, y : elementos) -> float:
    """Calcula la ordenada en el origen de la recta de ajuste"""
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)

    return float((np.sum(y)*np.sum(x**2) - np.sum(x)*np.sum(x*y))/(x.size * np.sum(x**2) - (np.sum(x))**2))

def sigma_y(x : elementos, y : elementos) -> float:
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)

    ŷ = line(x=x, pen=pen(x, y), n_0=n_0(x, y))
    return float(np.sqrt( (np.sum( (y-ŷ)**2 ) ) / (x.size - 2)))

def sigma_pen(x: elementos, y: elementos) -> float:
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)

    return float(sigma_y(x, y) *np.sqrt( x.size / (x.size * np.sum(x**2) - np.sum(x)**2) ))

def sigma_n_0(x: elementos, y: elementos) -> float:
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)
    return float(sigma_y(x, y) * np.sqrt( np.sum(x**2) / (x.size * np.sum(x**2) - np.sum(x)**2) ))

def wcalc_line(x: elementos, y: elementos, yerr: Opcional[[float, ...]]) -> float:
    return wpen(x, y, yerr), wn_0(x, y, yerr)

def wsigma_calc_line(x: elementos, y: elementos, yerr: Opcional[[float, ...]]) -> float:
    return wsigma_pen(x, y, yerr), wsigma_n_0(x, y, yerr)

def wpen(x: elementos, y: elementos, yerr: Opcional[[float, ...]] = None) -> float:
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        if yerr == None:
            yerr = y._error
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)
    yerr = yerr if type(yerr) == type(np.array) else yerr * np.ones(x.size)

    w = 1/yerr**2

    return float((np.sum(w)*np.sum(w*x*y) - np.sum(w*x)*np.sum(w*y)) / (np.sum(w) * np.sum(w*x**2) - np.sum(w*x)**2))

def wn_0(x: elementos, y: elementos, yerr: Opcional[[float, ...]] = None) -> float:
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        if yerr == None:
            yerr = y._error
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)
    yerr = yerr if type(yerr) == type(np.array) else yerr * np.ones(x.size)

    w = 1/yerr**2

    return float(( np.sum(w*y) * np.sum(w*x**2) - np.sum(w*x) * np.sum(w*x*y)) / (np.sum(w) * np.sum(w * x**2) - np.sum(w*x)**2))

def wsigma_pen(x: elementos, y: elementos, yerr: Opcional[[float, ...]] = None) -> float:
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        if yerr == None:
            yerr = y._error
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)
    yerr = yerr if type(yerr) == type(np.array) else yerr * np.ones(x.size)

    w = 1/yerr**2

    return float(np.sqrt(np.sum(w) / ( np.sum(w) * np.sum(w*x**2) - np.sum(w*x)**2 ) ))

def wsigma_n_0(x: elementos, y: elementos, yerr: Opcional[[float, ...]] = None) -> float:
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        if yerr == None:
            yerr = y._error
        y = y._medida
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)
    yerr = yerr if type(yerr) == type(np.array) else yerr * np.ones(x.size)

    w = 1/yerr**2

    return float(np.sqrt( np.sum(w*x**2) / (np.sum(w) * np.sum(w*x**2) - np.sum(w*x)**2) ))


def compativility(a, da, b, db, nameA = 'A', nameB = 'B'):
    maxA = a+da
    maxB = b+db
    minA = a-da
    minB = b-db
    if (maxA >= b and minA <= b) and (maxB >= a and minB <= a):
        return f'{nameA} en {nameB} y {nameB} en {nameA}'
    if (maxA >= b and minA <= b) and not (maxB >= a and minB <= a):
        return f'{nameB} en {nameA} pero no {nameA} en {nameB}'
    if not(maxA >= b and minA <= b) and  (maxB >= a and minB <= a):
        return f'{nameA} en {nameB} pero no {nameB} en {nameA}'
    if (minA < maxB and a>b):
        return f'{nameA} y {nameB} tienen un rango compatible: [{minA}, {maxB}]'
    if (minB < maxA and b>a):
        return f'{nameA} y {nameB} tienen un rango compatible: [{minB}, {maxA}]'
    return f'{nameA} y {nameB} no son compatibles'
