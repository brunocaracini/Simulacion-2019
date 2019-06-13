from random import randint

#PARAMETROS A CAMBIAR
n = 10000
z_inicial = 7
a = 5
c = 3
m = 16

def gcl():
    data = [0 for i in range(n)]

    data[0] = z_inicial

    for i in range(1,len(data)-1):
        #Zi = (a * Zi-1 + c)mod m
        data[i] = ((a*data[i-1])+c)%m

    return data

data = gcl()
for i in data:
    print(i)