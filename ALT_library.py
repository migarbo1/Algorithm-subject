#!/usr/bin/env python
#! -*- encoding utf8

#ZONA DE IMPORTS
import numpy as np
import re
import sys
import os
import pickle

#CLEAN
clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)

#CARGAR
def load_object(file_name):
    with open (file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj
#GUARDAR
def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

#TRIE
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

class trie:

    def __init__(self):
        self.array = []
        self.nodoRaiz = nodo(None, 0, None, None, 0)
        self.array += [self.nodoRaiz]

    def insertarPalabra(self, palabra):
        nodoActual = self.nodoRaiz  #empezamos por la raiz
        for l in range(len(palabra)):       #recorremos la palabra
            palabraaux = None
            res = nodoActual.devolverHijo(palabra[l])
            if res == 0:            #si hijo no existe con esa letra
                if l == len(palabra)-1:    # si ultima letra de la palabra
                    palabraaux = palabra    #sustituimos None por palabra
                nodoActual = nodoActual.insertarHijo(palabra[l], palabraaux, len(self.array)+1)     # insertamos hijo nuevo con letra que falta y palabra si es ultimo
                self.array += [nodoActual]

            else:
                nodoActual = res
                if l ==  len(palabra)-1:    # si ultima letra de la palabra
                    palabraaux = palabra    #sustituimos None por palabra
                    nodoActual.definirPalabra(palabraaux)



    def root(self): #para tener el nodo inicial del trie
        return self.nodoRaiz

    def insertarTexto(self, file):
        file = open(file,"r")
        text = file.read()
        file.close()
        text = clean_text(text)
        text = text.lower()
        text = text.split()
        text = sorted(text)
        for t in text:
            self.insertarPalabra(t)

    def guardar(self, nombre):
        save_object(self,nombre)

#ALGORITMOS

#distancia de levenstein sin ahorro espacial
def levenstein_distance(word1, word2):
    levMat = np.zeros(dtype=np.int8, shape=(len(word1) + 1,len(word2) + 1))
    #inicializamos la matriz del algoritmo de levenstein
    for i in range(1, len(word1)+1):
        levMat[i,0] = i

    for j in range(1, len(word2) + 1):
        levMat[0,j] = j

    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            dif = not (word1[i - 1] == word2[j - 1])
            levMat[i,j] = min(levMat[i-1, j], levMat[i-1, j-1], levMat[i, j-1]) + dif

    return levMat[len(word1), len(word2)]
#fin distancia levenstein 1

#distancia de levenstein con ahorro de espacio
def better_levenstein_distance(word1, word2):
    c_row = np.zeros(dtype=np.int8, shape=(len(word1) + 1))
    p_row = np.zeros(dtype=np.int8, shape=(len(word1) + 1))
    c_row[0] = 0
    for i in range(1, len(word1) + 1):
        c_row[i] = c_row[i - 1] + 1
    for j in range(1, len(word2) + 1):
        p_row,c_row = c_row,p_row
        c_row[0] = p_row[0] + 1 #esto es para sumarle 1 a la col[0], es decir, simular la insercion completa de la palabra
        for i in range(1, len(word1) + 1):
            c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[j - 1]))#elemento anteior en x e y mas si son diferentes (sustitucion por el mismo es 0)
    return c_row[len(word1)]
#fin distancia levenstein con ahorro espacial
#####################################################################################
def damerau_levenstein_distance(word1, word2):
    #dado que tenemos que acceder a la pposicios -2 en j tenemos que tener 3 filas
    c_row = np.zeros(dtype=np.int8, shape=(len(word1) + 1))
    p_row = np.zeros(dtype=np.int8, shape=(len(word1) + 1))
    aux_row = np.zeros(dtype=np.int8, shape=(len(word1) + 1)) #fila para acceder a la pos -2 en j
    c_row[0] = 0 #caso i = j = 1
    for i in range(1, len(word1) + 1): #caso i > 0 j = 0
        c_row[i] = c_row[i - 1] + 1

    p_row,c_row = c_row,p_row
    for i in range(0, len(word1) + 1): #caso j = 1 i > 0
        c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                    p_row[i] + 1, #elemento de abajo en y
                    p_row[i - 1] + (word1[i - 1] != word2[0]))

    for j in range(2, len(word2) + 1):
        aux_row,p_row,c_row = p_row,c_row,aux_row
        c_row[0] = p_row[0] + 1 #esto es para sumarle 1 a la col[0], es decir, simular la insercion completa de la palabra
        for i in range(1, len(word1) + 1):
            if (word1[i -1] == word2[j - 2] and word2[j -1] == word1[i - 2]):
                c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[j - 1]),#elemento anteior en x e y mas si son diferentes (sustitucion por el mismo es 0)
                            (aux_row[i - 2] + 1)) #transposicion
            else:
                c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[j - 1]))

    return c_row[-1]
