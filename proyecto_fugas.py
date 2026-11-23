#Proyecto final: Sistema de priorizacion de reparaciones de fugas de agua en Cajamarca
#Curso: Analisis de Algoritmos y Estrategias de Programacion - UPN 2026-2
#Integrantes:
#  Cachi Tantalean, Anderson Alexis
#  Chihuanhuaylla Trujillo, Hector Dylan
#  Chuquimango Verastegui, Jhocep Jhanpier
#  Cruz Lopez, Sara Elizabeth
#  Gamarra Olmedo, Alyson Adriana
#  Garcia Ahuanari, Luis Gerardo
#  Herrera Saavedra, Adriel Sebastian
#  Marin Diaz, Angel Eloy
#  Rojas Valdivia, Jhann Frank
#  Vasquez Villazon, Joseph Emanuel
"""
Problema:
Se detectaron 12 fugas de agua en Cajamarca (caso simulado), pero el dinero
y las horas de trabajo no alcanzan para repararlas todas.
Hay que decidir que fugas se reparan (COMPLETA) y cuales esperan (PENDIENTE).

Restricciones:
1. Presupuesto: S/ 10000
2. Tiempo: 48 horas-persona que se pueden pagar (plazo de 48 horas)
3. Una fuga se repara completa o no se repara (no hay reparaciones a medias)
4. Las fugas de riesgo Critico van primero (prioridad de emergencia)
5. Ninguna fuga puede pedir mas de 4 trabajadores

Beneficio de una fuga = caudal (m3/dia) x peso del riesgo
Critico = 4, Alto = 3, Medio = 2, Bajo = 1
ejemplo: F01 -> 38 m3/dia x 4 = 152

QUE USAMOS DE CADA SEMANA DEL CURSO
---------------------------------------------------------------------------
Semana 1  | Variables snake_case, tipos de datos y operaciones (//, %, round)
Semana 2  | Funciones (def, return), listas (append, for, in) y menu con match
Semana 3  | Diccionarios (cada fuga es un diccionario) y fuerza bruta
          | (05_fb_viajero.py: probar todas las opciones y quedarse con la mejor)
Semana 4  | Ordenamiento burbuja (ver las fugas ordenadas por prioridad)
Semana 5  | Busqueda binaria (buscar una fuga por su codigo)
Semana 7  | Algoritmo voraz (01_alg_voraz.py: cambio de monedas) y
          | cola de prioridad con heapq (03_mod_heapq.py) para las emergencias
Semana 8  | Recursividad: caso base y caso recursivo (01_alg_rec.py, 06_suma_lista.py)
Semana 9  | Divide y venceras: dividir en subproblemas y combinar (01_intro_dyc.py)
          | y conteo con diccionario (02_moda_vector.py)
Proyecto  | Programacion dinamica = recursividad (Sem 8) + subproblemas (Sem 9)
          | + guardar los resultados en un diccionario (Sem 3) para no repetirlos
---------------------------------------------------------------------------

DONDE ESTA CADA COSA EN ESTE ARCHIVO
- Funciones de apoyo: preparar_fugas, suma_recursiva, calcular_totales, contar_por_riesgo
- Semana 4 y 5: ordenamiento_burbuja y busqueda_binaria
- PASO 1 (las dos estrategias): reparar_emergencias con heapq
- ESTRATEGIA 01: alg_voraz
- ESTRATEGIA 02: prog_dinamica
- Comprobacion: fuerza_bruta
- Sistema: resolver, comparar, prueba_tiempos y el menu (al final)
"""
import heapq #Semana 7 - modulo heapq (03_mod_heapq.py)
import time #para medir cuanto demora cada algoritmo
import random #para crear casos de prueba
import sys
import tracemalloc #para medir la memoria que usa cada estrategia (lo vimos en la documentacion de Python)
from itertools import combinations #Semana 3 - igual que permutations del viajero

sys.setrecursionlimit(10000) #la recursion de la PD puede bajar varios niveles

#aqui se guarda cuantos subproblemas uso la ultima ejecucion de la PD (para comparar memoria)
info_pd = {"calculados": 0, "reutilizados": 0}


