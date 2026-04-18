from app.dicionario import categorias
from fastapi import FastAPI, HTTPException
import os
from typing import Optional
from pydantic import BaseModel
import shutil
from app.categorizacao import categorizador
from datetime import datetime


app = FastAPI()


@app.get("/")
async def rota():
    return {"message": "rota criada com sucesso"}



@app.get('/files')
def lista_arquivos(caminho:str,extensao: Optional[str] = None, nome: Optional[str] = None,dia: Optional[int] = None,
                   mes: Optional[int] = None,ano: Optional[int] = None,tamanho_minimo: Optional[int] = None):
    if not os.path.exists(caminho):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos = os.listdir( caminho )
    lugares={'arquivos':[],'pastas':[]}
    for itens in arquivos:
        caminho_completo=os.path.join(caminho,itens)
        if os.path.isfile( caminho_completo ):
            pode_entrar = True
            if nome and nome.lower() not in itens.lower():
                    pode_entrar = False
            if extensao and not itens.endswith('.'+extensao):
                    pode_entrar = False
            data_modificada = os.path.getmtime( caminho_completo )
            data_convertida = datetime.fromtimestamp( data_modificada )
            if dia and dia !=  data_convertida.day:
                pode_entrar = False
            if mes and mes != data_convertida.month:
                pode_entrar = False
            if ano and ano !=  data_convertida.year:
                pode_entrar = False
            tamanho=os.path.getsize(caminho_completo)
            if tamanho_minimo and tamanho_minimo>tamanho:
                pode_entrar = False
            if pode_entrar:
                lugares['arquivos'].append( itens )
        elif os.path.isdir(caminho_completo):
            lugares['pastas'].append(itens )
    return {'status': 'sucesso', 'caminho': caminho,'arquivos': lugares['arquivos'],'pastas':lugares['pastas']}




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
def stats(caminho:str):
    if not os.path.exists( caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos = os.listdir( caminho )
    nmr_pastas=0
    for diretorio in arquivos:
        caminho_completo = os.path.join( caminho, diretorio )
        if os.path.isdir(caminho_completo):
            nmr_pastas +=1
    arquivos_encontrados, total_arquivos = categorizador(  caminho )
    total_por_categoria = {}
    for chave, valor in arquivos_encontrados.items():
        total_por_categoria[chave] = len( valor )
    return {'status':'sucesso','total_arquivos':total_arquivos,'caminho': caminho,
            'total_de_pastas':nmr_pastas,'total_por_categoria':total_por_categoria}

@app.get('/recent')
def list_recen_arquivos(caminho:str, limite:Optional[int] = None):
    if not os.path.exists( caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos = os.listdir( caminho )
    lista_arquivos = []
    total_encontrado=0
    for arc in arquivos:
         caminho_completo = os.path.join( caminho,arc )
         if os.path.isfile(caminho_completo):
             data_modificada=os.path.getmtime(caminho_completo)
             data_convertida = datetime.fromtimestamp(  data_modificada )
             arquivo_info = {
                'nome':arc,
                'data': data_convertida,
              }
             total_encontrado += 1
             lista_arquivos.append(arquivo_info)
    lista_ordenada_reversa = sorted(lista_arquivos, key=lambda x: x['data'], reverse=True)
    if limite:
        lista_ordenada_reversa =  lista_ordenada_reversa[:limite]
    return {'status': 'sucesso',  'caminho': caminho,
            'lista_de_arquivos':  lista_ordenada_reversa,'total_encontrado': total_encontrado}
