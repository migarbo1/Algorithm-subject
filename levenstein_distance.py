#!/usr/bin/env python
#! -*- encoding utf8

## zona de imports
import numpy as np
import re
import sys
import os
##

clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)

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

def levenstein_caller(file, tollerance,token):
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
            dictionary[t] = [levenstein_distance(t,token)]

    #llegados a este punto tenemos un diccionario con clave = palabra y valor = distancia respecto al token
    #tenemos que pasarlo a un diccionario con clave = distancia y valor y palabras para así poder recuperar las que tengan distancia <= tollerance
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
#main
if __name__ == "__main__":
    if len(sys.argv) == 4:
        f = sys.argv[1]
        k = sys.argv[2]
        to = sys.argv[3]
        levenstein_caller(f,k,to)
    else:
        syntax()
