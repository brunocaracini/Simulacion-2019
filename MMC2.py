import numpy as np
import random
from matplotlib import pyplot

infinito = 99999999999
tma = 0.8

class Cliente():
    def __init__(self):
        self.tiempo_entrada = 0
        self.tiempo_salida = 0
        self.demora_cli = 0
        self.prioridad = np.random.random() < 0.1

    def entrada(self, tiempo):
        self.tiempo_entrada = tiempo

    def salida(self, tiempo):
        self.tiempo_salida = tiempo
        self.demora_cli = self.tiempo_salida - self.tiempo_entrada


class Cola():
    def __init__(self, numero):
        self.clientes = []
        self.cant_cli_acum = 0
        self.numero_cola = numero


    def disciplina_cola(self, algoritmo):
        #FIFO
        if algoritmo == '1':
            cliente = self.clientes.pop(0)
            return cliente

        #LIFO
        elif algoritmo == '2':
            cliente = self.clientes.pop()
            return cliente
        
        #PRIORIDADES
        if algoritmo == '31':
            cliente = False
            i = 0
            while cliente == False and i < len(self.clientes):
                if self.clientes[i].prioridad == True:
                    cliente = self.clientes.pop(i)
                else:
                    i += 1
            if cliente == False:
                cliente = self.clientes.pop(0)
                
        elif algoritmo =='32':
            cliente = False
            i = len(self.clientes) - 1
            while cliente == False and i >= 0:
                if self.clientes[i].prioridad == True:
                    cliente = self.clientes.pop(i)
                else:
                    i -= 1
            if cliente == False:
                cliente = self.clientes.pop()

        return cliente


class Servidor():
    def __init__(self, estado, numero, tiempo_m_servicio):
        self.ocupado = estado
        self.cliente = False
        self.numero = numero
        self.entrada_serv = 0
        self.salida_serv = 0
        self.tiempo_acumulado_servicio = 0
        self.tms = tiempo_m_servicio
        
    def asigna_cliente(self, cliente, tiempo):
        if cliente == False:
            self.salida_servidor(tiempo)
            self.ocupado = False
            self.tiempo_acumlado()
        else:
            self.cliente = cliente
            self.entrada_servidor(tiempo)
            self.ocupado = True

    def entrada_servidor(self, tiempo):
        self.entrada_serv = tiempo

    def salida_servidor(self, tiempo):
        self.salida_serv = tiempo
        self.cliente = False

    def tiempo_acumlado(self):
        self.tiempo_acumulado_servicio = self.tiempo_acumulado_servicio + (self.salida_serv - self.entrada_serv)


class Evento():
    def __init__(self,tipo,tiempo):
        self.tipo = tipo
        self.tiempo = tiempo

