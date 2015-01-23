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

from segmentation import *
from gui import InitGUI
from gui.event import *
from line import *

# TODO: Melhorar o algoritmo que encontra linhas adjacentes.
# TODO: Feedback de execução e de erros.
# TODO: Correlacionar a imagem da janela com a imagem original.
# TODO: Redimensionar imagem para um tamanho fixo, e não para proporção.
# TODO: Transformar equações utilizadas para funções paramétricas.
# TODO: Ao soltar uma imagem, exibí-la diretamente no campo de drag-n-drop.
# TODO: Adicionar ferramentas de edição de imagem, parte inferior da janela.
# TODO: Criação de um instalador automático de dependencias.


def ShowImage(img):
    """
    Prepara a janela para mostrar todos os passos de
    execução do algoritmo.
    @param img Primeira imagem a ser mostrada.
    """
    global window
    window = ImageWindow(config.appname, img)


def AddImage(img):
    """
    Adiciona uma imagem a ser exibida na janela.
    @param img Imagem a ser adicionada.
    """
    global window
    window.append(img)


def ShowResult(pcento, metros):
    """
    Mostra um texto na imagem indicando o resultado
    obtido do processamento da imagem alvo.
    @param pcento Porcentagem de falhas na imagem.
    @param metros Metros de falhas na imagem.
    """
    global window    
    window.text("Falhas: %.2f metros (%d%%)" % (metros, pcento), (20, -50))


def SetHandles():
    """
    Configura o tratamento dos eventos disparados pelo
    núcleo de execução do programa.
    """
    Event.listen("load", ShowImage)
    Event.listen("segment", AddImage)
    Event.listen("process", AddImage)
    Event.listen("result", ShowResult)


def LoadImage(address):
    """
    Carrega uma imagem.
    @param address Endereço da imagem a ser carregada.
    @return Imagem Imagem carregada.
    """
    img = Image.load(address).resize(.3)

    Event.get("load").trigger(img)
    return img


def SegmentImage(image):
    """
    Executa a segmentação da imagem.
    @param image Imagem a ser segmentada.
    @return ComponentList Lista de componentes.
    """
    img = Segmentation().apply(image)
    comps = Component.load(img)
    
    if not img.check(comps):
        comps = Component.load(img)

    Event.get("segment").trigger(img)
    return comps


def FindLines(comps):
    """
    Encontra as linhas de plantação sobre a imagem.
    @param comps Componentes encontrados.
    @return LineList Linhas encontradas.
    """
    lines = Line.first(comps[1])
    lines.complete()
    lineimg = lines.display()

    Event.get("process").trigger(lineimg)
    return lines, lineimg


def SaveImage(original, image):
    """
    Salva a imagem resultante.
    @param original Endereço da imagem original.
    @param image Imagem a ser salva.
    """
    name = original.rsplit('.', 1)
    image.save("{0}.processed.{1}".format(*name))


def GetResult(lines, distance):
    """
    Exibe o resultado do processamento.
    @param lines Linhas encontradas na imagem.
    @param distance Distância entre as linhas de plantação.
    """
    porcento, metro = lines.error(distance)
    Event.get("result").trigger(porcento, metro)


def Process(imaddr, distance):
    """
    Núcleo de execução do processamento de imagens. Esta função é a grande
    responsável pelo cálculo do resultado desejado do programa.
    @param imaddr Endereço da imagem alvo.
    @param distance Distância entre linhas de plantação na imagem.
    """
    SetHandles()
    image = LoadImage(imaddr)
    comps = SegmentImage(image)
    lines, lineim = FindLines(comps)
    
    SaveImage(imaddr, lineim)
    GetResult(lines, distance)


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
        InitGUI()
    else:
        Process(args.image, args.dist)
