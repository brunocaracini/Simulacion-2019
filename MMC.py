class Cliente():
    def __init__(self):
        pass

class Servidor():
    def __init__(self,tms,estado):
        self.tms = tms
        self.estado = estado

class Cola_Inicial():
    def __init__(self,clientes,tma):
        self.clientes=clientes
        self.tma=tma

class Cola():
    def __init__(self,clientes):
        self.clientes=clientes

class Linea():
    def __init__(self,entrada,servidores):
        self.entrada = entrada
        self.servidores = servidores

class Simulacion():
    def __init__(self):
        l1 = Linea(Cola_Inicial(0,0.8), [Servidor(0.5,"D"),Servidor(0.5,"D"),Servidor(0.5,"D")])
        l2 = Linea([Cola(0),Cola(0),Cola(0)], [Servidor(0.2,"D"),Servidor(0.4,"D"),Servidor(0.6,"D")])
        self.lineas = [l1,l2]

    def run(self):
        pass

    def tiempos(self):
        pass

    def reportes(self):
        pass


