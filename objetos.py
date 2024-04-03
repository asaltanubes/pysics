from .aprox import aprox
from .estadistica import media, desviacion_estandar, error_estandar
import numpy as np
from math import nan, ceil, floor
import mpmath
from . import calculos


# Markers para indexar en medidas
VALOR = object()
ERROR = object()


def _tratar_error(medida, error):
    '''
    Convierte un error pasado a una medida en un error que la medida puede manejar
    El tipo debe ser np.ndarray[Number]. Si se pasa un solo valor a la función se
    toma como un error constante para toda la medida
    '''
    
    if hasattr(error, '__iter__'):
        if not len(medida) == len(error):
            if len(error) != 1:
                raise ValueError(
                "No hay el mismo número de medidas que de errores o no es un error constante")
            error = (error * len(medida))
    else:
                error = [error]*len(medida)
    return np.array([abs(Number(i)) for i in error])
class Medida:
    """Objeto básico para guardar medidas. Se le puede dar una o varias medidas
    (en una lista) y sus respectivos errores"""
    def __init__(self, medida: list[float] or float, error: list[float] or float = None, aproximar: bool = True):
        if not isinstance(medida, Medida):
            error = 0 if error is None else error
            # Si no se pasa un iterable se convierte en uno
            if not hasattr(medida, '__iter__'):
                medida = [medida]
            
            self._medida = np.array([Number(i) for i in medida])
            self._error  = _tratar_error(medida, error)
        else:
            medida = medida.copy()
            self._medida = medida._medida
            if error is None:
                self._error = medida._error
            else:
                self._error = _tratar_error(medida._medida, error)
                
                
        if aproximar:
            self.aprox()
        self.__print_style = self.Estilo.pm

    @classmethod
    def from_pairs(self, *args, aproximar=False):
        '''
            Dado un grupo de parejas de valores con sus errores devuelve la medida correspondiente
        '''
        if not all([len(i) == 2 for i in args]):
            raise TypeError(f"Expected pairs of numbers but at least one of them isnt")
        return self([i[0] for i in args], [i[1] for i in args], aproximar=aproximar)

    @property
    def medida(self):
        return [float(i) for i in self._medida]
    
    @property
    def error(self):
        return [float(i) for i in self._error]

    def unpack(self) -> tuple[list[float], list[float]]:
        """Devuelve una tupla con la(s) medida(s) y su(s) error(es)"""
        return list(self._medida), list(self._error)

    def lista_de_medidas(self):
        """Devuelve una lista con los valores contenidos como medidas individuales"""
        return [Medida(*i, aproximar=False).cambia_estilo(self.__print_style) for i in zip(self._medida, self._error)]

    def copy(self):
        """Retorna una copia INDEPENDIENTE de si misma. Todos los punteros a los datos son distintos"""
        # los list son para hacer que las listas sean independientes
        return Medida(list(self._medida), list(self._error), aproximar=False).cambia_estilo(self.__print_style)

    def aprox(self, decimales = None):
        """Aproxima los valores de la medida"""
        if decimales is None:
            self._medida, self._error = aprox(self._medida, self._error)
        else:
            self._medida = np.array([calculos.round(i, decimales) for i in self._medida])
            self._error = np.array([calculos.round(i, decimales) for i in self._error])
            
        return self

    def media(self) -> float:
        """Calcula la media de los valores"""
        return float(media(*self._medida))

    def desviacion_estandar(self) -> float:
        """Calcula la desviación estandar de los valores de la medida"""
        return float(desviacion_estandar(*self._medida))

    def error_estandar(self) -> float:
        """Calcula el error estandar de los valores de la medida (desviación estandar de la media)"""
        return float(error_estandar(*self._medida))

    def estimacion(self):
        """Calcula la media de los valores de la medida y estima el error comparando el error cuadratico medio y el error estandar y devuelve el mayor"""
        error_cuadratico_medio = np.sqrt(np.sum(self._error**2))/len(self._error)
        return Medida(self.media(), np.max([self.error_estandar(), error_cuadratico_medio]), aproximar = False)
    
    def rad(self):
        '''Convierte a radianes desde grados'''
        m = [n.rad() for n in self._medida]
        e = [g.rad() for g in self._error]
        return Medida(m, e, aproximar=False)
    
    def grad(self):
        '''Convierte a grados desde radianes'''
        m = [n.grad() for n in self._medida]
        e = [g.grad() for g in self._error]
        return Medida(m, e, aproximar=False)

    def sqrt(self):
        m = np.array([m.sqrt() for m in self._medida])
        e = 1/(2*m)*self._error
        return Medida(m, e, aproximar=False)

    def cambia_estilo(self, estilo):
        """Cambia el estilo actual por otro"""
        if estilo in self.Estilo.__dict__.values():
            self.__print_style = estilo
            return self
        else:
            raise TypeError(f'El estilo {estilo} no es un estilo válido')

    class Estilo:
        """Clase conteninendo las diferentes funciones que representan la clase medida"""
        def lista(self):
            """[medidas] ± [errores]"""
            if len(self._medida) == 1:
                m = self._medida[0]
                e = self._error[0]
            else:
                m = [str(i) for i in self._medida]
                e = [str(i) for i in self._error]
            return f'{m} ± {e}'

        def pm(self):
            """medida 1 ± error 1, medida2 ± error 2, ..."""
            l = []
            for m, e in zip(self._medida, self._error):
                l.append(f'{m} ± {e}')
            return ', '.join(l)
        
        def a(self):
            return 'datos'

        def tabla(self):
            """Igual que pm pero solo funciona con una medida de longitud 1 por razones de debug"""
            if len(self._medida) == 1:
                m = self._medida[0]
                e = self._error[0]
                if e == 0:
                    return str(m)
                return f'{m} ± {e}'
            else:
                raise ValueError('La medida solo debe contener un valor para emplear el estilo "tabla"')

        def tabla_latex(self):
            """Igual que tabla pero en math mode"""
            if len(self._medida) == 1:
                m = self._medida[0]
                e = self._error[0]
                if e == 0:
                    return "$" + str(m)+ "$"
                return f'${m} ' +  r"\pm" + f' {e}$'
            else:
                raise ValueError('La medida solo debe contener un valor para emplear el estilo "tabla"')
            
        def tabla_typst(self):
            """Igual que tabla pero en math mode"""
            if len(self._medida) == 1:
                m = self._medida[0]
                e = self._error[0]
                if e == 0:
                    return "$" + str(m)+ "$"
                return f'${m} ' +  r"plus.minus" + f' {e}$'
            else:
                raise ValueError('La medida solo debe contener un valor para emplear el estilo "tabla"')

