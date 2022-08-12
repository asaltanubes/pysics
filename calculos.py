import decimal
from tkinter import ROUND
from typing import Type

decimal.DefaultContext.prec = 60

ROUND_UP = decimal.ROUND_HALF_UP
ROUND_DOWN = decimal.ROUND_HALF_DOWN

def set_rounding(rounding_mode):
    decimal.getcontext().rounding   = rounding_mode
    decimal.DefaultContext.rounding = rounding_mode

def set_precision(prec):
    decimal.getcontext().prec   = prec
    decimal.DefaultContext.prec = prec

def get_precision(prec):
    decimal.getcontext().prec = prec