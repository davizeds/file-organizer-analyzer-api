from fastapi import FastAPI
from app.routers import files,largest,organize,recent,stats

app = FastAPI()


@app.get("/")
async def rota():
    return {"message": "rota criada com sucesso"}
app.include_router(files.router)
app.include_router(organize.router)
app.include_router(recent.router)
app.include_router(stats.router)
app.include_router(largest.router)
