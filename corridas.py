from random import randint

#PARAMETROS A CAMBIAR
n = 20
v = True #modo verboso

#Generamos la data
data = [randint(0,1000)/1000 for i in range(n)]

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
def get_r(subs):
    less_than_six = 0
    more_than_or_six = 0
    for key in subs:
        if int(key) < 6:
            less_than_six += subs[key]
        else:
            more_than_or_six += subs[key]
