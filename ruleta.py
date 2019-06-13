from random import randint
import matplotlib.pyplot as plt
from matplotlib import ticker as tick
import statistics

#https://www.overleaf.com/project/5c9b84ff1e4a775dfb31fc34

n_muestras = 10000
min_n = 0
max_n = 36

data = []
promedio = []
promedio_promedio = []
varianza = []
varianza_media = []

def adjust_y_axis(x, pos):
    return x / (len(data) * 1.0)

def plot(a,p,pp,v,vm):

	#graficar histograma de frecuencias absolutas

	fig, ax = plt.subplots()
	n, bins, patches = ax.hist(a, bins = max_n+1)
	fig.tight_layout()
	plt.title("Histograma de frecuencia absoluta")
	plt.show()


	#graficar histograma frecuencia relativa
	fig, ax = plt.subplots()
	n, bins, patches = ax.hist(a, bins = max_n+1)
	fig.tight_layout()
	plt.title("Histograma de frecuencia relativa")
	ax.yaxis.set_major_formatter(tick.FuncFormatter(adjust_y_axis))
	plt.show()


	#graficar media
	plt.plot(list(range(len(p))), p, color='b')
	plt.title("Media")
	plt.show()
	
	#graficar media de media
	plt.plot(list(range(len(pp))), pp, color='b')
	plt.title("Media de las medias")
	plt.show()

	#graficar varianza
	plt.plot(list(range(len(v))), v, color='b')
	plt.title("Varianza")
	plt.show()

	#graficar varianza de media
	plt.plot(list(range(len(vm))), vm, color='b')
	plt.title("Varianza de las medias")
	plt.show()


def showarr(a):
	for i in range(min_n, max_n+1):
		print(str(i) + ": "+str(a.count(i)))


for i in range(n_muestras):
	data.append(randint(min_n,max_n))
	promedio.append(statistics.mean(data))
	promedio_promedio.append(statistics.mean(promedio))
	if i >= 2:
		varianza.append(statistics.variance(data))
		varianza_media.append(statistics.variance(promedio))


plot(data,promedio,promedio_promedio,varianza,varianza_media)
showarr(data)

#

