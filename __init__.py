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

    parser.add_argument(
        'width',
        metavar = 'width',
        type = int,
        nargs = '?',
        default = 200,
        help = "largura das amostras de recorte (default = 200)".decode('latin1')
    )

    parser.add_argument(
        'height',
        metavar = 'height',
        type = int,
        nargs = '?',
        default = 200,
        help = "altura das amostras de recorte (default = 200)".decode('latin1')
    )

    parser.add_argument(
        'rate',
        metavar = 'rate',
        type = float,
        nargs = '?',
        default = 0.6,
        help = "porcentagem de amostras a serem contabilizadas (default = 0.6)".decode('latin1')
    )

    args = parser.parse_args()

    from controller import Execute
    Execute(args.image, args.dist, args.width, args.height, args.rate)
