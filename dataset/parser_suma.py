import json
import csv
import os
import functools
import glob
import pandas as pd 

fichero = open("ransom_samples.json", "r", encoding="utf-8") #Fichero con info ransomware
contenido = fichero.read()
diccionario = json.loads(contenido)

apiDic = {} #Diccionario con APIs unicas

for item in diccionario: #para cada muestra del informe:
	apis = item["_source"]["behavior_apistats"] #extraer lista de apis
	for api in apis:
		#apis[api] accede al valor del par
		#api es la clave del par
		#Si la api no esta en el diccionario, se incluye
		if api not in apiDic:
			apiDic[api] = 0

fichero2 = open("benign_samples.json", "r", encoding="utf-8") #Fichero con info goodware
contenido2 = fichero2.read()
diccionario2 = json.loads(contenido2)

#Procdimiento identico al anterior
for item in diccionario2:
	apis = item["_source"]["behavior_apistats"]
	for api in apis:
		#apis[api] accede al valor del par
		#api contiene la clave del par
		if api not in apiDic:
			apiDic[api] = 0

#Recolección de apis en los ficheros de los analisis realizados en el laboratorio

ruta = './analyses/' #ruta donde se encuentran las carpetas de los informes

with os.scandir(ruta) as directorios:
	for directorio in directorios:
		rutaAux = ruta + directorio.name #rutaAux = ruta a la carpeta de un analisis concreto
		fichero3 = open(rutaAux+"/reports/report.json", "r") #Se abre el fichero report.json de la muestra

		contenido3 = fichero3.read()
		report = json.loads(contenido3)

		procesos = report["behavior"]["apistats"]
		for pid in procesos.keys(): #obtener pid de cada proceso
			for api in procesos[pid]: #acceder a cada api
				if api not in apiDic:
					apiDic[api] = 0

print("----------------------------------------------")
print("Número de características extraídas: ", len(apiDic.keys())) #Numero de APIs diferentes encontradas
print("----------------------------------------------")

#Creacion cabecera CSV
cabecera = list(apiDic.keys())
cabecera.insert(0, "label")
cabecera.insert(0, "id")

#FORMATO CABECERA:
# ID	LABEL	APIS

#CSV salida
csvObj = open("dataset_suma.csv", "w", encoding="utf-8")
csvWriter = csv.writer(csvObj, lineterminator="\n")
csvWriter.writerow(cabecera) #Escritura cabecera


#Rellenado CSV

for item in diccionario:
	aux = apiDic.copy() #Asignacion diccionario de APIs unicas
	resultado = []
	resultado.append(item["_source"]["signatures"]) #Campo ID --> signatures
	resultado.append(1) #porque es ransomware

	apis = item["_source"]["behavior_apistats"]
	for api in apis:
		#apis[api] accede al valor del par
		#api contiene la clave del par
		if api in aux:
			aux[api] = apis[api] #Numero de veces invocada
	resultado+=list(aux.values())
	csvWriter.writerow(resultado)

with os.scandir(ruta) as directorios:
	for directorio in directorios:
		rutaAux = ruta + directorio.name
		fichero3 = open(rutaAux+"/reports/report.json", "r")

		contenido3 = fichero3.read()
		report = json.loads(contenido3)

		aux = apiDic.copy() #Asignacion diccionario de APIs unicas
		resultado3 = []
		signatures = []
		signaturesRaw = report["signatures"]
		for firma in signaturesRaw:
			signatures.append(firma["name"])
		resultado3.append(signatures) #Campo ID --> signatures
		resultado3.append(1) #porque es ransomware


		procesos = report["behavior"]["apistats"]
		for pid in procesos.keys(): #obtener pid de cada proceso
			for api in procesos[pid]: #acceder a cada api
				if api in aux:
					aux[api] += procesos[pid][api]

		resultado3+=list(aux.values())
		csvWriter.writerow(resultado3)

for item in diccionario2:
	aux = apiDic.copy() #Asignacion diccionario de APIs unicas
	resultado2 = []
	resultado2.append(item["_source"]["signatures"]) #Campo ID --> signatures
	resultado2.append(0) #porque es ransomware

	apis = item["_source"]["behavior_apistats"]
	for api in apis:
		#apis[api] accede al valor del par
		#api contiene la clave del par
		if api in aux:
			aux[api] = apis[api]
	resultado2+=list(aux.values())
	csvWriter.writerow(resultado2)




csvObj.close()
dataset = pd.read_csv("dataset_suma.csv")
print("Tamaño inicial dataset: (1-ransomware, 0-goodware)")
print(dataset['label'].value_counts()) #Print cantidades iniciales
dataset2 = dataset.drop_duplicates(['id'])
print("----------------------------------------------")
print("Borrado de repetidos por signatures:")
print(dataset2['label'].value_counts()) #Print cantidades tras borrar repetidos por ID
dataset3 = dataset2.drop(['id'], axis=1) #Drop primera columna para preparar segunda limpieza
dataset4 = dataset3.drop_duplicates()
print("----------------------------------------------")
print("Borrado de repetidos por llamadas a API")
print(dataset4['label'].value_counts()) #Print cantidades tras segunda limpieza
dataset5 = dataset4[dataset4['label']==0].sample(n=3315) #3315 filas goodware aleatorias
dataset6 = dataset4[dataset4['label']==1]
dataset7 = pd.concat([dataset6, dataset5], axis=0)
print("----------------------------------------------")
print("Reparto final del dataset: ")
print(dataset7['label'].value_counts()) #Print reparto final
dataset7.to_csv("dataset_suma.csv")
