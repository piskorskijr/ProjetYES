import time
import requests
import json
import datetime
import signal
import sys
import schedule
import math
from math import*
import datetime
import MySQLdb
import random
from time import sleep

#Connexion a la base de donnees SQL 
db = MySQLdb.connect(host="localhost", user="root", passwd="pass", db="TestProjetYES")
curs= db.cursor()
#Heure actuelle
tday = datetime.date.today()
url = 'https://services8.arcgis.com/rxZzohbySMKHTNcy/arcgis/rest/services/ind_hdf_agglo/FeatureServer/0/query?where=code_zone%20=%20%2759350%27%20AND%20date_ech%20%3E=%20TIMESTAMP%20%27'+str(tday.year)+'-'+str(tday.month)+'-'+str(tday.day)+ '%27&outFields=date_ech,valeur,qualif,couleur&outSR=4326&f=json'
url2 = 'https://meteo-data.com/59000.json' 

#Recuperation donnees JSON ATMO et envoi toutes les heures
def job():
	json_data=requests.get(url).json()
	valeur_air = json_data['features'][0]['attributes']['valeur']
	couleur_air = json_data['features'][0]['attributes']['couleur']
	qualif_air = json_data['features'][0]['attributes']['qualif']
	json_data=requests.get(url2).json()
	temperature = json_data['temp']
	print("La temperature est de : " + str(temperature) + " degres celsius")
	print("La valeur de qualite d air est de : " + str(valeur_air))
	print("Aujourd hui l air est :  " + str(qualif_air))
	print("La couleur de la qualite d air est : " + str(couleur_air))
	curs.execute("UPDATE comptage SET  couleur_air='%s', valeur_air='%s', qualif_air='%s', temperature_air ='%s' WHERE (id=1)" % (couleur_air,valeur_air,qualif_air,temperature))
	db.commit()
schedule.every(2).seconds.do(job)

while True :
  schedule.run_pending()
  time.sleep(1)
