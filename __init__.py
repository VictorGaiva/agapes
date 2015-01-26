#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
PSG - Tecnologia Aplicada

Este é um módulo utilizado para contagem de falhas em
plantações de cana-de-açúcar através do uso de imagens
aéreas capturadas por VANT's ou aparelhos similares.

Este arquivo é responsável pelo desenho da interface do
programa e também pela execução e apresentação dos
resultados obtidos com a imagem fornecida.
"""
from controller import ExecuteCommandLine
import textwrap
import argparse
import sys
import os

sys.path.append(
    os.path.dirname(__file__)
)

if __name__ == '__main__':

    while sys.argv[0] != __file__:
        sys.argv.pop(0)

    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent("""\
            PSG - Tecnologia Aplicada.
            --------------------------
            Esta aplicação é utilizada para contar a
            quantidade de falhas presente em uma plantação
            de cana-de-açúcar. São utilizadas imagens aéreas
            para a contabilização das falhas presentes.
            """.decode('latin1'))
    )

    parser.add_argument(
        'image',
        metavar = 'image',
        type = str,
        nargs = '?',
        help = "imagem alvo da análise".decode('latin1')
    )

    parser.add_argument(
        'dist',
        metavar = 'dist',
        type = float,
        nargs = '?',
        help = "distância entre as linhas de plantação".decode('latin1')
    )

    args = parser.parse_args()
    
    if args.dist is None or args.image is None:
        from gui import InitGUI
        InitGUI()

    else:
        ExecuteCommandLine(args.image, args.dist)
