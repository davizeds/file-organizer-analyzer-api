import string
from fastapi import FastAPI, HTTPException
import os
from typing import Optional
from pydantic import BaseModel



app = FastAPI()


@app.get("/")
async def rota():
    return {"message": "rota criada com sucesso"}



@app.get('/files')
def lista_arquivos(caminho,extensao: Optional[str] = None):
    if not os.path.exists(caminho):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos = os.listdir( caminho )
    lugares={'arquivos':[],'pastas':[]}
    for itens in arquivos:
        caminho_completo=os.path.join(caminho,itens)
        if os.path.isfile(caminho_completo):
            if extensao:
                if itens.endswith('.'+extensao) :
                    lugares['arquivos'].append(itens)
            else:
                lugares['arquivos'].append(itens)
        elif os.path.isdir(caminho_completo):
            lugares['pastas'].append(itens )
    return lugares

class Dados(BaseModel):
    caminho:str


@app.post('/organize')
def preview_de_organização(dados: Dados):
    if not os.path.exists( dados.caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos = os.listdir( dados.caminho )
    categorias = {
    'audios': ['mp3', 'wav', 'aac', 'flac', 'ogg', 'wma', 'm4a', 'aiff', 'alac', 'opus',
               'amr', 'mid', 'midi', 'ra', 'dsd', 'ape'],

    'videos': ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'mpeg', 'mpg', '3gp',
               'm4v', 'vob', 'ts', 'ogv', 'f4v'],

    'imagens': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'heic', 'svg',
                'raw', 'psd', 'ico','avif','jfif'],

    'executaveis': ['exe', 'msi', 'bat', 'cmd', 'sh', 'jar', 'apk', 'app', 'deb',
                    'rpm', 'bin'],

    'documentos': ['txt', 'doc', 'docx', 'odt', 'pdf', 'rtf', 'tex', 'log', 'md', 'csv',
                   'json', 'xml', 'yaml', 'yml','xlsx','xls','ppt','pptx','ods','odp'],

    'arquivos_compactados': ['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'iso', 'dmg'],

    'scripts': ['py', 'js', 'html', 'css', 'java', 'c', 'cpp', 'cs', 'rb', 'php', 'go',
                'rs', 'swift','htm']}
    arquivos_encontrados = {'audios': [], 'videos': [], 'imagens': [], 'executaveis': [], 'documentos': [],
                            'arquivos_compactados': [], 'scripts': []}
    total_arquivos =0
    for arc in  arquivos:
        if os.path.isfile( os.path.join( dados.caminho, arc ) ):
            total_arquivos += 1
            arquivo_separado = arc.split( sep='.' )
            extensao = arquivo_separado[-1].lower()
            if extensao in categorias['audios']:
                arquivos_encontrados['audios'].append(arc)

            elif extensao in categorias['videos']:
                arquivos_encontrados['videos'].append( arc )

            elif extensao in categorias['imagens']:
                arquivos_encontrados['imagens'].append( arc )

            elif extensao in categorias['executaveis']:
                arquivos_encontrados['executaveis'].append( arc )

            elif extensao in categorias['documentos']:
                arquivos_encontrados['documentos'].append( arc )

            elif extensao in categorias['arquivos_compactados']:
                arquivos_encontrados['arquivos_compactados'].append(arc )

            elif extensao in categorias['scripts']:
                arquivos_encontrados['scripts'].append( arc )
    return {'status':'sucesso','caminho':dados.caminho,'total_arquivos':total_arquivos
            ,'categorias':arquivos_encontrados}