# -----------------------------------------------------------------------------
    def __abs__(self):
        return Medida(abs(self._medida), self._error)
    
    
    def __add__(self, other):
        if not isinstance(other, Medida):
            other = Medida(other)
        return Medida(self._medida + other._medida, np.sqrt(self._error**2 + other._error**2), aproximar = False)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not isinstance(other, Medida):
            other = Medida(other)
        return Medida(self._medida - other._medida, np.sqrt(self._error**2 + other._error**2), aproximar = False)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        # Si es un escalar
        if not isinstance(other, Medida):
            medida = self._medida * other
            error = self._error * abs(other)
        else:
            medida = self._medida*other._medida
            error = np.sqrt(np.array( (other._medida * self._error)**2 + (self._medida * other._error)**2 ))

        return Medida(medida, error, aproximar = False)

    def __rmul__(self, val):
        return Medida(val * self._medida, abs(val) * self._error, aproximar = False)

    def __truediv__(self, other):
        # Si es un escalar
        if not isinstance(other, Medida):
            medida = self._medida/other
            error = self._error/abs(other)
        else:
            medida = self._medida/other._medida
            error = np.sqrt(np.array( (1/other._medida * self._error)**2
                            + (self._medida/other._medida**2 * other._error)**2 ))
        return Medida(medida, error, aproximar = False)

    def __rtruediv__(self, other):
        return Medida(other/self._medida, abs(other/self._medida**2) * self._error, aproximar = False)

    def __pow__(self, other):
        medida = self._medida**other
        error = abs((other)*self._medida**(other-1))*self._error
        return Medida(medida, error, aproximar = False)

    def __and__(self, other):
        return Medida(self._medida + other._medida, self._error + other._error, aproximar = False)

    def __or__(self, other):
        return self & -other

    def __eq__(self, other):
        if not isinstance(other, Medida):
            raise TypeError(f"Unsuported operand type(s) for ==: Medida and {type(other)}")
        return self.media == other.medida and self.error == other.error
        
    def __len__(self):
        return len(self._medida)

    def __getitem__(self, index):
        if not hasattr(index, '__getitem__'):
            return Medida(self._medida[index], self._error[index], aproximar=False)
        
        indice_deseado = index[0]
        valor_o_error = index[1]
        if valor_o_error is VALOR:
            return self._medida[indice_deseado]
        elif valor_o_error is ERROR:
            return self._error[indice_deseado]
        raise TypeError("El valor del índice contiene algo que no es ni un valor ni un error")    
    
    def __setitem__(self, index, value):
        if hasattr(index, "__getitem__"):
            indice = index[0]
            valor_o_error = index[1]
            value = Medida(value)
            if type(indice) == slice:
                if valor_o_error is VALOR:
                    self._medida[indice] = value._medida
                elif valor_o_error is ERROR:
                    self._error[indice] = value._medida
                else: raise Exception("No se ha especificado si se debe actualizar medida o error")
                if len(self._medida) != len(self._error):
                    raise TypeError("El valor nuevo no llena todos los datos anteriores")
            else:
                if valor_o_error is VALOR:
                    self._medida[indice] = value._medida[0]
                elif valor_o_error is ERROR:
                    self._error[indice] = value._medida[0]
                else: raise Exception("No se ha especificado si se debe actualizar medida o error")
                if len(self._medida) != len(self._error):
                    raise TypeError("El valor nuevo no llena todos los datos anteriores")
        else:
            if type(index) == slice:
                if isinstance(value, Medida):
                    self._medida[index] = value._medida
                    self._error[index] = value._error
                if hasattr(value, "__getitem__"):
                    value = Medida(value[0], value[1])
                    self._medida[index] = value._medida
                    self._error[index] = value._error
            else:
                if isinstance(value, Medida):
                    self._medida[index] = value._medida[0]
                    self._error[index] = value._error[0]
                if hasattr(value, "__getitem__"):
                    value = Medida(value[0], value[1])
                    self._medida[index] = value._medida[0]
                    self._error[index] = value._error[0]
            
    def __neg__(self):
        return (-1)*self.copy()

    def __str__(self):
        return self.__print_style(self)

    def __repr__(self):
        return "Medida( " + str(self) + " )"
    
    def __iter__(self):
        return (float(i) for i in self.medida)


