from .approx import approx
from .statistic import mean, standard_deviation, standard_error
import numpy as np
from math import nan
from . import round
from typing import Self

type number = int | float
type listable = np.ndarray | list[int] | list[float] | Measure | Unit | number

# Markers to index in values
VALUE = object()
ERROR = object()

class UnitError(Exception):
    pass
class UnitBaseError(Exception):
    pass
class UnitlessConversionError(Exception):
    pass

class Unit:
    # kg m s A K mol cd
    def __init__(self, si: Self | list[int] | list[float] = [0]*7, scale: number = 1, value: number = 1, symbol: str =""):
        # If si is a Unit copy all of the non-specified values
        if type(si) == Unit:
            symbol = symbol if symbol != "" else si.symbol

            # since scale is defined with respect to si the scales have to be multiplied
            # Ex: keV = Unit(eV, 1000)
            # the keV scale is 1000 * electron charge
            scale = scale * si.scale
            value = value if value != 1 else si.value
            si = si.si

        if len(si)!=7: raise UnitError(f"The length of the vector must be 7 (one number for each unit of the si) got {len(si)} elements: {si}")

        self.si = np.array(si)
        self.value = value
        self.scale = scale
        self.symbol = symbol

    def convert(self, *basis: Self) -> Self:
        """
        Converts a unit to a diferent basis of units. For example, the units of electric field
        are V/m or N/C, in the first case the basis is V and m and in the second case is N and C.

        returns:  Self
            The new unit converted

        raises: UnitBaseError
            if the proposed basis cannot build the current unit
        """
        pow, fact = self.conversion_factor(*basis)
        value = self.value * fact
        res_unit: Self = np.prod([i**j for i, j in zip(basis, pow)]) # type: ignore
        return value*res_unit

    def conversion_factor(self, *basis: Self) -> tuple[list[float], float]:
        """
        Converts a unit to a diferent basis of units. For example, the units of electric field
        are V/m or N/C, in the first case the basis is V and m and in the second case is N and C.

        returns:   (exponents, scale)
            exponents: list conaining the exponents of units of the basis
            scale: scale factor such that multiplying the current unit it is converted to the desired units

        raises: UnitBaseError
            if the proposed basis cannot build the current unit
        """

        if (self.si == [0]*7).all():
            if len(basis) > 1:
                raise UnitlessConversionError("Multiple units were passed for a unitless conversion")
            else:
                assert(len(basis) == 1)
                if not np.isclose(self.si, basis[0].si).all():
                    raise UnitBaseError("The unit cannot be constructed by the proposed basis")
                return ([1],  self.scale/basis[0].scale)

        sol = np.linalg.lstsq(np.transpose([i.si for i in basis]), self.si, -1)[0]

        # Check the solution, lstsq minimices the least squares problem |Ax-B|^2 to find solutions to Ax=B.
        # However this doesn't mean that the solution found for x actually solves the ecuation if B isn't in the image of A.
        if not np.isclose(np.sum([i.si*s for i, s in zip(basis, sol)], axis=0), self.si).all():
            raise UnitBaseError("The unit cannot be constructed by the proposed basis")

        return (sol, np.prod(np.array([i.scale for i in basis]) ** (-sol))*self.scale) # type: ignore

    def __mul__(self, other):
        if not isinstance(other, Unit):
            other = Unit(value=other)

        si = self.si + other.si
        value = self.value * other.value
        scale = self.scale * other.scale

        symbol = self.symbol + " * " + other.symbol \
                    if self.symbol != "" and other.symbol != "" \
                    else self.symbol+other.symbol

        return Unit(si, scale, value, symbol)

    def __truediv__(self, other):
        return self*other**-1

    def __pow__(self, power):
        si = self.si*power
        scale = self.scale**power
        value = self.value**power

        elements = [(i.split("^")[0], str(float(i.split("^")[1])*power)) if len(i.split("^"))>1 else (i, str(power)) for i in self.symbol.split(" * ")
                    if i!=""]
        sym = " * ".join(["^".join(i) for i in elements])

        return Unit(si, scale, value, sym)

    def __rmul__(self, other):
        return self*other

    def __rtruediv__(self, other):
        return self**-1*other

    def __str__(self):
        if self.value != 1:
            return str(self.value) + " " + self.symbol
        return self.symbol

    def __repr__(self):
        return f"Unit(scale={self.scale}, value={self.value}, symbol={self.symbol}, si={self.si})"