#---------------------------------------------------------------
# DATOS DE APOYO
#---------------------------------------------------------------
#Semana 2 - Funciones: def + return
#Semana 3 - Diccionarios: fuga["clave"] y peso_riesgo.get(...)
def preparar_fugas(fugas):
    print("Calculando horas-persona y beneficio de cada fuga")
    for fuga in fugas: #Semana 2 - recorrer una lista con for
        fuga["hp"] = fuga["trab"] * fuga["horas"] #Semana 1 - multiplicacion
        peso = peso_riesgo.get(fuga["riesgo"], 1) #Semana 3 - .get con valor por defecto
        fuga["beneficio"] = fuga["caudal"] * peso
        print(f"{fuga['id']}: hp = {fuga['trab']} x {fuga['horas']} = {fuga['hp']}, "
              f"beneficio = {fuga['caudal']} x {peso} = {fuga['beneficio']}")
        if fuga["trab"] > trabajadores:
            print(f"OJO: {fuga['id']} pide {fuga['trab']} trabajadores y solo hay {trabajadores}")
    return fugas


#Semana 8 - Recursividad (06_suma_lista.py: suma de una lista)
#suma el campo pedido de todas las fugas de la lista
def suma_recursiva(lista, campo):
    if len(lista) == 0: #caso base
        return 0
    else: #caso recursivo
        return lista[0][campo] + suma_recursiva(lista[1:], campo)
        #   F01 + suma([F02, F03...]) -> F02 + suma([F03...]) -> ... -> 0


def calcular_totales(lista):
    costo = suma_recursiva(lista, "costo")
    hp = suma_recursiva(lista, "hp")
    beneficio = suma_recursiva(lista, "beneficio")
    caudal = suma_recursiva(lista, "caudal")
    return costo, hp, beneficio, caudal


#Semana 9 - Conteo con diccionario (02_moda_vector.py)
#cuenta cuantas fugas hay de cada nivel de riesgo
def contar_por_riesgo(fugas):
    conteo = {}
    for fuga in fugas:
        if not fuga["riesgo"] in conteo:
            conteo[fuga["riesgo"]] = 1
        else:
            conteo[fuga["riesgo"]] += 1
    mas_comun = max(conteo, key=conteo.get) #igual que la moda
    return conteo, mas_comun


def mostrar_fugas(fugas):
    print("-" * 95)
    print(f"{'ID':<4} {'Ubicacion':<28} {'Riesgo':<8} {'Caudal':>6} {'Costo':>6} {'Trab':>5} {'Horas':>5} {'HP':>4} {'Benef':>6}")
    print("-" * 95)
    for fuga in fugas:
        print(f"{fuga['id']:<4} {fuga['ubicacion']:<28} {fuga['riesgo']:<8} {fuga['caudal']:>6} {fuga['costo']:>6} "
              f"{fuga['trab']:>5} {fuga['horas']:>5} {fuga['hp']:>4} {fuga['beneficio']:>6}")
    costo, hp, beneficio, caudal = calcular_totales(fugas)
    print("-" * 95)
    print(f"{'TOTAL':<41} {caudal:>6} {costo:>6} {'':>5} {'':>5} {hp:>4} {beneficio:>6}")
    conteo, mas_comun = contar_por_riesgo(fugas)
    print(f"\nFugas por riesgo: {conteo}")
    print(f"\nTenemos S/ {presupuesto} y {horas_persona} horas-persona")
    #Semana 1 - operaciones: resta y round para el porcentaje
    print(f"Para reparar todo faltan S/ {costo - presupuesto} ({round((costo / presupuesto - 1) * 100, 1)} % mas) "
          f"y {hp - horas_persona} horas-persona ({round((hp / horas_persona - 1) * 100, 1)} % mas)")


