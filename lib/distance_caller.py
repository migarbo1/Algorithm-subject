#!/usr/bin/env python
#! -*- encoding utf8 -*-

## zona de imports
import re
import sys
import os
import copy
from levenstein_distance import better_levenstein_distance
from damerau_levenstein import damerau_levenstein_distance
##

# clean text
clean_re = re.compile('\W+')

def clean_text(text):
    return clean_re.sub(' ', text)
#fin clean text

#funcion que llama para cada palabra del diccionario a la funcion de levenstein
def caller(file, tollerance,token, mode):
    file = open(file,"r") # se abre el fichero
    text = file.read() # leemos el fichero
    file.close() # lo cerramos
    text = clean_text(text) # eliminamos los caracteres no alfanumericos
    text = text.lower() # minusculas
    text = text.split() # separamos las palabras
    dictionary = {}
    wordsPerDist = {} # diccionario de distancias y palabras
    print("Llenando diccionario")
    for t in text: #anadimos las palabras al diccionario
        d = dictionary.get(t,[])
        if d == []: # evitamos repetidas
            dictionary[t] = 1
            if mode == 1:
                r = better_levenstein_distance(token,t) ###aqui esta la llamada###
                wordsPerDist[r] = wordsPerDist.get(r,[])
                wordsPerDist[r] += [t]
            else:
                if(len(token)>=len(t)):
                    r = damerau_levenstein_distance(token,t) ###aqui esta la llamada###
                else:
                    r = damerau_levenstein_distance(t,token)
                if r <= tollerance:
                     print(r, t)
                wordsPerDist[r] = wordsPerDist.get(r,[])
                wordsPerDist[r] += [t]

    print("Mostrando resultados")
    #sobre el ultimo diccionario, recuperamos aquellas listas de palabras con clave <= tolerancia
    aux1 = []
    for k in sorted(wordsPerDist.keys()):
        if k == 0:
            aux1 = wordsPerDist[k]
        else:
            ak = k-1
            aux1 += wordsPerDist[ak]
            wordsPerDist[k] += copy.copy(aux1)
        aux1 = []

    for tol in range(0, int(tollerance) + 1):
        res = wordsPerDist.get(tol,[])
        if not res == []:
            print("tolerancia: " + str(tol) + "\n" + "palabras: " + str(len(res)))
            print(res)
    #sobre el ultimo diccionario, recuperamos aquellas listas de palabras con clave <= tolerancia
    for tol in wordsPerDist.keys():
        if int(tol) >= tollerance+1:
            break
        wordsPerDist[tol]
        if not wordsPerDist[tol] == []:
            print("tolerancia: " + str(tol) + "\n" + "palabras: " + str(len(wordsPerDist[tol])))
            print(wordsPerDist[tol])
            print("\n")
#fin de la funcion levenstein_caller

#main
if __name__ == "__main__":
    if len(sys.argv) == 5:
        f = sys.argv[1] #fichero
        k = sys.argv[2] #tolerancia
        to = sys.argv[3] #token
        m = sys.argv[4] #modo 1 = normal, !1 damerou
        caller(f,int(k),to,int(m))
    else:
        print("argumentos invalidos. Requerido nombre fichero, tolerancia, token y modo")
