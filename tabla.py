from .objetos import Medida
from tabulate import tabulate
from .type_alias import Opcional

def transpose(lista: list) -> list:
    return list(zip(*lista))

def create_table_list(lista: list, cabecera=None, transponer=False, estilo = Medida.Estilo.tabla) -> list[list]:
    a = []
    for element in lista:
        if isinstance(element, Medida):
            a.append([i.cambia_estilo(estilo) for i in element.lista_de_medidas()])
        else:
            a.append(element)
    lista = a
    max_len = max([len(i) for i in lista])
    lista = [i + ['']*(max_len - len(i) if len(i) < max_len else 0) for i in lista]
    if cabecera is not None:
        if len(cabecera) < len(lista):
            cabecera = cabecera + ['']*(len(lista)-len(cabecera))
        lista = [[h] + l for h, l in zip(cabecera, lista)]
    if not transponer:
        lista = transpose(lista)
    return [[str(l) for l in j] for j in lista]

def terminal(datos: list, cabecera: Opcional[list] = None, transponer: bool = False) -> str:
    """Devuelve una cadena de texto que representa una tabla que se puede mostrar por la terminal"""
    return tabulate(create_table_list(datos, cabecera, transponer), tablefmt='grid')

def latex(datos: list, cabecera: Opcional[list] = None, caption: str = 'Caption', label: str = 'tab:my_label', transponer: bool = False) -> str:
    """Devuelve una cadena de texto que representa una tabla de latex"""
    datos = create_table_list(datos, cabecera, transponer, estilo=Medida.Estilo.tabla_latex)
    
    tabular = '\t\t' + '\\\\ \n\t\t'.join(' & '.join(i) for i in datos)
    ancho = max((len(i) for i in datos))
    
    tabular = f'\t \\begin{"{"}tabular{"}"}{"{"}|{"|".join(["c"]*ancho)}|{"}"}\n' + tabular + '\n' + '\t\\end{tabular}'
    table = '\\begin{table}[ht]\n \\centering \n\n' + '\\caption{' + caption + '}\n\\label{' + label + '}\n\n' + tabular + '\n\n' + '\\end{table}'
    return table
