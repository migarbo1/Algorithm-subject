#!/usr/bin/env python
#! -*- encoding utf8

class nodo(object):

    def __init__(self, nodoPadre: nodo, profundidad: int, letraLlegada: chr, palabra: str):
        self.nodoPadre = nodoPadre
        self.hijos = {}
        self.letraLlegada = letraLlegada
        self.palabra = palabra
        self.profundidad = profundidad

    def insertarHijo(letra: char, palabra: str)
        self.hijos[letra] = nodo.__init__(self, self.profundidad + 1, letra, palabra)
    
    def char(nodo) #dado un nodo devuelve el caracter con el que se ha llegado al nodo
        return nodo.letraLlegada
    
    def parent(nodo) #dado un nodo devuelve padre
        return nodo.nodoPadre
    
    def profundidad(nodo) #dado un nodo devuelve la profundidad
        return nodo.profundidad

    

