from random import randint

#PARAMETROS A CAMBIAR
n = 10000
v = False #modo verboso

#Generamos la data
data = [randint(0,1000)/1000 for i in range(n)]

#vectores a y b provistos en el pdf
a = [[4529.4, 9044.9, 13568, 18091, 22615, 27892],
     [9044.9, 18097, 27139, 36187, 45234, 55789],
     [13568, 27139, 40721, 54281, 67852, 83685],
     [18091, 36187, 54281, 72414, 90470, 111580],
     [22615, 45234, 67852, 90470, 113262, 139476],
     [27892, 55789, 83685, 111580, 139476, 172860]]

b = [1/6,5/24,11/120,19/720,29/5040,1/840]

######## 1 ########
def get_subs(data):
    #Buscamos cadenas de números subsecuentes en la data
    #Y guardamos las frecuencias de su aparición de acuerdo a su largo

    subs = {}           #frecuencias de cadenas por largo
    len_of_sub = 1      #largo de la cadena 
    last_num = data[0]  #nro anterior al actual

    if v: print(data[0])

    for d in data[1:]:
        #Si el nro actual es mayor al nro anterior
        if d > last_num:
            #Sumamos uno al largo de la cadena actual
            len_of_sub += 1
        #Si es mas chico, o igual, terminamos la cadena
        else:
            if v: print("End of chain")
            #sumamos uno al contador de frecuencias para el largo actual
            s = str(len_of_sub)
            if s in subs.keys():
                subs[s] += 1
            else:
                subs[s] = 1
            #y seteamos el largo de la cadena actual a 1
            len_of_sub = 1

        if v: print(d)
        last_num = d

    if v: print(data)
    if v: print(subs)
    return subs
    
######## 2 ########
#Generamos arreglo r donde
#r[i] es igual a la cantidad de subsecuencias de largo i, si i < 6
#y r[6] es igual a la cantidad de subsecuencas de largo mayor a 6
def get_r(subs):
    r = [0 for i in range(6)]
    for key in subs:
        if int(key) < 6:
            r[int(key)-1] = subs[key]
        else:
            r[5] += subs[key]

    if v: print(r)
    return r

def get_chi2(r):
    #χ2 = 1/n * ΣΣ aij (ri - n*bi) (rj - n*bj)
    chi2 = 0
    for i in range(6):
        for j in range(6):
            chi2 += a[i][j] * (r[i] - (n*b[i])) * (r[j] - (n*b[j]))
    chi2 *= 1/n
    return chi2

subs = get_subs(data)
r = get_r(subs)
chi2 = get_chi2(r)
print("Chi2 = " + str(chi2))
