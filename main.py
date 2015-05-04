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

sys.path.append(os.path.dirname(__file__))

if __name__ == '__main__':
    from controller import execute
    import config

    while sys.argv[0] != __file__:
        sys.argv.pop(0)

    parser = argparse.ArgumentParser(
        prog = "main",
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent(u"""
            Esta aplicação é utilizada para contar a quantidade
            de falhas presente em uma plantação de cana-de-açúcar
            a partir de imagens aéreas da região a ser analizada.
            """)
    )

    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = config.version,
        help = u"exibe a versão atual do programa"
    )

    parser.add_argument(
        "--no-gui",
        dest = "gui",
        action = "store_false",
        help = u"inicializa o programa em modo de linha de comando"
    )

    args = parser.parse_args()
    execute(args)