###############################################################################################
def levenstein_vs_trie(tri, palabra, k):
    nod = tri.nodoRaiz
    matrix = np.zeros(dtype=np.int8, shape=(len(tri.array) + 1, len(palabra) + 1)) #creamos una matriz de nodos (filas) por simbolos de la palabra (columnas)
    result = []

    matrix[nod.idi,0] = 0 #case 1

    for i in range(1,len(palabra)+1): #case 2
        matrix[nod.idi,i] = i

    for n in tri.array:
        if(n != nod):
            matrix[n.idi,0] = n.profundidad#case 3
            for i  in range(1,len(palabra) + 1):#case 4
                matrix[n.idi,i] = min(
                    matrix[n.idi,i - 1] + 1,
                    matrix[n.nodoPadre.idi,i] + 1,
                    matrix[n.nodoPadre.idi,i - 1] + (palabra[i-1] != n.letraLlegada)
                )

    for n in tri.array:
        if(n != nod):
            if matrix[n.idi,-1] <= k:
                if n.palabra != None:
                    if n.palabra not in result:
                        result.append(n.palabra)

    return result
###############################################################################################
def damerau_levenstein_vs_trie(tri, word, toler):

    nod = tri.nodoRaiz
    matrix= np.zeros(dtype = np.int8,shape = (len(tri.array)+1, len(word)+1))
    res = []

    matrix[nod.idi, 0] = 0 #case 1

    for ln in range(1, len(word)+1): #case 2
        matrix[nod.idi, ln] = ln

    for n in tri.array:
        if n != nod:
            matrix[n.idi,0] = n.profundidad #case 3
            for i in range (1,len(word) + 1):
                if (word[i-1] == n.nodoPadre.letraLlegada and word[i-2] == n.letraLlegada) and n.nodoPadre.nodoPadre != None:
                    matrix[n.idi,i] = min(
                        matrix[n.idi,i - 1] + 1,
                        matrix[n.nodoPadre.idi,i] + 1,
                        matrix[n.nodoPadre.idi,i - 1] + (word[i-1] != n.letraLlegada),
                        matrix[n.nodoPadre.nodoPadre.idi,i - 2] + 1
                    )
                else:
                    matrix[n.idi,i] = min(
                        matrix[n.idi,i - 1] + 1,
                        matrix[n.nodoPadre.idi,i] + 1,
                        matrix[n.nodoPadre.idi,i - 1] + (word[i-1] != n.letraLlegada)
                    )

    for n in tri.array:
        if(n != nod):
            if matrix[n.idi,-1] <= toler:
                if n.palabra != None:
                    if n.palabra not in res:
                        res.append(n.palabra)

    return res
################################################################################
def levenstein_vs_trie_ramificacion(tri, palabra, k):
    lista = [(0,0,0)] # (elementode la plalabra, nodo, distancia a mi coraxon)
    nod = tri.root()
    result = []
    evitreps = {}
    while(len(lista)):
        i,n,d = lista.pop()

        if n == 0:
            nod = tri.array[n]
        else:
            nod = tri.array[n-1]

        #insercion
        if(d+1 <= k and len(nod.hijos) > 0 and i <= len(palabra)):
            for x in nod.hijos.keys():
                nn = nod.hijos.get(x, 0)
                lista.append((i,nn.idi ,d+1))

        #borracion
        if(d+1 <= k and i < len(palabra)): # ojo que aquí podría ir un <=, no lo se
            lista.append((i+1,nod.idi ,d+1))

        #sustitutusao
        if(d <= k and len(nod.hijos) > 0 and i < len(palabra)): #aqui no puede ir un <= poque si no palabra[i] hace pum pum
            for x in nod.hijos.keys():
                nn = nod.hijos.get(x, 0)
                if nn.letraLlegada != None:
                    lista.append((i+1,nn.idi,d + (palabra[i] != nn.letraLlegada)))
                else:
                    lista.append((i,nn.idi,d))

        if(d <= k and nod.palabra != None and (i == len(palabra))):
            cosa = evitreps.get(nod.palabra, 0)
            if cosa == 0:
                evitreps[nod.palabra] = 1
                result.append(nod.palabra)

    return result
##############################################################################
def levenstein_vs_trie_ramificacionD(tri, palabra, k):
    lista = [(0,0,0)]
    nod = tri.root()
    result = []
    evitreps = {}

    while (len(lista)):
        i,n,d = lista.pop()

        if n == 0:
            nod = tri.array[n]
        else:
            nod = tri.array[n-1]

        #insercion
        if(d+1 <= k and i <= len(palabra) and len(nod.hijos) > 0):
            for x in nod.hijos.keys():
                nn = nod.hijos.get(x,0)
                lista.append((i,nn.idi,d+1))

        #borrado
        if(d+1 <= k and i < len(palabra)):
            lista.append((i+1,nod.idi, d+1))

        #sustitucion
        if(d <= k and len(nod.hijos) > 0 and i < len(palabra)):
            for x in nod.hijos.keys():
                nn = nod.hijos.get(x, 0)
                if nn.letraLlegada != None:
                    lista.append((i+1,nn.idi,d + (palabra[i] != nn.letraLlegada)))
                else:
                    lista.append((i,nn.idi,d))

        #vueltacionNietos
        if(d+1 <= k and len(nod.hijos) > 0 and i+1 < len(palabra)):
            for x in nod.hijos.keys():
                nn = nod.hijos.get(x,0)
                if(nn.letraLlegada == palabra[i+1]):
                    for y in nn.hijos.keys():
                        nietos = nn.hijos.get(y,0)
                        if(nietos.letraLlegada == palabra[i]):
                            lista.append((i+2,nietos.idi,d+1))

        #result
        if(d <= k and nod.palabra != None and (i == len(palabra))):
            cosa = evitreps.get(nod.palabra, 0)
            if cosa == 0:
                evitreps[nod.palabra] = 1
                result.append(nod.palabra)

    return result
