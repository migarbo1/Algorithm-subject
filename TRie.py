#!/usr/bin/env python
#! -*- encoding utf8

class nodo:

    def __init__(self, nodoPadre, profundidad, letraLlegada, palabra, idi):
        self.nodoPadre = nodoPadre
        self.hijos = {}
        self.letraLlegada = letraLlegada
        self.palabra = palabra
        self.profundidad = profundidad
        self.idi = idi #para ser mas accesible la matriz (sera un entero root=0 y se ira incrementando)

    def insertarHijo(self, letra, palabra, identificador):
        self.hijos[letra] = nodo(self, self.profundidad + 1, letra, palabra, identificador)
        return self.hijos[letra]

    def definirPalabra(self, palabra):
        self.palabra = palabra

    def devolverHijo(self, letra):
        return self.hijos.get(letra, 0)

    def char(self): #dado un nodo devuelve el caracter con el que se ha llegado al nodo
        return self.letraLlegada

    def parent(self): #dado un nodo devuelve padre
        return self.nodoPadre

    def profundidad(self): #dado un nodo devuelve la profundidad
        return self.profundidad

    def sacarPalabra(self): #dado un nodo devuelve la palabra
        return self.palabra
# tenemos que hacer iun if para ver si algo es none xd
# haser to stringos 
class trie:

    def __init__(self):
        self.array = []
        self.nodoRaiz = nodo(None, 0, None, None, 0)
        self.array += [self.nodoRaiz]

    def insertarPalabra(self, palabra):
        nodoActual = self.nodoRaiz  #empezamos por la raiz
        for l in palabra:       #recorremos la palabra
            palabraaux = None
            res = nodoActual.devolverHijo(l)
            if res == 0:            #si hijo no existe con esa letra
                if l == palabra[-1]:    # si ultima letra de la palabra
                    palabraaux = palabra    #sustituimos None por palabra
                nodoActual = nodoActual.insertarHijo(l, palabraaux, len(self.array)+1)     # insertamos hijo nuevo con letra que falta y palabra si es ultimo
                self.array += [nodoActual]
                
            else:
                nodoActual = res
                if l == palabra[-1]:    # si ultima letra de la palabra
                    palabraaux = palabra    #sustituimos None por palabra
                    nodoActual.definirPalabra(palabraaux)



    def root(self): #para tener el nodo inicial del trie
        return self.nodoRaiz
