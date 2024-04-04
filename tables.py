from .objects import Measure
from tabulate import tabulate

def transposer(l: list) -> list:
    return list(zip(*l))

def create_table_list(l: list, header=None, transpose=False, style = Measure.Style.table) -> list[list]:
    a = []
    for element in l:
        if isinstance(element, Measure):
            a.append([i.change_style(style) for i in element.list_of_measures()])
        else:
            a.append(element)
    l = a
    max_len = max([len(i) for i in l])
    l = [i + ['']*(max_len - len(i) if len(i) < max_len else 0) for i in l]
    if header is not None:
        if len(header) < len(l):
            header = header + ['']*(len(l)-len(header))
        l = [[h] + l for h, l in zip(header, l)]
    if not transpose:
        l = transposer(l)
    return [[str(l) for l in j] for j in l]

def terminal(data: list, header: list = None, transpose: bool = False) -> str:
    """
    Creates a string that represents a table that can be shown in the terminal
    """
    return tabulate(create_table_list(data, header, transpose), tablefmt='grid')

def latex(data: list, header: list = None, caption: str = 'Caption', label: str = 'tab:my_label', transpose: bool = False) -> str:
    """
    Creates a string that represents a latex table
    """
    data = create_table_list(data, header, transpose, style=Measure.Style.latex_table)
    
    tabular = '\t\t' + '\\\\ \n\t\t'.join(' & '.join(i) for i in data)
    width = max((len(i) for i in data))
    
    tabular = f'\t \\begin{"{"}tabular{"}"}{"{"}|{"|".join(["c"]*width)}|{"}"}\n' + tabular + '\n' + '\t\\end{tabular}'
    table = '\\begin{table}[ht]\n \\centering \n\n' + '\\caption{' + caption + '}\n\\label{' + label + '}\n\n' + tabular + '\n\n' + '\\end{table}'
    return table

def typst(data: list, header: list = None, transpose: bool = False):
    """
    Creates a string that represents a typst table
    """
    data = create_table_list(data, header, transpose, style=Measure.Style.typst_table)
    data = [[f'[{i}]' for i in j] for j in data]
    
    tabular = '\n\t\t' + ', \n \t\t'.join(', '.join(i) for i in data)
    
    width = max((len(i) for i in data))
    table = f"\t table(\n\t columns: {width}, \n\t align: center, {tabular} \n)"
    return table
