# Detección de Amenazas Ransomware en Redes Empresariales EDR

#### Trabajo de Fin de Grado curso 2020-2021 realizado por Gonzalo Figueroa del Val, Marina López Osorio y Gonzalo Fernández Megia en los Grados en Ingeniería Informática, Ingeniería del Software e Ingeniería de Computadores.

#### Manual de uso del sistema propuesto

La primera sección incluye los requisitos necesarios para el correcto funcionamiento del código. La sección de construcción del *dataset* proporciona información acerca de la limpieza y composición de este pero su ejecución es opcional ya que incluimos los *datasets* (dataset_binario.csv y dataset_suma.csv) en [esta carpeta](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/dataset) listos para su utilización. Por último, la sección de ejecución del modelo proporciona información del uso del código del modelo construido y la generación de resultados.

La sección de construcción del *dataset* proporciona información acerca de la limpieza y composición de este pero su ejecución es opcional ya que incluimos los *datasets* (dataset_binario.csv y dataset_suma.csv) listos para su utilización.

## Instalación de requisitos previa

<details><summary>Expandir</summary>

Antes de ejecutar ningún script, será necesario instalar una serie de dependencias de Python que se encuentran en el fichero requirements.txt
  
    pip install -r requirements.txt
  
</details>
  
## Construcción del *Dataset* (opcional)


<details><summary>Expandir</summary>

El desarrollo de los *datasets* se ha realizado en un equipo con sistema operativo Linux con distribución Ubuntu 18.0.5 LTS. Antes de ejecutar ningún script será necesario extraer todos los informes del fichero [data](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/dataset/data.zip)

Para obtener el [dataset_binario](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/dataset/dataset_binario.csv) es necesario ejecutar el script [parser_binario.py](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/dataset/parser_binario.py):

El desarrollo de los *datasets* se ha realizado en un equipo con sistema operativo Linux con distribución Ubuntu 18.0.5 LTS.  

Para obtener el [dataset_binario](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/Dataset/dataset_binario.csv) es necesario ejecutar el script [parser_binario.py](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/Dataset/parser_binario.py):
  
    python3 parser_binario.py
  
La salida obtenida por consola será la siguiente:
  
    ----------------------------------------------
    Número de características extraídas:  302
    ----------------------------------------------
    Tamaño inicial dataset: (1-ransomware, 0-goodware)
    0    10896
    1     5456
    Name: label, dtype: int64
    ----------------------------------------------
    Borrado de repetidos por signatures:
    0    9648
    1    5416
    Name: label, dtype: int64
    ----------------------------------------------
    Borrado de repetidos por llamadas a API
    1    1596
    0     357
    Name: label, dtype: int64
    ----------------------------------------------
    Reparto final del dataset: 
    1    357
    0    357
    Name: label, dtype: int64
  

Para obtener el [dataset_suma](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/dataset/dataset_suma.csv) es necesario ejecutar el script [parser_suma.py](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/dataset/parser_suma.py):

Para obtener el [dataset_suma](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/Dataset/dataset_suma.csv) es necesario ejecutar el script [parser_suma.py](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/Dataset/parser_suma.py):
  
    python3 parser_suma.py
  
La salida obtenida por consola será la siguiente:
  
    ----------------------------------------------
    Número de características extraídas:  302
    ----------------------------------------------
    Tamaño inicial dataset: (1-ransomware, 0-goodware)
    0    10896
    1     5456
    Name: label, dtype: int64
    ----------------------------------------------
    Borrado de repetidos por signatures:
    0    9648
    1    5416
    Name: label, dtype: int64
    ----------------------------------------------
    Borrado de repetidos por llamadas a API
    0    6507
    1    3315
    Name: label, dtype: int64
    ----------------------------------------------
    Reparto final del dataset: 
    1    3315
    0    3315
    Name: label, dtype: int64
  
Con esto, los dos *datasets* estarán preparados.  

</details>

## Ejecución del modelo de *Machine Learning*

<details><summary>Expandir</summary>

