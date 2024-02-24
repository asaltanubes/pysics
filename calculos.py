from numpy import floor, ceil

ROUND_UP = 1
ROUND_DOWN = 2

ROUND_MODE = ROUND_DOWN


def set_rounding(rounding_mode):
    global ROUND_MODE
    ROUND_MODE = rounding_mode

def round(n, decimals=0, rounding = None):
    global ROUND_MODE, ROUND_UP
    multiplier = 10 ** decimals
    rounding = rounding if rounding is not None else ROUND_MODE
    if rounding is ROUND_UP:
        return floor(n*multiplier + 0.5) / multiplier
    else:
        return ceil(n*multiplier - 0.5) / multiplier