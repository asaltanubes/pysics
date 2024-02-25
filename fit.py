from .objects import Measure, Line
import numpy as np
from scipy.optimize import curve_fit
from inspect import signature


def curve(function, x: list[float], y: list[float], sigma = None, initial_guess: list[float] = None, aproximate: bool = False):
    """
    Makes a fit to an arbitrary curve given by the function passed as a parameter.
    If no parameter is passed for sigma, the fit has no weights, if an iterable is passed, the values are taken as errors
    the values in the iterable. Otherwise, the values of the error of y are taken.
    """
    
    # It extracts the values of the Measures and the value of the errors in case it is valid
    if isinstance(y, Measure):
        if sigma == True:
            sigma = y.error
    
    x = np.array(x)
    y = np.array(y)
        
    # If an initial value is passed that is not iterable, it is converted into an iterable
    if initial_guess is not None and not hasattr(initial_guess, '__iter__'):
        initial_guess = (initial_guess, )
    
    # Checks that the number of parameters is correct
    if len(signature(function).parameters) > 1 and initial_guess is not None and len(initial_guess) != len(signature(function).parameters) - 1:
        raise TypeError(f'Length of "initial_guess" must be {len(signature(function).parameters)}, obtained {len(initial_guess)} parameters.')        
    
    popt, error = curve_fit(function, x, y, p0=initial_guess, sigma = sigma)
    # Returns a tuple with the Measures obtained
    return tuple((Measure(v, e, aproximate=aproximate) for v, e in zip(popt, np.sqrt(np.diag(error)))))

def r_line(x: list[float], y: list[float]):
    x = np.array(x)
    y = np.array(y)
    des_x = x - x.mean()
    des_y = y - y.mean()
    sigma_x = sum(des_x**2)
    sigma_y = sum(des_y**2)
    return sum(des_x * des_y)/np.sqrt(sigma_x*sigma_y)

