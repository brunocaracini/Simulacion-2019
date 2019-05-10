from random import randint

#PARAMETROS A CAMBIAR
z_inicial = "1009"


#Creamos el array y lo llenamos de ceros
data = [[" ...  " for i in range(3)] for i in range(1000)]

#Comenzamos por llenar la primera fila fuera del loop
#El primer elemento de una fila es un numero al azar
data[0][0] = z_inicial

#El tercero es ese numero al cuadrado (como string)
data[0][2] = str(int(data[0][0]) ** 2)

#Si el numero elevado al cuadrado tiene menos de 8 cifras agregamos ceros a la izquierda
if len(data[0][2]) < 8:
    #Agregamos un cero por cantidad de cifras que faltan para llegar a 8
    data[0][2] = ("0" * (8-len(data[0][2]))) + data[0][2]

#Una vez agregados los ceros, tomamos los 4 digitos centrales del numero elevado al cuadrado
#Y lo guardamos en la columna 1 de la siguiente fila
data[1][0] =  data[0][2][2:-2]

#Este valor servira como el valor de la primera columna para generar los siguientes nros aleatorios
#Ahora se recorrera todo el array en un loop generando los valores

for row_number in range(1,len(data) - 1):
    #La primera columna de las filas habra sido generada en el paso anterior
    #Calculamos la segunda utilizando los nros de la primera como decimales
    data[row_number][1] = "0."+data[row_number][0]

    #como antes, llenamos la tercer columna con el nro elevado al cuadrado, y agregamos los ceros si es necesario
    data[row_number][2] = str(int(data[row_number][0]) ** 2)
    if len(data[row_number][2]) < 8:
        data[row_number][2] = ("0" * (8-len(data[row_number][2])))+ data[row_number][2]

    data[row_number+1][0] = data[row_number][2][2:-2]


#imprimimos los valores generados, hasta encontrar un 0
for row in data:
    print(str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) )
    if row[0] == "0000":
        break