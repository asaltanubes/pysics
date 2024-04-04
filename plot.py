from matplotlib import pyplot as plt
from os.path import exists
from .fit import line as fit_line
from .objects import Measure, Line
from numpy import linspace, geomspace
from typing import Union
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, '')
use_sci_notation = True
range_without_sci_notation = (-2, 2)

def scatter(x: list[float], y: list[float], c: str = 'tab:red', fill = True, marker: str = 'o', s: int = 50, label: str = None, zorder: int = 100, 
            xerr: list[float]=None, yerr: list[float] = None, errorbarcolor = "tab:red", barzorder = 0, **kargs):
    
    if isinstance(x, Measure):
        if xerr == True:
            xerr = x.error

    if isinstance(y, Measure):
        if yerr == True:
            yerr = y.error
    
    x = np.array(x)
    y = np.array(y)

    if xerr is not None or yerr is not None:
        errorbar(x, y, yerr = yerr, xerr = xerr, errorbarcolor = errorbarcolor, zorder = barzorder)

    facecolors = 'none' if not fill else c
    plt.scatter(x, y, s=s, marker = marker, facecolors = facecolors, edgecolors = c, label=label, zorder = zorder, **kargs)


def plot(x: list[float], y: list[float], label=None, **kargs):

    x = np.array(x) 
    y = np.array(y)
    
    plt.plot(x, y, label = label, **kargs)


def line(x: Union[list[float], Line], slope: Union[Measure, float, Line]=0, n_0=0, c = 'tab:blue', label=None, **kargs):
    if isinstance(x, Measure):
        x = x.value
    if isinstance(slope, Line):
        n_0 = slope.n_0
        slope = slope.slope
    if isinstance(x, Line):
        slope = x.slope
        n_0 = x.n_0
        x = x.x
    plt.plot(x, fit_line(x, slope, n_0), c=c, label=label, **kargs)

def curve(function, x, coefs, log_linspace = False, label = None, n=100, **kargs):
    # Coefs can be a Measure or an iterable of Measures
    # In the first case each coeficient is the value of each measure
    # In the second case each coeficient is the first value of the measure
    # If there is only one coeficient it is taken as a singular coeficient

    if isinstance(coefs, Measure):
        coefs = coefs.value
        
    if hasattr(coefs, '__iter__'):
        if isinstance(coefs[0], Measure):
            coefs = [i.value[0] for i in coefs]
    else:
        from inspect import signature
        if len(signature(function).parameters) == 2 or hasattr(coefs, '__iter__'):
            coefs = (coefs, )
            
    x = linspace(min(x), max(x), n) if not log_linspace else geomspace(min(x), max(x), n)
    y = [function(i, *coefs) for i in x]
    plot(x, y, label, **kargs)

def polar_plot(theta: list[float], r: list[float], label=None,  **kargs):
    if isinstance(theta, Measure):
        theta = theta.value
    if isinstance(r, Measure):
        r = r.value
    plt.polar(theta, r, label=label, **kargs)

def polar_scatter(theta, r, c: str = 'tab:red', fill = True, marker: str = 'o', s: int = 5, label: str = None, zorder: int = 100, **kargs):
    facecolors = 'none' if not fill else c
    polar_plot(theta, r, marker=marker, markerfacecolor= facecolors, markeredgecolor=c, linestyle='None', markersize=s, label=label, zorder=zorder, **kargs)
    
def polar_curve(function, theta, coefs, label=None, **kargs):
    if isinstance(coefs, Measure):
        coefs = coefs.value
        
    if hasattr(coefs, '__iter__'):
        if isinstance(coefs[0], Measure):
            coefs = [i.value[0] for i in coefs]
    else:
        from inspect import signature
        if len(signature(function).parameters) == 2 or hasattr(coefs, '__iter__'):
            coefs = (coefs, )
            
    theta = linspace(min(theta), max(theta))
    r = [function(i, *coefs) for i in theta]
    polar_plot(theta, r, label=label, **kargs)

def errorbar(x: list[float], y: list[float], yerr=None, xerr = None, errorbarcolor = 'tab:red', **kargs):
    if isinstance(x, Measure):
        if xerr == None:
            xerr = x.error
        x = x.value
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y.error
        y = y.value
    plt.errorbar(x, y, yerr = yerr, xerr = xerr, ecolor = errorbarcolor, fmt = 'none', **kargs)


def text(text: str = '', x: float = 0, y: float = 0, fontsize = 10, **kargs):
    plt.text(x, y, text, fontsize=fontsize, **kargs)

