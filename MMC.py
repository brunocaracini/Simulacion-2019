import numpy as np 

big_number = 9999999

class Cliente():
    def __init__(self):
        pass

class Servidor():
    def __init__(self,tms):
        self.tms = tms
        self.cliente = False

    def ingreso_servidor(self,cliente):
        pass

    def salida_servidor(self):
        self.cliente = False


class Cola():
    def __init__(self,clientes):
        self.clientes=clientes
    
    def ingreso_cola(self,cliente):
        pass

class Cola_Inicial(Cola):
    def __init__(self,clientes,tma):
        self.clientes=clientes
        self.tma=tma

class Linea():
    def __init__(self,colas_entrada,servidores):
        self.colas_entrada = colas_entrada
        self.servidores = servidores

class Simulacion():
    def __init__(self):
        self.reloj = 0
        self.nombres_eventos = ["Arribo", "Partida11", "Partida12", "Partida13", "Partida21", "Partida22", "Partida23"]
        l1 = Linea(Cola_Inicial(0,0.8), [Servidor(0.5),Servidor(0.5),Servidor(0.5)])
        l2 = Linea([Cola(0),Cola(0),Cola(0)], [Servidor(0.2),Servidor(0.4),Servidor(0.6)])
        self.lineas = [l1,l2]

        self.lista_eventos = []
        self.lista_eventos.append(np.random.exponential(1/self.lineas[0].colas_entrada.tma))
        for i in range(6):
            self.lista_eventos.append(big_number)


    def programa_principal(self):
        pass

    def tiempos(self):
        nro_evento = self.lista_eventos.index(min(self.lista_eventos))
        self.reloj = self.lista_eventos[nro_evento]
        self.eventos(self.nombres_eventos[nro_evento])



    def evitar_partidas_vacias(self):
        #si la cola esta vacio seteamos el tiempo de partida de ese servidor
        #a big_number para evitar partidas
        #si una cola esta vacia, se setean todas las partidas de los servidores vacios
        #directamente conectados a big_number
        pass

    def eventos(self,evento):
        if evento == "Arribo":
            cli = Cliente()
            nro_servidor = self.asignar_servidor()
            if nro_servidor:
                self.lineas[0].servidores[nro_servidor].ingreso_servidor(cli)
            else:
                self.lineas[0].colas_entrada.ingreso_cola(cli)

        elif evento == "Partida11":
            srv = self.lineas[0].servidores[0]
            cli = srv.cliente
            if cli:
                if self.lineas[1].servidores[0].cliente:
                    #Ingresa a la cola
                    self.lineas[1].colas_entrada[0].ingreso_cola(cli)
                else:
                    self.lineas[1].servidores[0].ingreso_servidor(cli)
            else:
                pass
            self.lineas[0].servidores[0].salida_servidor()

        elif evento == "Partida12":
            srv = self.lineas[0].servidores[1]
            cli = srv.cliente
            if cli:
                if self.lineas[1].servidores[1].cliente:
                    #Ingresa a la cola
                    self.lineas[1].colas_entrada[1].ingreso_cola(cli)
                else:
                    self.lineas[1].servidores[1].ingreso_servidor(cli)
            else:
                pass
            self.lineas[0].servidores[1].salida_servidor()

        elif evento == "Partida13":
            srv = self.lineas[0].servidores[2]
            cli = srv.cliente
            if cli:
                if self.lineas[1].servidores[2].cliente:
                    #Ingresa a la cola
                    self.lineas[1].colas_entrada[2].ingreso_cola(cli)
                else:
                    self.lineas[1].servidores[2].ingreso_servidor(cli)
            else:
                pass
            self.lineas[0].servidores[2].salida_servidor()
                
        elif evento == "Partida21":
            self.lineas[1].servidores[0].salida_servidor()

        elif evento == "Partida22":
            self.lineas[1].servidores[1].salida_servidor()

        elif evento == "Partida23":
            self.lineas[1].servidores[2].salida_servidor()
            
    def asignar_servidor(self):
        #Si todos los servidores estan ocupados, devuelve False
        #Sino, devuelve nro de servidor
        return False

    def reportes(self):
        pass


