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
    lista = [(0,0,0,"")] # (elementode la plalabra, nodo, distancia a mi coraxon)
    nodo = trie.root()
    result = []
    while(len(lista)):
        print("////////////////////////////////////////////////////////")
        i,n,d,s = lista.pop()
        print("Posicion de la palabra: ", i)
        print("Nodo: ", n)
        print("Distancia: ", d)
        print("Secuencia: ", s)
        if n == 0:
            nodo = trie.array[n]
        else:
            nodo = trie.array[n-1]
        print("Vengo de: ", nodo.letraLlegada)
        print("Tengo plalabra: ", nodo.palabra)
        #insercion
        if(d+1 <= k and len(nodo.hijos) > 0 and i < len(palabra)):
            for x in nodo.hijos.keys():
                if(x != palabra[i]):
                    nn = nodo.hijos.get(x, 0)
                    print("Inserto")
                    auxs = s + "i "
                    lista.append((i,nn.idi ,d+1,auxs))

        #borracion
        if(d+1 <= k and i < len(palabra)):
            print("Borro")
            auxs = s + "b "
            lista.append((i+1,nodo.idi ,d+1,auxs))

        #sustitutusao
        if(d <= k and len(nodo.hijos) > 0 and i < len(palabra)):
            for x in nodo.hijos.keys():
                nn = nodo.hijos.get(x, 0)
                if nodo.letraLlegada != None:
                    print("Sustituyo 1")
                    auxs = s + "s1 "
                    lista.append((i+1,nn.idi,d + (palabra[i] != nodo.letraLlegada),auxs))
                else:
                    print("Sustituyo 2")
                    auxs = s +"s2 "
                    lista.append((i,nn.idi,d,auxs))

        if(d <= k and nodo.palabra != None and i = len(palabra)):
            print("Soy resultado")
            result.append(nodo.palabra)

    return result
