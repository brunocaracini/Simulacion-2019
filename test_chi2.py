from random import randint

#PARAMETROS A CAMBIAR
k = 20
n = 200

#Generamos nros al azar con randint, esto se puede reemplazar por el generador a probar
data = [randint(0,1000)/1000 for i in range(n)]


def gen_chi2(data_arr):
    #Calculamos frecuencias absolutas
    freqs = [0 for i in range(k)]

    #Para cada rango
    for i in range(1,k+1):
        max = i/k
        min = max - (1/k)
        for d in data_arr:
            if d < max and d >= min:
                #Si el numero esta en el rango, sumamos 1 a la frecuencia de ese rango
                freqs[i-1]+=1

    #χ2 = k/n * Σ(fj - n/k)^2
    chi2 = (k/n) * sum([(i-(n/k))**2 for i in freqs])
    return chi2

chi2 = gen_chi2(data)
print("χ2 = " + str(chi2))