#---------------------------------------------------------------
# Semana 4 - ORDENAMIENTO BURBUJA (01_ord_burbuja.py)
#---------------------------------------------------------------
def ordenamiento_burbuja(lista):
    """
    Compara cada fuga con la siguiente y si la siguiente tiene mas beneficio
    las intercambia. Asi, al final quedan de mayor a menor beneficio.
    """
    n = len(lista)
    for i in range(n - 1): #i = 0,1,2...
        for j in range(n - 1 - i):
            #   beneficio de la izquierda < beneficio de la derecha -> intercambiar
            if lista[j]["beneficio"] < lista[j + 1]["beneficio"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def mostrar_por_prioridad(fugas):
    ordenadas = ordenamiento_burbuja(fugas.copy()) #copy para no cambiar la lista original
    print("\nFugas ordenadas de mayor a menor beneficio (prioridad):")
    for i in range(len(ordenadas)):
        fuga = ordenadas[i]
        print(f"{i + 1:>2}. {fuga['id']}  beneficio {fuga['beneficio']:>4}  {fuga['riesgo']:<8} {fuga['ubicacion']}")


#---------------------------------------------------------------
# Semana 5 - BUSQUEDA BINARIA (busq_binaria.py)
#---------------------------------------------------------------
def busqueda_binaria(lista, objetivo):
    """
    --> solo funciona si la lista esta ordenada (F01, F02, F03...)
    1. Tomamos la fuga del medio (// division entera)
    2. si es la que buscamos, fin
    3. si el codigo buscado es menor, seguimos en la mitad izquierda
    4. si es mayor, seguimos en la mitad derecha
    """
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2 #(0+11)//2 = 5
        valor_medio = lista[medio]["id"]
        print(f"Indice medio: {medio}, codigo en el medio: {valor_medio}")
        if valor_medio == objetivo:
            print("--> Encontrado en el medio")
            return medio
        elif objetivo < valor_medio:
            derecha = medio - 1
        else:
            izquierda = medio + 1
        print(f"Limites: izquierda: {izquierda}, derecha: {derecha}")
    print("No se encontro la fuga")
    return -1


def buscar_fuga(fugas):
    codigo = input("Ingrese el codigo de la fuga (ej. F05): ").strip().upper()
    posicion = busqueda_binaria(fugas, codigo)
    if posicion != -1:
        fuga = fugas[posicion]
        print(f"""
╔══════════════════════════════════════════════╗
║   Fuga {fuga['id']}
╚══════════════════════════════════════════════╝
║   Ubicacion: {fuga['ubicacion']}
║   Riesgo: {fuga['riesgo']}
║   Caudal perdido: {fuga['caudal']} m3/dia ({fuga['caudal'] * 1000} litros)
║   Costo: S/ {fuga['costo']}
║   Cuadrilla: {fuga['trab']} trabajadores x {fuga['horas']} horas = {fuga['hp']} h-p
║   Beneficio: {fuga['beneficio']}
╚══════════════════════════════════════════════╝""")


#---------------------------------------------------------------
# PASO 1: EMERGENCIAS (lo usan las dos estrategias)
# Semana 7 - Cola de prioridad con heapq (03_mod_heapq.py)
#---------------------------------------------------------------
def reparar_emergencias(fugas, presupuesto, horas, mostrar=True):
    """
    1. Meter las fugas criticas a una cola de prioridad (heapq)
    2. heapq saca primero el MENOR, por eso guardamos el beneficio en negativo
       asi sale primero la fuga critica con MAS beneficio
    3. Si alcanza el dinero y las horas, se repara
    """
    heap = []
    for i in range(len(fugas)):
        if fugas[i]["riesgo"] == "Critico":
            heapq.heappush(heap, (-fugas[i]["beneficio"], i)) #heappush: agregar con prioridad
    if mostrar:
        print(f"Cola de emergencias (beneficio negativo, posicion): {heap}")
    elegidas = []
    while heap:
        menos_beneficio, i = heapq.heappop(heap) #heappop: sacar el prioritario
        fuga = fugas[i]
        if mostrar:
            print(f"Sale de la cola: {fuga['id']} con beneficio {-menos_beneficio}")
        if fuga["costo"] <= presupuesto and fuga["hp"] <= horas:
            elegidas.append(fuga)
            presupuesto -= fuga["costo"]
            horas -= fuga["hp"]
            if mostrar:
                print(f"Reparamos {fuga['id']}. Quedan S/ {presupuesto} y {horas} horas-persona")
        else:
            if mostrar:
                print(f"{fuga['id']} no alcanza, queda pendiente")
    restantes = []
    for fuga in fugas:
        if fuga not in elegidas: #Semana 2 - operador in
            restantes.append(fuga)
    return elegidas, restantes, presupuesto, horas


#---------------------------------------------------------------
# ESTRATEGIA 01 - PASO 2: ALGORITMO VORAZ
# Semana 7 - Algoritmo voraz (01_alg_voraz.py: cambio de monedas)
#---------------------------------------------------------------
def alg_voraz(fugas, presupuesto, horas, mostrar=True):
    """
    Es la decision mas rapida, aunque no siempre es la mejor
    Elige lo mejor que tiene en el momento, sin pensar en el futuro
    (igual que con las monedas: primero la mas grande)

    1. Calcular la razon de cada fuga = beneficio / (lo que usa de dinero + lo que usa de horas)
    2. Ordenar de mayor a menor razon (sort reverse=True, igual que las monedas)
    3. Tomar cada fuga si todavia entra, sin volver atras
    """
    if presupuesto <= 0 or horas <= 0:
        return []
    razones = []
    for i in range(len(fugas)):
        fuga = fugas[i]
        uso = fuga["costo"] / presupuesto + fuga["hp"] / horas #Semana 1 - division decimal
        razon = fuga["beneficio"] / uso
        razones.append((razon, i)) #tupla (razon, posicion)
        if mostrar:
            print(f"{fuga['id']}: razon = {fuga['beneficio']} / {uso:.3f} = {razon:.1f}")
    razones.sort(reverse=True) #de mayor a menor, como monedas.sort(reverse=True)
    if mostrar:
        print(f"Orden voraz: {[fugas[i]['id'] for razon, i in razones]}")
    seleccion = []
    for razon, i in razones:
        fuga = fugas[i]
        if mostrar:
            print(f"probando con {fuga['id']} (S/ {fuga['costo']}, {fuga['hp']} hp)")
        #       1500       <=  4300         and   6   <=  20
        if fuga["costo"] <= presupuesto and fuga["hp"] <= horas:
            seleccion.append(fuga)
            presupuesto -= fuga["costo"] #presupuesto = presupuesto - costo
            horas -= fuga["hp"]
            if mostrar:
                print(f"Agregamos {fuga['id']}. Quedan S/ {presupuesto} y {horas} horas-persona")
        else:
            if mostrar:
                print(f"{fuga['id']} ya no entra, queda pendiente")
    return seleccion


#---------------------------------------------------------------
# ESTRATEGIA 02 - PASO 2: PROGRAMACION DINAMICA (mochila 0/1 con 2 restricciones)
# Semana 8 - Recursividad + Semana 9 - Divide y venceras
# + Semana 3 - Diccionario para guardar resultados
#---------------------------------------------------------------
def prog_dinamica(fugas, presupuesto, horas, mostrar=True):
    """
    mejor(i, p, h) = mayor beneficio usando las primeras i fugas,
                     con p bloques de S/ 50 y h horas-persona

    Divide (Sem 9): el problema con i fugas se divide en 2 subproblemas
        no tomar la fuga i -> mejor(i-1, p, h)
        tomar la fuga i    -> beneficio_i + mejor(i-1, p - costo_i, h - hp_i)
    Combina (Sem 9): nos quedamos con el MAYOR de los dos
    Caso base (Sem 8): si no hay fugas, dinero u horas -> 0

    Programacion dinamica: un mismo subproblema aparece muchas veces,
    asi que su resultado se guarda en el diccionario "tabla" (Sem 3)
    y la siguiente vez solo se consulta, no se vuelve a calcular.
    """
    n = len(fugas)
    P = presupuesto // 50 #Semana 1 - division entera: 4300 // 50 = 86 bloques
    H = horas
    tabla = {} #clave: (i, p, h) -> valor: mejor beneficio
    contador = {"calculados": 0, "reutilizados": 0}

    def bloques(fuga):
        return (fuga["costo"] + 49) // 50 #redondea hacia arriba para no pasarse del presupuesto

    def mejor(i, p, h):
        if i == 0 or p == 0 or h == 0: #caso base
            return 0
        if (i, p, h) in tabla: #ya se calculo antes -> se reutiliza
            contador["reutilizados"] += 1
            return tabla[(i, p, h)]
        #caso recursivo
        fuga = fugas[i - 1]
        no_tomar = mejor(i - 1, p, h)
        if bloques(fuga) <= p and fuga["hp"] <= h:
            tomar = fuga["beneficio"] + mejor(i - 1, p - bloques(fuga), h - fuga["hp"])
            resultado = max(no_tomar, tomar)
        else:
            resultado = no_tomar #no entra, solo queda no tomarla
        tabla[(i, p, h)] = resultado #guardar en la tabla
        contador["calculados"] += 1
        return resultado

    if mostrar:
        print(f"n = {n} fugas, P = {P} bloques de S/ 50, H = {H} horas-persona")
    total = mejor(n, P, H)
    #guardamos cuantos subproblemas se usaron antes de reconstruir
    info_pd["calculados"] = contador["calculados"]
    info_pd["reutilizados"] = contador["reutilizados"]
    if mostrar:
        print(f"Mejor beneficio posible: {total}")
        print(f"Subproblemas calculados y guardados en la tabla: {contador['calculados']}")
        print(f"Veces que se reutilizo un resultado guardado: {contador['reutilizados']}")
        print("\nAhora recorremos de la ultima fuga a la primera para saber cuales se tomaron")

    #reconstruir la respuesta: comparar tomar vs no tomar en cada fuga
    seleccion = []
    p = P
    h = H
    for i in range(n, 0, -1): #i = n, n-1, ... 1
        fuga = fugas[i - 1]
        sin_ella = mejor(i - 1, p, h)
        con_ella = mejor(i, p, h)
        if mostrar:
            print(f"{fuga['id']}: sin ella lo mejor es {sin_ella}, considerandola lo mejor es {con_ella}")
        if con_ella != sin_ella: #si cambia, la fuga se tomo
            seleccion.append(fuga)
            p -= bloques(fuga)
            h -= fuga["hp"]
            if mostrar:
                print(f"--> son distintos, {fuga['id']} SI se repara (quedan {p} bloques y {h} hp)")
        else:
            if mostrar:
                print(f"--> son iguales, {fuga['id']} no se repara")
    seleccion.reverse()
    return seleccion


#---------------------------------------------------------------
# COMPROBACION: FUERZA BRUTA (solo para comprobar)
# Semana 3 - Fuerza bruta (05_fb_viajero.py)
#---------------------------------------------------------------
def fuerza_bruta(fugas, presupuesto, horas, mostrar=True):
    """
    Igual que el viajero: probar TODAS las opciones y quedarse con la mejor.
    El viajero usaba permutations (importa el orden de las ciudades);
    aqui usamos combinations porque no importa el orden de las fugas.
    Con 9 fugas -> 2^9 = 512 combinaciones
    """
    mejor = []
    mayor_beneficio = -1 #en el viajero era float("inf") porque buscaba el menor
    revisadas = 0
    descartadas = 0
    for r in range(len(fugas) + 1): #grupos de 0, 1, 2 ... n fugas
        for combinacion in combinations(fugas, r):
            revisadas += 1
            costo, hp, beneficio, caudal = calcular_totales(list(combinacion))
            if costo <= presupuesto and hp <= horas:
                if beneficio > mayor_beneficio:
                    mayor_beneficio = beneficio
                    mejor = list(combinacion)
                    if mostrar:
                        ids = [fuga["id"] for fuga in combinacion]
                        print(f"Nueva mejor: {ids} beneficio {beneficio} (S/ {costo}, {hp} hp)")
            else:
                descartadas += 1 #se pasa del dinero o de las horas
    if mostrar:
        print(f"Combinaciones revisadas: {revisadas} (2^{len(fugas)} = {2 ** len(fugas)}), "
              f"descartadas por pasarse: {descartadas}")
    return mejor


#---------------------------------------------------------------
# SISTEMA COMPLETO
#---------------------------------------------------------------
def resolver(fugas, presupuesto, horas, metodo, mostrar=True):
    if mostrar:
        print("\n===== PASO 1: EMERGENCIAS (heapq) =====")
    criticas, restantes, presupuesto, horas = reparar_emergencias(fugas, presupuesto, horas, mostrar)
    if mostrar:
        print(f"\n===== PASO 2: {metodo.upper()} con S/ {presupuesto} y {horas} hp para {len(restantes)} fugas =====")
    inicio = time.perf_counter()
    match metodo: #Semana 2 - match / case
        case "voraz":
            resto = alg_voraz(restantes, presupuesto, horas, mostrar)
        case "dinamica":
            resto = prog_dinamica(restantes, presupuesto, horas, mostrar)
        case _:
            resto = fuerza_bruta(restantes, presupuesto, horas, mostrar)
    tiempo = (time.perf_counter() - inicio) * 1000 #milisegundos
    return criticas + resto, tiempo


def mostrar_resultado(fugas, seleccion, titulo, tiempo):
    costo, hp, beneficio, caudal = calcular_totales(seleccion)
    print(f"""
╔══════════════════════════════════════════════════════╗
║  {titulo:<52}║
╚══════════════════════════════════════════════════════╝""")
    for fuga in fugas:
        if fuga in seleccion:
            estado = "COMPLETA "
        else:
            estado = "PENDIENTE"
        print(f"║   {fuga['id']}  {estado}  {fuga['riesgo']:<8} {fuga['ubicacion']}")
    criticas_ok = True
    for fuga in fugas:
        if fuga["riesgo"] == "Critico" and fuga not in seleccion:
            criticas_ok = False
    print(f"""╚══════════════════════════════════════════════════════╝
║   Presupuesto usado: S/ {costo} de {presupuesto}
║   Horas-persona usadas: {hp} de {horas_persona}
║   Agua recuperada: {caudal} m3/dia
║   Beneficio total: {beneficio}
║   Tiempo: {tiempo:.3f} ms
║   Cumple dinero y horas: {costo <= presupuesto and hp <= horas_persona}
║   Criticas reparadas: {criticas_ok}
╚══════════════════════════════════════════════════════╝""")


def medir_memoria(fugas, metodo):
    #tracemalloc mide la memoria maxima (pico) que se uso mientras corria la estrategia
    tracemalloc.start()
    resolver(fugas, presupuesto, horas_persona, metodo, False)
    actual, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico / 1024 #en KB


def comparar(fugas):
    sel_v, t_v = resolver(fugas, presupuesto, horas_persona, "voraz", False)
    sel_pd, t_pd = resolver(fugas, presupuesto, horas_persona, "dinamica", False)
    tabla_pd = info_pd["calculados"]
    sel_fb, t_fb = resolver(fugas, presupuesto, horas_persona, "fuerza bruta", False)
    m_v = medir_memoria(fugas, "voraz")
    m_pd = medir_memoria(fugas, "dinamica")
    m_fb = medir_memoria(fugas, "fuerza bruta")
    costo_v, hp_v, b_v, caudal_v = calcular_totales(sel_v)
    costo_pd, hp_pd, b_pd, caudal_pd = calcular_totales(sel_pd)
    costo_fb, hp_fb, b_fb, caudal_fb = calcular_totales(sel_fb)
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                     COMPARACION DE ESTRATEGIAS                       ║
╚══════════════════════════════════════════════════════════════════════╝
║   Indicador              Voraz        Prog. dinamica   Fuerza bruta
║   Beneficio              {b_v:<12} {b_pd:<16} {b_fb}
║   Costo usado (S/)       {costo_v:<12} {costo_pd:<16} {costo_fb}
║   Horas-persona usadas   {hp_v:<12} {hp_pd:<16} {hp_fb}
║   Agua recuperada (m3)   {caudal_v:<12} {caudal_pd:<16} {caudal_fb}
║   Tiempo (ms)            {t_v:<12.3f} {t_pd:<16.3f} {t_fb:.3f}
║   Memoria pico (KB)      {m_v:<12.1f} {m_pd:<16.1f} {m_fb:.1f}
╚══════════════════════════════════════════════════════════════════════╝""")
    print(f"Voraz repara:    {[fuga['id'] for fuga in sel_v]}")
    print(f"PD repara:       {[fuga['id'] for fuga in sel_pd]}")
    print(f"La PD guardo {tabla_pd} subproblemas en su tabla")
    if b_pd == b_fb:
        print("La PD dio lo mismo que la fuerza bruta -> la PD encontro el optimo")
    if b_pd > b_v:
        print(f"La PD gana al voraz por {b_pd - b_v} puntos ({round((b_pd - b_v) / b_v * 100, 1)} % mas)")
    else:
        print("En este caso el voraz tambien llego al optimo")


#---------------------------------------------------------------
# ANALISIS EMPIRICO: casos aleatorios con mas fugas
#---------------------------------------------------------------
def crear_fugas_aleatorias(n):
    riesgos = ["Critico", "Alto", "Alto", "Medio", "Medio", "Medio", "Bajo", "Bajo", "Bajo"]
    fugas = []
    for i in range(n):
        fugas.append({"id": f"F{i + 1:02d}", "ubicacion": "-", "riesgo": random.choice(riesgos),
                      "caudal": random.randint(2, 40), "costo": random.randint(4, 54) * 50,
                      "trab": random.randint(1, 4), "horas": random.randint(2, 5)})
    for fuga in fugas:
        fuga["hp"] = fuga["trab"] * fuga["horas"]
        fuga["beneficio"] = fuga["caudal"] * peso_riesgo[fuga["riesgo"]]
    return fugas


def prueba_tiempos():
    random.seed(10) #semilla fija para que siempre salgan los mismos casos
    veces_optimo = 0
    casos = 0
    print()
    print(f"{'n':>3} | {'Voraz':>6} {'ms':>8} | {'PD':>6} {'ms':>9} {'tabla':>7} | {'F.bruta':>7} {'ms':>9}")
    print("-" * 72)
    for n in [6, 8, 10, 12, 14, 16, 18, 25, 30, 40, 50, 60]: #50 y 60 para estresar el modelo
        fugas = crear_fugas_aleatorias(n)
        costo, hp, beneficio, caudal = calcular_totales(fugas)
        p = int(costo * 0.6) // 50 * 50 #damos el 60 % de lo que costaria todo
        h = int(hp * 0.6)
        sel_v, t_v = resolver(fugas, p, h, "voraz", False)
        sel_pd, t_pd = resolver(fugas, p, h, "dinamica", False)
        tabla = info_pd["calculados"] #subproblemas guardados por la PD
        b_v = calcular_totales(sel_v)[2]
        b_pd = calcular_totales(sel_pd)[2]
        if n <= 18: #despues de 18 la fuerza bruta se demora mucho
            sel_fb, t_fb = resolver(fugas, p, h, "fuerza bruta", False)
            fb = f"{calcular_totales(sel_fb)[2]:>7} {t_fb:>9.2f}"
        else:
            fb = f"{'-':>7} {'-':>9}"
        print(f"{n:>3} | {b_v:>6} {t_v:>8.3f} | {b_pd:>6} {t_pd:>9.2f} {tabla:>7} | {fb}")
        casos += 1
        if b_v == b_pd:
            veces_optimo += 1
    print("-" * 72)
    print(f"El voraz llego al optimo en {veces_optimo} de {casos} casos")


def pausa():
    try:
        input("\nPresione ENTER para volver al menu...")
    except EOFError:
        pass


#---------------------------------------------------------------
# DATOS DEL CASO
# Semana 1 - Variables en snake_case
# Semana 3 - Diccionarios (cada fuga es un diccionario clave: valor)
#---------------------------------------------------------------
presupuesto = 10000
horas_persona = 48 #horas-persona que se pueden pagar
trabajadores = 4
peso_riesgo = {"Critico": 4, "Alto": 3, "Medio": 2, "Bajo": 1}

fugas = [
    {"id": "F01", "ubicacion": "Jr. Del Comercio", "riesgo": "Critico", "caudal": 38, "costo": 2400, "trab": 3, "horas": 4},
    {"id": "F02", "ubicacion": "Av. Atahualpa", "riesgo": "Alto", "caudal": 22, "costo": 1500, "trab": 2, "horas": 3},
    {"id": "F03", "ubicacion": "Barrio San Sebastian", "riesgo": "Bajo", "caudal": 3, "costo": 250, "trab": 1, "horas": 2},
    {"id": "F04", "ubicacion": "Av. Via de Evitamiento Norte", "riesgo": "Critico", "caudal": 30, "costo": 2100, "trab": 2, "horas": 5},
    {"id": "F05", "ubicacion": "Jr. Amalia Puga", "riesgo": "Medio", "caudal": 10, "costo": 800, "trab": 2, "horas": 2},
    {"id": "F06", "ubicacion": "Barrio Mollepampa", "riesgo": "Alto", "caudal": 18, "costo": 1600, "trab": 2, "horas": 4},
    {"id": "F07", "ubicacion": "Jr. Apurimac", "riesgo": "Bajo", "caudal": 2, "costo": 200, "trab": 1, "horas": 2},
    {"id": "F08", "ubicacion": "Zona Hospital Regional", "riesgo": "Critico", "caudal": 15, "costo": 1200, "trab": 2, "horas": 3},
    {"id": "F09", "ubicacion": "Barrio La Colmena", "riesgo": "Medio", "caudal": 12, "costo": 1900, "trab": 3, "horas": 3},
    {"id": "F10", "ubicacion": "Av. Independencia", "riesgo": "Medio", "caudal": 9, "costo": 700, "trab": 2, "horas": 2},
    {"id": "F11", "ubicacion": "Barrio Pueblo Nuevo", "riesgo": "Bajo", "caudal": 4, "costo": 450, "trab": 1, "horas": 3},
    {"id": "F12", "ubicacion": "Av. San Martin de Porres", "riesgo": "Alto", "caudal": 28, "costo": 2600, "trab": 4, "horas": 3},
]
#         caudal en m3/dia, costo en soles, trab = trabajadores, horas = lo que demora

fugas = preparar_fugas(fugas)

#---------------------------------------------------------------
# MENU
# Semana 2 - match / case con input (Funciones_sem_02.py)
#---------------------------------------------------------------
while True:
    print("""
============ SISTEMA DE REPARACION DE FUGAS ============
 1. Ver fugas detectadas
 2. Ver fugas ordenadas por prioridad (burbuja)
 3. Buscar una fuga por codigo (busqueda binaria)
 4. Resolver con algoritmo voraz
 5. Resolver con programacion dinamica
 6. Comprobar con fuerza bruta
 7. Comparar las estrategias
 8. Prueba de tiempos (analisis empirico)
 0. Salir
========================================================""")
    try:
        opc = input("Elegir: ").strip() #strip quita espacios y el salto de linea (\r) de Windows
    except EOFError: #si la consola no deja escribir
        print("\nNo se pudo leer la opcion. Ejecute el programa en la TERMINAL.")
        break
    match opc:
        case "1":
            mostrar_fugas(fugas)
            pausa()
        case "2":
            mostrar_por_prioridad(fugas)
            pausa()
        case "3":
            buscar_fuga(fugas)
            pausa()
        case "4":
            seleccion, tiempo = resolver(fugas, presupuesto, horas_persona, "voraz")
            mostrar_resultado(fugas, seleccion, "RESULTADO - ALGORITMO VORAZ", tiempo)
            pausa()
        case "5":
            seleccion, tiempo = resolver(fugas, presupuesto, horas_persona, "dinamica")
            mostrar_resultado(fugas, seleccion, "RESULTADO - PROGRAMACION DINAMICA", tiempo)
            pausa()
        case "6":
            seleccion, tiempo = resolver(fugas, presupuesto, horas_persona, "fuerza bruta")
            mostrar_resultado(fugas, seleccion, "RESULTADO - FUERZA BRUTA", tiempo)
            pausa()
        case "7":
            comparar(fugas)
            pausa()
        case "8":
            print("Calculando, espere unos segundos...")
            prueba_tiempos()
            pausa()
        case "0":
            print("Fin del programa")
            break
        case _:
            print(f"Opcion '{opc}' no valida, escriba un numero del 0 al 8")
