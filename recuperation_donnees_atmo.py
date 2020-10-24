import requests # pour l'installer executer la commande : python -m pip install requests
from datetime import datetime as time
from datetime import date
import datetime
import urllib
from pprint import pprint
import webbrowser, os, sys
import urllib
#import schedule


url1 = 'file:///Users/zacharietaieb/Documents/test/index.html'

url = 'https://api.openweathermap.org/data/2.5/weather?q=Lille,fr&appid=516e6363be8c13af250a48a49670e80e&units=metric'
res = requests.get(url)
data2 = res.json()

def requete(): #requete pour sur l'api d'ATMO
    v = time.today()
    today = date(v.year,v.month,v.day)# recuperation de la date du jour format Y-M-D
    # dictionnaire contenant les parametres de la requete
    payload = {"where" : "code_zone = '59350' AND date_ech >= TIMESTAMP '{}'".format(today), "outFields" : "date_ech,valeur,qualif,couleur", "outSR" : "4326",  "f" : "json"}
    param = urllib.parse.urlencode(payload, safe='='+',', quote_via=urllib.parse.quote) # encodage du dictionnaire des parametres
    r = requests.get('https://services8.arcgis.com/rxZzohbySMKHTNcy/arcgis/rest/services/ind_hdf_agglo/FeatureServer/0/query', params=param) # requete
    data1 = r.json()



    return releve(r) # appel de la fonction releve

#schedule.every(30).minutes.do(requete)  
def fichier(data,r,couleur,quality,temp,meteo): # fonction permettant d'enregistrer les données recuperées dans un fichier json (optionel)
    file = open('data.js','w')
    file.write("data='" +r.text+"';\n"
               +"couleur='" +str(couleur)+"';\n"
               +"quality='" +str(quality)+"';\n"
               +"temp='" +str(round(temp))+"';\n"
               +"meteo='" +str(meteo)+"';\n")
    file.close()
    
#schedule.every(30).minutes.do(fichier)

def releve(r): # recuperation des informations du releve
    data1 = r.json() # dictionnaire des données format json
    
    features = data1["features"][0]   #0 est l'indice du dernier releve
    attributes = features['attributes'] # toutes les informations du releve
    couleur = attributes["couleur"]
    quality = attributes["qualif"] # exemple de recuperation de la qualite de l'air du releve
    
    temp = data2['main']['temp']
    meteo = data2['weather'][0]['description']
    
    print("La temperature est de " + str(temp) + " degres celsius")
    print("Le ciel est de " + str(meteo))

    fichier(data1,r,couleur,quality,temp,meteo)   
    return couleur, quality, temp, meteo # renvoi de la donnee qui nous intéresse

#schedule.every(30).minutes.do(releve)


if __name__ == "__main__":
    requete()
    webbrowser.open(url1, new=2)  # open in new tab



