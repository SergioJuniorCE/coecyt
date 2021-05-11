from urllib.request import AbstractDigestAuthHandler
from science import *
from geojson import *
import json
import csv
from constantes import *

filename = 'Casos_Diarios_Municipio_Confirmados_20210509.csv'

fields = []
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
      
    # extracting field names through first row
    fields = next(csvreader)
  
    # extracting each data row one by one

    rows = [row for row in csvreader if row[0][:2]=='26']
    ceseve = []
    for i, row in enumerate(rows):
        if row[0][:2]=='26':
            ceseve.append(row)
with open('max.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(fields)
    write.writerows(rows)
df = pd.read_csv(filename)
df.to_json('max.json')