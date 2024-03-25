from .objects import Measure
from .tables import transposer


def load(file: str, separator: str = '\t', line: str = '\n', decimal: str = ',', headers: int = 0, by_columns=True) -> list[list[float]]:
    with open(file, 'rt') as file:
        data = file.read()
        rows = [i for i in data.split(line) if i.strip() != '']
        data = [[float(i.strip().replace(decimal, '.')) if i.strip() != '' else None for i in j.split(separator) ] for j in rows[headers:]]
    
    if by_columns:
        max_len = max((len(i) for i in data))        
        data = [[i[index] for i in data if index < len(i) and i[index] != None] for index in range(max_len)]
    
    return data

def save_latex(file: str, data: list, separator: str = '\t', line: str = '\n', by_columns=True, style = Measure.Style.latex_table):
    
    # Conversión de data a strings
    data = [row if hasattr(row, '__iter__') else [row] for row in data]
    
    def parser(data):
        iter = data if not isinstance(data, Measure) else data.copy().change_style(style).list_of_values()
        return list(map(str, iter))
        
    
    list_string = list(map(parser, data))
    
    # Add the missing spaces
    max_len = max((len(i) for i in list_string))        
    list_string = [line if len(line)==max_len else line + ['']*(max_len-len(line))  for line in list_string]
    if not by_columns:
        list_string = transposer(list_string)
    
    string = line.join([separator.join(element) for element in list_string])
    with open(file, 'w+') as file:
        file.write(string)
    