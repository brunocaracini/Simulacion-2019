from random import randint
import matplotlib.pyplot as plt
import numpy as np


#muestras por distribucion
mpd = 200000

#empirica, binom_negativa, geometrica, hipergeometrica, poisson,binomial

#Diccionario cuyas claves son los nombres de las distribuciones, y cuyos valores son el conjunto de datos aleatorios generados con esa distribucion
dists = {}

#Generacion de datos
dists["uniforme"] = np.random.uniform(0,100,mpd)
dists["normal"] = np.random.normal(0,1,mpd)
dists["log_normal"] = np.random.lognormal(0,0.25,mpd)
dists["geometrica"] = np.random.geometric(0.3,mpd)
dists["exponencial"] = np.random.exponential(1,mpd)
dists["gamma"] = np.random.gamma(5,1,mpd)
dists["binomial"] = np.random.binomial(100,0.8,mpd)
dists["binom_negativa"] = np.random.negative_binomial(3,0.5,mpd)
dists["poisson"] = np.random.poisson(5,mpd)

#Para cada llave en el diccionario, graficamos la data de su valor
for key in dists:
	if dists[key] != []:
		fig, ax = plt.subplots()
		n, bins, patches = ax.hist(dists[key], 100)
		fig.tight_layout()
		plt.title("Histograma de frecuencia absoluta para distribucion " + key)
		plt.show()
		

#Generamos y graficamos la distribucion empirica, a partir de la normal estandar

#con mdp numeros
data = np.random.normal(0,1,500)
data.sort()
emp = np.array([(i/500*2) for i in range(1,500+1)])
plt.plot(data,emp)

#con 500 nros, para comparar suavidad de curva
data = np.random.normal(0,1,mpd)
data.sort()
emp = np.array([(i/mpd*2) for i in range(1,mpd+1)])
plt.plot(data,emp)


plt.title("Grafica de funcion de funcion de distribucion empirica acumulada")
plt.show()
