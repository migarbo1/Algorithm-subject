#!/usr/bin/env python
#! -*- encoding utf8

## zona de imports
import re
import sys
import os
import copy
from levenstein_distance import better_levenstein_distance
from damerau_levenstein import damerau_levenstein_distance
##

dictionary = {}
wordsPerDist = {}

# clean text
clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)
#fin clean text

#funcion que llama para cada palabra del diccionario a la funcion de levenstein
def caller(file, tollerance,token, mode):
    file = open(file,"r")
    text = file.read()
    file.close()
    text = clean_text(text)
    text = text.lower()
    text = text.split()
    for t in text:
        dictionary[t] = dictionary.get(t,[])
        if dictionary[t] == []:
            dictionary[t] = ["v"]
            if mode == 1:
                r = int(better_levenstein_distance(t,token)) ###aqui esta la llamada###
                wordsPerDist[r] = wordsPerDist.get(r,[])
                wordsPerDist[r] += [t]
            else:
                r = int(damerau_levenstein_distance(t,token)) ###aqui esta la llamada###
                wordsPerDist[r] = wordsPerDist.get(r,[])
                wordsPerDist[r] += [t]
    first = True
    for k in wordsPerDist.keys():
        print("al principio")
        print(wordsPerDist[k])
        if first:
            aux1 = wordsPerDist[k]
            first = False
        else:
            aux1 += wordsPerDist[k]
        wordsPerDist[k] = copy.copy(aux1)
        print("despues")
        print(wordsPerDist[k])
        print("\n")
    #sobre el ultimo diccionario, recuperamos aquellas listas de palabras con clave <= tolerancia
    print("Printenado las cosas")
    print("\n")
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
        m = sys.argv[4] #modo
        caller(f,int(k),to,int(m))
    else:
        print("argumentos invalidos. Requerido nombre fichero, tolerancia, token y modo")
