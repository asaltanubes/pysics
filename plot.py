from matplotlib import pyplot as plt
from os.path import exists
from .ajuste import line as ajuste_linea
from .objetos import Medida, Recta
from .type_alias import elementos
from numpy import linspace
import locale
locale.setlocale(locale.LC_ALL, '')
usar_notacion_cientifica = True
rango_sin_notacion_cientifica = (-2, 2)

def scatter(x: elementos, y: elementos, c: str = 'tab:red', marker: str = 'o', s: int = 50, label: str = None, zorder: int = 100, **kargs):
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    plt.scatter(x, y, s=s, marker = marker, facecolors = 'none', edgecolors = c, label=label, zorder = zorder, **kargs)


def plot(x: elementos, y: elementos, label=None, **kargs):
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    if isinstance(y, Recta):
        y = ajuste_linea(x, y)
    plt.plot(x, y, label = label, **kargs)

def line(x: elementos, pen: Medida or float or Recta=0, n_0=0, c = 'tab:blue', label=None, **kargs):
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(pen, Recta):
        n_0 = pen.n_0
        pen = pen.pendiente
    if isinstance(x, Recta):
        pen = x.pendiente
        n_0 = x.n_0
        x = x.x._medida
    plt.plot(x, ajuste_linea(x, pen, n_0), c=c, label=label, **kargs)

def curva(funcion, x, coeficientes, label = None, **kargs):
    if isinstance(coeficientes, Medida):
        coeficientes = coeficientes.medida
    if hasattr(coeficientes, '__iter__'):
        if isinstance(coeficientes[0], Medida):
            coeficientes = [i.medida[0] for i in coeficientes]
    else:
        from inspect import signature
        if len(signature(funcion).parameters) == 2:
            coeficientes = (coeficientes, )
    x = linspace(min(x), max(x))
    y = [funcion(i, *coeficientes) for i in x]
    plot(x, y, label, **kargs)

def hollow_errorbar(x: elementos, y: elementos, yerr = None, xerr = None, dotcolor = 'tab:blue', marker = 'o', s = 50, errorbarcolor = 'tab:red', barzorder = 0, dotzorder = 100, label=None):
    if isinstance(x, Medida):
        if xerr == None:
            xerr = x.error
        x = x.medida
    if isinstance(y, Medida):
        if yerr == None:
            yerr = y.error
        y = y.medida
    plt.errorbar(x, y, yerr = yerr, xerr = xerr, ecolor = errorbarcolor, fmt = 'none', zorder = barzorder)
    plt.scatter(x, y, s=s, marker = marker, c = 'none', edgecolors = dotcolor, label=label, zorder = dotzorder)

def errorbar(x: elementos, y: elementos, yerr=None, xerr = None, errorbarcolor = 'tab:red', **kargs):
    if isinstance(x, Medida):
        if xerr == None:
            xerr = x.error
        x = x.medida
    if isinstance(y, Medida):
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

def xlabel(text, fontsize = 12, **kargs):
    plt.xlabel(text, fontsize = fontsize, **kargs)

def ylabel(text, fontsize = 12, **kargs):
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

def guardar(lugar: str = 'figura', formato='pdf', sobrescribir = True, dpi = 'figure', auto_size = True, auto_tick_format = True, **kargs):
    if not sobrescribir:
        if exists(f'{lugar}.{formato}'):
            i = 0
            while exists(f'{lugar}({i}).{formato}'):
                i += 1
            lugar = lugar + f'({i})'
    if auto_tick_format: tick_format()
    if auto_size: tight_layout()
    notacion_cientifica(usar_notacion_cientifica, rango_sin_notacion_cientifica)
    plt.savefig(f'{lugar}.{formato}', dpi=dpi, format = formato, **kargs)

def show(auto_size = True, auto_tick_format = True):
    if auto_tick_format: tick_format()
    if auto_size: tight_layout()
    notacion_cientifica(usar_notacion_cientifica, rango_sin_notacion_cientifica)
    plt.show()

def tick_format(locale = True, useMathText=True, style = '', scilimits = None, **kargs):
    plt.ticklabel_format(useLocale=locale, style=style, scilimits=scilimits, useMathText=useMathText, **kargs)

def set_notacion_cientifica(usar=usar_notacion_cientifica, rango=rango_sin_notacion_cientifica):
    usar_notacion_cientifica = usar
    rango_sin_notacion_cientifica = rango

def notacion_cientifica(usar=True, rango = (0, 0)):
    style = 'sci' if usar else 'plain'
    plt.ticklabel_format(style=style, scilimits=rango)
    
def use_latex(usar=True):
    if usar: plt.rcParams.update({"text.usetex": usar})