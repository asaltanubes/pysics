from zmq import has
from pysics.aprox import aprox
from pysics.estadistica import media, desviacion_estandar, error_estandar
import numpy as np
from math import nan

class Medida:
    """Objeto básico para guardar medidas. Se le puede dar una o varias medidas
    (en una lista) y sus respectivos errores"""
    def __init__(self, medida: list[float] or float, error: list[float] or float = 0, aproximar: bool = True):
        if not isinstance(medida, Medida):
            if not isinstance(medida, np.ndarray):
                if not hasattr(medida, '__iter__'):
                    medida = np.array([medida])
                else:
                    medida = np.array(medida)
            if not isinstance(error, np.ndarray):
                if not hasattr(error, '__iter__'):
                    error = np.array([error]*len(medida))
                else:
                    if len(medida) == len(error):
                        error = np.array(error)
                    else:
                        if len(error) > 1 or error == []:
                            raise ValueError(
                            "No hay el mismo número de medidas que de errores o no es el mismo error para todas las medidas")
                        error = np.array(error * len(medida))
            self._medida: np.ndarray[float] = medida
            self._error: np.ndarray[float] = error
        else:
            self._medida = medida._medida
            self._error = medida._error
        if aproximar:
            self.aprox()
        self.__print_style = self.Estilo.pm

    @property
    def medida(self):
        return list(self._medida)
    
    @property
    def error(self):
        return list(self.error)

    def unpack(self) -> tuple[list[float], list[float]]:
        """Devuelve una tupla con la(s) medida(s) y su(s) error(es)"""
        return list(self._medida), list(self._error)

    def lista_de_medidas(self):
        return [Medida(*i, aproximar=False) for i in zip(self._medida, self._error)]

    def copy(self):
        """Retorna una copia INDEPENDIENTE de si misma"""
        # los list son para hacer que las listas sean independientes
        return Medida(list(self._medida), list(self._error), aproximar=False)

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
        return Medida(self.media()* (1+0*self._error), list(np.sqrt( self.error_estandar()**2 + self._error**2 )), aproximar = False)

    def cambia_estilo(self, estilo):
        if estilo in self.Estilo.__dict__.values():
            self.__print_style = estilo
            return self
        else:
            raise TypeError(f'El estilo {estilo} no es un estilo válido')

    class Estilo:
        def lista(self):
            if len(self._medida) == 1:
                m = self._medida[0]
                e = self._error[0]
            else:
                m = self._medida
                e = self._error
            return f'{m} ± {e}'

        def pm(self):
            l = []
            for m, e in zip(self._medida, self._error):
                l.append(f'{m} ± {e}')
            return ', '.join(l)

        def tabla(self):
            if len(self._medida) == 1:
                m = self._medida[0]
                e = self._error[0]
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

    def __len__(self):
        return len(self._medida)

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError("Indice fuera de rango")
        return Medida(self._medida[index], self._error[index])

    def __neg__(self):
        return (-1)*self.copy()

    def __str__(self):
        return self.__print_style(self)


    def __repr__(self):
        return "Medida( " + str(self) + " )"


class Recta:
    def __init__(self, pendiente=0, n_0=0, x=[]):
        self.pendiente = Medida(pendiente, aproximar = False)
        self.n_0 = Medida(n_0, aproximar = False)
        self.x = Medida(x)

    def aprox(self):
        self.pendiente.aprox()
        self.n_0.aprox()
        return self

    def copy(self):
        return Recta(self.pendiente.copy(), self.n_0.copy())

    def corte(self, other):
        if not isinstance(other, Recta):
            other = Recta(0, other)
        delta_p = self.pendiente - other.pendiente
        delta_n = other.n_0 - self.n_0
        if delta_p == 0:
            return nan
        x = delta_n/delta_p
        y = self.pendiente * x + self.n_0
        return (x, y)

    def __iter__(self):
        return (i for i in (self.pendiente, self.n_0))

    def __str__(self):
        return f'y = ({self.pendiente}) x + ({self.n_0})'

    def __repr__(self):
        return f'Recta( {self} )'

if __name__ == '__main__':
    # pass
    print()
    m = Medida([353.72, 1532.6, 632], [2.56, 1, 1])
    print(f'm -> {m}')
    m.cambia_estilo(Medida.Estilo.lista)
    print(m)
