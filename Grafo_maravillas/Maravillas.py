from Extras.Cola import Cola
from Extras.Monticulo import Monticulo
from Extras.Pila import Pila

class NodoArista():
    def __init__(self, info, destino):
        self.info = info
        self.destino = destino
        self.sig = None
    
class NodoVertice():
    def __init__(self, info, nombre, pais, tipo):
        self.info = info
        self.nombre = nombre
        self.pais = pais
        self.tipo = tipo
        self.sig = None
        self.visitado = False 
        self.adyacentes = Arista()

class Arista():
    def __init__(self):
        self.inicio = None
        self.tamanio = 0     
        
class Grafo():
    def __init__(self, dirigido=False):
        self.inicio = None
        self.dirigido = dirigido
        self.tamanio = 0

    def insertar_vertice(self, dato, nombre, pais, tipo):
        nodo = NodoVertice(dato, nombre, pais, tipo)
        if self.inicio is None or self.inicio.info > dato:
            nodo.sig = self.inicio
            self.inicio = nodo
        else:
            ant = self.inicio
            act =  self.inicio.info
            while act is not None and act.info < nodo.info:
                ant = act
                act = act.sig
            nodo.sig = act
            ant.sig = nodo
        self.tamanio += 1

    def agregar_arista(self, dato, origen, destino):
        nodo = NodoArista(dato, destino)
        if origen.inicio is None or origen.inicio.destino > destino:
            nodo.sig = origen.inicio
            origen.inicio = nodo
        else:
            ant = origen.inicio
            act = origen.inicio.sig
            while act is not None and act.destino < nodo.destino:
                ant = act
                act = act.sig
            nodo.sig = act
            ant.sig = nodo
        self.tamanio += 1
    
    def adyacentes(self, vertice):
        aux = vertice.adyacentes.inicio
        while aux is not None:
            print(aux.destino, aux.info)
            aux = aux.sig

    def insertar_arista(self, dato, origen, destino):
        self.agregar_arista(origen.adyacentes, dato, destino.info)
        if not self.dirigido:
            self.agregar_arista(destino.adyacentes, dato, origen.info)
    
    def eliminar_arista(self, vertice, destino):
        x = None
        if vertice.inicio.destino == destino:
            x = vertice.inicio.info
            vertice.inicio = vertice.inicio.sig
            vertice.tamanio -= 1 
        else:
            ant = vertice.inicio
            act = vertice.inicio.sig
            while act is not None and act.destino != destino:
                ant = act
                act = act.sig
            if act is not None: 
                x = act.info
                ant.sig = act.sig
                vertice.tamanio -= 1
        return x

    def eliminar_vertice(self, clave):
        x = None
        if self.inicio.info == clave:
            z = self.inicio.info
            self.inicio = self.inicio.sig
            self.tamanio += 1
        else:
            ant = self.inicio
            act = self.inicio.sig
            while act is not None and act.info != clave:
                ant = act
                act = act.sig
            if act is not None:
                x = act.info
                ant.sig = act.sig
                self.tamanio -= 1
        if x is not None:
            aux = self.inicio
            while aux is not None:
                if aux.adyacentes.inicio is not None:
                    self.eliminar_arista(aux.vertice, clave)
                aux = aux.sig
        return x

    def buscar_vertice(self, buscado):
        aux = self.inicio
        while aux is not None and aux.info != buscado:
            aux = aux.sig
        return aux

    def buscar_arista(self, vertice, buscado):
        aux = vertice.adyacentes.inicio
        while aux is not None and aux.destino != buscado:
            aux = aux.sig
        return aux

    def tamanio(self):
        return self.tamanio
    
    def grafo_vacio(self):
        return self.inicio is None
    
    def existe_paso(self, origen, destino):
        resultado = False
        if not origen.visitado:
            origen.visitado = True
            vadyacentes = origen.adyacentes.inicio
            while vadyacentes is not None and not resultado:
                adyacente = self.buscar_vertice(vadyacentes.destino)
                if adyacente.info == destino.info:
                    return True
                elif not adyacente.visitado:
                    resultado = self.existe_paso(adyacente, destino)
                vadyacentes = vadyacentes.sig
        return resultado

    def es_adyacente(self, vertice, destino):
        resultado = False
        aux = vertice.adyacentes.inicio
        while aux is not None and not resultado:
            if aux.destino == resultado:
                resultado = True
            aux = aux.sig
        return resultado
    
    def marcar_no_visitado(self):
        aux = self.inicio
        while aux is not None:
            aux.visitado = False
            aux = aux.sig

    def barrido_vertices(self):
        aux = self.inicio
        while aux is not None:
            print(aux.info)
            aux = aux.sig
    
    def barrido_profundidad(self, vertice):
        while vertice is not None:
            if not vertice.visitado:
                vertice.visitado = True
                print(vertice.info)
                adyacentes = vertice.adyacentes.inicio
                while adyacentes is not None:
                    adyacente = self.buscar_vertice(adyacentes.destino)
                    if not adyacente.visitado:
                        self.barrido_profundidad(adyacente)
                    adyacentes = adyacentes.sig
            vertice = vertice.sig

    def barrido_amplitud(self, vertice):
        cola = Cola()
        while vertice is not None:
            if not vertice.visitado:
                vertice.visitado = True
                cola.arribo(vertice)
                while not cola.cola_vacia():
                    nodo = cola.atencion()
                    print(nodo.info)
                    adyacentes = nodo.adyacentes.inicio
                    while adyacentes is not None:
                        adyacente = self.buscar_vertice(adyacentes.destino)
                        if not adyacente.visitado:
                            adyacente.visitado = True
                            cola.arribo(adyacente)
                        adyacentes = adyacentes.sig
            vertice = vertice.sig

    def dijkstra(self, origen, destino):
        no_visitados = Monticulo(self.tamanio)
        camino = Pila()
        aux = self.inicio
        while aux is not None:
            if aux.info == origen:
                no_visitados.arribo([aux, None], 0)
            else:
                no_visitados.arribo([aux, None], aux.info)
            aux = aux.sig
        while not no_visitados.monticulo_vacio():
            dato = no_visitados.atencion()
            camino.apilar(dato)
            aux = dato[1][0].adyacentes.inicio
            while aux is not None:
                pos = no_visitados.buscar(aux.destino)
                if no_visitados.vector[pos][0] > dato[0] + aux.info:
                    no_visitados.vector[pos][1][1] = dato[1][0].info
                    no_visitados.cambiar_prioridad(pos, dato[0] + aux.info)
                aux = aux.sig
        return camino