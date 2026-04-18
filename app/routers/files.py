from fastapi import APIRouter
from fastapi import  HTTPException
import os
from typing import Optional
from datetime import datetime


router=APIRouter()

@router.get('/files')
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
            if tamanho_minimo is not None and tamanho<tamanho_minimo:
                pode_entrar = False
            if pode_entrar:
                lugares['arquivos'].append( itens )
        elif os.path.isdir(caminho_completo):
            lugares['pastas'].append(itens )
    return {'status': 'sucesso', 'caminho': caminho,'arquivos': lugares['arquivos'],'pastas':lugares['pastas']}
