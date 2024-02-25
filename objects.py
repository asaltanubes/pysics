from .aprox import aprox
from .estadistica import mean, standard_deviation, standard_error
import numpy as np
from math import nan
from . import calculos

# Markers para indexar en values
VALUE = object()
ERROR = object()

def _get_error(value, error):
    '''
    Convierte un error pasado a una value en un error que la value puede manejar
    El tipo debe ser np.ndarray[Number]. Si se pasa un solo valor a la función se
    toma como un error constante para toda la value
    '''
    
    if hasattr(error, '__iter__'):
        if not len(value) == len(error):
            if len(error) != 1:
                raise ValueError(
                "No hay el mismo número de values que de errores o no es un error constante")
            error = (error * len(value))
    else:
                error = [error]*len(value)
    return np.array([abs(i) for i in error])
class Measure:
    """Objeto básico para guardar values. Se le puede dar una o varias values
    (en una lista) y sus respectivos errores"""
    def __init__(self, value: list[float], error: list[float] = None, aproximate: bool = True):
        if not isinstance(value, Measure):
            error = 0 if error is None else error
            # Si no se pasa un iterable se convierte en uno
            if not hasattr(value, '__iter__'):
                value = [value]
            
            self._value = np.array([i for i in value])
            self._error  = _get_error(value, error)
        else:
            value = value.copy()
            self._value = value._value
            if error is None:
                self._error = value._error
            else:
                self._error = _get_error(value._value, error)
                
        if aproximate:
            self.aprox()
        self.__print_style = self.Estilo.pm

    @classmethod
    def from_pairs(self, *args, aproximate=False):
        '''
            Dado un grupo de parejas de valores con sus errores devuelve la value correspondiente
        '''
        if not all([len(i) == 2 for i in args]):
            raise TypeError(f"Expected pairs of numbers but at least one of them isnt")
        return self([i[0] for i in args], [i[1] for i in args], aproximate=aproximate)

    @property
    def value(self):
        return [float(i) for i in self._value]
    
    @property
    def error(self):
        return [float(i) for i in self._error]

    def unpack(self) -> tuple[list[float], list[float]]:
        """Devuelve una tupla con la(s) value(s) y su(s) error(es)"""
        return list(self._value), list(self._error)

    def list_of_values(self):
        """Devuelve una lista con los valores contenidos como values individuales"""
        return [Measure(*i, aproximate=False).cambia_estilo(self.__print_style) for i in zip(self._value, self._error)]

    def copy(self):
        """Retorna una copia INDEslope de si misma. Todos los punteros a los datos son distintos"""
        # los list son para hacer que las listas sean indeslopes
        return Measure(list(self._value), list(self._error), aproximate=False).cambia_estilo(self.__print_style)

    def aprox(self, decimales = None):
        """Aproxima los valores de la value"""
        if decimales is None:
            self._value, self._error = aprox(self._value, self._error)
        else:
            self._value = np.array([calculos.round(i, decimales) for i in self._value])
            self._error = np.array([calculos.round(i, decimales) for i in self._error])
            
        return self

    def mean(self) -> float:
        """Calcula la media de los valores"""
        return float(mean(*self._value))

    def standard_deviation(self) -> float:
        """Calcula la desviación estandar de los valores de la value"""
        return float(standard_deviation(*self._value))

    def standard_error(self) -> float:
        """Calcula el error estandar de los valores de la value (desviación estandar de la media)"""
        return float(standard_error(*self._value))

    def estimation(self):
        """Calcula la media de los valores de la value y el error de esta sumando en cuadratura el error estandar y el error"""
        return Measure([self.media()]*len(self._error), list(np.sqrt( self.error_estandar()**2 + self._error**2 )), aproximate = False)

    def sqrt(self):
        m = np.array([m.sqrt() for m in self._value])
        e = 1/(2*m)*self._error
        return Measure(m, e, aproximate=False)

    def cambia_style(self, estilo):
        """Cambia el estilo actual por otro"""
        if estilo in self.Estilo.__dict__.values():
            self.__print_style = estilo
            return self
        else:
            raise TypeError(f'El estilo {estilo} no es un estilo válido')

    class Style:
        """Clase conteninendo las diferentes funciones que representan la clase value"""
        def list(self):
            """[values] ± [errores]"""
            if len(self._value) == 1:
                m = self._value[0]
                e = self._error[0]
            else:
                m = [str(i) for i in self._value]
                e = [str(i) for i in self._error]
            return f'{m} ± {e}'

        def pm(self):
            """value 1 ± error 1, value2 ± error 2, ..."""
            l = []
            for m, e in zip(self._value, self._error):
                l.append(f'{m} ± {e}')
            return ', '.join(l)
        
        def a(self):
            return 'datos'

        def table(self):
            """Igual que pm pero solo funciona con una value de longitud 1 por razones de debug"""
            if len(self._value) == 1:
                m = self._value[0]
                e = self._error[0]
                if e == 0:
                    return str(m)
                return f'{m} ± {e}'
            else:
                raise ValueError('La value solo debe contener un valor para emplear el estilo "tabla"')

        def latex_table(self):
            """Igual que tabla pero en math mode"""
            if len(self._value) == 1:
                m = self._value[0]
                e = self._error[0]
                if e == 0:
                    return "$" + str(m)+ "$"
                return f'${m} ' +  r"\pm" + f' {e}$'
            else:
                raise ValueError('La value solo debe contener un valor para emplear el estilo "tabla"')
            
        def typst_table(self):
            """Igual que tabla pero en math mode"""
            if len(self._value) == 1:
                m = self._value[0]
                e = self._error[0]
                if e == 0:
                    return "$" + str(m)+ "$"
                return f'${m} ' +  r"plus.minus" + f' {e}$'
            else:
                raise ValueError('La value solo debe contener un valor para emplear el estilo "tabla"')

