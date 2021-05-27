# Detección de Amenazas Ransomware en Redes Empresariales EDR

La sección de construcción del *dataset* proporciona información acerca de la limpieza y composición de este pero su ejecución es opcional ya que incluimos los *datasets* (dataset_binario.csv y dataset_suma.csv) listos para su utilización.

## Instalación de requisitos previa

<details><summary>Expandir</summary>

Antes de ejecutar ningún script, será necesario instalar una serie de dependencias de Python que se encuentran en el fichero requirements.txt
  
    pip install -r requirements.txt
  
</details>
  
## Construcción del *Dataset* (opcional)


<details><summary>Expandir</summary>

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

  
</details>
