from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import science
import geojson

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return {
        'rutas': {
            'Casos confirmados acumulados por municipio': '/casos_municipios',
            'Sonora Casos Confirmados': '/casos_sonora'
        }
    }


# Casos confirmados acumulados por municipio
@app.get('/casos_municipios')
def casos_municipios():
    """
    Regresa un geojson con los casos confirmados y defunciones acumuladas por municipio
    """
    return geojson.geojson()

# Sonora Casos Confirmados
@app.get('/casos_sonora')
def casos_sonora():
    """
    Regresa casos confirmados acumulados por municipio
    """
    return science.casos_sonora()

@app.get('/mas_afectados/{afectados}')
def mas_afectados(afectados):
    """
    Regresa los estados mas afectados
    """
    return science.mas_afectados(afectados)