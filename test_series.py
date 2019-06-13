from random import randint

#PARAMETROS A CAMBIAR
k = 10
n = 100

#Generamos nros al azar con randint, esto se puede reemplazar por el generador a probar
data = [[randint(0,1000)/1000 for i in range(2)] for i in range(n)]

#Calculamos frecuencias absolutas
freqs = [[0 for i in range(k)] for i in range(k)]

#Para cada par de rangos (i,j)
for i in range(1,k+1):
    maxI = i/k
    minI = maxI - (1/k)
    for j in range(1,k+1):
        maxJ = j/k
        minJ = maxJ - (1/k)
        for d in data:
            if d[0] < maxI and d[0] >= minI and d[1] < maxJ and d[1] >= minJ:
                #Si el primer elemento esta en el rango i, y el segundo en el j,
                #sumamos 1 a la frecuencia de esos rangos
                freqs[i-1][j-1]+=1

#χ2 = k/n * Σ(fj - n/k)^2

chi2 = ((k**2)/n) * sum([sum((i-(n/(k**2)))**2 for i in row) for row in freqs])

print("chi2 = " + str(chi2))