# Pysics
Pysics is a Python module designed to perform calculations typically done in physics laboratories. It is based on the use of the "Measure" class, which allows storing measures with errors and performing standard approximation (first significant digit of the error, two if it is a 1).

## Table of Contents
1. [Installation](#installation)
2. [Basic Operations](#basic-operations)
3. [Units](#units)
4. [Plot](#plot)
5. [Fit](#fit)
6. [Func](#func)
7. [Read](#read)
8. [Tables](#tables)
9. [Acknowledgements](#acknowledgements)

## Installation

The library is available in pip so you can install it with:

```
pip install pysics
```

## Basic Operations
The fundamental part of the module is the Measure class. Initializing an object can be done in several ways.
```python
# If it is a measure without error because it is negligible or for some other reason, it can be done simply by passing the value
m = Measure(9.81)
# If we have an error, it will be passed as the second argument, e.g., (7.831 ± 0.0138).
a = Measure(7.831, 0.0138)
```

If we execute the previous line, we will see that the result of `a` is 7.831 ± 0.014.
This is because by default, Measure performs the approximation when initializing the object.
To avoid this, you can pass the argument `approximate=False`
```python
b = Measure(7.831, 0.0138, approximate=False)
```

If we want to perform the approximation later, it can be done with `.approx()`
```python
b.approx()
# approx also returns a pointer to the object, which allows things like
b = b.approx()
# now a==b
# or
c = (a+b).approx()
# which would be equivalent to
c = a+b
c.approx()
```
Measures can also be a list of several values, e.g., c = 1.1 ± 0.1, 2.2 ± 0.1, 3.3 ± 0.1
```python
# Since all values have the same error, it is enough to write it once
c = Measure([1.1, 2.2, 3.3], 0.1, approximate=False)
```
d = 1.1 ± 0.1, 2.2 ± 0.2, 3.3 ± 0.3
In this case, there are different errors, so two lists are passed: the first contains the values, and the second contains the errors such that the index of each list is a value and its corresponding error. If the lists do not have the same length, an error will be thrown.
```python
d = Measure([1.1, 2.2, 3.3], [0.1, 0.2, 0.3])
```
For this kind of Measures, the class method "from_pairs" is provided, which allows passing a list of values in tuples.
The following code is equivalent to the previous one.
```python
d = Measure.from_pairs([1.1, 0.1], [2.2, 0.2], [3.3, 0.3], approximate=True)
```

Measure objects can be added, subtracted, multiplied, etc., by other Measures and by scalars, always returning other Measures.
Additionally, approximations will not be performed when making a calculation; this is to allow concatenating several operations without losing precision.
When performing these calculations, errors are recalculated. For ALL cases except & and ||, Measures are considered independent, so the error is the sum in quadrature.
Operations between Measures are defined element by element, i.e., the first is added to the first, the second to the second, etc.
Operations with scalars are defined as the operation of the scalar over the entire measure, e.g., c+1 will result in Measure([1.1 + 1, 2.2 + 1, 3.3 + 1], [0.1], approximate=False).
If there is a measure with a single value, e.g., Measure(1, 0.1), it will be considered as a scalar taking into account the error. If two Measures with different numbers of elements are added, and neither has a single element, e.g., Measure([1, 2]) + Measure([1, 2, 3]), an error will be thrown.
``` python
e = (a+b).approx() # 15.662 ± 0.02
f = (c*d).approx() # 1.21 ± 0.16, 4.8 ± 0.5, 10.9 ± 1.0
```
If two Measures are dependent and want to be added or subtracted, the operators & and | should be used.
```python
# To add dependent Measures, use the & operator
h = (a&b).approx() # 15.66 ± 0.03
# To subtract dependent Measures, use the | operator
i = (a|b).approx() # 0.0 ± 0.03 equivalent to (a&(-b))
```

To make copies of a measure, you can use the copy method.
In the following example, a copy with the approximations of c is made without modifying c.
```python
j = c.copy().approx()
# If instead of the above we used the following, we would modify c, and it is possible that certain changes applied to j would affect c
j = c.approx()
```

To retrieve the values of the Measures or errors in a list, you can use the properties `measure` and `error`.
```python
print(d.value) # [1.1, 2.2, 3.3]
print(d.error)  # [0.1, 0.2, 0.3]
measure, error = d.unpack()
```
To calculate the mean, standard deviation, and standard error of a measure, you can use the methods of the same name.
```python
mean = d.mean()
standard_deviation = d.standard_deviation()
standard_error = d.standard_error() # Standard deviation of the mean
mean, standard_error = d.estimation()
```

## Units

The `Measure` object also supports operations with units. To create a `Measure` with units, you can simply multiply by the unit:

```python
a = Measure(2, 0.1) * kg
print(a)  # 2 ± 0.1 kg
```

This will create `a` as a measure with `kg` as its unit. The most common units are predefined in *units* for your convenience. However, you can also create your own unit using the `Unit` class constructor:

```python
year = Unit(s, scale=365.25*24*3600, symbol="year")
```

To define a custom unit:
1. Provide its equivalent in the [International System of Units (SI)](https://en.wikipedia.org/wiki/International_System_of_Units). This can be a combination of existing units.
2. Specify the `scale` factor to convert your unit to the SI unit.
3. Set a `symbol` for concise representation of the unit.

The `scale` is the factor you multiply your unit by to convert it to the SI unit. The `symbol` is used for formatting when printing the value with its unit.

Once created, you can use your custom unit just like the predefined ones.


## Plot

Pysics also provides a powerful plotting API that integrates seamlessly with the `Measure` class. It offers various types of plots and data fitting capabilities.

### Basic Plotting

The plotting module supports different types of plots, including scatter, line and polar plots. Here's an example using them:

```python
from pysics.plot import scatter, plot, polar_plot, show, legend
from pysics.constants import pi
import numpy as np

x = Measure([1, 2, 3, 4, 5], 0.1)
y = Measure([2, 4, 5, 4, 5], 0.2)

# Create a scatter plot with error bars
scatter(x, y, xerr=True, yerr=True, label='Data with Errors')
# The xerr and yerr parameters set to True tell the function to use the errors from the Measure objects. You can also pass a list of errors to them and it will use that list as errors.

# Create a line plot using the same data
plot(x, y, label='Data Line')

# Create a polar plot
theta = np.linspace(0, 2*pi, 100)
r = np.cos(4*theta)

polar_plot(theta, r, label='Polar Data')

# Displays the labels
legend()
# Display the plots
show()
```

This example demonstrates how to create diferent plots with error bars using Measure objects. The `scatter` function automatically uses the error values from the Measure objects when `xerr` and `yerr` are set to True. There is also a `polar_scatter` function.

### Customizing Plots

Pysics allows for extensive customization of plots, including the use of LaTeX for rendering labels:

```python
from pysics.plot import scatter, xlabel, ylabel, title, use_latex, show

use_latex()  # Enable LaTeX rendering

x = [1,2,3,4]
y = [1,2,3,4]

scatter(x, y)

# Set axis labels and title using LaTeX syntax
xlabel(r'$x$ axis')
ylabel(r'$y$ axis')
title(r'Plot with $\LaTeX$ labels')

show()
```

The `use_latex()` function enables LaTeX rendering for all text elements in the plot. The `r` prefix before the strings denotes raw strings, which is useful when writing LaTeX code to avoid issues with backslashes.

Furthermore, since Pysics uses Matplotlib underneath, you can use Matplotlib functions to further customize your plots.

### Saving Plots

Saving plots to various file formats is straightforward:

```python
from pysics.plot import scatter, save

scatter(x, y)
save('my_plot', format='png')
```

This code creates a scatter plot and saves it as 'my_plot.png' in the current directory. The `save` function supports various formats including 'png', 'pdf', 'svg', and more.


## Fit

The Fit module in Pysics provides functions for fitting data to various models using measures. Here's an example of a linear fit:

```python
from pysics.fit import least_squares
from pysics.plot import scatter, line

x = Measure([1, 2, 3, 4, 5], 0.3)
y = Measure([2.1, 3.9, 6.2, 7.8, 9.9], 0.1)

# Perform a linear fit
fit_result = least_squares(x, y)

# Plot the original data
scatter(x, y)

# Plot the fit line
line(x, fit_result)

show()
```

In this example, `least_squares` performs a linear fit on the data. The resulting `fit_result` contains the parameters of the fit (slope and intercept) as Measure objects, including the errors of the fit. The `line` function then uses these parameters to plot the fit line.

Here's another example of fitting data, this time we use a custom function:

```python
from pysics.fit import curve as curve_fit
from pysics.plot import curve as curve_plot, show

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

x = [0, 1, 2, 3, 4, 5]
y = [1, 2.1, 5.2, 10.3, 17.4, 26.5]

fit_params = curve_fit(quadratic, x, y)

# Plot the fit curve
curve_plot(quadratic, x, fit_params)
show()
```

In this example:
1. We define a quadratic function `quadratic(x, a, b, c)` that represents our model.
2. We provide x and y data points.
3. The `curve_fit` function fits the data to the quadratic model.
4. `fit_params` contains the best-fit values for a, b, and c as Measure objects, including their uncertainties.
5. `curve_plot` function plots the obtained curve.

This powerful fitting capability allows you to fit your data to any custom function, making it versatile for various scientific applications.

## Func

The `func` module provides a comprehensive set of mathematical and physics-related functions that work seamlessly with the `Measure` class. The functions available are:

1. Trigonometric functions: sin, cos, tan, and their inverses (asin, acos, atan)
2. Angular conversions: rad (degrees to radians) and grad (radians to degrees)
3. Logarithmic and exponential functions: ln, exp
4. Other mathematical operations: sqrt, atan2 (polar coordinate angle)
5. Utility functions: delta (difference between consecutive values)

All these functions are designed to work with `Measure` objects, handling both scalar and array inputs.

Examples of usage:

1. Trigonometric functions:
```python
from pysics import Measure, units, func

angle = Measure(45, 1, units=units.deg)
sin_value = func.sin(func.rad(angle))
print(f"sin(45°) = {sin_value}")
```

2. Inverse trigonometric functions:
```python
x = Measure(0.5, 0.01)
angle = func.asin(x)
print(f"arcsin(0.5) = {angle}")
```

3. Logarithmic and exponential functions:
```python
value = Measure(10, 0.1)
log_value = func.ln(value)
exp_value = func.exp(Measure(1, 0.01))
print(f"ln(10) = {log_value}")
print(f"e^1 = {exp_value}")
```

4. Square root:
```python
number = Measure(16, 0.5)
root = func.sqrt(number)
print(f"sqrt(16) = {root}")
```

5. Polar coordinate angle:
```python
x = Measure(3, 0.1)
y = Measure(4, 0.1)
angle = func.atan2(y, x)
print(f"atan2(4, 3) = {angle}")
```

6. Delta function (for array inputs):
```python
values = Measure([1, 3, 6, 10], [0.1, 0.1, 0.2, 0.2])
differences = func.delta(values)
print(f"Differences: {differences}")
```

These functions automatically handle error propagation, making it easy to perform complex calculations while keeping track of uncertainties. They also include warnings for potentially incorrect usage, such as passing non-angular values to trigonometric functions.

## Read

The `reader` module in Pysics provides functions for loading data from files and saving data in LaTeX format.

To load data from a file:

```python
from pysics.reader import load

data = load("input.txt", separator=",", headers=1)
```

The `load` function parameters are:
- `file`: Path to the input file.
- `separator`: Character used to separate values (default: '\t').
- `line`: Character used to separate rows (default: '\n').
- `decimal`: Character used as decimal separator (default: ',').
- `headers`: Number of header rows to skip (default: 0).
- `by_columns`: If True, organizes data by columns; if False, by rows (default: True).

To save data in LaTeX format:

```python
from pysics.reader import save_latex

save_latex("output.tex", data, separator="&", style=Measure.Style.scientific)
```

The `save_latex` function parameters are:
- `file`: Path to the output file.
- `data`: List of data to be saved.
- `separator`: Character used to separate values (default: '\t').
- `line`: Character used to separate rows (default: '\n').
- `by_columns`: If True, organizes data by columns; if False, by rows (default: True).
- `style`: Style for formatting Measure objects (default: Measure.Style.latex_table).

This function converts the input data to strings, ensures consistent row lengths, and writes the formatted data to the specified file.

## Tables

The `tables` module in Pysics provides utilities for creating and formatting tables in various output formats.

To create a formatted table as a list of lists:

```python
from pysics.tables import create_table_list

data = [[1, 2, 3], [4, 5, 6]]
header = ['A', 'B', 'C']
formatted_table = create_table_list(data, header=header, style=Measure.Style.table)
```

To create a string representation of a table for terminal display:

```python
from pysics.tables import terminal

data = [[1, 2, 3], [4, 5, 6]]
header = ['A', 'B', 'C']
print(terminal(data, header=header))
```

To create a LaTeX representation of a table:

```python
from pysics.tables import latex

data = [[1, 2, 3], [4, 5, 6]]
header = ['A', 'B', 'C']
latex_table = latex(data, header=header, caption="My Table", label="tab:example")
print(latex_table)
```

To create a Typst representation of a table:

```python
from pysics.tables import typst

data = [[1, 2, 3], [4, 5, 6]]
header = ['A', 'B', 'C']
typst_table = typst(data, header=header)
print(typst_table)
```

These functions provide flexible table formatting options for various output formats, making it easy to present data in the desired style for different applications.

## Acknowledgements
Special thanks to [Jonathan Dönszelmann](https://donsz.nl/) for the pypi project name