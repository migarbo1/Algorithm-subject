#!/usr/bin/env python
#! -*- encoding utf8

## zona de imports
#import numpy as np
import re
import sys
import os
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
    file = open(file,"r")
    text = file.read()
    file.close()
    text = clean_text(text)
    text = text.lower()
    text = text.split()
    dictionary = {}
    for t in text:
        dictionary[t] = dictionary.get(t,[])
        if dictionary[t] == []:
            if mode == 1:
                dictionary[t] = [better_levenstein_distance(t,token)] ###aqui esta la llamada###
            else:
                dictionary[t] = [damerau_levenstein_distance(t,token)] ###aqui esta la llamada###

    #llegados a este punto tenemos un diccionario con clave = palabra y valor = distancia respecto al token
    #tenemos que pasarlo a un diccionario con clave = distancia y valor y palabras para asi poder recuperar las que tengan distancia <= tollerance
    wordsPerDist = {}
    for k in dictionary:
        v = dictionary[k][0]
        wordsPerDist[v] = wordsPerDist.get(v,[])
        if wordsPerDist[v] == []:
            wordsPerDist[v] = [k]
        else:
            wordsPerDist[v] = wordsPerDist.get(v) + [k]

    #sobre el ultimo diccionario, recuperamos aquellas listas de palabras con clave <= tolerancia
    for tol in range(0, int(tollerance)):
        res = wordsPerDist.get(tol,[])
        if not res == []:
            print("tolerancia: " + str(tol) + "\n" + "palabras: ")
            print(res)
            print("\n")
#fin de la funcion levenstein_caller

#main
if __name__ == "__main__":
    if len(sys.argv) == 5:
        f = sys.argv[1]
        k = sys.argv[2]
        to = sys.argv[3]
        m = sys.argv[4]
        caller(f,k,to,m)
    else:
        syntax()
