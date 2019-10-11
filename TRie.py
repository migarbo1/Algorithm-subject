#!/usr/bin/env python
#! -*- encoding utf8

class nodo(object):

    def __init__(self, nodoPadre: nodo, profundidad: int, letraLlegada: chr, palabra: str):
        self.nodoPadre = nodoPadre
        self.hijos = {}
        self.letraLlegada = letraLlegada
        self.palabra = palabra
        self.profundidad = profundidad

    def insertarHijo(letra: char, palabra: str):
        self.hijos[letra] = nodo.__init__(self, self.profundidad + 1, letra, palabra)

    def devolverHijo(letra: char):
        return hijos.get(letra, 0)
    
    def char(): #dado un nodo devuelve el caracter con el que se ha llegado al nodo
        return self.letraLlegada
    
    def parent(): #dado un nodo devuelve padre
        return self.nodoPadre
    
    def profundidad(): #dado un nodo devuelve la profundidad
        return self.profundidad

class trie(object):

    def __init__(self, nodoRaiz: nodo):
        self.array = []
        self.nodoRaiz = nodoRaiz
        self.array.add(self.nodoRaiz)

    def insertarPalabra(palabra: str):
        nodoActual = self.nodoRaiz
        for l in palabra:
            res = nodoActual.devolverHijo(l)
            if res == 0:
                if l
                nodoActual.insertarHijo(l, none)
    

