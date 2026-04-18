import os
from app.dicionario import categorias





def categorizador(caminho):
    arquivos_encontrados = {'audios': [], 'videos': [], 'imagens': [], 'executaveis': [], 'documentos': [],
                            'arquivos_compactados': [], 'scripts': [],'outros': []}
    arquivos = os.listdir( caminho )
    total_arquivos=0
    for arc in arquivos:
        if os.path.isfile( os.path.join(caminho, arc ) ):
            total_arquivos += 1
            arquivo_separado = arc.split( sep='.' )
            extensao = arquivo_separado[-1].lower()
            if extensao in categorias['audios']:
                arquivos_encontrados['audios'].append( arc )

            elif extensao in categorias['videos']:
                arquivos_encontrados['videos'].append( arc )

            elif extensao in categorias['imagens']:
                arquivos_encontrados['imagens'].append( arc )

            elif extensao in categorias['executaveis']:
                arquivos_encontrados['executaveis'].append( arc )

            elif extensao in categorias['documentos']:
                arquivos_encontrados['documentos'].append( arc )

            elif extensao in categorias['arquivos_compactados']:
                arquivos_encontrados['arquivos_compactados'].append( arc )

            elif extensao in categorias['scripts']:
                arquivos_encontrados['scripts'].append( arc )

            else:
                arquivos_encontrados['outros'].append( arc )
    return  arquivos_encontrados, total_arquivos