# -----------------------------------------------------------------------------
    def __abs__(self):
        return Measure(abs(self._value), self._error)
    
    
    def __add__(self, other):
        if not isinstance(other, Measure):
            other = Measure(other)
        return Measure(self._value + other._value, np.sqrt(self._error**2 + other._error**2), aproximate = False)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not isinstance(other, Measure):
            other = Measure(other)
        return Measure(self._value - other._value, np.sqrt(self._error**2 + other._error**2), aproximate = False)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        # Si es un escalar
        if not isinstance(other, Measure):
            value = self._value * other
            error = self._error * abs(other)
        else:
            value = self._value*other._value
            error = np.sqrt(np.array( (other._value * self._error)**2 + (self._value * other._error)**2 ))

        return Measure(value, error, aproximate = False)

    def __rmul__(self, val):
        return Measure(val * self._value, abs(val) * self._error, aproximate = False)

    def __truediv__(self, other):
        # Si es un escalar
        if not isinstance(other, Measure):
            value = self._value/other
            error = self._error/abs(other)
        else:
            value = self._value/other._value
            error = np.sqrt(np.array( (1/other._value * self._error)**2
                            + (self._value/other._value**2 * other._error)**2 ))
        return Measure(value, error, aproximate = False)

    def __rtruediv__(self, other):
        return Measure(other/self._value, abs(other/self._value**2) * self._error, aproximate = False)

    def __pow__(self, other):
        value = self._value**other
        error = abs((other)*self._value**(other-1))*self._error
        return Measure(value, error, aproximate = False)

    def __and__(self, other):
        return Measure(self._value + other._value, self._error + other._error, aproximate = False)

    def __or__(self, other):
        return self & -other

    def __eq__(self, other):
        if not isinstance(other, Measure):
            raise TypeError(f"Unsuported operand type(s) for ==: Measure and {type(other)}")
        return self.media == other.value and self.error == other.error
        
    def __len__(self):
        return len(self._value)

    def __getitem__(self, index):
        if not hasattr(index, '__getitem__'):
            return Measure(self._value[index], self._error[index], aproximate=False)
        
        indice_deseado = index[0]
        valor_o_error = index[1]
        if valor_o_error is VALUE:
            return self._value[indice_deseado]
        elif valor_o_error is ERROR:
            return self._error[indice_deseado]
        raise TypeError("El valor del índice contiene algo que no es ni un valor ni un error")    
    
    def __setitem__(self, index, value):
        if hasattr(index, "__getitem__"):
            indice = index[0]
            valor_o_error = index[1]
            value = Measure(value)
            if type(indice) == slice:
                if valor_o_error is VALUE:
                    self._value[indice] = value._value
                elif valor_o_error is ERROR:
                    self._error[indice] = value._value
                else: raise Exception("No se ha especificado si se debe actualizar value o error")
                if len(self._value) != len(self._error):
                    raise TypeError("El valor nuevo no llena todos los datos anteriores")
            else:
                if valor_o_error is VALUE:
                    self._value[indice] = value._value[0]
                elif valor_o_error is ERROR:
                    self._error[indice] = value._value[0]
                else: raise Exception("No se ha especificado si se debe actualizar value o error")
                if len(self._value) != len(self._error):
                    raise TypeError("El valor nuevo no llena todos los datos anteriores")
        else:
            if type(index) == slice:
                if isinstance(value, Measure):
                    self._value[index] = value._value
                    self._error[index] = value._error
                if hasattr(value, "__getitem__"):
                    value = Measure(value[0], value[1])
                    self._value[index] = value._value
                    self._error[index] = value._error
            else:
                if isinstance(value, Measure):
                    self._value[index] = value._value[0]
                    self._error[index] = value._error[0]
                if hasattr(value, "__getitem__"):
                    value = Measure(value[0], value[1])
                    self._value[index] = value._value[0]
                    self._error[index] = value._error[0]
            
    def __neg__(self):
        return (-1)*self.copy()

    def __str__(self):
        return self.__print_style(self)

    def __repr__(self):
        return "Measure( " + repr(self) + " )"
    
    def __iter__(self):
        return (float(i) for i in self.value)

class Line:
    '''Objeto que representa una recta, contiene dos values, una para la ordenada en el origen y otra para la
    slope de la recta. Pueden obtenerse desestructurandola al igual que una tupla (slope, n_0)'''
    def __init__(self, slope=0, n_0=0, x=[]):
        self.slope = Measure(slope, aproximate = False)
        self.n_0 = Measure(n_0, aproximate = False)
        self.x = Measure(x)

    def aprox(self):
        self.slope.aprox()
        self.n_0.aprox()
        return self

    def copy(self):
        return Line(self.slope.copy(), self.n_0.copy())

    def intersection(self, other):
        """Punto de corte con otra recta"""
        if not isinstance(other, Line):
            other = Line(0, other)
        delta_p = self.slope - other.slope
        delta_n = other.n_0 - self.n_0
        if delta_p == 0:
            return nan
        x = delta_n/delta_p
        y = self.slope * x + self.n_0
        return (x, y)

    def plot(self, c = 'tab:blue', label=None, **kargs):
        from .plot import line as plot_line
        plot_line(self, c=c, label=label, **kargs)
        return self

    def __iter__(self):
        return (i for i in (self.slope, self.n_0))

    def __str__(self):
        return f'y = ({self.slope}) x + ({self.n_0})'

    def __repr__(self):
        return f'Recta( {self} )'

if __name__ == '__main__':
    # pass
    print()
    m = Measure([353.72, 1532.6, 632], [2.56, 1, 1])
    print(f'm -> {m}')
    m.cambia_estilo(Measure.Estilo.lista)
    print(m)
