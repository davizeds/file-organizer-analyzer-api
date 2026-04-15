from app.dicionario import categorias
from fastapi import FastAPI, HTTPException
import os
from typing import Optional
from pydantic import BaseModel
import shutil
from categorizacao import categorizador


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

@app.post('/organize/preview')
def preview_de_organização(dados: Dados,):
    if not os.path.exists( dados.caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos_encontrados, total_arquivos = categorizador(dados.caminho)
    return {'status': 'sucesso', 'caminho': dados.caminho, 'total_arquivos': total_arquivos
        , 'categorias': arquivos_encontrados}


@app.post('/organize/run')
def criar_e_move_pasta(dados: Dados,):
    if not os.path.exists( dados.caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos_encontrados, total_arquivos = categorizador( dados.caminho )
    pastas_criadas = 0
    arquivos_movidos = 0
    categorias_afetadas = []
    for chave in categorias.keys():
        if not os.path.exists( os.path.join( dados.caminho, chave ) ):
            os.mkdir( os.path.join( dados.caminho, chave ) )
            pastas_criadas += 1
    for chave, valor in arquivos_encontrados.items():
        for arc in valor:
            if not os.path.exists( os.path.join( dados.caminho, chave, arc ) ):
                shutil.move( os.path.join( dados.caminho, arc ), os.path.join( dados.caminho, chave, arc ) )
                arquivos_movidos += 1
    for chave,valor in arquivos_encontrados.items():
        if valor:
            categorias_afetadas.append(chave)
    return {'status':'sucesso','caminho':dados.caminho,'total_arquivos':total_arquivos,'pastas_criadas': pastas_criadas,
            'arquivos_movidos': arquivos_movidos, 'categorias_afetadas': categorias_afetadas }

@app.get('/stats')
def stats(dados: Dados):
    if not os.path.exists( dados.caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos = os.listdir( dados.caminho )
    nmr_pastas=0
    for diretorio in arquivos:
        caminho_completo = os.path.join( dados.caminho, diretorio )
        if os.path.isdir(caminho_completo):
            nmr_pastas +=1
    arquivos_encontrados, total_arquivos = categorizador( dados.caminho )
    total_por_categoria = {}
    for chave, valor in arquivos_encontrados.items():
        total_por_categoria[chave] = len( valor )
    return {'status':'sucesso','total_arquivos':total_arquivos,'caminho':dados.caminho,
            'total_de_pastas':nmr_pastas,'total_por_categoria':total_por_categoria}
