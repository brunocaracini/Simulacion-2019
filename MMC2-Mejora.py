import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

infinito = 99999999999
tma = 0.8

class Resultado():
    def __init__(self, clocks, demora_acumulada_array, demora_acumulada_prioridad_array, colas, lineas, clock, algoritmo):
        self.clocks = clocks
        self.demora_acumulada_array = demora_acumulada_array
        self.demora_acumulada_prioridad_array = demora_acumulada_prioridad_array
        self.colas = colas
        self.lineas = lineas
        self.clock = clock
        self.algoritmo = algoritmo


class Cliente():
    def __init__(self):
        self.tiempo_entrada = 0
        self.tiempo_salida = 0
        self.demora_cli = 0
        self.prioridad = np.random.random() < 0.03

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
        self.cant_cli_acum_array = []
        self.cant_cli_acum_prioridad = 0
        self.cant_cli_acum_prioridad_array = []
        self.clientes_prioritarios = []


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
        self.tiempo_acumulado_servicio_array = []
        self.tiempo_acumlado_servicio_promedio_array = []
        
    def asigna_cliente(self, cliente, tiempo):
        if cliente == False:
            self.salida_serv = tiempo
            self.cliente = False
            self.ocupado = False
            self.tiempo_acumulado_servicio = self.tiempo_acumulado_servicio + (self.salida_serv - self.entrada_serv)
        else:
            self.cliente = cliente
            self.entrada_serv = tiempo
            self.ocupado = True
       
    def tiempo_acumlado(self, tiempo):
        self.tiempo_acumulado_servicio_array.append(self.tiempo_acumulado_servicio)
        self.tiempo_acumlado_servicio_promedio_array.append(self.tiempo_acumulado_servicio/tiempo)


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
        self.colas = [self.cola0,self.cola1]
        self.linea1 = [self.serv1, self.serv2, self.serv3]
        self.linea2 = [self.serv4, self.serv5, self.serv6]
        self.demora_acumulada = 0
        self.clientes_completaron_demora = 0 
        self.tiempo_ult_evento = 0
        self.muestra_diagnostico = muestra_diagnostico
        self.algoritmo = algoritmo
        self.cant_cli_prioridad = 0
        self.clocks = []
        self.demora_acumulada_array=[]
        self.demora_acumulada_prioridad = 0
        self.clientes_completaron_demora_prioridad = 0
        self.demora_acumulada_prioridad_array = []
        self.clientes_completaron_demora_array = []
        self.clientes_completaron_demora_prioridad_array = []
    
    
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
        self.clocks.append(self.clock)
        #Guardamos el tiempo ultimo tiempo en la lista que contiene el historial del reloj
        self.clock = evento.tiempo 
        #Actualizamos el reloj al tiempo del proximo evento
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
                servidores_disponibles = [] 
                #Creamos un arreglo vacío de servidores disponibles.
                for servidor in self.linea2: 
                #Por cada uno de los servidores, se chequea si está ocupado o no y se añade a la lista de servidores disponibes.
                    if servidor.ocupado == False:
                        servidores_disponibles.append(servidor)
                if len(servidores_disponibles) == 0: 
                  self.colas[1].clientes.append(cliente)
                #Si no hubo ninguno disponible, se añade el cliente a a la cola.

                else: 
                #Si hubo servidores disponibles, entonces:
                    servidor = random.choice(servidores_disponibles) 
                    #Elegimos un servidor al azar de la lista de servidores disponibles.
                    servidor.asigna_cliente(cliente, self.clock)  
                    #Registramos que el elciente se encuentra en ese servidor 
                    # Actualizamos el estado de ocupación del servidor.
                    index_serv = self.linea2.index(servidor)    
                    self.linea2[index_serv] = servidor 
                    #Actualizamos los datos del servidor igualandolo a la copia.
                    tiempo = self.clock + np.random.exponential(servidor.tms)
                    prox_partida = Evento('partida', tiempo)
                    self.l_evento[servidor.numero] = prox_partida                        
                    #Calculamos el tiempo de partida para el cliente en el nuevo servidor

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

                if self.algoritmo == '31' or '32':
                    if self.linea2[index_prox_evento - 4].cliente.prioridad:
                        self.clientes_completaron_demora_prioridad += 1
                        self.demora_acumulada_prioridad += self.linea2[index_prox_evento - 4].cliente.demora_cli
                #Sumamos uno al numero de clientes prioritarios que completaron la demora, y sumamos la demora del cliente prioritario a la 
                #demora acumulada de clientes prioritarios.

                self.linea2[index_prox_evento - 4].asigna_cliente(False, self.clock)
                #Cambiamos el estado del servidor a disponible

                if len(self.colas[1].clientes) == 0:
                #Chequeamos si la cola que alimenta el servidor está vacía.    
                    prox_partida = Evento('partida', infinito)
                    self.l_evento[index_prox_evento] = prox_partida
                    #Si lo está, ponemos la partida de ese servidor en infinito, y actualizamos la lista de eventos.
                    
                else:
                #Si la cola no estaba vacía, entonces:
                    cliente = self.colas[1].disciplina_cola(self.algoritmo)
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
            cola.cant_cli_acum_array.append(cola.cant_cli_acum/self.clock)
        #Se suman en cada iteración y en cada cola la cantidad de clientes acumulados aplicando la formula.

        for servidor in (self.linea1 + self.linea2):
            servidor.tiempo_acumlado(self.clock)
        #Se actualiza en cada iteracion la utilizacion de cada servidor para el tiempo de reloj actual.
        
        if self.clientes_completaron_demora == 0:
            self.demora_acumulada_array.append(0)
        else:
            self.demora_acumulada_array.append(self.demora_acumulada/self.clientes_completaron_demora)
        #Se actualiza en cada iteracion la demora promedio de los clientes para el tiempo de reloj actual.

        if algoritmo == '32' or '31':
            if self.clientes_completaron_demora_prioridad == 0:
                self.demora_acumulada_prioridad_array.append(0)
            else:
                self.demora_acumulada_prioridad_array.append(self.demora_acumulada_prioridad/self.clientes_completaron_demora_prioridad)
        ##Se actualiza en cada iteracion la demora promedio de los clientes para el tiempo de reloj actual para los clientes prioritarios.

    
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

    def diagnostico(self, tipo_prox_evento, index_prox_evento):
        print('----*'*15)
        print('')
        print('reloj: ', self.tiempo_ult_evento)
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
        lineas = self.linea1 + self.linea2
        resultado = Resultado(self.clocks, self.demora_acumulada_array, self.demora_acumulada_prioridad_array, self.colas, lineas , self.clock, self.algoritmo) 
        return resultado


