import string
from fastapi import FastAPI, HTTPException
import os
from typing import Optional



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
