import numpy as np 

class sim():
    reloj, ts_acumulado, demora_acumulada, area_q_t, tiempo_ultimo_evento = 0.0,0.0,0.0,0.0,0.0
    nro_clientes_cola, completaron_demora, paso = 0,0,0
    tm_entre_arribos = 7.0
    tm_servicio = 9.0
    iniciado = False
    estado_servidor = "" #D - disponible | O - ocupado
    proximo_evento = ""  #A - Arribo | P - partida
    lista_eventos = []
    cola = []

def inicializar():
    sim.estado_servidor = "D"
    sim.proximo_evento = ""
    sim.reloj, sim.ts_acumulado, sim.demora_acumulada, sim.area_q_t, sim.tiempo_ultimo_evento = 0.0,0.0,0.0,0.0,0.0
    sim.nro_clientes_cola, sim.completaron_demora, sim.paso = 0,0,0
    
    #Tiempo del primer arribo
    sim.lista_eventos.append(np.random.exponential(1/sim.tm_entre_arribos))

    #numero grande para asegurar que el primer evento sea un arribo
    sim.lista_eventos.append(99999999)
    sim.iniciado = False

def run():
    print("Inicializando simulacion")
    inicializar()
    while sim.reloj < 50 or sim.nro_clientes_cola != 0 or sim.estado_servidor != "D":
        print("reloj: ",sim.reloj)
        tiempos()
        
        if sim.proximo_evento == "A":
            arribo()
        else:
            partida()

    reportes()

def tiempos():
    sim.tiempo_ultimo_evento = sim.reloj
    if sim.lista_eventos[0] <= sim.lista_eventos[1]:
        sim.reloj = sim.lista_eventos[0]
        sim.proximo_evento = "A"
    else:
        sim.reloj = sim.lista_eventos[1]
        sim.proximo_evento = "P"

def arribo():
    sim.lista_eventos[0] = sim.reloj + np.random.exponential(1/sim.tm_entre_arribos)
    if sim.estado_servidor == "D":
        sim.estado_servidor = "O"
        sim.lista_eventos[1] = sim.reloj + np.random.exponential(1/sim.tm_servicio)
        sim.ts_acumulado += (sim.lista_eventos[1] - sim.reloj)
        sim.completaron_demora += 1
    else:
        sim.area_q_t += sim.nro_clientes_cola * (sim.reloj - sim.tiempo_ultimo_evento)
        sim.nro_clientes_cola += 1
        sim.cola.append(sim.reloj)


def partida():
    if sim.nro_clientes_cola > 0:
        sim.lista_eventos[1] = sim.reloj + np.random.exponential(1/sim.tm_servicio)
        sim.demora_acumulada += sim.reloj - sim.cola[0]
        sim.completaron_demora += 1
        sim.ts_acumulado += sim.lista_eventos[1] - sim.reloj
        sim.area_q_t += (sim.nro_clientes_cola * (sim.reloj - sim.tiempo_ultimo_evento))
        sim.nro_clientes_cola -= 1
        sim.cola.pop(0)
    else:
        sim.estado_servidor = "D"
        sim.lista_eventos[1] = 99999999


def reportes():
    if sim.reloj != 0:
        nro_clientes_prom_cola = sim.area_q_t/sim.reloj
    else:
        nro_clientes_prom_cola = 0

    print("Cantidad promedio de clientes en cola: ", nro_clientes_prom_cola)

    if sim.reloj != 0:
        uilizacion_prom_servidor = sim.ts_acumulado/sim.reloj
    else:
        uilizacion_prom_servidor = 0

    print("Utilizacion promedio del servidor: ", uilizacion_prom_servidor)

    if sim.completaron_demora != 0:
        demora_prom_cliente = sim.demora_acumulada/sim.completaron_demora
    else:
        demora_prom_cliente = 0

    print("Demora promedio de cliente: ", demora_prom_cliente)

run()