def _get_error(value, error):
    """
    Transform the error passed to a value into an error that the value can handle
    The type must be np.ndarray[Number]. If a single value is passed to the function, it is
    taken as a constant error for the entire value
    """

    if hasattr(error, '__iter__'):
        if not len(value) == len(error):
            if len(error) != 0:
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
    def __init__(self, value: listable , error: listable | None = None, approximate: bool = True, units = None):
        if isinstance(value, Unit):
            units = Unit(value.si, scale=value.scale, value=1, symbol=value.symbol)
            value = np.array([value.value])


        if not isinstance(value, Measure):
            error = 0 if error is None else error
            # If it is not an iterable, it is converted into one
            if not hasattr(value, '__iter__'):
                value = [value] # type: ignore

            self._value: np.ndarray = np.array(value)
            self._error: np.ndarray  = _get_error(value, error)
        else:
            value = value.copy()
            self._value = value._value
            if error is None:
                self._error = value._error
            else:
                self._error = _get_error(value._value, error)
            units = value.units

        if units is None:
            units = Unit()
        elif type(units) != Unit:
            units = Unit(units)

        self.units = units

        if approximate:
            self.approx()
        self.__print_style = self.Style.pm

    @classmethod
    def from_pairs(cls, *args, approximate=False) -> Self:
        """
        Given a group of pairs of values with their errors, it returns the corresponding value
        """
        if not all([len(i) == 2 for i in args]):
            raise TypeError(f"Expected pairs of numbers but at least one of them isnt")
        return cls([i[0] for i in args], [i[1] for i in args], approximate=approximate)

    @property
    def value(self) -> list[float]:
        return [float(i) for i in self._value]

    @property
    def error(self) -> list[float]:
        return [float(i) for i in self._error]

    def unpack(self) -> tuple[list[float], list[float]]:
        """
        Returns a tuple with the value(s) and its (their) error(s)
        """
        return list(self._value), list(self._error)

    def list_of_measures(self) -> list["Measure"]:
        """Returns a list with the values contained as individual values"""
        return [Measure(*i, approximate=False, units=self.units).change_style(self.__print_style) for i in zip(self._value, self._error)]

    def copy(self) -> "Measure":
        """Returns an independent copy of itself. All the pointers to the data are different"""
        # the list are to make the lists independent
        return Measure(list(self._value), list(self._error), approximate=False, units=self.units).change_style(self.__print_style)

    def approx(self, decimals = None) -> Self:
        """approximate the values of the value"""
        # The list are to make the lists independent
        if decimals is None:
            self._value, self._error = approx(self._value, self._error)
        else:
            self._value = np.array([round.round(i, decimals) for i in self._value])
            self._error = np.array([round.round(i, decimals) for i in self._error])

        return self

    def convert(self, *base) -> Self:
        pow, scale = self.units.conversion_factor(*base)
        units = np.prod([i**j for i, j in zip(base, pow)])
        conv = self*scale
        conv.units = units
        return conv

    def si(self) -> Self:
        si = self * self.units.scale
        si.units.scale = 1
        si.units.symbol = " * ".join([f"{i}^{j}" if j!=1 else i for i, j in zip(["kg", "m", "s", "A", "K", "mol", "cd"], self.units.si) if j!=0])
        return si

    def mean(self) -> float:
        """Calculate the mean of the values"""
        return float(mean(*self._value))

    def standard_deviation(self) -> float:
        """Calculates the standard deviation of the values of the value"""
        return float(standard_deviation(*self._value))

    def standard_error(self) -> float:
        """Calculates the standard error of the values of the value (standard deviation of the mean)"""
        return float(standard_error(*self._value))

    def estimation(self) -> Self:
        """Calculates the mean of the values of the value and estimates the error by comparing
        the standard error and the mean error and takes the larger of the two"""
        mean_error = np.sqrt(np.sum(self._error**2))/len(self._error)
        return Measure(self.mean(), list(np.max([self.standard_error(), mean_error])), approximate = False)

    def change_style(self, style) -> Self:
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
            return f'{v} ± {e} {self.units.symbol}'

        def pm(self):
            """value 1 ± error 1, value 2 ± error 2, ..."""
            l = []
            for v, e in zip(self._value, self._error):
                l.append(f'{v} ± {e}')
            return ', '.join(l) + f" {self.units.symbol}"

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
        return Measure(abs(self._value), self._error, approximate=False, units=self.units)


    def __add__(self, other):
        if not isinstance(other, Measure):
            other = Measure(other, units=self.units.si)

        if (self.units.si != other.units.si).any():
            raise UnitError(f"Units are different. left: {self.units.si}, right: {other.units.si}")

        finalunits = self.units if self.units.scale>other.units.scale else other.units
        self = self.convert(finalunits)
        other = other.convert(finalunits)

        return Measure(self._value + other._value, np.sqrt(self._error**2 + other._error**2), approximate = False, units=finalunits)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not isinstance(other, Measure):
            other = Measure(other, units=self.units)

        if (self.units.si != other.units.si).any():
            raise UnitError(f"Units are different. left: {self.units.si}, right: {other.units.si}")

        finalunits = self.units if self.units.scale>other.units.scale else other.units
        self = self.convert(finalunits)
        other = other.convert(finalunits)

        return Measure(self._value - other._value, np.sqrt(self._error**2 + other._error**2), approximate = False, units = finalunits)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        # If it is a scalar
        other = Measure(other)
        value = self._value*other._value
        error = np.sqrt(np.array( (other._value * self._error)**2 + (self._value * other._error)**2 ))
        units = self.units*other.units

        return Measure(value, error, approximate = False, units=units)

    def __rmul__(self, val):
        return Measure(val * self._value, abs(val) * self._error, approximate = False)

    def __truediv__(self, other):
        return self*other**-1

    def __rtruediv__(self, other):
        return other*self**-1

    def __pow__(self, other):
        value = self._value**other
        error = abs((other)*self._value**(other-1))*self._error
        units = self.units**other
        return Measure(value, error, approximate = False, units=units)

    def __and__(self, other):
        return Measure(self._value + other._value, self._error + other._error, approximate = False, units=self.units)

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
            return Measure(self._value[index], self._error[index], approximate=False)

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
        self.slope = Measure(slope, approximate = False)
        self.n_0 = Measure(n_0, approximate = False)
        if not isinstance(x, Measure):
            self.x = Measure(x)
        else:
            self.x = x

    def approx(self):
        self.slope.approx()
        self.n_0.approx()
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
    m.change_style(Measure.Style.list)
    print(m)
