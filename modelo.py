#!/usr/bin/env python
# coding: utf-8

# Load libraries
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

dataset = pd.read_csv("dataset/dataset_binario.csv")
dataset = dataset.sample(frac=1) #desordena las filas

#para comprobar el shuffle
dataset.to_csv("dataset_test.csv", index=False, sep=',') 


array = dataset.values
X = array[:,2:] #Para entrenar el modelo se utilizan todas las apis, desde la columna 2 hasta el final
y = array[:,1] #Para la prediccion se utiliza el label, ubicado en la columna 1

X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.3, random_state=1) #30% test, 70% training  

#---------------------------
#DICCIONARIOS PARA LOS DATOS DE LAS GRAFICAS


results = []
graficaPrec = {}
graficaPrecMaxMin = {}
graficaPrec8020 = {}
graficaExac = {}
graficaRecall = {}
graficas = {}
graficaF1 = {}
graficaPrecKF = {}
graficaExacKF = {}
graficaRecallKF = {}
graficaF1KF = {}
graficaPrecKF5 = {}
graficaPrecKF15 = {}


#-------------------------

models = []
names = []


#-------------------------
#Algoritmos añadidos al modelo

models.append(('SVM Lin.', SVC(kernel='linear', gamma='auto'))) 
models.append(('SVM RBF 1', SVC(gamma='auto', C=1.0))) 
models.append(('DT', DecisionTreeClassifier()))
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('NB', GaussianNB()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('RF',RandomForestClassifier(max_depth=10, random_state=0)))


#Cuando se usa el dataset suma se debe descomentar para el escalado de los datos:
'''
sc = StandardScaler() #StandardScaler estandariza los valores de X restando la media y luego escalando a la varianza de la unidad.
X_train = sc.fit_transform(X_train)
X_validation = sc.transform(X_validation)
'''

for name,model in models:
    print("------",name,"------")
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    #---METRICAS--#
    print(name,"Accuracy:",metrics.accuracy_score(Y_validation, predictions))
    graficaPrec[name] = metrics.accuracy_score(Y_validation, predictions)
    names.append(name)	
    print(name,"Precision:",metrics.precision_score(Y_validation, predictions))
    graficaExac[name] = metrics.precision_score(Y_validation, predictions)
    print(name,"F1 score:",metrics.f1_score(Y_validation, predictions))
    graficaF1[name] = metrics.f1_score(Y_validation, predictions)
    print(name,"Recall:",metrics.recall_score(Y_validation, predictions))
    graficaRecall[name] = metrics.recall_score(Y_validation, predictions)
    print(name,"Confusion Matrix:")
    print(metrics.confusion_matrix(Y_validation, predictions))
    matrix = metrics.confusion_matrix(Y_validation, predictions)
    graficas[name] = (matrix[0][1] + matrix[1][0])/6630
    print(metrics.classification_report(Y_validation, predictions))

    #Cross Validation k-fold, k = 10
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    accuracy = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    precision = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='precision')
    recall = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='recall')
    f1 = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='f1')
    results.append(accuracy) 
    print('Cross-validation %s:' % (name))
    print('%f accuracy with a deviation of %f' % (accuracy.mean(), accuracy.std()))
    graficaPrecKF[name] = accuracy.mean() 
    print('%f precision with a deviation of %f' % (precision.mean(), precision.std()))
    graficaExacKF[name] = precision.mean()
    print('%f recall with a deviation of %f' % (recall.mean(), recall.std()))
    graficaRecallKF[name] = recall.mean()
    print('%f f1 score with a deviation of %f' % (f1.mean(), f1.std()))
    graficaF1KF[name] = f1.mean()
    print('\n')

#----------------------
#Descomentar lo siguiente para obtener la grafica de comparacion entre los metodos de escalado
'''
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
'''
#--------------------------
#Descomentar lo siguiente para obtener la grafica de comparacion entre los diferentes valores de k para la validacion cruzada 
'''
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
'''
#------------------------
#Descomentar lo siguiente para obtener la grafica de comparacion con diferentes distribuciones test-entrenamiento del dataset
'''
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
'''

#------------------------
#Graficas para los algoritmos

fig,ax = pyplot.subplots()
ax.bar(names, graficaPrec.values())
ax.set_title('Precision de los algoritmos')
pyplot.savefig("PrecisionSuma3.jpg")

fig,ax1 = pyplot.subplots()
ax1.bar(names, graficas.values())
ax1.set_title('Tasa de error de los algoritmos')
pyplot.savefig("TasaErrorSuma3.jpg")

fig,ax2 = pyplot.subplots()
ax2.bar(names, graficaExac.values())
ax2.set_title('Exactitud de los algoritmos')
pyplot.savefig("ExactitudSuma3.jpg")

fid,ax3 = pyplot.subplots()
ax3.bar(names, graficaF1.values())
ax3.set_title('F1-score de los algoritmos')
pyplot.savefig("F1Suma3.jpg")

fig,ax4 = pyplot.subplots()
ax4.bar(names, graficaRecall.values())
ax4.set_title('Recall de los algoritmos')
pyplot.savefig("RecallSuma3.jpg")

fig,ax5 = pyplot.subplots()
ax5.bar(names, graficaPrecKF.values())
ax5.set_title('Precision de K-Fold')
pyplot.savefig("PrecisionSumaKF3.jpg")

fig,ax6 = pyplot.subplots()
ax6.bar(names, graficaExacKF.values())
ax6.set_title('Exactitud de K-Fold')
pyplot.savefig("ExactitudSumaKF3.jpg")

fig,ax7 = pyplot.subplots()
ax7.bar(names, graficaF1KF.values())
ax7.set_title('F1-score de K-Fold')
pyplot.savefig("F1SumaKF3.jpg")

fig,ax8 = pyplot.subplots()
ax8.bar(names, graficaRecallKF.values())
ax8.set_title('Recall de K-Fold')
pyplot.savefig("RecallSumaKF3.jpg")
