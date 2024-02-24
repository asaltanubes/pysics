from .objetos import Measure, Line
import numpy as np
from scipy.optimize import curve_fit
from inspect import signature



def curva(funcion, x: list[float], y: list[float], sigma = None, initial_guess: list[float] = None, aproximar: bool = False):
    '''Hace un ajuste a una curva arbitraria dada por la funcion pasada como parametro.
    Si no se pasa parametro para sigma el ajuste no tiene pesos, si se pasa un iterable se toman como erroes
    los valores en el iterable. En otro caso se toman los valores del error de y'''
    
    # Se extraen los valores de las Measures y el valor de los errores en caso valido
    # if isinstance(x, Measure):
        # x = x._Measure
    if isinstance(y, Measure):
        if sigma == True:
            sigma = y.error
    
    x = np.array(x)
    y = np.array(y)
        
    # Si se pasa un valor inicial que no sea iterable se convierte en un iterable
    if initial_guess is not None and not hasattr(initial_guess, '__iter__'):
        initial_guess = (initial_guess, )
    
    # Se comprueba que el número de parámetros sea el correcto
    if len(signature(funcion).parameters) > 1 and initial_guess is not None and len(initial_guess) != len(signature(funcion).parameters) - 1:
        raise TypeError(f'La longitud de "initial_guess" debe ser {len(signature(funcion).parameters)} se obtuvieron {len(initial_guess)} parametros')        
    
    popt, error = curve_fit(funcion, x, y, p0=initial_guess, sigma = sigma)
    # Se devuelve una tupla con las Measures obtenidas
    return tuple((Measure(v, e, aproximar=aproximar) for v, e in zip(popt, np.sqrt(np.diag(error)))))

def r_line(x: list[float], y: list[float]):
    x = np.array(x)
    y = np.array(y)
    des_x = x - x.mean()
    des_y = y - y.mean()
    sigma_x = sum(des_x**2)
    sigma_y = sum(des_y**2)
    return sum(des_x * des_y)/np.sqrt(sigma_x*sigma_y)

def r_curva(funcion, x, y, sigma = None, initial_guess=None, aproximar = False) -> float:
    if isinstance(y, Measure):
        if hasattr(sigma, '__iter__'):
            sigma = y.error

    x = np.array(x)    
    y = np.array(y)

    if initial_guess is not None and len(initial_guess) != len(signature(funcion).parameters) - 1:
        raise TypeError(f'La longitud de "initial_guess" debe ser {len(signature(funcion).parameters)} se obtuvieron {len(initial_guess)} parametros')    
    
    if  len(signature(funcion).parameters) - 1 > 0 and initial_guess is not None and not hasattr(initial_guess, '__iter__'):
        initial_guess = (initial_guess, )
    
    popt, pcov = curve_fit(funcion, x, y)
    residuals = y- funcion(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    return np.sqrt(1 - (ss_res / ss_tot))

def minimos_cuadrados(x: list[float], y: list[float], aproximar: bool = False) -> Line:
    """
    Calcula la Line de ajuste por mínimos cuadrados para dos Measures.

    return tuple(Measure, Measure)
    (pen, n_0)
    pen: pendiente de la Line de ajuste
    n_0: ordenada en el origen de la Line de ajuste
    """
    p, n = calc_line(x, y)
    dp, dn = sigma_calc_line(x, y)
    pen: Measure = Measure(p, dp, aproximar=aproximar)
    n_0: Measure = Measure(n, dn, aproximar=aproximar)
    if isinstance(x, Measure):
        x = x.Measure
    return Line(pen, n_0, x)

def minimos_pesados(x: Measure, y: Measure, yerr: list[float] = None, aproximar: bool = False) -> Line:
    """
    Calcula la Line de ajuste por mínimos cuadrados pesados para dos Measures.
    El error del eje y se extrae de la Measure \"y\" y el error del eje x se
    desprecia
    Args: 
        pen: pendiente de la Line de ajuste
        n_0: ordenada en el origen de la Line de ajuste
    
    Returns:
        tuple(Measure, Measure): (pendiente, ordenada en el origen)
    """

    p, n = wcalc_line(x=x, y=y, yerr=yerr)
    dp, dn = wsigma_calc_line(x=x, y=y, yerr=yerr)
    pen: Measure = Measure(p, dp, aproximar=aproximar)
    n_0: Measure = Measure(n, dn, aproximar=aproximar)
    if isinstance(x, Measure):
        x = x.Measure
    return Line(pen, n_0, x)

def line(x: list[float] , pen: float, n_0: float=0) -> list[float]:
    """Dados una pendiente, una ordenada en el orígen y un rango de valores del eje x crea una línea evaluandola en los puntos de x

    Args:
        x (elementos): puntos en los que la Line va a ser evaluada
        pen (float): pendiente de la Line
        n_0 (float, optional): ordenada en el origen de la Line. Defaults to 0.

    Returns:
        list[float]: la Line dada evaluada en los puntos proporcionados en x
    """

    if isinstance(pen, Line):
        n_0 = pen.n_0
        pen = pen.pendiente


    x = np.array(x)
    pen = np.array(pen)
    n_0 = np.array(n_0)    
    
    return x*pen + n_0

def calc_line(x: list[float], y: list[float]) -> tuple[float, float]:
    """Dadas 2 listas con los valores x e y de un conjunto de puntos devuelve el ajuste por mínimos cuadrados de esta"""
    return pen(x, y), n_0(x, y)

def sigma_calc_line(x: float, y: float) -> tuple[float, float]:
    """Dadas 2 listas con los valores x e y de un conjunto de puntos devuelve los errores de la pendiente y la ordenada en el origen"""
    return sigma_pen(x, y), sigma_n_0(x, y)

def pen(x : list[float], y : list[float]) -> float:
    """Calcula la pendiente de la Line de ajuste"""

    x = np.array(x)
    y = np.array(y)
    
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)

    return float((x.size*np.sum(x*y) - np.sum(x)*np.sum(y))/(x.size*np.sum(x**2) - np.sum(x)**2))

