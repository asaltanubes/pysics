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
            self.medida: np.ndarray[float] = medida
            self.error: np.ndarray[float] = error
        else:
            self.medida = medida.medida
            self.error = medida.error
        if aproximar:
            self.aprox()
        self.__print_style = self.Estilo.pm

    def datos():
        doc = "The medida property. Pero permite ser usado solo con listas para el usuario"
        def fget(self):
            return list(self._medida)
        def fset(self, value):
            self.medida = value
        def fdel(self):
            del self._medida
        return locals()
    datos = property(**datos())

    def unpack(self) -> tuple[list[float], list[float]]:
        """Devuelve una tupla con la(s) medida(s) y su(s) error(es)"""
        return list(self.medida), list(self.error)

    def lista_de_medidas(self):
        return [Medida(*i, aproximar=False) for i in zip(self.medida, self.error)]

    def copy(self):
        """Retorna una copia INDEPENDIENTE de si misma"""
        # los list son para hacer que las listas sean independientes
        return Medida(list(self.medida), list(self.error), aproximar=False)

    def aprox(self):
        """Aproxima los valores de la medida"""
        self.medida, self.error = aprox(self.medida, self.error)
        return self

    def media(self) -> float:
        """Calcula la media de los valores"""
        return float(media(*self.medida))

    def desviacion_estandar(self) -> float:
        """Calcula la desviación estandar de los valores de la medida"""
        return float(desviacion_estandar(*self.medida))

    def error_estandar(self) -> float:
        """Calcula el error estandar de los valores de la medida (desviación estandar de la media)"""
        return float(error_estandar(*self.medida))

    def estimacion(self):
        """Calcula la media de los valores de la medida y el error de esta sumando en cuadratura el error estandar y el error"""
        return Medida(self.media()* (1+0*self.error), list(np.sqrt( self.error_estandar()**2 + self.error**2 )), aproximar = False)

    def cambia_estilo(self, estilo):
        if estilo in self.Estilo.__dict__.values():
            self.__print_style = estilo
            return self
        else:
            raise TypeError(f'El estilo {estilo} no es un estilo válido')

    class Estilo:
        def lista(self):
            if len(self.medida) == 1:
                m = self.medida[0]
                e = self.error[0]
            else:
                m = self.medida
                e = self.error
            return f'{m} ± {e}'

        def pm(self):
            l = []
            for m, e in zip(self.medida, self.error):
                l.append(f'{m} ± {e}')
            return ', '.join(l)

        def tabla(self):
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
        return Medida(self.medida + other.medida, np.sqrt(self.error**2 + other.error**2), aproximar = False)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not isinstance(other, Medida):
            other = Medida(other)
        return Medida(self.medida - other.medida, np.sqrt(self.error**2 + other.error**2), aproximar = False)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        # Si es un escalar
        if not isinstance(other, Medida):
            medida = self.medida * other
            error = self.error * abs(other)
        else:
            medida = self.medida*other.medida
            error = np.sqrt(np.array( (other.medida * self.error)**2 + (self.medida * other.error)**2 ))

        return Medida(medida, error, aproximar = False)

    def __rmul__(self, val):
        return Medida(val * self.medida, abs(val) * self.error, aproximar = False)

    def __truediv__(self, other):
        # Si es un escalar
        if not isinstance(other, Medida):
            medida = self.medida/other
            error = self.error/abs(other)
        else:
            medida = self.medida/other.medida
            error = np.sqrt(np.array( (1/other.medida * self.error)**2
                            + (self.medida/other.medida**2 * other.error)**2 ))
        return Medida(medida, error, aproximar = False)

    def __rtruediv__(self, other):
        return Medida(other/self.medida, abs(other/self.medida**2) * self.error, aproximar = False)

    def __pow__(self, other):
        medida = self.medida**other
        error = abs((other)*self.medida**(other-1))*self.error
        return Medida(medida, error, aproximar = False)

    def __and__(self, other):
        return Medida(self.medida + other.medida, self.error + other.error, aproximar = False)

    def __or__(self, other):
        return self & -other

    def __len__(self):
        return len(self.medida)

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError("Indice fuera de rango")
        return Medida(self.medida[index], self.error[index])

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
