import scipy.constants as consts
from .units import *

pi = consts.pi
golden = consts.golden
golden_ratio = consts.golden_ratio

c = consts.c * m/s
e = consts.e * C
h = consts.h * J*s
hbar = consts.hbar * J*s
G = consts.G * N * m**2/kg**2
eps_0 = consts.epsilon_0 * C**2 * N**-1 * m**-2
mu_0 = consts.mu_0 * N/A**2
g = consts.g * m/s**2
N_A = consts.N_A / mol
k_b = consts.k * J/K
m_e = consts.m_e * kg
m_p = consts.proton_mass * kg
m_n = consts.m_n * kg
R = consts.R * J/(K*mol)
alpha = consts.alpha