def r_curve(function, x, y, sigma = None, initial_guess=None, aproximate = False) -> float:
    if isinstance(y, Measure):
        if hasattr(sigma, '__iter__'):
            sigma = y.error

    x = np.array(x)    
    y = np.array(y)

    if initial_guess is not None and len(initial_guess) != len(signature(function).parameters) - 1:
        raise TypeError(f'Length of "initial_guess" must be {len(signature(function).parameters)}, obtained {len(initial_guess)} parameters.')        
    
    if  len(signature(function).parameters) - 1 > 0 and initial_guess is not None and not hasattr(initial_guess, '__iter__'):
        initial_guess = (initial_guess, )
    
    popt, pcov = curve_fit(function, x, y)
    residuals = y- function(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    return np.sqrt(1 - (ss_res / ss_tot))

def least_squares(x: list[float], y: list[float], aproximate: bool = False) -> Line:
    """
    Calculates the Line of adjustment by least squares for two Measures.

    return tuple(Measure, Measure)
    (slope, n_0)
    slope: slope of the Line of adjustment
    n_0: ordinate in the origin of the Line of adjustment
    """
    slope, n_0 = calc_line(x, y)
    dslope, dn_0 = sigma_calc_line(x, y)
    slope: Measure = Measure(slope, dslope, aproximate=aproximate)
    n_0: Measure = Measure(n_0, dn_0, aproximate=aproximate)
    if isinstance(x, Measure):
        x = x.Measure
    return Line(slope, n_0, x)

def wleast_squares(x: Measure, y: Measure, yerr: list[float] = None, aproximate: bool = False) -> Line:
    """
    Calculates the Line of adjustment by weighted least squares for two Measures.
    The error of the y axis is extracted from the Measure \"y\" and the error of the x axis is
    neglected

    Args:
        slope: slope of the Line of adjustment
        n_0: ordinate in the origin of the Line of adjustment

    Returns:
        tuple(Measure, Measure): (slope, n_0)
    """

    slope, n_0 = wcalc_line(x=x, y=y, yerr=yerr)
    dslope, dn_0 = wsigma_calc_line(x=x, y=y, yerr=yerr)
    slope: Measure = Measure(slope, dslope, aproximate=aproximate)
    n_0: Measure = Measure(n_0, dn_0, aproximate=aproximate)
    if isinstance(x, Measure):
        x = x.Measure
    return Line(slope, n_0, x)

def line(x: list[float] , slope: float, n_0: float=0) -> list[float]:
    """
    Given a slope, an ordinate in the origin and a range of values of the x axis, it creates a line evaluating it at the points of x

    Args:
        x (elements): points at which the Line will be evaluated
        slope (float): slope of the Line
        n_0 (float, optional): ordinate in the origin of the Line. Defaults to 0.

    Returns:
        list[float]: the given Line evaluated at the points provided in x
    """

    if isinstance(slope, Line):
        n_0 = slope.n_0
        slope = slope.slopediente


    x = np.array(x)
    slope = np.array(slope)
    n_0 = np.array(n_0)    
    
    return x*slope + n_0

def calc_line(x: list[float], y: list[float]) -> tuple[float, float]:
    """
    Given 2 lists with the values x and y of a set of points returns the least squares fit of this set of points
    """
    return slope(x, y), n_0(x, y)

def sigma_calc_line(x: float, y: float) -> tuple[float, float]:
    """
    Given 2 lists with the values x and y of a set of points returns the errors of the slope and the ordinate in the origin of the least squares fit of this set of points
    """
    return sigma_slope(x, y), sigma_n_0(x, y)

def slope(x : list[float], y : list[float]) -> float:
    """
    Calculates the slope of the Line of adjustment by least squares for two Measures.
    """

    x = np.array(x)
    y = np.array(y)
    
    x = x if type(x) == type(np.array) else np.array(x)
    y = y if type(y) == type(np.array) else np.array(y)

    return float((x.size*np.sum(x*y) - np.sum(x)*np.sum(y))/(x.size*np.sum(x**2) - np.sum(x)**2))

def n_0 (x : list[float], y : list[float]) -> float:
    """
    Calculates the ordinate in the origin of the Line of adjustment by least squares for two Measures.
    """
    x = np.array(x) 
    y = np.array(y) 

    return float((np.sum(y)*np.sum(x**2) - np.sum(x)*np.sum(x*y))/(x.size * np.sum(x**2) - (np.sum(x))**2))

def sigma_y(x : list[float], y : list[float]) -> float:
    """
    Calculates the standard deviation of the experimental values to their least squares fit Line

    Args:
        x (iterable o Measure): values of the points on the x axis
        y (iterable o Measure): values of the points on the y axis

    Returns:
        float: standard deviation of the Line
    """
    x = np.array(x) 
    y = np.array(y) 

    ŷ = line(x=x, slope=slope(x, y), n_0=n_0(x, y))
    return float(np.sqrt( (np.sum( (y-ŷ)**2 ) ) / (x.size - 2)))

def sigma_slope(x: list[float], y: list[float]) -> float:
    """
    Calculates the standard deviation of the slope of a least squares fit

    Args:
        x (iterable o Measure): values of the points on the x axis
        y (iterable o Measure): values of the points on the y axis

    Returns:
        float: standard deviation of the slope
    """
    x = np.array(x) 
    y = np.array(y) 

    return float(sigma_y(x, y) *np.sqrt( x.size / (x.size * np.sum(x**2) - np.sum(x)**2) ))

def sigma_n_0(x: list[float], y: list[float]) -> float:
    """
    Calculates the standard deviation of the ordinate in the origin of a least squares fit

    Args:
        x (iterable o Measure): values of the points on the x axis
        y (iterable o Measure): values of the points on the y axis  

    Returns:
        float: standard deviation of the ordinate in the origin
    """
    x = np.array(x) 
    y = np.array(y) 

    return float(sigma_y(x, y) * np.sqrt( np.sum(x**2) / (x.size * np.sum(x**2) - np.sum(x)**2) ))


def wcalc_line(x: list[float], y: list[float], yerr: list[float] = None) -> tuple[float, float]:
    """
    Calculate a Line by weighted least squares

    Args:
        x (elements): Values of the x axis of the Line
        y (elements): Values of the y axis of the Line
        yerr (Optional[[float, ...]]): Errors in the y axis (If no value is passed then the error of the y is taken in case it is a Measure)

    Returns:
        tuple[float, float]: pajera slopedinete-ordenada en el origen de los valores obtenidos
    """
    return wslope(x, y, yerr), wn_0(x, y, yerr)

def wsigma_calc_line(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """
    Calculate the standard errors of the weighted least squares fit

    Args:
        x (elements): Values of the x axis of the Line
        y (elements): Values of the y axis of the Line
        yerr (Optional[[float, ...]]): Errors in the y axis (If no value is passed then the error of the y is taken in case it is a Measure)

    Returns:
        tuple[float, float]: pajera error de la slopedinete-ordenada en el origen de los valores obtenidos (sigma slope, sigma n_0)
    """
    return wsigma_slope(x, y, yerr), wsigma_n_0(x, y, yerr)

def wslope(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """
    Calculates the slope of a Line by weighted least squares
    """
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y._error
    yerr = yerr if yerr.len() != 1 else yerr * np.ones(x.size)

    x = np.array(x) 
    y = np.array(y) 
    
    w = 1/yerr**2

    return float((np.sum(w)*np.sum(w*x*y) - np.sum(w*x)*np.sum(w*y)) / (np.sum(w) * np.sum(w*x**2) - np.sum(w*x)**2))

def wn_0(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """
    Calculates the ordinate in the origin of a Line by weighted least squares
    """
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y._error
    yerr = yerr if yerr.len() != 1 else yerr * np.ones(x.size)

    x = np.array(x) 
    y = np.array(y) 
    

    w = 1/yerr**2

    return float(( np.sum(w*y) * np.sum(w*x**2) - np.sum(w*x) * np.sum(w*x*y)) / (np.sum(w) * np.sum(w * x**2) - np.sum(w*x)**2))

def wsigma_slope(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """Calculates the standard error of the slope of a Line by weighted least squares"""
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y._error
    yerr = yerr if yerr.len() != 1 else yerr * np.ones(x.size)

    x = np.arary(x)    
    y = np.arary(y)    
    
    w = 1/yerr**2

    return float(np.sqrt(np.sum(w) / ( np.sum(w) * np.sum(w*x**2) - np.sum(w*x)**2 ) ))

def wsigma_n_0(x: list[float], y: list[float], yerr: list[float] = None) -> float:
    """Calculates the standard error of the ordinate in the origin of a Line by weighted least squares"""
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
