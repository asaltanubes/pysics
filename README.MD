# pysics
Pysics es un módulo escrito en python para realizar los cálculos que suelen realizarse en laboratorios de física. 
Este se basa en el uso de la clase ""Medida"" la cual permite guardar mediciones con error y realizar la aproximación estandar
(primera cifra significativa del error, dos si se trata de un 1).

### Uso
La parte fundamental del módulo es la clase Medida. La inicialización de un objeto puede realizarse de varias formas.
```python
# Si se trata de una medida sin error porque se desprecia o por alguna otra razón puede hacerse simplemente pasando el valor
m = Medida(9.81)
# Si tenemos un error se pasará como segundo argumento ej (7.831 ± 0.0138).
a = Medida(7.831, 0.0138)
```

Si ejecutamos la linea anterior observaremos que el resultado de a es 7.831 ± 0.014.
Esto es porque por defecto Medida realiza la aproximación al inicializar el objeto.
Para evitarlo se puede pasar como argumento aproximar=False
```python
b = Medida(7.831, 0.0138, aproximar=False)
```

Si queremos realizar la aproximación más adelante puede hacerse con .aprox()
```python
b.aprox()
# aprox también devuelve un puntero a el objeto lo que permite cosas como
b = b.aprox()
print(a == b) # True

# o
c = (a+b).aprox()
# que sería equivalente a
c = a+b
c.aprox()
```
Las medidas también pueden ser una lista de varios valores ej: c = 1.1 ± 0.1, 2.2 ± 0.1, 3.3 ± 0.1
```python
# Como todos los valores tienen el mismo error vale con escribirlo una vez
c = Medida([1.1, 2.2, 3.3], 0.1, aproximar=False)
```
d = 1.1 ± 0.1, 2.2 ± 0.2, 3.3 ± 0.3
 En este caso hay errores distintos por lo que se pasan dos listas, la primera contiene los valores y la segunda los errores de tal forma que el indice de cada lista es un valor y su correspondiente error. Si las listas no tienen la misma longitud se lanzará un error.
```python
d = Medida([1.1, 2.2, 3.3], [0.1, 0.2, 0.3])
```
Para esta clase de Medidas se proporciona el classmethod "from_pairs" que permite pasar una lista de valores en tuplas.
El siguiente código es equivalente al anterior.
```python
d = Medida.from_pairs([1.1, 0.1], [2.2, 0.2], [3.3, 0.3], aproximar=True)
```

Los objetos de medida pueden ser sumados, restados, multiplicados... por medidas y por escalares devolviendo siempre otras Medidas.
Además no se realizarán las aproximaciones al realizar un cálculo, esto es para poder concatenar varias operaciones sin perder precisión.
Al realizar estos calculos se recalculan los errores. Para TODOS los casos exceptuando & y || las medidas se consideran independientes por lo que
el error es la suma en cuadratura
Las operaciones entre medidas están definidas elemento por elemento, es decir, se suman el primero con el primero, el segundo con el segundo...
Las operacions con escalares están definidas como la operación del escalar sobre toda la medida, ej: c+1 resultará en Medida([1.1 + 1, 2.2 + 1, 3.3 + 1], [0.1], aproximar=False)
Si hay una medida con un único valor, ej: Medida(1, 0.1), se considerará como un escalar teniendo en cuenta el error. Si se suman dos medidas con distinta cantidad de elementos
y ninguna tiene un unico elemento, ej: Medida([1, 2]) + Medida([1, 2, 3]), se lanzará un error.
``` python
e = (a+b).aprox() # 15.662 ± 0.02
f = (c*d).aprox() # 1.21 ± 0.16, 4.8 ± 0.5, 10.9 ± 1.0
```
Si dos medidas son dependientes y quieren sumarse o restarse se deben usar los operadores & y |
```python
# Para realizar sumas de medidas dependientes se usa el operador &
h = (a&b).aprox() # 15.66 ± 0.03
# Para realizar restas de medidas dependientes se usa el operador |
i = (a|b).aprox() # 0.0 ± 0.03 equivalente a (a&(-b))
```

Para realizar copias de una medida se puede emplear el metodo copy.
En el siguiente ejemplo se hace una copia con las aproximaciones de c sin modificar c.
```python
j = c.copy().aprox()
# Si en vez de lo anterior usasemos los siguiente modificaríamos c, además, es posible que ciertos cambios aplicados a j afectasen a c
j = c.aprox()
```

Para recoger los valores de las medidas o errores en una lista se pueden usar las propiedades medida y error.
```python
print(d.medida) # [Number(1.1), Number(2.2), Number(3.3)]
print(d.error)  # [Number(0.1), Number(0.2), Number(0.3)]
medida, error = d.unpack()
```
Para calcular la media, desviación estandar y error estandar de una medida pueden usarse los métodos del mismo nombre
```python
media = d.media()
desviacion_estandar = d.desviacion_estandar()
error_estandar = d.error_estandar() # Desviación estandar de la media
media, error_estandar = d.estimacion()
```
