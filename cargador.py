def cargar(archivo: str, separador: str = '\t', linea: str = '\n', decimal: str = ',', cabeceras: int = 0, transposed=True) -> list[list[str]]:
    with open(archivo, 'rt') as file:
        data = file.read()
        filas = [i for i in data.split(linea) if i.strip() != '']
        datos = [[float(i.strip().replace(decimal, '.')) if i.strip() != '' else None for i in j.split(separador) ] for j in filas[cabeceras:]]
    
    if transposed:
        max_len = max((len(i) for i in datos))        
        datos = [[i[index] for i in datos if index < len(i) and i[index] != None] for index in range(max_len)]
    
    return datos
