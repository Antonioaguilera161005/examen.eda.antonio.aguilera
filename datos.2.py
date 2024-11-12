from collections import deque, defaultdict
import heapq
import timeit

# Representación del grafo
localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)]
}

# Función para encontrar la ruta más corta usando Dijkstra
def dijkstra_shortest_path(grafo, inicio, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    prev = {nodo: None for nodo in grafo}
    pq = [(0, inicio)]

    while pq:
        (dist_actual, nodo_actual) = heapq.heappop(pq)
        if nodo_actual == destino:
            break

        for vecino, peso in grafo[nodo_actual]:
            distancia = dist_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                prev[vecino] = nodo_actual
                heapq.heappush(pq, (distancia, vecino))

    ruta = []
    actual = destino
    while actual:
        ruta.append(actual)
        actual = prev[actual]
    ruta.reverse()

    return ruta, distancias[destino] if distancias[destino] != float('inf') else None

# Función para identificar localidades con todas sus conexiones < 15 km
def localidades_con_conexiones_cortas(grafo):
    resultado = []
    for localidad, conexiones in grafo.items():
        if all(distancia < 15 for _, distancia in conexiones):
            resultado.append(localidad)
    return resultado

# Función para verificar la conectividad del grafo usando BFS
def es_conexo(grafo):
    visitados = set()
    nodo_inicial = list(grafo.keys())[0]

    cola = deque([nodo_inicial])
    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            visitados.add(nodo)
            cola.extend([vecino for vecino, _ in grafo[nodo] if vecino not in visitados])

    return len(visitados) == len(grafo)

# Función para encontrar todas las rutas sin ciclos usando BFS modificado
def rutas_sin_ciclos(grafo, inicio, destino):
    rutas = []
    cola = deque([[inicio]])

    while cola:
        ruta = cola.popleft()
        nodo_actual = ruta[-1]

        if nodo_actual == destino:
            rutas.append(ruta)
        else:
            for vecino, _ in grafo[nodo_actual]:
                if vecino not in ruta:
                    nueva_ruta = ruta + [vecino]
                    cola.append(nueva_ruta)

    return rutas

# Nueva función: Ruta más larga posible sin ciclos
def ruta_mas_larga_sin_ciclos(grafo, origen, destino):
    def dfs(localidad_actual, destino, visitadas, distancia_actual, ruta_actual):
        nonlocal ruta_maxima, distancia_maxima
        
        if localidad_actual == destino:
            if distancia_actual > distancia_maxima:
                distancia_maxima = distancia_actual
                ruta_maxima = ruta_actual[:]
            return
        
        for vecina, distancia in grafo.get(localidad_actual, []):
            if vecina not in visitadas:
                visitadas.add(vecina)
                ruta_actual.append(vecina)
                dfs(vecina, destino, visitadas, distancia_actual + distancia, ruta_actual)
                # Backtrack
                visitadas.remove(vecina)
                ruta_actual.pop()
    
    distancia_maxima = -1
    ruta_maxima = []
    visitadas = set([origen])
    
    dfs(origen, destino, visitadas, 0, [origen])
    
    if ruta_maxima:
        return ruta_maxima, distancia_maxima
    else:
        return "No hay ruta válida sin ciclos entre las localidades especificadas."

# Mostrar localidades disponibles
localidades_disponibles = list(localidades.keys())
print("Localidades disponibles:", ", ".join(localidades_disponibles))

# Solicitar inputs al usuario con validación
while True:
    origen = input("Introduce la localidad de origen: ")
    if origen in localidades:
        break
    else:
        print("Localidad no válida. Por favor, selecciona una de las localidades disponibles.")

while True:
    destino = input("Introduce la localidad de destino: ")
    if destino in localidades:
        break
    else:
        print("Localidad no válida. Por favor, selecciona una de las localidades disponibles.")

# 1. Ruta más corta entre las localidades ingresadas
ruta, distancia = dijkstra_shortest_path(localidades, origen, destino)
if ruta:
    print("Ruta más corta de", origen, "a", destino, ":", ruta)
    print("Distancia total:", distancia, "km")
else:
    print("No se encontró una ruta de", origen, "a", destino)

# 2. Localidades con todas las conexiones < 15 km
print("Localidades con todas las conexiones menores de 15 km:", localidades_con_conexiones_cortas(localidades))

# 3. Verificar si el grafo es conexo
print("¿El grafo es conexo?", "Sí" if es_conexo(localidades) else "No")

# 4. Todas las rutas sin ciclos entre las localidades ingresadas
rutas = rutas_sin_ciclos(localidades, origen, destino)
print("Rutas sin ciclos de", origen, "a", destino, ":", rutas)

# 5. Ruta más larga posible sin ciclos
ruta_larga, distancia_larga = ruta_mas_larga_sin_ciclos(localidades, origen, destino)
print("Ruta más larga sin ciclos de", origen, "a", destino, ":", ruta_larga)
print("Distancia total de la ruta más larga:", distancia_larga, "km")

# Función para medir la eficiencia de la función dijkstra_shortest_path
tiempo_ruta_mas_corta = timeit.timeit(
      f"dijkstra_shortest_path(localidades, '{origen}', '{destino}')",
    globals=globals(),
    number=1000  # Número de repeticiones para obtener un promedio
)

print("Tiempo de ejecución para la ruta más corta:", tiempo_ruta_mas_corta, "segundos")

tiempo_conexiones_cortas = timeit.timeit(
    "localidades_con_conexiones_cortas(localidades)",
    globals=globals(),
    number=1000  # Número de repeticiones para obtener un promedio
)
print("Tiempo de ejecución para identificar localidades con conexiones cortas:", tiempo_conexiones_cortas, "segundos")

tiempo_es_conexo = timeit.timeit(
    "es_conexo(localidades)",
    globals=globals(),
    number=1000  # Número de repeticiones para obtener un promedio
)
print("Tiempo de ejecución para verificar si el grafo es conexo:", tiempo_es_conexo, "segundos")

tiempo_rutas_sin_ciclos = timeit.timeit(
    "rutas_sin_ciclos(localidades, 'Madrid', 'Getafe')",
    globals=globals(),
    number=100  # Menor número de repeticiones si la función es costosa
)
print("Tiempo de ejecución para encontrar rutas sin ciclos:", tiempo_rutas_sin_ciclos, "segundos")