La ejecución del [modelo](https://gitlab.fdi.ucm.es/marina.lopez/tfg-ransomware-20-21/-/blob/master/modelo.py) se ha llevado a cabo en una máquina virtual Kali Linux 2020.3 utilizando el software de virtualización VirtualBox y se ha hecho uso de la versión 3.9.2 de Python.

El modelo realizará pruebas y generará gráficos de barras para diferentes métricas con los siguientes algoritmos:
- Máquina de Soporte Vectorial (*Support Vector Machine* - SVM) con kernel lineal. 
- Máquina de Soporte Vectorial (*Support Vector Machine* - SVM) con kernal RBF.
- Árboles de decisión (*Decission Tree* - DT).
- Regresión Logística (*Logistic Regression* - LR).
- Bayesiano ingenuo (*Naive Bayes* - NB).
- K vecinos más cercanos (*K-Neighbors* - KNN).
- Bosques Aleatorios (Random Forest - RF) con profundidad máxima 10.

Las métricas escogidas para la generación de gráficos han sido:
- Precisión
- Exactitud
- Tasa de error
- F1-score
- Recall
- Precisión de k-fold
- Exactitud de k-fold
- F1-score de k-fold
- Recall de k-fold

En el código se encuentra por defecto la configuración siguiente:

- *Dataset*: dataset_binario.csv
- Distribución del *dataset*: 70% entrenamiento y 30% prueba.
- Validación cruzada: k = 10
- Mecanismo de escalada: Ninguno
- Gráficas: gráficas de barras de cada una de las métricas analizadas.

Para cambiar el *dataset* en el que se realizan las pruebas será neceserio editar la línea 23 script. Las opciones posibles son `dataset_binario.csv` y `dataset_suma.csv`

```python
dataset = pd.read_csv("dataset/dataset_binario.csv")
```

Cuando se quiera hacer uso del *dataset* `dataset_suma.csv` es necesario realizar un escalado de los datos, para ello habrá que descomentar las líneas 75-77 del código que llevan acabo el escalado con la técnica *Standard*: 

```python
sc = StandardScaler() #StandardScaler estandariza los valores de X restando la media y luego escalando a la varianza de la unidad.
X_train = sc.fit_transform(X_train)
X_validation = sc.transform(X_validation)
```

Si se descomentan las líneas 122-139 del código se realizará la comparación de las técnicas de escalado *Standard* y *MinMax* y se generará la consecuente gráfica (sólo para `dataset_suma.csv`):

```python
sc = MinMaxScaler() #MinMaxScaler pone los valores de X entre 0 y 1
X_train = sc.fit_transform(X_train)
X_validation = sc.transform(X_validation) 

for name,model in models:
    print("------",name,"------")
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    graficaPrecMaxMin[name] = metrics.accuracy_score(Y_validation, predictions)

fig, ax9 = pyplot.subplots()
print(names)
print(graficaPrec.values())
ax.plot(names,  graficaPrec.values(), color = 'tab:purple',label = 'Escalado Standard')
ax.plot(names,  graficaPrecMaxMin.values(), color = 'tab:green', label = 'Escalado MinMax')
ax.set_title('Comparación del escalado de los datos')
ax.legend(loc='lower left')
pyplot.savefig("ComparacionEscalado.jpg")
```

Para realizar la comparación entre la precisión ofrecida por la distribución 70:30 y por la distribución 80:20 (entrenamiento:prueba) y obtener la gráfica correspondiente es necesario descomentar el código incluido en las líneas 172-186:
        
```python
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.2, random_state=1) #20% test, 80% training  
for name,model in models:
    print("------",name,"------")
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    graficaPrec8020[name] = metrics.accuracy_score(Y_validation, predictions)

fig, ax11 = pyplot.subplots()
print(names)
print(graficaPrec.values())
ax.plot(names,  graficaPrec.values(), color = 'tab:purple',label = '70:30')
ax.plot(names,  graficaPrec8020.values(), color = 'tab:green', label = '80:20')
ax.set_title('Comparación de la distribucion del detaset')
ax.legend(loc='lower left')
pyplot.savefig("ComparacionDistribucion.jpg")
```

Si se quieren obtener las gráficas relativas a las pruebas de validación cruzada con diferentes valores para la variable 'k' será necesario descomentar las líneas 144-167 del código:

```python
-+-+-+-+-
k = 5
-+-+-+-+-
for name, model in models:
    kfold = StratifiedKFold(n_splits=5, random_state=1, shuffle=True)
    accuracy = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    graficaPrecKF5[name] = accuracy.mean() 
-+-+-+-+-
k = 15
-+-+-+-+-
for name, model in models:
    kfold = StratifiedKFold(n_splits=15, random_state=1, shuffle=True)
    accuracy = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    graficaPrecKF15[name] = accuracy.mean() 

fig, ax10 = pyplot.subplots()
print(names)
print(graficaPrec.values())
ax.plot(names,  graficaPrec.values(), color = 'tab:purple',label = 'K=10')
ax.plot(names,  graficaPrecK15.values(), color = 'tab:green', label = 'K=15')
ax.plot(names,  graficaPrecK5.values(), color = 'tab:red', label = 'K=5')
ax.set_title('Comparación de la validacion cruzada')
ax.legend(loc='lower left')
pyplot.savefig("ComparacionKFold.jpg")
```

</details>
