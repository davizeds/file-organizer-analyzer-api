from fastapi import  HTTPException
import os
from app.services.categorizacao import categorizador
from fastapi import APIRouter

router=APIRouter()

@router.get('/stats')
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