class Simulacion():
    def __init__(self, muestra_diagnostico, algoritmo):
        self.clock = 0
        self.l_evento = [] 
        self.l_tiempo = []
        self.serv1 = Servidor(False, 1, 0.5)
        self.serv2 = Servidor(False, 2, 0.5)
        self.serv3 = Servidor(False, 3, 0.5)
        self.serv4 = Servidor(False, 4, 0.2)
        self.serv5 = Servidor(False, 5, 0.4)
        self.serv6 = Servidor(False, 6, 0.6)
        self.cola0 = Cola(0)
        self.cola1 = Cola(1)
        self.cola2 = Cola(2)
        self.cola3 = Cola(3)
        self.colas = [self.cola0,self.cola1,self.cola2,self.cola3]
        self.linea1 = [self.serv1, self.serv2, self.serv3]
        self.linea2 = [self.serv4, self.serv5, self.serv6]
        self.demora_acumulada = 0
        self.clientes_completaron_demora = 0 
        self.tiempo_ult_evento = 0
        self.muestra_diagnostico = muestra_diagnostico
        self.algoritmo = algoritmo
        self.cant_cli_prioridad = 0


    def inicializacion(self):
        self.clock = 0  
        #Inicializamos el reloj en 0.
        tiempo = self.clock + np.random.exponential(tma)  
        #Calculamos el tiempo del primer arribo para inicializar la lista de eventos.
        prox_evento = Evento('arribo', tiempo) 
        #Creamos un objeto del tipo evento, que recibe como parametro el tiempo calculado y el tipo de evento.
        self.l_evento.append(prox_evento)  
        #Asignamos el evento arribo que creamos en la posición 0 de la lista de eventos.
        for i in range(1,7): 
        #Llenamos las posiciones restantes de la lista de eventos con partidas.
            tiempo = infinito 
            #Ponemos el tiempo en infinito para estas partidas.
            prox_evento = Evento('partida', tiempo) 
            #Creamos un objeto del tipo evento, que recibe como parametro el tiempo calculado y el tipo de evento.
            self.l_evento.append(prox_evento) 
            # Asignamos el evento arribo que creamos en la posición i de la lista de eventos.


    def tiempos(self):
        self.l_tiempo = []
        for evento in self.l_evento: 
        #En este for se obtiene el tiempo de todos los eventos de la lista de eventos, y lo guardamos en una lista de tiempos.
            self.l_tiempo.append(evento.tiempo)
        tiempo_prox_evento = min(self.l_tiempo) 
        #Elegimos el mas chico de esa lista de tiempos.
        index_prox_evento = self.l_tiempo.index(tiempo_prox_evento) 
        evento = self.l_evento[index_prox_evento] 
        #Buscamos el evento que corresponde a ese tiempo en la lista de eventos
        self.tiempo_ult_evento = self.clock
        #Guardamos el tiempo del ultimo evento
        self.clock = evento.tiempo 
        #Actualizamos el reloj a ese tiempo
        return [evento.tipo, index_prox_evento] 
        #Devolvemos el tipo de evento y su índice para identificar a que servidor corresponde.
        

    def eventos(self, evento_tipo, index_prox_evento):
        def arribo():
            tiempo = self.clock + np.random.exponential(tma) 
            #Calcula el nuevo tiempo de arribo.
            prox_evento = Evento('arribo', tiempo) 
            #Creamos un objeto del tipo Evento, que recibe como parametro el tiempo calculado y el tipo de evento.
            self.l_evento[0] = prox_evento 
            #Asignamos el evento arribo que creamos en la posición 0 de la lista de eventos.
            cliente = Cliente()
            cliente.entrada(self.clock)
            #Creamos un objeto del tipo Cliente.
            if (cliente.prioridad == True) and (self.algoritmo == '31' or self.algoritmo == '32'):
                self.cant_cli_prioridad += 1
            #Si el cliente es prioritario, sumamos uno al estadistico de clientes prioritarios
            servidores_disponibles = [] 
            #Creamos un arreglo vacío de servidores disponibles.
            for servidor in self.linea1: 
            #Por cada uno de los servidores, se chequea si está ocupado o no y se añade a la lista de servidores disponibes.
                if servidor.ocupado == False:
                    servidores_disponibles.append(servidor)
            if len(servidores_disponibles) == 0: 
                self.colas[0].clientes.append(cliente)
            #Si no hubo ninguno disponible, se añade el cliente a a la cola.

            else: 
            #Si hubo servidores disponibles, entonces:
                servidor = random.choice(servidores_disponibles) 
                #Elegimos un servidor al azar de la lista de servidores disponibles.
                servidor.asigna_cliente(cliente, self.clock)  
                #Registramos que el elciente se encuentra en ese servidor
                #Actualizamos el estado de ocupación del servidor.
                index_serv = self.linea1.index(servidor)    
                self.linea1[index_serv] = servidor 
                #Actualizamos los datos del servidor igualandolo a la copia.
                tiempo = self.clock + np.random.exponential(servidor.tms)
                prox_partida = Evento('partida', tiempo)
                self.l_evento[servidor.numero] = prox_partida
                #Calculamos el tiempo de partida para el arribo creado.
                 
        def partida(index_prox_evento):
            if index_prox_evento in [1,2,3]:
            #corroboramos que la partida corresponda a un servidor de la primera linea
                cliente = self.linea1[index_prox_evento - 1].cliente
                #tomamos el cliente que está en ese servidor y lo guardamos en una variable.
                if self.linea2[index_prox_evento - 1].ocupado == True:   
                    self.colas[index_prox_evento].clientes.append(cliente)
                #Chequeamos si el servidor que está en línea recta está ocupado, y si lo está asignamos el cliente a la cola.
                else:
                    self.linea2[index_prox_evento - 1].asigna_cliente(cliente, self.clock)
                    #En caso de que esté vacío, asignamos al cliente a ese servidor.
                    #Ponemos el servidor al que paso el cliente como ocupado.
                    tiempo = self.clock + np.random.exponential(self.linea1[index_prox_evento - 1].tms)
                    prox_partida = Evento('partida', tiempo)
                    self.l_evento[index_prox_evento + 3] = prox_partida
                    #Calculamos un evento partida para ese cliente en el nuevo servidor.
                    

                self.linea1[index_prox_evento - 1].asigna_cliente(False, self.clock)   
                #Cambiamos el estado del servidor y borramos el cliente que ha partido.

                if len(self.colas[0].clientes) == 0:
                    prox_partida = Evento('partida', infinito)
                    self.l_evento[index_prox_evento] = prox_partida
                # Chequeamos si la longitud de la cola que alimenta la primera linea es 0, si es así, 
                # ponemos la partida de ese servidor en infinito
                else:
                #Si la cola no está vacia, entonces:
                    cliente = self.colas[0].disciplina_cola(self.algoritmo)
                    #agarramos el primer cliente de la cola y lo guardamos en una variable, moviendo
                    #los demás clientes una posición hacia adelante.
                    self.linea1[index_prox_evento - 1].asigna_cliente(cliente, self.clock)
                    #asignamos el cliente al servidor que quedó vacío en la partida.
                    #Cambiamos el estado del servidor a ocupado.
                    tiempo = self.clock + np.random.exponential(self.linea1[index_prox_evento - 1].tms)
                    prox_partida = Evento('partida', tiempo)
                    self.l_evento[index_prox_evento] = prox_partida
                    #Calculamos un evento partida para ese cliente, y lo guardamos en la lista de eventos.
                    
            else:
            #Si la partida no fue de la primera línea, entonces:
                
                self.linea2[index_prox_evento - 4].cliente.salida(self.clock)
                #Registramos el tiempo en el que el cliente sale del sistema
                
                self.clientes_completaron_demora += 1
                #Sumamos uno al numero de clientes que completaron la demora

                self.demora_acumulada +=  self.linea2[index_prox_evento - 4].cliente.demora_cli
                #Sumamos la demora del cliente a la demora acumulada

                self.linea2[index_prox_evento - 4].asigna_cliente(False, self.clock)
                #Cambiamos el estado del servidor a disponible

                if len(self.colas[index_prox_evento - 3].clientes) == 0:
                #Chequeamos si la cola que alimenta el servidor está vacía.    
                    prox_partida = Evento('partida', infinito)
                    self.l_evento[index_prox_evento] = prox_partida
                    #Si lo está, ponemos la partida de ese servidor en infinito, y actualizamos la lista de eventos.
                    
                else:
                #Si la cola no estaba vacía, entonces:
                    cliente = self.colas[index_prox_evento - 3].disciplina_cola(self.algoritmo)
                    #agarramos el primer cliente de la cola y lo guardamos en una variable, moviendo
                    #los demás clientes una posición hacia adelante.                
                    self.linea2[index_prox_evento - 4].asigna_cliente(cliente, self.clock)
                    #asignamos el cliente al servidor que quedó vacío en la partida.
                    tiempo = self.clock + np.random.exponential(self.linea2[index_prox_evento - 4].tms)
                    prox_partida = Evento('partida', tiempo)
                    self.l_evento[index_prox_evento] = prox_partida
                    #Calculamos un evento partida para el cliente que se asigna al servidor.


        if evento_tipo == 'arribo':
            arribo()
        if evento_tipo == 'partida':
            partida(index_prox_evento)
        
        for cola in self.colas:
            cola.cant_cli_acum += len(cola.clientes) * (self.clock - self.tiempo_ult_evento)
        #Se suman en cada iteración y en cada cola la cantidad de clientes acumulados aplicando la formula.
    
    def reportes(self):
        print('')
        print('--------'*15)
        print(" "*50, 'REPORTES: ')
        print('--------'*15)
        if self.algoritmo == '1':
            print('Algoritmo de colas utilizado: FIFO')
        elif self.algoritmo == '2':
            print('Algoritmo de colas utilizado: LIFO')
        elif self.algoritmo == '31':
            print('Algoritmo de colas utilizado: PRIORIDADES - FIFO')
            print('--------'*15)
            print('Cantidad total de clientes prioritarios:', self.cant_cli_prioridad)
        elif self.algoritmo == '32':
            print('Algoritmo de colas utilizado: PRIORIDADES - LIFO')
            print('--------'*15)
            print('Cantidad total de clientes prioritarios:', self.cant_cli_prioridad)
        print('--------'*15)
        print('Reloj detenido en:', self.clock)
        print('--------'*15)
        #Utilizacion de servidores u(t)
        print('Utilizacion de servidores u(t):')
        print('')
        for servidor in (self.linea1+self.linea2):
            print('Utilizacion promedio del servidor', servidor.numero, ':', servidor.tiempo_acumulado_servicio/self.clock)
        print('--------'*15)
        
        #Demora promedio del cliente d(t)
        d_t_promedio =  self.demora_acumulada/self.clientes_completaron_demora
        print("Demora promedio de clientes d(t): ",d_t_promedio)
        print('--------'*15)

        #Cantidad promedio de clientes en cola q(t)
        print('Cantidad promedio de clientes en cola q(t):')
        print('')
        for cola in self.colas:
            print('Cantidad promedio de clientes en la cola', cola.numero_cola,':', cola.cant_cli_acum/self.clock)
        print('--------'*15)

    def plots(self):
        pass
            

    def diagnostico(self, tipo_prox_evento, index_prox_evento):
        print('----*'*15)
        print('')
        print('reloj: ', self.clock)
        print('Lista de tiempos:', self.l_tiempo)
        print('')
        print('proximo evento:', tipo_prox_evento,' ' , index_prox_evento)
        i = 0
        print('')
        for cola in self.colas:
            cant_cli = len(cola.clientes)
            print('Cantidad de clientes en la cola ', i, ': ', cant_cli)
            i +=1
        print('')
        for servidor in (self.linea1 + self.linea2):
            if servidor.ocupado == True:
                print('Servidor ', servidor.numero, ': ocupado')
            else:
                 print('Servidor ', servidor.numero, ': disponible')
        print('')

    def programa_principal(self):
        #LLamamos a la rutina de inicialización.
        self.inicializacion()

        while(self.clock < tiempo_terminacion):
            #Llamamos a la rutina de tiempos, que devuelve el proximo evento, y lo guardamos en una variable.
            array = self.tiempos()
            tipo_prox_evento = array[0]
            index_prox_evento = array[1]
            
            #LLamamos a la rutina de eventos, y le mandamos como parámetro el tipo de evento del proximo evento.
            self.eventos(tipo_prox_evento, index_prox_evento)
            if self.muestra_diagnostico == True:
                self.diagnostico(tipo_prox_evento, index_prox_evento)
        
        self.reportes()

#Main:
tiempo_terminacion = eval(input('Ingrese tiempo de fin de la simulacion: '))
algoritmo = input('Seleccione algoritmo de colas a utilizar: \n 1)FIFO \n 2)LIFO \n 3)PRIORIDADES\n')
if algoritmo == '3':
    ans = input('Seleccione algoritmo suplementario a utilizar: \n 1)FIFO \n 2)LIFO\n')
    if ans == '1':
        algoritmo = '31'
    else:
        algoritmo = '32'
ans = input('¿Desea ver un detalle de la simulacion paso a paso? (S/N) \n')


if ans == 'S' or ans == 's':
    sim = Simulacion(True, algoritmo)
    sim.programa_principal()

else:
    sim = Simulacion(False, algoritmo)
    sim.programa_principal()

