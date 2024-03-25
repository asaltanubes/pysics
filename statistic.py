import numpy as np

def mean(*args: float) -> float:
    return np.array(sum(args)/len(args))

def standard_deviation(*args: float) -> float:
    return np.sqrt(sum((args - mean(*args))**2)/(len(args)-1))

def standard_error(*args: float) -> float:
    return standard_deviation(*args)/np.sqrt(len(args))