def annotate(text: str = '', xy = (0,0), xytext =(0,0), fontsize = 10, arrowstyle='->', arc = 0,**kargs):
    arrowprops = dict(arrowstyle=arrowstyle, connectionstyle=f"arc3, rad ={arc}")
    if isinstance(xy[0], (list, tuple)):
        for point in xy[1:]:   
            plt.annotate(text, xy=point, xytext=xytext, fontsize=fontsize, arrowprops = arrowprops, color=(0, 0, 0, 0),**kargs)
        xy = xy[0]
    plt.annotate(text, xy=xy, xytext=xytext, fontsize=fontsize, arrowprops = arrowprops,**kargs)

def arrow(xy0 = (0,0), xy1=(0,0), arc=0):
    arrowprops = dict(arrowstyle='->', connectionstyle=f"arc3, rad ={arc}")
    plt.annotate('', xy1, xy0, arrowprops=arrowprops)

def limits(bottom=None, top=None, left=None, right=None):
    plt.ylim(bottom, top)
    plt.xlim(left, right)

def doble_y(*args, **kargs):
    """
    Add a second y axis to the plot. From the call to this function the values are added to the second axis
    """
    plt.twinx(*args, **kargs)

def doble_x(*args, **kargs):
    """
    Add a second x axis to the plot. From the call to this function the values are added to the second axis
    """
    plt.twiny(*args, **kargs)

def xlabel(text, fontsize = 15, **kargs):
    plt.xlabel(text, fontsize = fontsize, **kargs)

def ylabel(text, fontsize = 15, **kargs):
    plt.ylabel(text, fontsize = fontsize, **kargs)

def ticks(fontsize = 14, **kargs):
    plt.xticks(fontsize=fontsize, **kargs)
    plt.yticks(fontsize=fontsize, **kargs)

def xticks(fontsize=14, **kargs):
    plt.xticks(fontsize=fontsize, **kargs)

def yticks(fontsize=14, **kargs):
    plt.yticks(fontsize=fontsize, **kargs)

def title(text, fontsize=18, **kargs):
    plt.title(text, fontsize=fontsize, **kargs)

def legend(*args, **kargs):
    plt.legend(*args, **kargs)

def figure(id, **kargs):
    plt.figure(id, **kargs)

def clic_input():
    try:
        import pyperclip
        while True:
            d = plt.ginput(1, timeout = -1)[0]
            pyperclip.copy(str(d))
    except ModuleNotFoundError:
        while True:
            d = plt.ginput(1, timeout = -1)[0]
            print(d)

def tight_layout():
    plt.tight_layout()

def size(left=.1, right = .9, bottom=.1, top=.9, **kargs):
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, **kargs)

def save(path: str = 'figura', format='pdf', overwrite = True, dpi = 'figure', auto_size = True, auto_tick_format = True, xlogscale=False, **kargs):
    if not overwrite:
        if exists(f'{path}.{format}'):
            i = 0
            while exists(f'{path}({i}).{format}'):
                i += 1
            path = path + f'({i})'
    if xlogscale:
        if auto_tick_format: print("WARNING: auto_tick_format does not support logscale. It has been automatically deactivated. ")
    if auto_tick_format and not xlogscale: 
        try:
            tick_format()
        except AttributeError:
            print("WARNING: auto_tick_format does not work on polar plots and is disabled by default.")
    if auto_size: tight_layout()
    if xlogscale: plt.xscale("log")
    if use_sci_notation: plt.ticklabel_format(style="sci", scilimits=range_without_sci_notation)
    plt.savefig(f'{path}.{format}', dpi=dpi, format = format, **kargs)

def show(*args, auto_size = True, auto_tick_format = True, xlogscale = False):
    if xlogscale:
        if auto_tick_format: print("WARNING: auto_tick_format does not support logscale. It has been automatically deactivated.")
    if auto_tick_format and not xlogscale: 
        try:
            tick_format()
        except AttributeError:
            print("WARNING: auto_tick_format does not work on polar plots and is disabled by default.")
        
    if auto_size: tight_layout()
    if xlogscale: plt.xscale("log")
    if use_sci_notation: plt.ticklabel_format(style="sci", scilimits=range_without_sci_notation)
    plt.show(*args)

def tick_format(locale = True, useMathText=True, style = '', scilimits = None, **kargs):
    plt.ticklabel_format(useLocale=locale, style=style, scilimits=scilimits, useMathText=useMathText, **kargs)

def set_sci_notation(usar=use_sci_notation, rango=range_without_sci_notation):
    global range_without_sci_notation, use_sci_notation
    use_sci_notation = usar
    range_without_sci_notation = rango
    
def use_latex(use=True):
    plt.rc("text", usetex= use)

def use_latex_packages(*packages):
     plt.rc('text.latex', preamble="\n".join((r"\usepackage{" + i + "}" for i in packages)))
    
def add_latex_code(code):
    plt.rc('text.latex', preamble="\n".join(code))
