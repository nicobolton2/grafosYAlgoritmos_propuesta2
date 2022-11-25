#/bin/python3 -m pip install openpyxl matplotlib networkx pandas geopandas -U --user --force-reinstall

# %%
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import geopandas as gpd

# %%
df = pd.read_excel('Aeropuertos_del_mundo.xlsx')
df_dict = df.to_dict()
print("-----------..-------")
print(f'{df_dict=}')
worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
fig, ax = plt.subplots(figsize = (12, 6))
worldmap.plot(color='lightgrey', ax = ax)
x = df['Longitud']
y = df['Latitud']
plt.scatter(x, y, s = 10, c = None, alpha = 1)
# %%
class Vertice:
    def __init__(self, i, name, latitud, longitud):
        self.id = i
        self.name = name
        self.latitud = latitud
        self.longitud = longitud
        self.vecinos = []
        self.visitado = False
        self.padre = None
        self.distanciaMinima = float('inf')

    def agregarVecino(self, v, p):
        if v not in self.vecinos:
            self.vecinos.append([v, p])

# %%
class Grafica:
    def __init__(self):
        self.vertices = {}
        self.optimo = []
        self.tiempoActual = 0
        self.opt = []

    def agregarVertice(self, id, name, xpoint, ypoint):
        if id not in self.vertices:
            self.vertices[id] = Vertice(id, name, xpoint, ypoint)

    def agregarArista(self, a, b):
        if a in self.vertices and b in self.vertices:
            p = (((self.vertices[a].latitud - self.vertices[b].latitud)**2) + ((self.vertices[a].longitud - self.vertices[b].longitud)**2))**(1/2)
            self.vertices[a].agregarVecino(b, p)
            self.vertices[b].agregarVecino(a, p)

    def imprimirGrafica(self, a):
        for v in self.vertices:
            if(v != a):
                print('La distancia del vertice ' + str(v) + ' es ' + str(self.vertices[v].distanciaMinima) + ' llegando desde ' + str(self.
                vertices[v].padre))
                self.opt.append((str(self.vertices[v].padre), str(v)))
                x_points = [self.vertices[str(self.vertices[v].padre)].longitud, self.vertices[str(v)].longitud]
                y_points = [self.vertices[str(self.vertices[v].padre)].latitud, self.vertices[str(v)].latitud] 
                plt.plot(x_points,y_points)

    def minimo(self, lista):
        if len(lista) > 0:
            m = self.vertices[lista[0]].distanciaMinima
            v = lista[0]
            for e in lista:
                if m > self.vertices[e].distanciaMinima:
                    m = self.vertices[e].distanciaMinima
                    v = e
            return v

    def dijkstra(self, a):
        if a in self.vertices:
            self.vertices[a].distanciaMinima = 0
            actual = a
            noVisitados = []

            for v in self.vertices:
                if v != a:
                    self.vertices[v].distanciaMinima = float('inf')
                self.vertices[v].padre = None
                noVisitados.append(v)

            while len(noVisitados) > 0:
                for b in self.vertices[actual].vecinos:
                    if self.vertices[b[0]].visitado == False:
                        if self.vertices[actual].distanciaMinima + b[1] < self.vertices[b[0]].distanciaMinima:
                            self.vertices[b[0]].distanciaMinima = self.vertices[actual].distanciaMinima + b[1]
                            self.vertices[b[0]].padre = actual

                self.vertices[actual].visitado = True
                noVisitados.remove(actual)

                actual = self.minimo(noVisitados)
        else:
            return False
 
    def camino(self, a, b):
        self.dijkstra(a)
        camino = []
        actual = b
        while actual != None:
            camino.insert(0, actual)
            actual = self.vertices[actual].padre
        return [camino, self.vertices[b].distanciaMinima]

# %%
#g = Grafica()
#g.agregarVertice('DXB','Dubai', 25.25, 55.333333333333)
#g.agregarVertice('HND','Haneda', 35.552777777778, 139.76666666667)
#g.agregarVertice('ORD','Chicago-O Hare', 41.983333333333, -87.9)
#g.agregarVertice('ATL','Hartsfield-Jackson', 33.65, -84.433333333333)
#g.agregarVertice('HKG','Hong Kong', 22.333333333333, 114.2)
#g.agregarVertice('PEK','Pekin', 40.05, 116.58333333333)
#g.agregarVertice('PVG','Shanghai Pudong', 31.1486590900604, 121.800956726074)
#g.agregarVertice('CDG','Paris-Charles de Gaulle', 49.016666666667, 2.55)
#g.agregarVertice('LHR','Londres-Heathrow', 51.466666666667, -0.45)
#g.agregarVertice('LAX','Los Angeles', 33.933333333333, -118.4)
#for i in g.vertices:
#    for j in g.vertices:
#        g.agregarArista(f'{i}',f'{j}')
#print(g.camino('DXB', 'CDG'))
#g.imprimirGrafica('DXB')


# %%
g = Grafica()
for index, row in df.iterrows():
    g.agregarVertice(row[1], row[0], row[2], row[3])
for i in g.vertices:
    for j in g.vertices:
        g.agregarArista(i ,j)
print(f'{g=}')
print(f'{g.vertices=}')
abc = {k:(v.latitud, v.longitud)for k, v in g.vertices.items()}
print(f'{abc=}')
print(g.vertices['DXB'].latitud)
print(g.camino('DXB', 'CDG'))
g.imprimirGrafica('DXB')
print(g.opt)
#g.imprimirGrafica('DXB')

# %%
x = df['Longitud']
y = df['Latitud']
plt.scatter(x, y, s = 10, c = None, alpha = 1)
for i in range(len(x)):
    for j in range(len(y)):
        x_value = [x[i], x[j]]
        y_value = [y[i], y[j]]
        print(x_value)
        print(y_value)
        plt.plot(x_value, y_value)
plt.xlim([-180, 180])
plt.ylim([-90, 90])
plt.xlabel('Longitud')
plt.ylabel('Latitud')


# %%
G = nx.Graph()
nodos = {}
nodos = map(str, g.vertices)
G.add_nodes_from(nodos)
G.add_edges_from(g.opt)
nx.draw(G, with_labels=True)
# %%
x = list()
y = list()
for i in g.vertices:
    x.append(g.vertices[i].latitud)
    y.append(g.vertices[i].longitud)
print(x)
print(y)
plt.plot(x, y, 'ro')
plt.show()
# %%
