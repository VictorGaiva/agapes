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
from segmentation import *
from component import *
from gui import InitGUI
from image import *
from event import *
from line import *
import __builtin__
import textwrap
import argparse
import os

__builtin__.__path__ = os.path.dirname(os.path.realpath(__file__))
__builtin__.__author__ = "Rodrigo Siqueira <rodriados@gmail.com>"
__builtin__.__appname__ = "PSG - Tecnologia Aplicada"
__builtin__.__version__ = "0.4"

# TODO:     Feedback de execução e de erros. Mostra ao usuário que
#           o programa está executando corretamente e os erros que
#           ocorreram.

# TODO:     Correlacionar a imagem da janela com a imagem original,
#           tornando mais fácil a localização da área visualizada
#           na imagem original.

# TODO:     Redimensionar imagem para um tamanho fixo, e não para
#           uma proporção da imagem original como está sendo feito.

# TODO:     Transformar equações utilizadas para funções paramétricas
#           permitindo, assim, aumentar o leque de curvas que podem
#           ser descritas.

# TODO:     Retirar a execução do programa diretamente do campo
#           de drag-n-drop.

# TODO:     Ao soltar uma imagem, exibí-la no campo de drag-n-drop
#           e permitir a edição da imagem diretamente desse campo.

# TODO:     Adicionar ferramentas de edição de imagem na barra
#           horizontal inferior da janela.

# TODO:     Criação de um instalador para que as dependências do
#           programa sejam automaticamente instaladas, sem intervenção
#           manual.
def ShowImage(img):
    """
    Prepara a janela para mostrar todos os passos de
    execução do algoritmo.
    @param Image img Primeira imagem a ser mostrada.
    """
    global window
    window = ImageWindow(__appname__, img)
    
def AddImage(img):
    """
    Adiciona uma imagem a ser exibida na janela.
    @param Image img Imagem a ser adicionada.
    """
    global window
    window.append(img)
    
def ShowResult(pcento, metros):
    """
    Mostra um texto na imagem indicando o resultado
    obtido do processamento da imagem alvo.
    @param float pcento Porcentagem de falhas na imagem.
    @param float metros Metros de falhas na imagem.
    """
    global window    
    window.text("Falhas: %.2f metros (%d%%)" % (metros, pcento), (20, -50))

def SetHandles():
    """
    Configura o tratamento dos eventos disparados pelo
    núcleo de execução do programa.
    """
    Event.load = ShowImage
    Event.segment = AddImage
    Event.process = AddImage
    Event.result = ShowResult

def LoadImage(address):
    """
    Carrega uma imagem.
    @param str address Endereço da imagem a ser carregada.
    @return Imagem Imagem carregada.
    """
    img = Image.load(address).resize(.3)
    Event.load.trigger(img)
    
    return img
    
def SegmentImage(image):
    """
    Executa a segmentação da imagem.
    @param Image Imagem a ser segmentada.
    @return ComponentList Lista de componentes.
    """
    img = Segmentation().apply(image)
    comps = Component.load(img)
    
    if not img.check(comps):
        comps = Component.load(img)
        
    Event.segment.trigger(img)
    return comps

def FindLines(comps):
    """
    Encontra as linhas de plantação sobre a imagem.
    @param ComponentList comps Componentes encontrados.
    @return LineList Linhas encontradas.
    """
    lines = Line.first(comps[1])
    lines.complete()
    
    lineimg = lines.display()
    Event.process.trigger(lineimg)
    
    return lines, lineimg

def SaveImage(original, image):
    """
    Salva a imagem resultante.
    @param str original Endereço da imagem original.
    @param Imagem image Imagem a ser salva.
    """
    name = original.rsplit('.', 1)
    image.save("{0}.processed.{1}".format(*name))

def GetResult(lines, distance):
    """
    Exibe o resultado do processamento.
    @param LineList lines Linhas encontradas na imagem.
    @param float distance Distância entre as linhas de plantação.
    """
    porcento, metro = lines.error(distance)
    Event.result.trigger(porcento, metro)

def Process(imaddr, distance):
    """
    Núcleo de execução do processamento de imagens. Esta
    função é a grande responsável pelo cálculo do resultado
    desejado do programa.
    @param str imgaddr Endereço da imagem alvo.
    @param float distance Distância entre linhas de plantação na imagem.
    """
    SetHandles()
    image = LoadImage(imaddr)
    comps = SegmentImage(image)
    lines, lineim = FindLines(comps)
    
    SaveImage(imaddr, lineim)
    GetResult(lines, distance)

if __name__ == '__main__':
    
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
        InitGUI(Process)
    else:
        Process(args.image, args.dist)
    