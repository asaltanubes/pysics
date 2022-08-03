from matplotlib import pyplot as plt
from os.path import exists
from .ajuste import line as ajuste_linea
from .objetos import Medida, Recta
from .type_alias import elementos

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
    plt.plot(x, y, label = label, **kargs)


def hollow_errorbar(x: elementos, y: elementos, yerr = None, xerr = None, dotcolor = 'tab:red', marker = 'o', s = 50, errorbarcolor = 'tab:red', barzorder = 0, dotzorder = 100, label=None):
    if isinstance(x, Medida):
        if xerr == None:
            xerr = x._error
        x = x._medida
    if isinstance(y, Medida):
        if yerr == None:
            yerr = y._error
        y = y._medida
    plt.errorbar(x, y, yerr = yerr, xerr = xerr, ecolor = errorbarcolor, fmt = 'none', label=label, zorder = barzorder)
    plt.scatter(x, y, s=s, marker = marker, c = 'none', edgecolors = dotcolor, label=label, zorder = dotzorder)


def errorbar(x: elementos, y: elementos, yerr, xerr = None, dotcolor = 'tab:blue', errorbarcolor = 'tab:red', **kargs):
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(y, Medida):
        y = y._medida
    plt.errorbar(x, y, yerr = yerr, xerr = xerr, ecolor = errorbarcolor, fmt = 'o', color = dotcolor, zorder = 0, **kargs)


def line(x: elementos, pen: Medida or float or Recta, n_0=0, c = 'tab:blue', label=None, **kargs):
    if isinstance(x, Medida):
        x = x._medida
    if isinstance(pen, Recta):
        n_0 = pen.n_0
        pen = pen.pendiente
    plt.plot(x, ajuste_linea(x, pen, n_0), c=c, label=label, **kargs)


def text(texto: str = '', x: float = 0, y: float = 0, fontsize = 10, **kargs):
    plt.text(x, y, texto, fontsize=fontsize, **kargs)

def anotar(texto: str = '', xy: tuple[float, float] = (0,0), xytext: tuple[float, float]=(0,0), fontsize = 10, arrowprops = {'arrowstyle': '->'},**kargs):
    plt.annotate(texto, xy=xy, xytext=xytext, fontsize=fontsize, arrowprops = arrowprops,**kargs)


def xlabel(text, fontsize = 12, **kargs):
    plt.xlabel(text, fontsize = fontsize, **kargs)

def ylabel(text, fontsize = 12, **kargs):
    plt.ylabel(text, fontsize = fontsize, **kargs)

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

def guardar(lugar: str = 'figura', formato='pdf', sobrescribir = True, dpi = 'figure', auto_size = True, **kargs):
    if not sobrescribir:
        if exists(f'{lugar}.{formato}'):
            i = 0
            while exists(f'{lugar}({i}).{formato}'):
                i += 1
            lugar = lugar + f'({i})'
    
    if auto_size: tamaño()
    plt.savefig(f'{lugar}.{formato}', dpi=dpi, format = formato, **kargs)

def show(auto_size = True):
    if auto_size: tamaño()
    plt.show()
