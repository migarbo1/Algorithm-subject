#!/usr/bin/env python
#! -*- encoding utf8

#trie es una estructura en la que calculas la distancia de lenestein desde el nodo 0 en adelante. para cada nodo debes enfrontar la letra de la transicion con la el simbolo actual de la palabra
#levenstein_vs_trie(a[0],0) = 0 donde 0 es el idientificador del nodo (case 1)
#levenstein_vs_trie(a[i],0) = i donde i es la posicion de la letra que estas analizando dentro de la palabra
#levenstein_vs_trie(a[0],X) = depth(X) donde X es un nodo diferente del 0
#levenstein_vs_trie(a[i],X) =
#min(
#levenstein_vs_trie(a[i - 1], X) + 1
#levenstein_vs_trie(a[i], parent(X)) + 1
#levenstein_vs_trie(a[i - 1], parent(X)) + 1 * a[i] != char(X)
#)

#zona de imports
import numpy as np
import TRie as trie

def levenstein_vs_trie(trie, palabra, k):
    nodo = trie.root()
    matrix = np.zeros(dtype=np.int8, shape=(len(trie.array) + 1, len(palabra) + 1)) #creamos una matriz de nodos (filas) por simbolos de la palabra (columnas)
    result = []

    matrix[nodo.idi,0] = 0 #case 1

    for i in range(len(palabra)+1): #case 2
        matrix[nodo.idi,i] = i

    for n in trie.array: #case 3
        matrix[n.idi,0] = n.profundidad
        for i  in range(len(palabra) + 1):
            if (nodo.idi != n.idi):
                matrix[n.idi,i] = min(
                    matrix[n.idi,i - 1] + 1,
                    matrix[n.nodoPadre.idi,i] + 1,
                    matrix[n.nodoPadre.idi,i - 1] + (palabra[i-1] != n.char())
                )

    for n in trie.array:
        if(n != nodo):
            if matrix[n.idi,len(palabra)] <= k:
                if n.palabra != None:
                    if n.palabra not in result:
                        result.append(n.palabra)

    return result
