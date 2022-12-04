from .objetos import Medida
from .tabla import transpose


def cargar(archivo: str, separador: str = '\t', linea: str = '\n', decimal: str = ',', cabeceras: int = 0, por_columnas=True) -> list[list[float]]:
    with open(archivo, 'rt') as file:
        data = file.read()
        filas = [i for i in data.split(linea) if i.strip() != '']
        datos = [[float(i.strip().replace(decimal, '.')) if i.strip() != '' else None for i in j.split(separador) ] for j in filas[cabeceras:]]
    
    if por_columnas:
        max_len = max((len(i) for i in datos))        
        datos = [[i[index] for i in datos if index < len(i) and i[index] != None] for index in range(max_len)]
    
    return datos

def guardar_latex(datos: list, archivo: str, separador: str = '\t', linea: str = '\n', por_columnas=True, estilo = Medida.Estilo.tabla_latex):
    
    # Conversión de datos a strings
    datos = [fila if hasattr(fila, '__iter__') else [fila] for fila in datos]
    
    def parser(dato):
        iter = dato if not isinstance(dato, Medida) else dato.copy().cambia_estilo(estilo).lista_de_medidas()
        return list(map(str, iter))
        
    
    list_string = list(map(parser, datos))
    
    # Añadir los huecos que faltan
    max_len = max((len(i) for i in list_string))        
    list_string = [line if len(line)==max_len else line + ['']*(max_len-len(line))  for line in list_string]
    if not por_columnas:
        list_string = transpose(list_string)
    
    string = linea.join([separador.join(elemento) for elemento in list_string])
    with open(archivo, 'w+') as file:
        file.write(string)
    
    
