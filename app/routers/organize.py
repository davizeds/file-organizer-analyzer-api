import shutil
from fastapi import HTTPException
import os
from pydantic import BaseModel
from app.core.dicionario import categorias
from app.services.categorizacao import categorizador
from fastapi import APIRouter

router=APIRouter()
class Dados(BaseModel):
    caminho:str

@router.post('/organize/preview')
def preview_de_organização(dados: Dados,):
    if not os.path.exists( dados.caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos_encontrados, total_arquivos = categorizador(dados.caminho)
    return {'status': 'sucesso', 'caminho': dados.caminho, 'total_arquivos': total_arquivos
        , 'categorias': arquivos_encontrados}

@router.post('/organize/run')
def criar_e_move_pasta(dados: Dados,):
    if not os.path.exists( dados.caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos_encontrados, total_arquivos = categorizador( dados.caminho )
    pastas_criadas = 0
    arquivos_movidos = 0
    categorias_afetadas = []
    for chave in arquivos_encontrados.keys():
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
