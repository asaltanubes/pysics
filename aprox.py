import numpy as np
# from VACIO import NULL
from math import log10, trunc, floor, isnan, isinf, nan
from .type_alias import elementos
def aprox(valor: list[float] or float, error: list[float] or float) -> tuple[float, float] or tuple[list[float], list[float]]:
    # Si error no es un objeto iterable entonces se aplica la versión que no itera. Si es iterable entonces aplica la version que itera
    if not hasattr(valor, '__iter__'):
        return apr(valor, error)
    p = apr_list(valor, error)
    return p

def truncar(numero: float, digitos: int) -> float:
    stepper = 10**digitos
    return trunc(stepper*float(numero))/stepper

def apr(valor: float, error: float) -> tuple[float, float]:
    if error == 0 or isnan(error):
        return (valor, error)
    if isnan(valor):
        return (nan, apr(1, error)[1])
    if isinf(error):
        return (0, error)
    if isinf(valor):
        return (valor, apr(1, error)[1])
    a = truncar(error, -floor(log10(abs(error))))
    if log10(a) == floor(log10(a)):
        return (round(valor, 1-floor(log10(abs(error)))), round(error, 1-floor(log10(abs(error)))))
    return (round(valor, -floor(log10(abs(error)))), round(error, -floor(log10(abs(error)))))

def apr_list(valor: list[float], error: list[float]) -> tuple[list[float], list[float]]:
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
