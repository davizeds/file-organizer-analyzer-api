from fastapi import HTTPException
import os
from pydantic import BaseModel
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
