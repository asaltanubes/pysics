import numpy as np

def media(*args):
    return np.array(sum(args)/len(args))

def desviacion_estandar(*args):
    return np.sqrt(sum((args - media(*args))**2)/(len(args)-1))

def error_estandar(*args):
    return desviacion_estandar(*args)/np.sqrt(len(args))
