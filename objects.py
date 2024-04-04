from .aprox import aprox
from .statistic import mean, standard_deviation, standard_error
import numpy as np
from math import nan
from . import calculos

# Markers to index in values
VALUE = object()
ERROR = object()

def _get_error(value, error):
    """
    Transform the error passed to a value into an error that the value can handle
    The type must be np.ndarray[Number]. If a single value is passed to the function, it is
    taken as a constant error for the entire value
    """
    
    if hasattr(error, '__iter__'):
        if not len(value) == len(error):
            if len(error) != 1:
                raise ValueError(
                "There is not the same number of values as errors or it is not a constant error")
            error = (error * len(value))
    else:
                error = [error]*len(value)
    return np.array([abs(i) for i in error])
class Measure:
    """
    Basic object to store values. It can be given one or several values
    (in a list) and their respective errors
    """
    def __init__(self, value: list[float], error: list[float] = None, aproximate: bool = True):
        if not isinstance(value, Measure):
            error = 0 if error is None else error
            # If it is not an iterable, it is converted into one
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
        self.__print_style = self.Style.pm

    @classmethod
    def from_pairs(self, *args, aproximate=False):
        """
        Given a group of pairs of values with their errors, it returns the corresponding value
        """
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
        """
        Returns a tuple with the value(s) and its (their) error(s)
        """
        return list(self._value), list(self._error)

    def list_of_measures(self):
        """Returns a list with the values contained as individual values"""
        return [Measure(*i, aproximate=False).change_style(self.__print_style) for i in zip(self._value, self._error)]

    def copy(self):
        """Returns an independent copy of itself. All the pointers to the data are different"""
        # the list are to make the lists independent
        return Measure(list(self._value), list(self._error), aproximate=False).change_style(self.__print_style)

    def aprox(self, decimals = None):
        """Aproximate the values of the value"""
        # The list are to make the lists independent
        if decimals is None:
            self._value, self._error = aprox(self._value, self._error)
        else:
            self._value = np.array([calculos.round(i, decimals) for i in self._value])
            self._error = np.array([calculos.round(i, decimals) for i in self._error])
            
        return self

    def mean(self) -> float:
        """Calculate the mean of the values"""
        return float(mean(*self._value))

    def standard_deviation(self) -> float:
        """Calculates the standard deviation of the values of the value"""
        return float(standard_deviation(*self._value))

    def standard_error(self) -> float:
        """Calculates the standard error of the values of the value (standard deviation of the mean)"""
        return float(standard_error(*self._value))

    def estimation(self):
        """Calculates the mean of the values of the value and estimates the error by comparing 
        the standard error and the mean squared error and takes the larger of the two"""
        mean_squared_error = np.sqrt(np.sum(self._error**2))
        return Measure(self.mean(), list(np.max([self.standard_error(), mean_squared_error])), aproximate = False)

    def sqrt(self):
        v = np.array([np.sqrt(v) for v in self._value])
        e = 1/(2*v)*self._error
        return Measure(v, e, aproximate=False)

    def change_style(self, style):
        """Changes the current style for another"""
        if style in self.Style.__dict__.values():
            self.__print_style = style
            return self
        else:
            raise TypeError(f'El estilo {style} no es un estilo válido')

    class Style:
        """Class containing the different functions that represent the value class"""
        def list(self):
            """[values] ± [errors]"""
            if len(self._value) == 1:
                v = self._value[0]
                e = self._error[0]
            else:
                v = [str(i) for i in self._value]
                e = [str(i) for i in self._error]
            return f'{v} ± {e}'

        def pm(self):
            """value 1 ± error 1, value 2 ± error 2, ..."""
            l = []
            for v, e in zip(self._value, self._error):
                l.append(f'{v} ± {e}')
            return ', '.join(l)
        
        def a(self):
            return 'datos'

        def table(self):
            """Same as pm but only works with a value of length 1 for debug reasons"""
            if len(self._value) == 1:
                v = self._value[0]
                e = self._error[0]
                if e == 0:
                    return str(v)
                return f'{v} ± {e}'
            else:
                raise ValueError("The value must contain only one value to use the 'table' style")

        def latex_table(self):
            """Same as table but in math mode for latex"""
            if len(self._value) == 1:
                v = self._value[0]
                e = self._error[0]
                if e == 0:
                    return "$" + str(v)+ "$"
                return f'${v} ' +  r"\pm" + f' {e}$'
            else:
                raise ValueError("The value must contain only one value to use the 'table' style")
            
        def typst_table(self):
            """Same as table but in math mode for typst"""
            if len(self._value) == 1:
                v = self._value[0]
                e = self._error[0]
                if e == 0:
                    return "$" + str(v)+ "$"
                return f'${v} ' +  r"plus.minus" + f' {e}$'
            else:
                raise ValueError("The value must contain only one value to use the 'table' style")

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
        # If it is a scalar
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
        # If it is a scalar
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
        
        expected_index = index[0]
        value_o_error = index[1]
        if value_o_error is VALUE:
            return self._value[expected_index]
        elif value_o_error is ERROR:
            return self._error[expected_index]
        raise TypeError("The index value contains something that is not a value or an error")    
    
    def __setitem__(self, index, value):
        if hasattr(index, "__getitem__"):
            indx = index[0]
            value_or_error = index[1]
            value = Measure(value)
            if type(indx) == slice:
                if value_or_error is VALUE:
                    self._value[indx] = value._value
                elif value_or_error is ERROR:
                    self._error[indx] = value._value
                else: raise Exception("It has not been specified if it should update value or error")
                if len(self._value) != len(self._error):
                    raise TypeError("The new value does not fill all the previous data")
            else:
                if value_or_error is VALUE:
                    self._value[indx] = value._value[0]
                elif value_or_error is ERROR:
                    self._error[indx] = value._value[0]
                else: raise Exception("It has not been specified if it should update value or error")
                if len(self._value) != len(self._error):
                    raise TypeError("The new value does not fill all the previous data")
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
        return "Measure( " + str(self) + " )"
    
    def __iter__(self):
        return (float(i) for i in self.value)

class Line:
    """
    Object that represents a line, it contains two values, one for the slope and another for the
    ordinate in the origin. It can be deconstructed as a tuple (slope, n_0)
    """
    def __init__(self, slope=0, n_0=0, x=[]):
        self.slope = Measure(slope, aproximate = False)
        self.n_0 = Measure(n_0, aproximate = False)
        if not isinstance(x, Measure):
            self.x = Measure(x)
        else:
            self.x = x

    def aprox(self):
        self.slope.aprox()
        self.n_0.aprox()
        return self

    def copy(self):
        return Line(self.slope.copy(), self.n_0.copy())

    def intersection(self, other):
        """Point of intersection with another line"""
        if not isinstance(other, Line):
            other = Line(0, other)
        delta_s = self.slope - other.slope
        delta_n = other.n_0 - self.n_0
        if delta_s.value == 0:
            return nan
        x = delta_n/delta_s
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
        return f'Line( {self} )'

if __name__ == '__main__':
    # pass
    print()
    m = Measure([353.72, 1532.6, 632], [2.56, 1, 1])
    print(f'm -> {m}')
    m.cambia_estilo(Measure.Estilo.lista)
    print(m)
