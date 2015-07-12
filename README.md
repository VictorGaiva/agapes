**A**utomatic **Gap** **E**valuation **S**ystem for Sugarcane Lines (AGapES - Sugar)
==========================
######Parceria Laboratório de Inteligência Artificial (LIA) e PSG - Tecnologia Aplicada
- Última atualização: **12/07/2015**.
- Versão: **0.2.1** (veja o log de alteração para maiores informações);

O AGapES - Suger foi desenvolvido por [Rodrigo Albuquerque de Oliveira Siqueira](http://lattes.cnpq.br/6242098395565903) e o [Edson Takashi Matsubara](facom.ufms.br/~edsontm/). Desenvolvido em [Python](https://www.python.org/) com objetivo de contabilizar a quantidade de falhas em uma plantação de cana-de-açúcar a partir de imagens aéreas obtidas através de aeronaves não-tripuladas, como VANTs.

Atualmente o sistema funciona apenas no Windows, por conta da biblioteca **ver o nome**. O sistema é proprietário, e para maiores detalhes entre em contato com a PSG. 

![alt text](http://www.psgtecnologiaaplicada.com.br/Theme/Images/visao_aerea_plantacao_cana.png)

-----------------------

###Como utilizar, passo a passo.
##### Bibliotecas necessárias:
Instalar nessa ordem:

1. [OpenCV](http://sourceforge.net/projects/opencvlibrary/files/opencv-win/3.0.0/opencv-3.0.0.exe/download)
2. [Python 2.7](https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi) (**32 bits**) 
3. Sub-biblioteca:
    - [NumPy](http://sourceforge.net/projects/numpy/files/NumPy/1.9.2/numpy-1.9.2-win32-superpack-python2.7.exe/download)
    - [SciPy](http://sourceforge.net/projects/scipy/files/scipy/0.14.0/scipy-0.14.0-win32-superpack-python2.7.exe/download) (**0.14.0**)
    - [wxPython](http://sourceforge.net/projects/wxpython/files/wxPython/3.0.2.0/wxPython3.0-win32-3.0.2.0-py27.exe/download)
    - [scikit-learn](http://sourceforge.net/projects/scikit-learn/files/scikit-learn-0.13.1.win32-py2.7.exe/download) (**0.13.1**)



### To do
#####Funções à serem implementadas.
- [ ] Eliminar as árvores na segmentação;
- [ ] Implementar versão para o terminal para facilitar os testes;
- [ ] Utilizar o Geoprocessamento para obter o tamanho da platação e melhorar o espaçamento entre as linhas;
- [ ] Criar o relatório;
- [ ] Salvar os dados;
- [ ] Criar um resultado parcial;
- [ ] Importar uma pasta;

#####Para correção.
- [ ] Reorganizar o core;
- [ ] Corrigir o zoomIn (está centralizando no centro da imagem);
- [ ] Mostrar o tamanho da plantação;
- [ ] ;

-----------------------
#### Update 0.2
- [X] Implementação de segmentação avulsa.

#### Update 0.1
- [X] Versão inicial do programa.