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

def levenstein_vs_trie_ramificacion(trie, palabra, k):
    lista = [(0,0,0)] # (elementode la plalabra, nodo, distancia a mi coraxon)
    nodo = trie.root()
    result = []

    while(len(lista)):
        i,n,d = lista.pop()
        nodo = trie.array[n]
        #insercion
        if(d+1 <= k and len(nodo.hijos) > 0):
            for x in nodo.hijos.keys:
                if(x != palabra[i]):
                    nn = nodo.hijos.get(x, 0)
                    lista.append((i,nn.idi,d+1))
        
        #borracion
         if(d+1 <= k and i < len(palabra)):
            lista.append((i+1,nodo,d+1))

        #sustitutusao
        if(d <= k and len(nodo.hijos) > 0 and i <= len(palabra)):   #Esta mal, te que ser menor estricte, ja que no pots estar en la posicio: paraula[len(praula)], si comença desde 0
            for x in nodo.hijos.keys:
                nn = nodo.hijos.get(x, 0)
                lista.append((i+1,nn.idi,d + (palabra[i] != x))

        #vueltacionNietos
        if(d+1 <= k and len(nodo.hijos) > 0 and i+1 < len(palabra)):
            for x in nodo.hijos.keys:
                if(x == palabra[i+1]):
                    for y in x.hijos.keys:
                        if(y == palabra[i]):
                            lista.append((i+2,y,d+1))

        #ponicion en el result
        if(d <= k and nodo.palabra != None):
            if(nodo.palabra not in result):
                result.append(nodo.palabra)

    return result
