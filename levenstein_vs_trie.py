#!/usr/bin/env python
#! -*- encoding utf8

#trie es una estructura en la que calculas la distancia de lenestein desde el nodo 0 en adelante. para cada nodo debes enfrontar la letra de la transición con la el simbolo actual de la palabra
#levenstein_vs_trie(a[0],0) = 0 donde 0 es el identificador del nodo (case 1)
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
import TRie

def levenstein_vs_trie(trie: trie, palabra, k):
    nodo = trie.root()
    matrix = np.zeros(shape(len(trie.array) + 1), len(palabra) + 1) #creamos una matriz de nodos (filas) por simbolos de la palabra (columnas)
    result = []

    matrix[nodo.id,0] = 0 #case 1
    
    for i in len(palabra)+1: #case 2
        matrix[nodo.id,i] = i
    
    for n in trie.array: #case 3
        matrix[n.id,0] = n.profundidad()
        for i  in len(palabra)+1:
            matrix[n.id,i] = min(
                matrix[n.id,i - 1] + 1,
                matrix[n.parent().id,i] + 1,
                matrix[n.parent().id,i - 1] + (a[i] != n.char())
            )
    print(matrix)

    for n in trie.array:
        if matrix[n.id,len(palabra)] <= k:
            result[n] = n.sacarPalabra()

    return result
    