def plots(res1, res2, res3):
     #Tiempo acumulado de servicio
        
        fig, axs = plt.subplots(3, 2)

        fig.suptitle('Tiempo acumulado de servicio')

        
        axs[0, 0].plot(res1.clocks, res1.lineas[0].tiempo_acumulado_servicio_array, color = '#7C8788', label = 'Corrida 1')
        axs[0, 0].plot(res2.clocks, res2.lineas[0].tiempo_acumulado_servicio_array, color = '#F9CF51', label = 'Corrida 2')
        axs[0, 0].plot(res3.clocks, res3.lineas[0].tiempo_acumulado_servicio_array, color = '#E26D5C', label = 'Corrida 3')
        axs[0, 0].set_title('Servidor 1')
        axs[0, 0].set_ylabel('Tas')
        axs[0, 0].legend(loc = 'best')

        axs[0, 1].plot(res1.clocks, res1.lineas[1].tiempo_acumulado_servicio_array, color = '#7C8788', label = 'Corrida 1')
        axs[0, 1].plot(res2.clocks, res2.lineas[1].tiempo_acumulado_servicio_array, color = '#F9CF51', label = 'Corrida 2')
        axs[0, 1].plot(res3.clocks, res3.lineas[1].tiempo_acumulado_servicio_array, color = '#E26D5C', label = 'Corrida 3')
        axs[0, 1].set_title('Servidor 2')
        axs[0, 1].legend(loc = 'best')
        
        axs[1, 0].plot(res1.clocks, res1.lineas[2].tiempo_acumulado_servicio_array, color = '#7C8788', label = 'Corrida 1')
        axs[1, 0].plot(res2.clocks, res2.lineas[2].tiempo_acumulado_servicio_array, color = '#F9CF51', label = 'Corrida 2')
        axs[1, 0].plot(res3.clocks, res3.lineas[2].tiempo_acumulado_servicio_array, color = '#E26D5C', label = 'Corrida 3')
        axs[1, 0].set_title('Servidor 3')
        axs[1, 0].set_ylabel('Tas')
        axs[1, 0].legend(loc = 'best')
        
        axs[1, 1].plot(res1.clocks, res1.lineas[3].tiempo_acumulado_servicio_array, color = '#7C8788', label = 'Corrida 1')
        axs[1, 1].plot(res2.clocks, res2.lineas[3].tiempo_acumulado_servicio_array, color = '#F9CF51', label = 'Corrida 2')
        axs[1, 1].plot(res3.clocks, res3.lineas[3].tiempo_acumulado_servicio_array, color = '#E26D5C', label = 'Corrida 3')
        axs[1, 1].set_title('Servidor 4')
        axs[1, 1].set_title('Servidor 4')
        axs[1, 1].set_title('Servidor 4')
        axs[1, 1].legend(loc = 'best')
        
        axs[2, 0].plot(res1.clocks, res1.lineas[4].tiempo_acumulado_servicio_array, color = '#7C8788', label = 'Corrida 1')
        axs[2, 0].plot(res2.clocks, res2.lineas[4].tiempo_acumulado_servicio_array, color = '#F9CF51', label = 'Corrida 2')
        axs[2, 0].plot(res3.clocks, res3.lineas[4].tiempo_acumulado_servicio_array, color = '#E26D5C', label = 'Corrida 3')
        axs[2, 0].set_title('Servidor 5')
        axs[2, 0].set_xlabel('Reloj de la simulación')
        axs[2, 0].set_ylabel('Tas')
        axs[2, 0].legend(loc = 'best')
        
        axs[2, 1].plot(res1.clocks, res1.lineas[5].tiempo_acumulado_servicio_array, color = '#7C8788', label = 'Corrida 1')
        axs[2, 1].plot(res2.clocks, res2.lineas[5].tiempo_acumulado_servicio_array, color = '#F9CF51', label = 'Corrida 2')
        axs[2, 1].plot(res3.clocks, res3.lineas[5].tiempo_acumulado_servicio_array, color = '#E26D5C', label = 'Corrida 3')
        axs[2, 1].set_title('Servidor 6')
        axs[2, 1].set_xlabel('Reloj de la simulación')
        axs[2, 1].legend(loc = 'best')
        
        plt.show()


        #Utilizacion promedio de servidores u(t)
        fig2, axs2 = plt.subplots(3, 2)
        
        fig.suptitle('Utilización promedio de los servidores U(t)')

        axs2[0, 0].plot(res1.clocks, res1.lineas[0].tiempo_acumlado_servicio_promedio_array, color = '#7C8788', label = 'Corrida 1')
        axs2[0, 0].plot(res2.clocks, res2.lineas[0].tiempo_acumlado_servicio_promedio_array, color = '#F9CF51', label = 'Corrida 2')
        axs2[0, 0].plot(res3.clocks, res3.lineas[0].tiempo_acumlado_servicio_promedio_array, color = '#E26D5C', label = 'Corrida 3')
        axs2[0, 0].set_title('Servidor 1')
        axs2[0, 0].set_ylabel('U(t)')

        axs2[0, 1].plot(res1.clocks, res1.lineas[1].tiempo_acumlado_servicio_promedio_array, color = '#7C8788', label = 'Corrida 1')
        axs2[0, 1].plot(res2.clocks, res2.lineas[1].tiempo_acumlado_servicio_promedio_array, color = '#F9CF51', label = 'Corrida 2')
        axs2[0, 1].plot(res3.clocks, res3.lineas[1].tiempo_acumlado_servicio_promedio_array, color = '#E26D5C', label = 'Corrida 3')
        axs2[0, 1].set_title('Servidor 2')
    
        axs2[1, 0].plot(res1.clocks, res1.lineas[2].tiempo_acumlado_servicio_promedio_array, color = '#7C8788', label = 'Corrida 1')
        axs2[1, 0].plot(res2.clocks, res2.lineas[2].tiempo_acumlado_servicio_promedio_array, color = '#F9CF51', label = 'Corrida 2')
        axs2[1, 0].plot(res3.clocks, res3.lineas[2].tiempo_acumlado_servicio_promedio_array, color = '#E26D5C', label = 'Corrida 3')
        axs2[1, 0].set_title('Servidor 3')
        axs2[1, 0].set_ylabel('U(t)')
        
        axs2[1, 1].plot(res1.clocks, res1.lineas[3].tiempo_acumlado_servicio_promedio_array, color = '#7C8788', label = 'Corrida 1')
        axs2[1, 1].plot(res2.clocks, res2.lineas[3].tiempo_acumlado_servicio_promedio_array, color = '#F9CF51', label = 'Corrida 2')
        axs2[1, 1].plot(res3.clocks, res3.lineas[3].tiempo_acumlado_servicio_promedio_array, color = '#E26D5C', label = 'Corrida 3')
        axs2[1, 1].set_title('Servidor 4')
    
        axs2[2, 0].plot(res2.clocks, res2.lineas[4].tiempo_acumlado_servicio_promedio_array, color = '#F9CF51', label = 'Corrida 1')
        axs2[2, 0].plot(res3.clocks, res3.lineas[4].tiempo_acumlado_servicio_promedio_array, color = '#E26D5C', label = 'Corrida 2')
        axs2[2, 0].plot(res1.clocks, res1.lineas[4].tiempo_acumlado_servicio_promedio_array, color = '#7C8788', label = 'Corrida 3')
        axs2[2, 0].set_title('Servidor 5')
        axs2[2, 0].set_xlabel('Reloj de la simulación')
        axs2[2, 0].set_ylabel('U(t)')
        
        axs2[2, 1].plot(res1.clocks, res1.lineas[5].tiempo_acumlado_servicio_promedio_array, color = '#7C8788', label = 'Corrida 1')
        axs2[2, 1].plot(res2.clocks, res2.lineas[5].tiempo_acumlado_servicio_promedio_array, color = '#F9CF51', label = 'Corrida 2')
        axs2[2, 1].plot(res3.clocks, res3.lineas[5].tiempo_acumlado_servicio_promedio_array, color = '#E26D5C', label = 'Corrida 3')
        axs2[2, 1].set_title('Servidor 6')
        axs2[2, 1].set_xlabel('Reloj de la simulación')

        axs2[0, 0].legend(loc = 'best')
        axs2[0, 1].legend(loc = 'best')
        axs2[1, 0].legend(loc = 'best')
        axs2[1, 1].legend(loc = 'best')
        axs2[2, 0].legend(loc = 'best')
        axs2[2, 1].legend(loc = 'best')

        plt.show()
        
        
        #Utilización promedio de servidores u(t) - Grafico de barras:
        u1 = res1.lineas[0].tiempo_acumulado_servicio/res1.clock
        u2 = res1.lineas[1].tiempo_acumulado_servicio/res1.clock
        u3 = res1.lineas[2].tiempo_acumulado_servicio/res1.clock
        u4 = res1.lineas[3].tiempo_acumulado_servicio/res1.clock
        u5 = res1.lineas[4].tiempo_acumulado_servicio/res1.clock
        u6 = res1.lineas[5].tiempo_acumulado_servicio/res1.clock
       
        u11 = res2.lineas[0].tiempo_acumulado_servicio/res2.clock
        u22 = res2.lineas[1].tiempo_acumulado_servicio/res2.clock
        u33 = res2.lineas[2].tiempo_acumulado_servicio/res2.clock
        u44 = res2.lineas[3].tiempo_acumulado_servicio/res2.clock
        u55 = res2.lineas[4].tiempo_acumulado_servicio/res2.clock
        u66 = res2.lineas[5].tiempo_acumulado_servicio/res2.clock
       
        u111 = res3.lineas[0].tiempo_acumulado_servicio/res3.clock
        u222 = res3.lineas[1].tiempo_acumulado_servicio/res3.clock
        u333 = res3.lineas[2].tiempo_acumulado_servicio/res3.clock
        u444 = res3.lineas[3].tiempo_acumulado_servicio/res3.clock
        u555 = res3.lineas[4].tiempo_acumulado_servicio/res3.clock
        u656 = res3.lineas[5].tiempo_acumulado_servicio/res3.clock

        serv1 = [u1,u11,u111]
        serv2 = [u2,u22,u222]
        serv3 = [u3,u33,u333]
        serv4 = [u4,u44,u444]
        serv5 = [u5,u55,u555]
        serv6 = [u6,u66,u656]
        
        servidores = [serv1,serv2,serv3,serv4,serv5,serv6]

        ancho_barras = 1.5
        espacio_entre_grupos = 8
        x=[2,4,6]
        x_vals = []
        for s in servidores:
            colors=["#E2854F","#C13228","#CE520A"]
            x=[i+espacio_entre_grupos for i in x]
            b = plt.bar(x,s,width=ancho_barras)
            [i.set_color(colors.pop(0)) for i in b]
            x_vals.append(x[1]) 
        plt.xticks(x_vals,["Servidor 1","Servidor 2", "Servidor 3", "Servidor 4", "Servidor 5", "Servidor 6"])
        plt.legend(handles=[Patch(facecolor=i[0],edgecolor=i[0],label=i[1]) for i in list(zip(["#E2854F","#C13228","#CE520A"],["Corrida 1","Corrida 2","Corrida 3"]))], bbox_to_anchor=(0.65, -0.05), ncol=3)
        plt.ylabel('u(t)')
        plt.title('Utilización promedio de servidores u(t) - Grafico de barras')
        plt.show()

        
        #Demora promedio del cliente d(t)
        plt.plot(res1.clocks, res1.demora_acumulada_array, color = '#7C8788', label = 'Clientes corrida 1')
        plt.plot(res2.clocks, res2.demora_acumulada_array, color = '#F9CF51', label = 'Clientes corrida 2')
        plt.plot(res3.clocks, res3.demora_acumulada_array, color = '#E26D5C', label = 'Clientes corrida 3')
        plt.legend(loc = 'best')
        plt.title('Demora promedio d(t) de los clientes')
        plt.xlabel('Reloj de la simulación')
        plt.ylabel('Demora promedio del cliente d(t)')
        plt.show()

        if res1.algoritmo == '32' or res1.algoritmo =='31':
            demora_acumulada_array = []
            demora_acumulada_array_prioridad = []
            clocks1 = []
            clocks2 = []
            len_demoras = min([len(res1.demora_acumulada_array), len(res2.demora_acumulada_array), len(res3.demora_acumulada_array)])
            len_demoras_prioridad = min([len(res1.demora_acumulada_prioridad_array), len(res2.demora_acumulada_prioridad_array), len(res3.demora_acumulada_prioridad_array)])
            for i in range (0, len_demoras):
                demora_acumulada_array_prioridad.append((res1.demora_acumulada_prioridad_array[i]+res2.demora_acumulada_prioridad_array[i]+res3.demora_acumulada_prioridad_array[i])/3)
                clocks1.append((res1.clocks[i] + res2.clocks[i] + res3.clocks[i])/3)
            for i in range (0, len_demoras_prioridad):
                demora_acumulada_array.append((res1.demora_acumulada_array[i]+res2.demora_acumulada_array[i]+res3.demora_acumulada_array[i])/3)
                clocks2.append((res1.clocks[i] + res2.clocks[i] + res3.clocks[i])/3)
            
            plt.plot(clocks2, demora_acumulada_array, color = '#F9CF51', label = 'Todos los clientes - promedio' )
            plt.plot(clocks1, demora_acumulada_array_prioridad, color = '#E26D5C', label = 'Clientes Prioritarios - Promedio')

            plt.legend(loc = 'best')
            plt.title('Demora promedio d(t) de clientes totales vs clientes prioritarios')
            plt.xlabel('Reloj de la simulación')
            plt.ylabel('Demora promedio del cliente d(t)')
            plt.show()
        
        #Cantidad promedio de clientes en cola q(t):

        fig3, axs3 = plt.subplots(1,2)
        
        plt.title('Cantidad promedio de clientes en cola q(t)')

        plt.subplot(2,1,1)
        plt.plot(res1.clocks, res1.colas[0].cant_cli_acum_array, color = '#7C8788', label = 'Corrida 1')
        plt.plot(res2.clocks, res2.colas[0].cant_cli_acum_array, color = '#F9CF51', label = 'Corrida 2')
        plt.plot(res3.clocks, res3.colas[0].cant_cli_acum_array, color = '#E26D5C', label = 'Corrida 3')
        plt.title('Cola 0')
        plt.ylabel('q(t)')
        plt.xlabel('Reloj de la simulación')
        plt.legend(loc = 'best')
        
        plt.subplot(2,1,2)
        plt.plot(res1.clocks, res1.colas[1].cant_cli_acum_array, color = '#7C8788', label = 'Corrida 1')
        plt.plot(res2.clocks, res2.colas[1].cant_cli_acum_array, color = '#F9CF51', label = 'Corrida 2')
        plt.plot(res3.clocks, res3.colas[1].cant_cli_acum_array, color = '#E26D5C', label = 'Corrida 3')
        plt.title('Cola 1')
        plt.xlabel('Reloj de la simulación')
        plt.ylabel('q(t)')
        plt.legend(loc = 'best')

        
        plt.show()
        
        #Cantidad promedio de clientes en cola q(t) - Grafico de barras

        q0 = res1.colas[0].cant_cli_acum/res1.clock
        q1 = res1.colas[1].cant_cli_acum/res1.clock
        q4 = res2.colas[0].cant_cli_acum/res2.clock
        q5 = res2.colas[1].cant_cli_acum/res2.clock
        q8 = res3.colas[0].cant_cli_acum/res3.clock
        q9 = res3.colas[1].cant_cli_acum/res3.clock

        cola0 =[q0, q4 ,q8]
        cola1 = [q1, q5, q9]
        colas = [cola0,cola1]

        ancho_barras = 1.5
        espacio_entre_grupos = 8
        x=[2,4,6]
        x_vals = []
        for c in colas:
            colors=["#E2854F","#C13228","#CE520A"]
            x=[i+espacio_entre_grupos for i in x]
            b = plt.bar(x,c,width=ancho_barras)
            [i.set_color(colors.pop(0)) for i in b]
            x_vals.append(x[1]) 
        plt.xticks(x_vals,["Cola 0","Cola 1"])
        plt.legend(handles=[Patch(facecolor=i[0],edgecolor=i[0],label=i[1]) for i in list(zip(["#E2854F","#C13228","#CE520A"],["Corrida 1","Corrida 2","Corrida 3"]))])
        plt.ylabel('q(t)')
        plt.title('Cantidad promedio de clientes en cola q(t) - Grafico de barras')
        plt.show()


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
    sim1 = Simulacion(True, algoritmo)
    res1 = sim1.programa_principal()
    sim2 = Simulacion(True, algoritmo)
    res2 = sim2.programa_principal()
    sim3 = Simulacion(True, algoritmo)
    res3 = sim3.programa_principal()
    plots(res1, res2, res3)

else:
    sim1 = Simulacion(False, algoritmo)
    res1 = sim1.programa_principal()
    sim2 = Simulacion(False, algoritmo)
    res2 = sim2.programa_principal()
    sim3 = Simulacion(False, algoritmo)
    res3 = sim3.programa_principal()
    plots(res1, res2, res3)


