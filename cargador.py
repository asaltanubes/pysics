def cargar(archivo: str, separador: str = '\t', linea: str = '\n', decimal: str = ',',cabeceras: int = 0, data_type: type = float) -> list[list[str]]:
    with open(archivo, 'rt') as file:
        data = file.read().strip()
        filas = [i.strip() for i in data.split(linea)]
        datos = [[data_type(i.strip().replace(decimal, '.')) for i in j.split(separador)] for j in filas[cabeceras:]]
    return datos
