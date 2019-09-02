import numpy as np
import random

infinito = 99999999999
tma = 0.8

class Cliente():
    def __init__(self):
        self.tiempo_entrada = 0
        self.tiempo_salida = 0

class Cola():
    def __init__(self):
        self.clientes = []

class Servidor():
    def __init__(self, estado, numero, tiempo_m_servicio):
        self.ocupado = estado
        self.cliente = False
        self.numero = numero
        self.tms = tiempo_m_servicio
        #En la funcion de ingreso al servidor (que vas a hacer porque sos buen programador)
        #Seteas el tiempo de entrada del cliente actual al reloj en el momento

        #Y en la funcion de salida del servidor (que tambien vas a hacer)
        #Le sumas al tiempo acumulado de servicio (clock - tiempo_entrada_cliente_actual)
        self.tiempo_acumulado_servicio = 0
        self.tiempo_entrada_cliente_actual = 0
    
class Evento():
    def __init__(self,tipo,tiempo):
        self.tipo = tipo
        self.tiempo = tiempo

class Simulacion():
    def __init__(self):
        self.clock = 0
        self.l_evento = [] 
        self.l_tiempo = []
        self.serv1 = Servidor(False, 1, 0.5)
        self.serv2 = Servidor(False, 2, 0.5)
        self.serv3 = Servidor(False, 3, 0.5)
        self.serv4 = Servidor(False, 4, 0.2)
        self.serv5 = Servidor(False, 5, 0.4)
        self.serv6 = Servidor(False, 6, 0.6)
        self.cola0 = Cola()
        self.cola1 = Cola()
        self.cola2 = Cola()
        self.cola3 = Cola()
        self.colas = [self.cola0,self.cola1,self.cola2,self.cola3]
        self.linea1 = [self.serv1, self.serv2, self.serv3]
        self.linea2 = [self.serv4, self.serv5, self.serv6]
        self.clientes_completaron_demora = 0

    def inicializacion(self):
        self.clock = 0  #Inicializamos el reloj en 0.
        tiempo = self.clock + np.random.exponential(1/tma)  #Calculamos el tiempo del primer arribo para inicializar la lista de eventos.
        prox_evento = Evento('arribo', tiempo) #Creamos un objeto del tipo evento, que recibe como parametro el tiempo calculado y el tipo de evento.
        self.l_evento[0] = prox_evento  #Asignamos el evento arribo que creamos en la posición 0 de la lista de eventos.
        for i in range(1,7): #Llenamos las posiciones restantes de la lista de eventos con partidas.
            tiempo = infinito #Ponemos el tiempo en infinito para estas partidas.
            prox_evento = Evento('partida', tiempo) #Creamos un objeto del tipo evento, que recibe como parametro el tiempo calculado y el tipo de evento.
            self.l_evento[i] = prox_evento # Asignamos el evento arribo que creamos en la posición i de la lista de eventos.


    def tiempos(self):
        i = 0
        for evento in self.l_evento: #En este for se obtiene el tiempo de todos los eventos de la lista de eventos, y lo guardamos en una lista de tiempos.
            i +=1
            self.l_tiempo[i] = evento.tiempo
        tiempo_prox_evento = min(self.l_tiempo) #Elegimos el mas chico de esa lista de tiempos.
        index_prox_evento = self.l_tiempo.index(tiempo_prox_evento) 
        evento = self.l_evento[index_prox_evento] #Buscamos el evento que corresponde a ese tiempo en la lista de eventos
        self.clock = evento.tiempo #Actualizamos el reloj a ese tiempo
        return [evento.tipo, index_prox_evento] #Devolvemos el tipo de evento.
        

    def eventos(self, evento_tipo, index_prox_evento):
        if evento_tipo == 'arribo':
            arribo()
        if evento_tipo == 'partida':
            partida(index_prox_evento)

        def arribo():
            tiempo = self.clock + np.random.exponential(1/tma) #Calcula el nuevo tiempo de arribo.
            prox_evento = Evento('arribo', tiempo) #Creamos un objeto del tipo Evento, que recibe como parametro el tiempo calculado y el tipo de evento.
            self.l_evento[0] = prox_evento #Asignamos el evento arribo que creamos en la posición 0 de la lista de eventos.
            cliente = Cliente() #Creamos un objeto del tipo Cliente.
            servidores_disponibles = [] #Creamos un arreglo vacío de servidores disponibles.
            for servidor in self.linea1: #Por cada uno de los servidores, se chequea si está ocupado o no y se añade a la lista de servidores disponibes.
                if servidor.ocupado == False:
                    servidores_disponibles.append(servidor)
            if len(servidores_disponibles) == 0: #Si no hubo ninguno disponible, se añade el cliente a a la cola.
                self.colas[0].clientes.append(cliente)
            else: 
                servidor = random.choice(servidores_disponibles) #Elegimos un servidor al azar de la lista de servidores disponibles.
                servidor.cliente = cliente  #Registramos que el elciente se encuentra en ese servidor
                servidor.ocupado = True #Actualizamos el estado de ocupación del servidor.
                index_serv = self.linea1.index(servidor)    
                self.linea1[index_serv] = servidor #Actualizamos los datos del servidor igualandolo a la copia.
                tiempo = self.clock + np.random.exponential(1/servidor.tms)
                prox_partida = Evento('partida', tiempo)
                self.l_evento[servidor.numero] = prox_partida
                 
        def partida(index_prox_evento):
            if index_prox_evento in [1,2,3]:

                cliente = self.linea1[index_prox_evento - 1].cliente
                if self.linea2[index_prox_evento - 1].ocupado == True:
                    self.colas[index_prox_evento].clientes.append(cliente)
                else:
                    self.linea2[index_prox_evento - 1].cliente = cliente
                    tiempo = self.clock + np.random.exponential(1/servidor.tms)
                    prox_partida = Evento('partida', tiempo)
                    self.l_evento[index_prox_evento] = prox_partida
                    
                self.linea1[index_prox_evento - 1].cliente = False   
                self.linea1[index_prox_evento - 1].ocupado == False

                if len(self.colas[0]) == 0:
                    prox_partida = Evento('partida', infinito)
                    self.l_evento[index_prox_evento] = prox_partida
                else:
                    cliente = self.colas[0].clientes.pop()
                    self.linea1[index_prox_evento - 1].cliente = cliente
                    tiempo = self.clock + np.random.exponential(1/servidor.tms)
                    prox_partida = Evento('partida', tiempo)
                    self.l_evento[index_prox_evento] = prox_partida

            else:
                if len(self.colas[index_prox_evento - 3]) == 0:
                    prox_partida = Evento('partida', infinito)
                    self.l_evento[index_prox_evento] = prox_partida
                else:
                    cliente = self.colas[index_prox_evento - 3].pop()
                    self.linea2[index_prox_evento - 4].cliente = cliente
                    tiempo = self.clock + np.random.exponential(1/servidor.tms)
                    prox_partida = Evento('partida', tiempo)
                    self.l_evento[index_prox_evento] = prox_partida

                self.linea2[index_prox_evento - 4].cliente = False
                self.linea2[index_prox_evento - 4].ocupado = False

                    


                


                
                    
                
    def reportes(self):
        pass    
            
    def programa_principal(self):
        #LLamamos a la rutina de inicialización.
        self.inicializacion()

        #Llamamos a la rutina de tiempos, que devuelve el proximo evento, y lo guardamos en una variable.
        array = self.tiempos()
        tipo_prox_evento = array[0]
        index_prox_evento = array[1]
        
        #LLamamos a la rutina de eventos, y le mandamos como parámetro el tipo de evento del proximo evento.
        self.eventos(tipo_prox_evento, index_prox_evento)



        
              




