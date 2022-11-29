from pysics.aprox import aprox
from pysics.estadistica import media, desviacion_estandar, error_estandar
import numpy as np
from math import nan
import decimal

class Medida:
    """Objeto básico para guardar medidas. Se le puede dar una o varias medidas
    (en una lista) y sus respectivos errores"""
    def __init__(self, medida: list[float] or float, error: list[float] or float = 0, aproximar: bool = True):
        if not isinstance(medida, Medida):
            if not isinstance(medida, np.ndarray):
                if not hasattr(medida, '__iter__'):
                    medida = [medida]
                else:
                    medida = medida
            if not isinstance(error, np.ndarray):
                if not hasattr(error, '__iter__'):
                    error = [error]*len(medida)
                else:
                    if not len(medida) == len(error):
                        if len(error) > 1 or error == []:
                            raise ValueError(
                            "No hay el mismo número de medidas que de errores o no es el mismo error para todas las medidas")
                        error = np.array(error * len(medida))
            self._medida = np.array([Number(i) for i in medida])
            self._error  = np.array([Number(i) for i in error])
        else:
            medida = medida.copy()
            self._medida = medida._medida
            self._error = medida._error
        if aproximar:
            self.aprox()
        self.__print_style = self.Estilo.pm

    @classmethod
    def from_pairs(*args, aproximar=False):
        if not all([len(i) == 2 for i in args]):
            raise TypeError(f"Expected pairs of numbers but at least one of them isnt")
        return Medida([i[0] for i in args], [i[1] for i in args], aproximar=aproximar)

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
        return [Medida(*i, aproximar=False) for i in zip(self._medida, self._error)]

    def copy(self):
        """Retorna una copia INDEPENDIENTE de si misma"""
        # los list son para hacer que las listas sean independientes
        return Medida(list(self._medida), list(self._error), aproximar=False).cambia_estilo(self.__print_style)

    def aprox(self):
        """Aproxima los valores de la medida"""
        self._medida, self._error = aprox(self._medida, self._error)
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
        """Calcula la media de los valores de la medida y el error de esta sumando en cuadratura el error estandar y el error"""
        return Medida([self.media()]*len(self._error), list(np.sqrt( self.error_estandar()**2 + self._error**2 )), aproximar = False)

    def iter_medida(self):
        return (Medida(i, j, aproximar=False) for i,j in zip(self._medida, self._error))

    def cambia_estilo(self, estilo):
        if estilo in self.Estilo.__dict__.values():
            self.__print_style = estilo
            return self
        else:
            raise TypeError(f'El estilo {estilo} no es un estilo válido')

    class Estilo:
        """Clase conteninendo las diferentes funciones que representan la clase medida"""
        def lista(self):
            """[medidas] ± [errores]"""
            if len(self.medida) == 1:
                m = self.medida[0]
                e = self.error[0]
            else:
                m = [str(i) for i in self.medida]
                e = [str(i) for i in self.error]
            return f'{m} ± {e}'

        def pm(self):
            """medida 1 ± error 1, medida2 ± error 2, ..."""
            l = []
            for m, e in zip(self.medida, self.error):
                l.append(f'{m} ± {e}')
            return ', '.join(l)
        
        def a(self):
            return 'datos'

        def tabla(self):
            """Igual que pm pero solo funciona con una medida de longitud 1 por razones de debug"""
            if len(self.medida) == 1:
                m = self.medida[0]
                e = self.error[0]
                if e == 0:
                    return str(m)
                return f'{m} ± {e}'
            else:
                raise ValueError('La medida solo debe contener un valor para emplear el estilo "tabla"')

# -----------------------------------------------------------------------------

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
        return Medida(self._medida[index], self._error[index], aproximar=False)

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
            self.value = decimal.Decimal(value)
        elif isinstance(value, str):
            self.value = decimal.Decimal(value)
        elif isinstance(value, decimal.Decimal):
            self.value = value
        elif type(value).__module__ == np.__name__:
            value = float(value)
            self.value = decimal.Decimal(str(value))
        else: raise TypeError(f"Value not suported :{type(value)}")
    
    def sqrt(self):
        return Number(self.value.sqrt())
    
    def exp(self):
        return Number(self.value.exp())
    
    def log10(self):
        return Number(self.value.log10())

    def log(self):
        return Number(self.value.ln())
    
    def sin(self):
        decimal.getcontext().prec += 2
        i, lasts, s, fact, num, sign = 1, 0, self.value, 1, self.value, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i-1)
            num *= self.value * self.value
            sign *= -1
            s += num / fact * sign
        decimal.getcontext().prec -= 2
        return Number(+s)

    def cos(self):
        decimal.getcontext().prec += 2
        i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i-1)
            num *= self.value * self.value
            sign *= -1
            s += num / fact * sign
        decimal.getcontext().prec -= 2
        return Number(+s)

    def tan(self):
        return self.sin()/self.cos()
    
    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __add__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(self.value + other.value)
    __radd__ = __add__
    
    def __sub__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(self.value - other.value)
    def __rsub__(self, other): 
        if not isinstance(other, Number):
            other = Number(other)
        return Number(other.value - self.value)
    
    def __mul__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(self.value * other.value)
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(self.value / other.value)
    def __rtruediv__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(other.value / self.value)
    
    def __pow__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        if isinstance(other, (int, float)):
            other = Number(other)
        return Number(self.value**other.value)
    def __rpow__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return Number(other.value ** self.value)
    
    def __eq__(self, other):
        if not isinstance(other, (Number, int, float)):
            raise TypeError(f"Unsuported operand type(s) for ==: Number and {type(other)}")
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
        return (-1)*self
    
    def __abs__(self):
        return Number(self.value.copy_abs())
    
    def __round__(self, ndigits=0):
        return Number(round(self.value, ndigits))
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


if __name__ == '__main__':
    # pass
    print()
    m = Medida([353.72, 1532.6, 632], [2.56, 1, 1])
    print(f'm -> {m}')
    m.cambia_estilo(Medida.Estilo.lista)
    print(m)
