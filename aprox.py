import numpy as np
# from VACIO import NULL
from math import log10, trunc, floor, isnan, isinf, nan
from .type_alias import elementos

def aprox(valor: list[float] or float, error: list[float] or float) -> tuple[float, float] or tuple[list[float], list[float]]:
    """Aproxima un valor y su error a la primera cifra significativa del error (3.894 ± 0.26 -> 4.0 ± 0.3) o a las dos primeras si la primera es 1 (3.834 ± 0.169 -> 3.83 ± 0.17)
       Si se pasan una lista de valores se aplica a cada pareja por separado

    Args:
        valor (list[float]orfloat): valor/es a aproximar
        error (list[float]orfloat): error/es de las medidas

    Returns:
        tuple[float, float] or tuple[list[float], list[float]]: (valor/es, error/es) devuleve el valor/es y el/los error/es aproximados
    """
    # Si error no es un objeto iterable entonces se aplica la versión que no itera. Si es iterable entonces aplica la version que itera
    if not hasattr(valor, '__iter__'):
        return apr(valor, error)
    p = apr_list(valor, error)
    return p

def truncar(numero: float, digitos: int) -> float:
    """Trunca un valor con n digitos donde n es el número de digitos tras el "." 
        ejemplos(truncar(10.93, 1) -> 10.9; truncar(10.935, 2) -> 10.93; truncar(10.720, 0) -> 10; truncar(11.111, -1) -> 10)

    Args:
        numero (float): valor a truncar
        digitos (int): número de digitos a coger tras el .

    Returns:
        float: valor truncado
    """
    stepper = 10**digitos
    return trunc(stepper*float(numero))/stepper

def cifra_significativa(num: float) -> int:
    """Calcula la posición de la primera cifra significativa
       Ejemplos: (5 -> 1; 11 -> 2; 123 -> 3; 0.001 -> -3)

    Args:
        num (float): valor del que se desea conocer la cifra significativa

    Returns:
        int: posición de la cifra significativa (10**cifra_sinificativa tiene el mismo orden de magnitud que num)
    """
    return floor(log10(abs(num)))

def apr(valor: float, error: float) -> tuple[float, float]:
    """Aproxima un valor y su error a la primera cifra significativa del error (3.894 ± 0.26 -> 4.0 ± 0.3) o a las dos primeras si la primera es 1 (3.834 ± 0.169 -> 3.83 ± 0.17)

    Args:
        valor (float): valor a aproximar
        error (float): error de la medida

    Returns:
        tuple[float, float]: (valor, error) devuleve el valor y el error aproximados
    """
    
    if error == 0 or isnan(error):
        return (valor, error)
    if isnan(valor):
        return (nan, apr(1, error)[1])
    if isinf(error):
        return (0, error)
    if isinf(valor):
        return (valor, apr(1, error)[1])
    a = truncar(error, -cifra_significativa(error))
    
    # Si la primera cifra significativa es un 1
    if log10(a) == floor(log10(a)):
        return (round(valor, 1-cifra_significativa(error)), round(error, 1-cifra_significativa(error)))
    return (round(valor, -cifra_significativa(error)), round(error, -cifra_significativa(error)))

def apr_list(valor: list[float], error: list[float]) -> tuple[list[float], list[float]]:
    """Aplica apr a una lista de valores y errores"""
    if not isinstance(valor, np.ndarray):
        valor = np.array(valor)
    # Si error es un escalar se transforma en una lista de la misma longitud que valor
    if not hasattr(error, '__iter__'):
        error = np.array(error + 0*valor)
    vallist = []
    errlist = []
    for i in zip(valor, error):
        v, e = apr(*i)
        vallist.append(v)
        errlist.append(e)
    vallist = np.array(vallist)
    errlist = np.array(errlist)
    return (vallist, errlist)

# rip monstruosidad de función de aproximación larga vida a apr con logaritmos
# def apr(valor, error):
#     if error == 0:
#         return (valor, error)
#     valor = float(valor)
#     error = float(error)
#     string_error = str('%f' % error)
#
#     valores_error = string_error.replace('.', '')
#
#     cifra_significativa = 0
#     ignored_valores = ['0', '1']
#     while valores_error[cifra_significativa] in ignored_valores:
#         cifra_significativa += 1
#         if valores_error[cifra_significativa-1] == '1':
#             break
#         if cifra_significativa >=len(valores_error):
#             if valores_error[-1] == '1':
#                 cifra_significativa += 1
#             break
#     posición_punto = string_error.find('.') if '.' in string_error else len(string_error)
#     round_pos = cifra_significativa - posición_punto + 1
#     return (round(valor, round_pos), round(error, round_pos))

if __name__ == '__main__':
    a = [8.365241, 935.27, 89523.68586583]
    e = [.35, 1.34, 1.389656]
    print(aprox(a, e))
