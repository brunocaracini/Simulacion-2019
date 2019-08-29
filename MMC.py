import numpy as np 

big_number = 9999999

class Cliente():
    def __init__(self,t_entrada):
        self.demora = 0
        self.t_entrada = t_entrada

    def salida_sistema(self,reloj):
        self.demora = reloj - self.t_entrada



class Servidor():
    def __init__(self,tms):
        self.tms = tms
        self.cliente = False
        self.tiempo_servicio_acumulado = 0
        self.tiempo_entrada_actual = False

    def ingreso_servidor(self,cliente,reloj):
        self.cliente = cliente
        self.tiempo_entrada_actual = reloj

    def salida_servidor(self,reloj):
        self.cliente = False
        self.tiempo_servicio_acumulado += (reloj - self.tiempo_entrada_actual)


class Cola():
    def __init__(self,clientes):
        self.clientes = clientes
        self.cantidad_clientes = 0
    
    def ingreso_cola(self,cliente):
        self.clientes.append(cliente)

    def salida_cola(self):
        self.cantidad_clientes += 1
        return self.clientes.pop()


class Cola_Inicial(Cola):
    def __init__(self,clientes,tma):
        self.clientes = clientes
        self.tma = tma


class Linea():
    def __init__(self,colas_entrada,servidores):
        self.colas_entrada = colas_entrada
        self.servidores = servidores


class Simulacion():
    def __init__(self):
        """
        Establece la topologia de la simulacion
        Inicializa la simulacion en t = 0
        Establece la lista de eventos y sus tiempos iniciales 
        """
        self.reloj = 0
        #creamos una lista de nombres para llamar al evento correspondiente de lista_eventos
        self.nombres_eventos = ["Arribo", "Partida11", "Partida12", "Partida13", "Partida21", "Partida22", "Partida23"]
        self.clientes = []

        #creamos la topologia de la simulacion, estableciendo las lineas, servidores, y colas
        l1 = Linea(Cola_Inicial([],0.8), [Servidor(0.5),Servidor(0.5),Servidor(0.5)])
        l2 = Linea([Cola([]),Cola([]),Cola([])], [Servidor(0.2),Servidor(0.4),Servidor(0.6)])
        self.lineas = [l1,l2]

        #Creamos la lista de eventos, estableciendo todas las partidas en big_number para evitar partidas de servidores desocupados
        self.lista_eventos = []
        self.lista_eventos.append(np.random.exponential(1/self.lineas[0].colas_entrada.tma))
        for _ in self.nombres_eventos[1:]:
            self.lista_eventos.append(big_number)


    def programa_principal(self):
        """
        Llama a las subrutinas de la simulacion
        E itera hasta que se cumplen las condiciones de finalizacion
        """
        while(False):
            nro_evento = self.tiempos()
            self.eventos(nro_evento)
        self.reportes()


    def tiempos(self):
        """
        Avanza el reloj hasta el siguiente evento y devuelve el evento correspondiente
        """
        nro_evento = self.lista_eventos.index(min(self.lista_eventos))
        self.reloj = self.lista_eventos[nro_evento]
        return nro_evento


    def eventos(self,nro_evento):
        """
        Se llama con el argumento del evento correspondiente
        Actualiza el estado del sistema de acuerdo al evento
        Al ocurrir un evento, actualiza lista_eventos
        """
        evento = self.nombres_eventos[nro_evento]   

        if evento == "Arribo":
            arribo()
        else:
            partidas(evento)
        
        def arribo():
            self.lista_eventos[nro_evento] = self.reloj + np.random.exponential(1/self.lineas[0].colas_entrada.tma)
            cli = Cliente()
            nro_servidor = self.asignar_servidor()
            if nro_servidor:
                nro_servidor -= 1
                self.lista_eventos[nro_servidor+1] = self.reloj + np.random.exponential(1/self.lineas[0].servidores[nro_servidor].tms)
                self.lineas[0].servidores[nro_servidor].ingreso_servidor(cli,self.reloj)
            else:
                self.lineas[0].colas_entrada.ingreso_cola(cli)

        def partidas(s):
            n_linea, n_servidor = int(s[-2])-1 ,int(s[-1])-1
            self.lista_eventos[nro_evento] = self.reloj + np.random.exponential(1/self.lineas[n_linea].servidores[n_servidor].tms)
            if n_linea == 0:
                srv = self.lineas[0].servidores[n_servidor]
                cli = srv.cliente
                if cli:
                    if self.lineas[1].servidores[n_servidor].cliente:
                        #Ingresa a la cola
                        self.lineas[1].colas_entrada[n_servidor].ingreso_cola(cli)
                    else:
                        self.lineas[1].servidores[n_servidor].ingreso_servidor(cli,self.reloj)
                else:
                    pass
                self.lineas[0].servidores[n_servidor].salida_servidor(self.reloj)

                if self.lineas[0].colas_entrada.clientes == []:
                    self.lista_eventos[n_servidor+1] = big_number
                else:
                    self.lineas[0].servidores[n_servidor].ingreso_servidor(self.lineas[0].colas_entrada.salida_cola())

            elif n_linea == 1:
                self.lineas[1].servidores[n_servidor].cliente.salida_sistema(self.reloj)
                self.lineas[1].servidores[n_servidor].salida_servidor(self.reloj)

                if self.lineas[1].colas_entrada[n_servidor].clientes == []:
                    self.lista_eventos[n_servidor+4] = big_number
                else:
                    self.lineas[1].servidores[n_servidor].ingreso_servidor(self.lineas[1].colas_entrada[n_servidor].salida_cola())

    
            
    def asignar_servidor(self):
        """
        Establece una lista de prioridades para comprobar la disponibilidad de los servidores
        de la primer linea y asigna el servidor correspondiente
        """
        #Si todos los servidores estan ocupados, devuelve False
        #Sino, devuelve nro de servidor
        servidores = [1,2,3]
        np.random.shuffle(servidores)
        for nro_servidor in servidores:
            if not self.lineas[0].servidores[nro_servidor].clientes:
                return nro_servidor
        return False


    def reportes(self):
        """
        Genera los reportes estadisticos al finalizar la simulacion
        """
        utilizacion_servidores = []
        for l in self.lineas:
            for s in l.servidores:
                utilizacion_servidores.append(s.tiempo_servicio_acumulado/self.reloj)

        demora_clientes = []
        for cli in self.clientes:
            demora_clientes.append(cli.demora)

        promedio_clientes_cola_l1 = self.lineas[0].colas_entrada.cantidad_clientes / self.reloj
        promedio_clientes_cola_l2 = [(c.cantidad_clientes/self.reloj) for c in self.lineas[1].colas_entrada]

        p_ut = np.average(utilizacion_servidores)
        p_dm = np.average(demora_clientes)
        pcc1 = promedio_clientes_cola_l1
        pcc2 = np.average(promedio_clientes_cola_l2)

        print(p_ut,"\n",p_dm,"\n",pcc1,"\n",pcc2)


sim = Simulacion()
sim.programa_principal()