class Recta:
    '''Objeto que representa una recta, contiene dos medidas, una para la ordenada en el origen y otra para la
    pendiente de la recta. Pueden obtenerse desestructurandola al igual que una tupla (pendiente, n_0)'''
    def __init__(self, pendiente=0, n_0=0, x=[]):
        self.pendiente = Medida(pendiente, aproximar = False)
        self.n_0 = Medida(n_0, aproximar = False)
        if not isinstance(x, Medida):
            self.x = Medida(x)
        else:
            self.x = x

    def aprox(self):
        self.pendiente.aprox()
        self.n_0.aprox()
        return self

    def copy(self):
        return Recta(self.pendiente.copy(), self.n_0.copy())

    def corte(self, other):
        """Punto de corte con otra recta"""
        if not isinstance(other, Recta):
            other = Recta(0, other)
        delta_p = self.pendiente - other.pendiente
        delta_n = other.n_0 - self.n_0
        if delta_p == 0:
            return nan
        x = delta_n/delta_p
        y = self.pendiente * x + self.n_0
        return (x, y)

    def plot(self, c = 'tab:blue', label=None, **kargs):
        from .plot import line as plot_line
        plot_line(self, c=c, label=label, **kargs)
        return self

    def __iter__(self):
        return (i for i in (self.pendiente, self.n_0))

    def __str__(self):
        return f'y = ({self.pendiente}) x + ({self.n_0})'

    def __repr__(self):
        return f'Recta( {self} )'
    
