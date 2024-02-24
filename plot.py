from matplotlib import pyplot as plt
from os.path import exists
from .ajuste import line as ajuste_linea
from .objetos import Measure, Line
from numpy import linspace, geomspace
from typing import Union
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, '')
usar_notacion_cientifica = True
rango_sin_notacion_cientifica = (-2, 2)

def scatter(x: list[float], y: list[float], c: str = 'tab:red', relleno = True, marker: str = 'o', s: int = 50, label: str = None, zorder: int = 100, 
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
        plt.errorbar(x, y, yerr = yerr, xerr = xerr, ecolor = errorbarcolor, zorder = barzorder)

    facecolors = 'none' if not relleno else c
    plt.scatter(x, y, s=s, marker = marker, facecolors = facecolors, edgecolors = c, label=label, zorder = zorder, **kargs)


def plot(x: list[float], y: list[float], label=None, **kargs):

    x = np.array(x) 
    y = np.array(y)
    
    plt.plot(x, y, label = label, **kargs)


def line(x: Union[list[float], Line], pen: Union[Measure, float, Line]=0, n_0=0, c = 'tab:blue', label=None, **kargs):
    if isinstance(x, Measure):
        x = x._medida
    if isinstance(pen, Line):
        n_0 = pen.n_0
        pen = pen.slope
    if isinstance(x, Line):
        pen = x.slope
        n_0 = x.n_0
        x = x._medida
    plt.plot(x, ajuste_linea(x, pen, n_0), c=c, label=label, **kargs)

def curva(funcion, x, coeficientes, log_linspace = False, label = None, n=100, **kargs):
    # Coeficientes puede ser una medida o un iterable de medidas
    # En el primero cada coeficiente es el valor de cada medida.
    # En el segundo cada coeficiente es el primer valor de la medida
    # Si solo hay un coeficiente se toma como coeficiente singular
    if isinstance(coeficientes, Measure):
        coeficientes = coeficientes.value
        
    if hasattr(coeficientes, '__iter__'):
        if isinstance(coeficientes[0], Measure):
            coeficientes = [i.medida[0] for i in coeficientes]
    else:
        from inspect import signature
        if len(signature(funcion).parameters) == 2 or hasattr(coeficientes, '__iter__'):
            coeficientes = (coeficientes, )
            
    x = linspace(min(x), max(x), n) if not log_linspace else geomspace(min(x), max(x), n)
    y = [funcion(i, *coeficientes) for i in x]
    plot(x, y, label, **kargs)

def polar_plot(theta: list[float], r: list[float], label=None,  **kargs):
    if isinstance(theta, Measure):
        theta = theta._medida
    if isinstance(r, Measure):
        r = r._medida
    plt.polar(theta, r, label=label, **kargs)

def polar_scatter(theta, r, c: str = 'tab:red', relleno = True, marker: str = 'o', s: int = 5, label: str = None, zorder: int = 100, **kargs):
    facecolors = 'none' if not relleno else c
    polar_plot(theta, r, marker=marker, markerfacecolor= facecolors, markeredgecolor=c, linestyle='None', markersize=s, label=label, zorder=zorder, **kargs)
    
def polar_curva(funcion, theta, coeficientes, label=None, **kargs):
    if isinstance(coeficientes, Measure):
        coeficientes = coeficientes.medida
        
    if hasattr(coeficientes, '__iter__'):
        if isinstance(coeficientes[0], Measure):
            coeficientes = [i.medida[0] for i in coeficientes]
    else:
        from inspect import signature
        if len(signature(funcion).parameters) == 2 or hasattr(coeficientes, '__iter__'):
            coeficientes = (coeficientes, )
            
    theta = linspace(min(theta), max(theta))
    r = [funcion(i, *coeficientes) for i in theta]
    polar_plot(theta, r, label=label, **kargs)

def hollow_errorbar(x: list[float], y: list[float], yerr = None, xerr = None, dotcolor = 'tab:blue', puntos_rellenos = True, marker = 'o', s = 50, errorbarcolor = 'tab:red', barzorder = 0, dotzorder = 100, label=None):
    if isinstance(x, Measure):
        if xerr == None:
            xerr = x.error
        x = x.medida
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y.error
        y = y.medida
    plt.errorbar(x, y, yerr = yerr, xerr = xerr, ecolor = errorbarcolor, zorder = barzorder)
    facecolor = 'none' if not puntos_rellenos else dotcolor
    plt.scatter(x, y, s=s, marker = marker, c = facecolor, edgecolors = dotcolor, label=label, zorder = dotzorder)

def errorbar(x: list[float], y: list[float], yerr=None, xerr = None, errorbarcolor = 'tab:red', **kargs):
    if isinstance(x, Measure):
        if xerr == None:
            xerr = x.error
        x = x.medida
    if isinstance(y, Measure):
        if yerr == None:
            yerr = y.error
        y = y.medida
    plt.errorbar(x, y, yerr = yerr, xerr = xerr, ecolor = errorbarcolor, fmt = 'none', zorder = 0, **kargs)


def text(texto: str = '', x: float = 0, y: float = 0, fontsize = 10, **kargs):
    plt.text(x, y, texto, fontsize=fontsize, **kargs)

def anotar(texto: str = '', xy = (0,0), xytext =(0,0), fontsize = 10, arrowstyle='->', arco = 0,**kargs):
    arrowprops = dict(arrowstyle=arrowstyle, connectionstyle=f"arc3, rad ={arco}")
    if isinstance(xy[0], (list, tuple)):
        for point in xy[1:]:   
            plt.annotate(texto, xy=point, xytext=xytext, fontsize=fontsize, arrowprops = arrowprops, color=(0, 0, 0, 0),**kargs)
        xy = xy[0]
    plt.annotate(texto, xy=xy, xytext=xytext, fontsize=fontsize, arrowprops = arrowprops,**kargs)

def flecha(xy0 = (0,0), xy1=(0,0), arco=0):
    arrowprops = dict(arrowstyle='->', connectionstyle=f"arc3, rad ={arco}")
    plt.annotate('', xy1, xy0, arrowprops=arrowprops)

def limits(bottom=None, top=None, left=None, right=None):
    plt.ylim(bottom, top)
    plt.xlim(left, right)

def doble_y(*args, **kargs):
    '''Añade un segundo eje y al plot.
    A partir de la llamada a esta funcion se añaden los valores al segundo eje'''
    plt.twinx(*args, **kargs)

def doble_x(*args, **kargs):
    '''Añade un segundo eje x al plot.
    A partir de la llamada a esta funcion se añaden los valores al segundo eje'''
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

def figura(id, **kargs):
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

def tamaño(left=.1, right = .9, bottom=.1, top=.9, **kargs):
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, **kargs)

