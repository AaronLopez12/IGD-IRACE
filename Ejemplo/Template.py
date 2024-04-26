#!/usr/bin/env python3 

import numpy as np 
import sys

path 			 = sys.argv[1]
n_iteraciones  	 = int(sys.argv[2])
n_individuos  	 = int(sys.argv[3])
proporcion_selec = float(sys.argv[4])
prob			 = float(sys.argv[5])
semilla 		 = int(sys.argv[6])
np.random.seed(semilla)

def Creacion_de_poblacion(Mat_B, Vec_Pes, Prob, num_individuos, num_items, num_mochilas):
	Poblacion = np.zeros((num_individuos, num_items + 1))

	for j in range(num_items):
		Beneficio = Mat_B[j,j]
		Pesos     = Vec_Pes[:, j]
		Cocientes = np.divide(Beneficio * np.ones(num_mochilas), Pesos)
		
		PV 		  = [Prob ] + [ (1-Prob)*Cocientes[i]/np.sum(Cocientes) for i in range(num_mochilas)]

		for i in range(num_individuos):
			Poblacion[i,j] = np.random.choice(range(-1,num_mochilas),  p = PV)

	return Poblacion

def Lectura_instancia(path):
	with open(path) as f:
		objetos_mochilas = f.readline()
		obj  = int(objetos_mochilas.split()[0])
		moch = int(objetos_mochilas.split()[1])
		todo = f.readlines()
		M 	 = todo[1:-1*(int(3 + moch))]
		P 	 = todo[obj + 2:-2]
		C 	 = todo[obj + moch + 3 : ]	
		
	valores = [linea.strip().split() for linea in M]
	matriz  = np.array(valores, dtype = int)

	valores_pesos = [peso.strip().split() for peso in P]
	pesos = np.array(valores_pesos, dtype = int)
	
	valores_capacidades = [capacidades.strip().split() for capacidades in C]
	cap = np.array(valores_capacidades, dtype = int)[0]

	return obj, moch, matriz, pesos, cap

def Funcion_MQKP(n_items, V_Pesos, V_Cap, M_Benef, V_Solucion):
	V_Solucion_evaluado = np.copy(V_Solucion)
	V_Solucion_evaluado[-1] = 0
	
	for i in range(n_items):
		indices = np.where(V_Solucion[0:n_items] == i)[0]
		
		if len(indices) == 0:
			continue
		
		elif (np.sum(V_Pesos[i][indices]) > V_Cap[i]):
			V_Solucion_evaluado[-1] = -1000
			break

		else:
			for i in range(len(indices)):
				for j in range(i,len(indices)):
					V_Solucion_evaluado[-1] += M_Benef[indices[i], indices[j]]				
	return V_Solucion_evaluado



Seleccion_ind 	= proporcion_selec*(n_individuos)
n_objetos, n_mochilas, beneficios, pesos, capacidades = Lectura_instancia(path)

Poblacion_inicial = Creacion_de_poblacion( beneficios, pesos , prob, n_individuos, n_objetos, n_mochilas)

#########################
### Inicio del ciclo ####
for i in range(n_iteraciones):
	
	# Evaluación de la población inicial
	for ii in range(n_individuos):
		Poblacion_inicial[ii] = Funcion_MQKP(n_objetos, pesos, capacidades, beneficios, Poblacion_inicial[ii])

	# Reordenamiento de la matriz, reverse = True para problemas de maximización
	Poblacion_inicial = np.array(sorted(Poblacion_inicial, key = lambda x: x[-1], reverse = True))

	# Seleccion de los individuos:
	Poblacion_Seleccionada = np.zeros((int(Seleccion_ind), n_objetos+ 1))
	Poblacion_Seleccionada = Poblacion_inicial[0:int(Seleccion_ind)]

	# Estimación de parámetros
	Parametros = np.zeros(( n_objetos, n_mochilas + 1))
	
	for l in range(n_objetos):
		for k in range(-1, n_mochilas):
			Parametros[l,k+1] = len(np.where(Poblacion_Seleccionada[:,l] == k)[0]) / (int(Seleccion_ind) )

	# Creacion de nueva poblacion:
	Nueva_Poblacion = np.zeros((n_individuos, n_objetos + 1))

 	# Creacion de la poblacion basado en los parámetros calculados
	for jj in range(n_individuos):
		for kk in range(n_objetos):
 			Nueva_Poblacion[jj, kk] = np.random.choice(range(-1,n_mochilas), p = Parametros[kk])
			
	# Renombre de la nueva generacion de individuos
	Poblacion_inicial = Nueva_Poblacion.copy()		



Poblacion_inicial = np.array(sorted(Poblacion_inicial, key = lambda x: x[-1], reverse = True))
print(-1*Poblacion_inicial[0, -1])