class Number:
    def __init__(self, value):
        if isinstance(value, Number):
            self.value = value.value
        elif isinstance(value, (int, float)):
            value = str(value)
            self.value = mpmath.mpf(value)
        elif isinstance(value, str):
            self.value = mpmath.mpf(value)
        elif isinstance(value, mpmath.mpf):
            self.value = value
        elif type(value) == type(mpmath.mp.pi):
            self.value = mpmath.mpf(value)
        elif type(value).__module__ == np.__name__:
            value = float(value)
            self.value = mpmath.mpf(str(value))
        elif isinstance(value, mpmath.mpc):
            raise TypeError("Un número complejo salvaje ha aparecido, algo ha ido mal :/")
        else: raise TypeError(f"Value not suported : {type(value)}")
    
    def sqrt(self):
        return Number(self.value.sqrt())
    
    def exp(self):
        return Number(mpmath.mp.exp(self.value))
    
    def log10(self):
        return Number(mpmath.mp.log10(self.value))

    def log(self):
        return Number(mpmath.mp.ln(self.value))
    
    def sin(self):
        return Number(mpmath.mp.sin(self.value, prec=mpmath.mp.prec+2))

    def cos(self):
        return Number(mpmath.mp.cos(self.value, prec=mpmath.mp.prec+2))

    def tan(self):
        return Number(mpmath.mp.tan(self.value, prec=mpmath.mp.prec+2))
    
    def asin(self):
        return Number(mpmath.mp.asin(self.value, prec=mpmath.mp.prec+2))
    
    def acos(self):
        return Number(mpmath.mp.acos(self.value, prec=mpmath.mp.prec+2))
    
    def atan(self):
        return Number(mpmath.mp.atan(self.value, prec=mpmath.mp.prec+2))
    
    arcsin = asin
    arccos = acos
    arctan = atan
     
    def rad(self):
        return Number(mpmath.radians(self.value))
    
    def grad(self):
        return Number(mpmath.degrees(self.value))
    
    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __add__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(mpmath.fadd(self.value, other.value, prec=mpmath.mp.prec+2))
    __radd__ = __add__
    
    def __sub__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(mpmath.fsub(self.value, other.value, prec=mpmath.mp.prec+2))
    
    def __rsub__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(mpmath.fsub(other.value, self.value, prec=mpmath.mp.prec+2))
    
    def __mul__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(mpmath.fmul(self.value, other.value, prec=mpmath.mp.prec+2))
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(mpmath.fdiv(self.value, other.value, prec=mpmath.mp.prec+2))
    def __rtruediv__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(mpmath.fdiv(other.value, self.value, prec=mpmath.mp.prec+2))
    
    def __pow__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        if isinstance(other, (int, float)):
            other = Number(other)
        return Number(mpmath.power(self.value, other.value))
    def __rpow__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(mpmath.power(other.value, self.value))
    
    def __eq__(self, other):
        # if not isinstance(other, (Number, int, float)):
        #     raise TypeError(f"Unsuported operand type(s) for ==: Number and {type(other)}")
        if isinstance(other, (int, float)):
            other = Number(other)
        return self.value == other.value
        
    def __lt__(self, other):
        if isinstance(other, Number):
            other = other.value
        return self.value < other
    
    def __gt__(self, other):
        if isinstance(other, Number):
            other = other.value
        return self.value > other
    
    def __le__(self, other):
        if isinstance(other, Number):
            other = other.value
        return self.value <= other
    
    def __ge__(self, other):
        if isinstance(other, Number):
            other = other.value
        return self.value >= other
    
    def __ne__(self, other):
        if isinstance(other, Number):
            other = other.value
        return self.value != other
    
    def __neg__(self):
        return Number(mpmath.fneg(self.value))
    
    def __abs__(self):
        return Number(mpmath.fabs(self.value))
    
    def __round__(self, ndigits=0):
        return Number(round(self.value, ndigits=ndigits))
    
    def __ceil__(self):
        return Number(mpmath.ceil(self.value))
    
    def __floor__(self):
        return Number(mpmath.floor(self.value))
    
    def __str__(self):
        return mpmath.nstr(self.value, mpmath.mp.dps, min_fixed=-4, max_fixed=5)
    
    def __trunc__(self):
        return Number(floor(self.value))

    def __repr__(self):
        return f"Number({mpmath.nstr(self.value, mpmath.mp.dps, min_fixed=-4, max_fixed=5)})"


if __name__ == '__main__':
    # pass
    print()
    m = Medida([353.72, 1532.6, 632], [2.56, 1, 1])
    print(f'm -> {m}')
    m.cambia_estilo(Medida.Estilo.lista)
    print(m)
