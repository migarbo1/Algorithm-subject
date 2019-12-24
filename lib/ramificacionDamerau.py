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

def levenstein_vs_trie_ramificacionD(trie, palabra, k):
    lista = [(0,0,0)]
    nodo = trie.root()
    result = []
    evitreps = {}

    while (len(lista)):
        i,n,d = lista.pop()

        if n == 0:
            nodo = trie.array[n]
        else:
            nodo = trie.array[n-1]

        #insercion
        if(d+1 <= k and i <= len(palabra) and len(nodo.hijos) > 0):
            for x in nodo.hijos.keys():
                nn = nodo.hijos.get(x,0)
                lista.append((i,nn.idi,d+1))

        #borrado
        if(d+1 <= k and i < len(palabra)):
            lista.append((i+1,nodo.idi, d+1))

        #sustitucion
        if(d <= k and len(nodo.hijos) > 0 and i < len(palabra)):
            for x in nodo.hijos.keys():
                nn = nodo.hijos.get(x, 0)
                if nn.letraLlegada != None:
                    lista.append((i+1,nn.idi,d + (palabra[i] != nn.letraLlegada)))
                else:
                    lista.append((i,nn.idi,d))

        #vueltacionNietos
        if(d+1 <= k and len(nodo.hijos) > 0 and i+1 < len(palabra)):
            for x in nodo.hijos.keys():
                nn = nodo.hijos.get(x,0)
                if(nn.letraLlegada == palabra[i+1]):
                    for y in nn.hijos.keys():
                        nietos = nn.hijos.get(y,0)
                        if(nietos.letraLlegada == palabra[i]):
                            lista.append((i+2,nietos.idi,d+1))

        #result
        if(d <= k and nodo.palabra != None and (i == len(palabra))):
            cosa = evitreps.get(nodo.palabra, 0)
            if cosa == 0:
                evitreps[nodo.palabra] = 1
                result.append(nodo.palabra)

    return result
