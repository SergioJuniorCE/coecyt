import pandas as pd
import os
from urllib.request import urlopen
from zipfile import ZipFile
from datetime import datetime, timedelta, date

from constantes import *


def casos_municipios():
    data = pd.read_csv(f'datos/{filename_sonora()}')
    json = {}
    for i in range(1, 72 + 1):
        positivo = len(data[(data.RESULTADO_LAB == 1)
                       & (data['MUNICIPIO_RES'] == i)])
        defunciones = len(
            data[(data.FECHA_DEF != '9999-99-99') & (data['MUNICIPIO_RES'] == i)])
        json[i] = {
            'NAME': d_municipio[i],
            'POSITIVOS': positivo,
            'DEFUNCIONES': defunciones
        }
    return json


def casos_sonora():
    # Reading file
    data = pd.read_csv(f'datos/{filename_sonora()}')
    # Filtrando positivos
    casos = data[(data.RESULTADO_LAB == 1)]

    yesterday = date.today() - timedelta(days=1)
    datelist = pd.date_range(start='2020-01-20', end=yesterday).tolist()
    jason = {}
    for i in range(len(casos)-1):
        try:
            fecha = str(datelist[i]).split(' ')[0]
            caso = data[data.FECHA_INGRESO == fecha]

            confirmado = len(caso[(caso.RESULTADO_LAB == 1)])
            sospechosos = len(caso[(caso.CLASIFICACION_FINAL == 6)])
            negativos = len(caso[(caso.RESULTADO_LAB == 2)])
            defunciones = len(caso[(caso.FECHA_DEF != '9999-99-99')])

            jason[fecha] = {
                "CONFIRMADOS": confirmado,
                "SOSPECHOSOS": sospechosos,
                "NEGATIVOS": negativos,
                "DEFUNCIONES": defunciones
            }
        except IndexError:
            pass
    return jason


def filename_sonora():
    if os.path.exists(f'datos/{get_fecha()}COVID19SONORA.csv'):
                return f'{get_fecha()}COVID19SONORA.csv'
    dias = 1
    while True:
        if os.path.exists(f'datos/{get_fecha(delta=dias)}COVID19SONORA.csv'):
            return f'{get_fecha(delta=dias)}COVID19SONORA.csv'
        elif dias == 1000:
          raise Exception("No se encontro ningun archivo en mas de 1000 dias")  
        else:
            dias += 1


def filename_mexico():
    if os.path.exists(f'datos/{get_fecha()}COVID19MEXICO.csv'):
        return f'{get_fecha()}COVID19MEXICO.csv'
    return f'{get_fecha(delta=1)}COVID19MEXICO.csv'


def get_fecha(delta: int = 0):
    """
    Retorna la fecha en formato YYMMDD
    """
    if delta != 0:
        date = datetime.now() - timedelta(days=delta)
        return date.strftime('%y%m%d')
    return datetime.now().strftime('%y%m%d')


def filtrar(estado: int = 26):
    """
    Filtra todos los casos de personas que residen en Sonora y 
    crea un archivo csv con los datos.
    """
    # Lee archivo de descargas
    data = pd.read_csv(f'downloads/{filename_mexico()}')
    # Filtra los datos
    data = data[data['ENTIDAD_RES'] == estado]

    # Guarda los datos filtrados en un nuevo csv
    data.to_csv(f'datos/{filename_sonora()}')


def filtrar_municipios():
    sonora = {}
    sonora['SONORA'] = casos('ENTIDAD_RES', 26)
    fun_start = datetime.now()
    for i in range(1, 72 + 1):
        start = datetime.now()
        sonora[d_municipio[i]] = casos('MUNICIPIO_RES', i)
        print(d_municipio[i], datetime.now()-start)
    print('total', datetime.now()-fun_start)
    return sonora


def descargar_datos():
    # Si ya existe
    if os.path.exists(f'downloads/{filename_mexico()}'):
        return 0
    filename = 'datos_abiertos_covid19.zip'
    url = 'http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip'
    # Lo intenta descargar
    try:
        print('downloading...')
        r = urlopen(url)
        tempzip = open(f'downloads/{filename}', "wb")
        tempzip.write(r.read())
        tempzip.close()
        zf = ZipFile(f'downloads/{filename}')
        zf.extractall(path='downloads')
        zf.close()
        return 1
    # Si falla
    except Exception:
        return -1
