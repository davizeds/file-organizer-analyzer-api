from fastapi import  HTTPException
import os
from typing import Optional
from datetime import datetime
from fastapi import APIRouter

router=APIRouter()


@router.get('/recent')
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
