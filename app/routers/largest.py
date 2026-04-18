from fastapi import  HTTPException
import os
from typing import Optional
from fastapi import APIRouter

router=APIRouter()

@router.get('/largest')
def ordena_maior(caminho:str,limite:Optional[int] = None):
    if not os.path.exists( caminho ):
        raise HTTPException( status_code=404, detail='esse caminho nao existe' )
    arquivos=os.listdir( caminho )
    guarda_arquivos= []
    total_encontrado = 0
    for itens in arquivos:
        caminho_completo = os.path.join( caminho,itens )
        if os.path.isfile( caminho_completo ):
            tamanho = os.path.getsize( caminho_completo )
            arquivo_info = {
                'nome': itens,
                'tamanho': tamanho,
            }
            guarda_arquivos.append( arquivo_info )
            total_encontrado += 1
    lista_ordenada_reversa = sorted( guarda_arquivos, key=lambda x: x['tamanho'], reverse=True )
    if limite is not None: lista_ordenada_reversa = lista_ordenada_reversa[:limite]
    return {'status': 'sucesso', 'caminho': caminho,
                    'lista_de_arquivos': lista_ordenada_reversa, 'total_encontrado': total_encontrado}