def n_0 (x : list[float], y : list[float]) -> float:
    """Calcula la ordenada en el origen de la Line de ajuste"""
    x = np.array(x) 
    y = np.array(y) 

    return float((np.sum(y)*np.sum(x**2) - np.sum(x)*np.sum(x*y))/(x.size * np.sum(x**2) - (np.sum(x))**2))

def sigma_y(x : list[float], y : list[float]) -> float:
    """Calcula la desviación estandar de los valores experimentales a su Line de ajuste por mínimos cuadrados

    Args:
        x (iterable o Measure): valores de los puntos en el eje x
        y (iterable o Measure): valores de los puntos en el eje y

    Returns:
        float: desviación estandar de la Line
    """
    x = np.array(x) 
    y = np.array(y) 

    ŷ = line(x=x, pen=pen(x, y), n_0=n_0(x, y))
    return float(np.sqrt( (np.sum( (y-ŷ)**2 ) ) / (x.size - 2)))

def sigma_pen(x: list[float], y: list[float]) -> float:
    """Calcula la desviación estandar de la pendiente de un ajuste por mínimos cuadrados

    Args:
        x (Iterable o Measure): Valores de los puntos en el eje x
        y (Iterable o Measure): Valores de los puntos en el eje y

    Returns:
        float: Desviación estandar de la pendiente
    """
    x = np.array(x) 
    y = np.array(y) 

    return float(sigma_y(x, y) *np.sqrt( x.size / (x.size * np.sum(x**2) - np.sum(x)**2) ))

def sigma_n_0(x: list[float], y: list[float]) -> float:
    """Calcula la desviación estandar de la ordenada en el origen de un ajuste por mínimos cuadrados

    Args:
        x (Iterable o Measure): Valores de los puntos en el eje x
        y (Iterable o Measure): Valores de los puntos en el eje y

    Returns:
        float: Desviación estandar de la ordenada en el origen
    """
    x = np.array(x) 
    y = np.array(y) 

    return float(sigma_y(x, y) * np.sqrt( np.sum(x**2) / (x.size * np.sum(x**2) - np.sum(x)**2) ))


def wcalc_line(x: list[float], y: list[float], yerr: list[float] = None) -> tuple[float, float]:
    """Calcula una Line por mínimos cuadrados pesados

    Args:
        x (elementos): Valores del eje x de la Line
        y (elementos): Valores del eje y de la Line
        yerr (Opcional[[float, ...]]): Errores en el eje y (Si no se pasa un valor entoces se tomo el error de la y en caso de ser una Measure)

    Returns:
        tuple[float, float]: pajera pendinete-ordenada en el origen de los valores obtenidos
    """
    return wpen(x, y, yerr), wn_0(x, y, yerr)

def wsigma_calc_line(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """Calcula los errores estandard del ajuste por mínimos cuadrados pesados

    Args:
        x (elementos): Valores del eje x de la Line
        y (elementos): Valores del eje y de la Line
        yerr (Opcional[[float, ...]]): Errores en el eje y (Si no se pasa un valor entoces se tomo el error de la y en caso de ser una Measure)

    Returns:
        tuple[float, float]: pajera error de la pendinete-ordenada en el origen de los valores obtenidos (sigma pen, sigma n_0)
    """
    return wsigma_pen(x, y, yerr), wsigma_n_0(x, y, yerr)

def wpen(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """Calcula la pendiente por un ajuste por mínimos cuadrados pesados"""
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y._error
    yerr = yerr if yerr.len() != 1 else yerr * np.ones(x.size)

    x = np.array(x) 
    y = np.array(y) 
    
    w = 1/yerr**2

    return float((np.sum(w)*np.sum(w*x*y) - np.sum(w*x)*np.sum(w*y)) / (np.sum(w) * np.sum(w*x**2) - np.sum(w*x)**2))

def wn_0(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """Calcula la ordenada en el orígen por un ajuste por mínimos cuadrados pesados"""
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y._error
    yerr = yerr if yerr.len() != 1 else yerr * np.ones(x.size)

    x = np.array(x) 
    y = np.array(y) 
    

    w = 1/yerr**2

    return float(( np.sum(w*y) * np.sum(w*x**2) - np.sum(w*x) * np.sum(w*x*y)) / (np.sum(w) * np.sum(w * x**2) - np.sum(w*x)**2))

def wsigma_pen(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """Calcula el error estandar en la ordenada en el orígen del ajuste por mínimos pesados"""
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y._error
    yerr = yerr if yerr.len() != 1 else yerr * np.ones(x.size)

    x = np.arary(x)    
    y = np.arary(y)    
    
    w = 1/yerr**2

    return float(np.sqrt(np.sum(w) / ( np.sum(w) * np.sum(w*x**2) - np.sum(w*x)**2 ) ))

def wsigma_n_0(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """Calcula el error estandar en la ordenada en el orígen del ajuste por mínimos pesados"""
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y._error
    yerr = yerr if yerr.len() != 1 else yerr * np.ones(x.size)

    x = np.array(x)    
    y = np.array(y)    
    
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
