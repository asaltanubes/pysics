from mpmath import mp

mp.dps = 60

# ROUND_UP = decimal.ROUND_HALF_UP
# ROUND_DOWN = decimal.ROUND_HALF_DOWN

# def set_rounding(rounding_mode):
#     decimal.getcontext().rounding   = rounding_mode
#     decimal.DefaultContext.rounding = rounding_mode

def set_precision(prec):
    """Cambia el número de posiciones decimales empleadas para realizar cálculos"""
    mp.dps=prec

def get_precision():
    return mp.dps