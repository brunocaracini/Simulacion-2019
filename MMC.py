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
        self.q_t = 0
    
    def calcular_q_t(self,reloj,tue):
        self.q_t += len(self.clientes) * (reloj - tue)

    def ingreso_cola(self,cliente):
        self.clientes.append(cliente)

    def salida_cola(self):
        self.cantidad_clientes += 1
        return self.clientes.pop()


class Cola_Inicial(Cola):
    def __init__(self,clientes,tma):
        Cola.__init__(self,clientes)
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
        self.tiempo_ultimo_evento = 0

        #creamos la topologia de la simulacion, estableciendo las lineas, servidores, y colas
        l1 = Linea(Cola_Inicial([],0.8), [Servidor(0.5),Servidor(0.5),Servidor(0.5)])
        l2 = Linea([Cola([]),Cola([]),Cola([])], [Servidor(0.2),Servidor(0.4),Servidor(0.6)])
        self.lineas = [l1,l2]

        #Creamos la lista de eventos, estableciendo todas las partidas en big_number para evitar partidas de servidores desocupados
        self.lista_eventos = []
        self.lista_eventos.append(np.random.exponential(self.lineas[0].colas_entrada.tma))
        for _ in self.nombres_eventos[1:]:
            self.lista_eventos.append(big_number)


    def programa_principal(self):
        """
        Llama a las subrutinas de la simulacion
        E itera hasta que se cumplen las condiciones de finalizacion
        """
        while(self.reloj<50):
            print(self.lista_eventos)
            nro_evento = self.tiempos()
            self.eventos(nro_evento)
            self.diagnostico()
        self.reportes()


    def tiempos(self):
        """
        Avanza el reloj hasta el siguiente evento y devuelve el evento correspondiente
        """
        nro_evento = self.lista_eventos.index(min(self.lista_eventos))
        self.tiempo_ultimo_evento = self.reloj
        self.reloj = self.lista_eventos[nro_evento]
        return nro_evento


    def eventos(self,nro_evento):
        """
        Se llama con el argumento del evento correspondiente
        Actualiza el estado del sistema de acuerdo al evento
        Al ocurrir un evento, actualiza lista_eventos
        """

                
        def arribo():
            self.lista_eventos[nro_evento] = self.reloj + np.random.exponential(self.lineas[0].colas_entrada.tma)
            cli = Cliente(self.reloj)
            nro_servidor = self.asignar_servidor()
            if nro_servidor:
                nro_servidor -= 1
                self.lista_eventos[nro_servidor+1] = self.reloj + np.random.exponential(self.lineas[0].servidores[nro_servidor].tms)
                self.lineas[0].servidores[nro_servidor].ingreso_servidor(cli,self.reloj)
            else:
                self.lineas[0].colas_entrada.ingreso_cola(cli)

        def partidas(s):
            #obtenemos el nro de linea y de servidor del nombre del evento
            n_linea, n_servidor = int(s[-2])-1 ,int(s[-1])-1
            self.lista_eventos[nro_evento] = self.reloj + np.random.exponential(self.lineas[n_linea].servidores[n_servidor].tms)
            #partida de primera linea:
            if n_linea == 0:
                srv = self.lineas[0].servidores[n_servidor]
                cli = srv.cliente
                if cli:
                    if self.lineas[1].servidores[n_servidor].cliente:
                        #Ingresa a la cola
                        self.lineas[1].colas_entrada[n_servidor].ingreso_cola(cli)
                    else:
                        self.lista_eventos[n_servidor+4] = self.reloj + np.random.exponential(self.lineas[n_linea].servidores[n_servidor].tms)
                        self.lineas[1].servidores[n_servidor].ingreso_servidor(cli,self.reloj)
                else:
                    pass
                self.lineas[0].servidores[n_servidor].salida_servidor(self.reloj)

                if self.lineas[0].colas_entrada.clientes == []:
                    self.lista_eventos[n_servidor+1] = big_number
                else:
                    self.lineas[0].servidores[n_servidor].ingreso_servidor(self.lineas[0].colas_entrada.salida_cola(), self.reloj)

            elif n_linea == 1:
                self.clientes.append(self.lineas[1].servidores[n_servidor].cliente)
                self.lineas[1].servidores[n_servidor].cliente.salida_sistema(self.reloj)
                self.lineas[1].servidores[n_servidor].salida_servidor(self.reloj)

                if self.lineas[1].colas_entrada[n_servidor].clientes == []:
                    self.lista_eventos[n_servidor+4] = big_number
                else:
                    self.lineas[1].servidores[n_servidor].ingreso_servidor(self.lineas[1].colas_entrada[n_servidor].salida_cola(),self.reloj)
        
        def actualizar_q_t():
            self.lineas[0].colas_entrada.calcular_q_t(self.reloj,self.tiempo_ultimo_evento)
            for cola in self.lineas[1].colas_entrada:
                cola.calcular_q_t(self.reloj,self.tiempo_ultimo_evento)

        actualizar_q_t()
        evento = self.nombres_eventos[nro_evento]   
        if evento == "Arribo":
            arribo()
        else:
            partidas(evento)
    
            
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
            if not self.lineas[0].servidores[nro_servidor-1].cliente:
                return nro_servidor
        return False


    def reportes(self):
        """
        Genera los reportes estadisticos al finalizar la simulacion
        """
        print()
        print("="*40)
        print()
        utilizacion_servidores = []
        for l in self.lineas:
            for s in l.servidores:
                utilizacion_servidores.append(s.tiempo_servicio_acumulado/self.reloj)

        demora_clientes = []
        for cli in self.clientes:
            demora_clientes.append(cli.demora)

        promedio_clientes_cola_l1 = self.lineas[0].colas_entrada.q_t / self.reloj
        promedio_clientes_cola_l2 = [(c.q_t/self.reloj) for c in self.lineas[1].colas_entrada]
        
        p_ut = np.average(utilizacion_servidores)
        p_dm = np.average(demora_clientes)
        pcc1 = promedio_clientes_cola_l1
        pcc2 = np.average(promedio_clientes_cola_l2)

        print(p_dm)
        print("Prom clientes en cola de entrada: ",pcc1)
        print("Prom clientes en cola l2: ",promedio_clientes_cola_l2)
        print(utilizacion_servidores)
        #print(p_ut,"\n",p_dm,"\n",pcc1,"\n",pcc2)

    def diagnostico(self):
        print("Cola entrada: ", len(self.lineas[0].colas_entrada.clientes))
        print("Servidor 0,0: ", self.lineas[0].servidores[0].cliente)
        print("Servidor 0,1: ", self.lineas[0].servidores[1].cliente)
        print("Servidor 0,2: ", self.lineas[0].servidores[2].cliente)
        print("Cola 0: ", len(self.lineas[1].colas_entrada[0].clientes))
        print("Servidor 1,0: ", self.lineas[1].servidores[0].cliente)
        print("Cola 1: ", len(self.lineas[1].colas_entrada[1].clientes))
        print("Servidor 1,1: ", self.lineas[1].servidores[1].cliente)
        print("Cola 2: ", len(self.lineas[1].colas_entrada[2].clientes))
        print("Servidor 1,2: ", self.lineas[1].servidores[2].cliente)


sim = Simulacion()
sim.programa_principal()