from .objects import Unit
from scipy.constants import e as electron_charge
from scipy.constants import pi

kg  = Unit([1, 0, 0, 0, 0, 0, 0], symbol="kg")
m   = Unit([0, 1, 0, 0, 0, 0, 0], symbol="m")
s   = Unit([0, 0, 1, 0, 0, 0, 0], symbol="s")
A   = Unit([0, 0, 0, 1, 0, 0, 0], symbol="A")
K   = Unit([0, 0, 0, 0, 1, 0, 0], symbol="K")
mol = Unit([0, 0, 0, 0, 0, 1, 0], symbol="mol")
cd  = Unit([0, 0, 0, 0, 0, 0, 1], symbol="cd")
rad = Unit([0, 0, 0, 0, 0, 0, 0], symbol="rad")

N   = Unit(kg * m * s**-2, symbol="N")
J   = Unit(N*m, symbol="J")
C   = Unit(A*s, symbol="C")
W   = Unit(J/s, symbol="W")
Pa  = Unit(N*m**-2, symbol="Pa")
Bar = Unit(Pa, scale=1e5, symbol="bar")
Atm = Unit(Pa, scale=101325, symbol="atm")
V   = Unit(W*A**-1, symbol="V")
Ohm = Unit(V/A, symbol="Ohm")
Mho = Unit(Ohm**-1, symbol="Mho")
Wb  = Unit(V*s, symbol="Wb")
T   = Unit(Wb/m**2, symbol="T")
H   = Unit(Wb/A, symbol="H")
Hz  = Unit(s**-1, symbol="Hz")
Bq  = Unit(Hz, symbol="Bq")
eV  = Unit(J, scale=electron_charge, symbol="eV")


g   = Unit(kg, scale=1e-3, symbol="g")
mg  = Unit(kg, scale=1e-6, symbol="mg")

km  = Unit(m, scale=1e3, symbol="km")
cm  = Unit(m, scale=1e-2, symbol="cm")
mm  = Unit(m, scale=1e-3, symbol="mm")
mum = Unit(m, scale=1e-6, symbol="μm")
nm  = Unit(m, scale=1e-9, symbol ="nm")

year= Unit(s, scale=365.25*24*3600, symbol="year")
day = Unit(s, scale=24*3600, symbol="day")
h   = Unit(s, scale=3600, symbol="h")
min = Unit(s, scale=60, symbol="min")
ms  = Unit(s, scale=1e-3, symbol="ms")
mus = Unit(s, scale=1e-6, symbol="μs")
ns  = Unit(s, scale=1e-9, symbol="ns")

mA  = Unit(A, scale=1e-3, symbol="mA")
muA = Unit(A, scale=1e-6, symbol="μA")
nA = Unit(A, scale=1e-9, symbol="nA")

grad = Unit(rad, scale=pi/180, symbol="°")
arcmin = Unit(grad, scale=1/60, symbol="'")
arcsec = Unit(grad, scale=1/3600, symbol="''")

keV = Unit(eV, scale=1000, symbol="keV")
MeV = Unit(eV, scale=1e6, symbol="MeV")
GeV = Unit(eV, scale=1e9, symbol="GeV")

mL = Unit(cm**3, scale=1, symbol="mL")
L = Unit(mL, scale=1000, symbol="L")