def guardar(lugar: str = 'figura', formato='pdf', sobrescribir = True, dpi = 'figure', auto_size = True, auto_tick_format = True, xlogscale=False, **kargs):
    if not sobrescribir:
        if exists(f'{lugar}.{formato}'):
            i = 0
            while exists(f'{lugar}({i}).{formato}'):
                i += 1
            lugar = lugar + f'({i})'
    if xlogscale:
        if auto_tick_format: print("WARNING: auto_tick_format no es compatible con logscale. Se ha desactivado automaticamente")
    if auto_tick_format and not xlogscale: 
        try:
            tick_format()
        except AttributeError:
            print("WARNING: auto_tick_format no funciona en plots polares y se desactiva por defecto")
    if auto_size: tight_layout()
    if xlogscale: plt.xscale("log")
    if usar_notacion_cientifica: plt.ticklabel_format(style="sci", scilimits=rango_sin_notacion_cientifica)
    plt.savefig(f'{lugar}.{formato}', dpi=dpi, format = formato, **kargs)

def show(*args, auto_size = True, auto_tick_format = True, xlogscale = False):
    if xlogscale:
        if auto_tick_format: print("WARNING: auto_tick_format no es compatible con logscale. Se ha desactivado automaticamente")
    if auto_tick_format and not xlogscale: 
        try:
            tick_format()
        except AttributeError:
            print("WARNING: auto_tick_format no funciona en plots polares y se desactiva por defecto")
        
    if auto_size: tight_layout()
    if xlogscale: plt.xscale("log")
    if usar_notacion_cientifica: plt.ticklabel_format(style="sci", scilimits=rango_sin_notacion_cientifica)
    plt.show(*args)

def tick_format(locale = True, useMathText=True, style = '', scilimits = None, **kargs):
    plt.ticklabel_format(useLocale=locale, style=style, scilimits=scilimits, useMathText=useMathText, **kargs)

def set_notacion_cientifica(usar=usar_notacion_cientifica, rango=rango_sin_notacion_cientifica):
    global rango_sin_notacion_cientifica, usar_notacion_cientifica
    usar_notacion_cientifica = usar
    rango_sin_notacion_cientifica = rango
    
def use_latex(usar=True):
    plt.rc("text", usetex= usar)

def use_latex_packages(*packages):
     plt.rc('text.latex', preamble="\n".join((r"\usepackage{" + i + "}" for i in packages)))
    
def add_latex_code(code):
    plt.rc('text.latex', preamble="\n".join(code))