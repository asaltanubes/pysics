import numpy as np
from math import trunc, isnan, isinf, nan
from . import calculos

def aprox(value: list[float], error: list[float]) -> tuple[list[float], list[float]]:
    """
    Aproximate a value and its error to the first significant figure of the error (3.894 ± 0.26 -> 4.0 ± 0.3) or to the first two if the first is 1 (3.834 ± 0.169 -> 3.83 ± 0.17)
    If a list of values is passed, it is applied to each pair separately

    Args:
        value (list[float]orfloat): value/s to approximate
        error (list[float]orfloat): error/s of the measures

    Returns:
        tuple[float, float] or tuple[list[float], list[float]]: (value/s, error/s) returns the value/s and the/los error/s approximated
    """
    # If error is not an iterable object then the version that does not iterate is applied. If it is iterable then the version that iterates is applied
    if not hasattr(value, '__iter__'):
        return apr(value, error)
    p = apr_list(value, error)
    return p

def truncate(number: float, digits: int) -> float:
    """
    Truncate a value with n digits where n is the number of digits after the "."
    examples(truncate(10.93, 1) -> 10.9; truncate(10.935, 2) -> 10.93; truncate(10.720, 0) -> 10; truncate(11.111, -1) -> 10)
    
    Args:
        number (float): value to truncate
        digits (int): number of digits to take after the .

    Returns:
        float: truncated value
    """
    stepper = 10**digits
    return trunc(stepper*float(number))/stepper

def significative_figure(num: float) -> int:
    """
    Calculates the position of the first significant figure
    Examples: (5 -> 1; 11 -> 2; 123 -> 3; 0.001 -> -3)

    Args:
        num (float): value of which you want to know the significant figure

    Returns:
        int: position of the significant figure (10**significative_figure has the same order of magnitude as num)
    """
    return np.floor(np.log10(abs(num)))

def apr(value: float, error: float) -> tuple[float, float]:
    """
    Aproximate a value and its error to the first significant figure of the error (3.894 ± 0.26 -> 4.0 ± 0.3) or to the first two if the first is 1 (3.834 ± 0.169 -> 3.83 ± 0.17)

    Args:
        value (float): value to approximate
        error (float): error of the measure

    Returns:
        tuple[float, float]: (value, error) returns the value and the error approximated
    """
    
    if error == 0 or isnan(error):
        return (value, error)
    if isnan(value):
        return (nan, apr(1, error)[1])
    if isinf(error):
        return (0, error)
    if isinf(value):
        return (value, apr(1, error)[1])
    
    error_figures = -significative_figure(error)
    a = truncate(error, error_figures)
    
    # If the first significant figure is 1
    if np.log10(a) == np.floor(np.log10(a)):
        # If when approximating to the next one the result is 1 then the next one is also taken.
        # I check if it is less than 2 for possible floating point errors. I hate floating point arithmetic.
        if calculos.round(error, error_figures) < 2*10**(-error_figures):
            error_figures += 1
    return (calculos.round(value, error_figures), calculos.round(error, error_figures))

def apr_list(value: list[float], error: list[float]) -> tuple[list[float], list[float]]:
    """
    Apply apr to a list of values and errors
    """
    if not isinstance(value, np.ndarray):
        value = np.array(value)
    # If error is a scalar, it is transformed into a list of the same length as value
    if not hasattr(error, '__iter__'):
        error = np.array(error + 0*value)
    vallist = []
    errlist = []
    for i in zip(value, error):
        v, e = apr(*i)
        vallist.append(v)
        errlist.append(e)
    vallist = np.array(vallist)
    errlist = np.array(errlist)
    return (vallist, errlist)

# rip monstruosidad de función de aproximación larga vida a apr con logaritmos
# def apr(value, error):
#     if error == 0:
#         return (value, error)
#     value = float(value)
#     error = float(error)
#     string_error = str('%f' % error)
#
#     valuees_error = string_error.replace('.', '')
#
#     cifra_significativa = 0
#     ignored_valuees = ['0', '1']
#     while valuees_error[cifra_significativa] in ignored_valuees:
#         cifra_significativa += 1
#         if valuees_error[cifra_significativa-1] == '1':
#             break
#         if cifra_significativa >=len(valuees_error):
#             if valuees_error[-1] == '1':
#                 cifra_significativa += 1
#             break
#     posición_punto = string_error.find('.') if '.' in string_error else len(string_error)
#     calculos.round_pos = cifra_significativa - posición_punto + 1
#     return (calculos.round(value, calculos.round_pos), calculos.round(error, calculos.round_pos))

if __name__ == '__main__':
    a = [8.365241, 935.27, 89523.68586583]
    e = [.35, 1.34, 1.389656]
    print(aprox(a, e))
