import numpy as np

def media(*args: float) -> float:
    return np.array(sum(args)/len(args))

def desviacion_estandar(*args: float) -> float:
    return np.sqrt(sum((args - media(*args))**2)/(len(args)-1))

def error_estandar(*args: float) -> float:
    return desviacion_estandar(*args)/np.sqrt(len(args))
