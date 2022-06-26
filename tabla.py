from pysics.objetos import Medida
from tabulate import tabulate

def transpose(lista: list) -> list:
    return list(zip(*lista))

def create_table_list(lista, cabecera=None, transponer=False):
    a = []
    for element in lista:
        if isinstance(element, Medida):
            a.append([i.cambia_estilo(Medida.Estilo.tabla) for i in element.lista_de_medidas()])
        else:
            a.append(element)
    lista = a
    if cabecera is not None:
        if len(cabecera) < len(lista):
            cabecera = cabecera + ['']*(len(lista)-len(cabecera))
        lista = [[h] + l for h, l in zip(cabecera, lista)]
    if not transponer:
        lista = transpose(lista)
    return lista

def terminal(datos, cabecera = None, transponer = False):
    return tabulate(create_table_list(datos, cabecera, transponer), tablefmt='grid')

def latex(datos, cabecera = None, caption='Caption', label = 'tab:my_label', transponer = False):
    tabular = '\n'.join(tabulate(create_table_list(datos, cabecera, transponer), tablefmt='latex').replace(r'\\', '\\\\ \n \\hline').split('\n')[1:-2])
    ancho = len(tabular.split('\\hline')[1].split('&'))
    tabular = f'\\begin{"{"}tabular{"}"}{"{"}|{"|".join(["c"]*ancho)}|{"}"}\n' + tabular + '\n' + r'\end{tabular}'
    table = '\\begin{table}[ht]\n \\centering \n\n' + tabular + '\n\n' + '\\caption{' + caption + '}\n\\label{' + label + '}\n\\end{table}'
    return table
