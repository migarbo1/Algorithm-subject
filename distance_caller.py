#!/usr/bin/env python
#! -*- encoding utf8

## zona de imports
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
    wordsPerDist = {}
    for t in text:
        dictionary[t] = dictionary.get(t,[])
        if dictionary[t] == []:
            if mode == 1:
                r = [better_levenstein_distance(t,token)] ###aqui esta la llamada###
                if wordsPerDist.get(r,[]) == []:
                    wordsPerDist[r] = [t]
                else:
                    wordsPerDist[r] += [t]
            else:
                r = [damerau_levenstein_distance(t,token)] ###aqui esta la llamada###
                if wordsPerDist.get(r,[]) == []:
                    wordsPerDist[r] = [t]
                else:
                    wordsPerDist[r] += [t]

    #sobre el ultimo diccionario, recuperamos aquellas listas de palabras con clave <= tolerancia
    for tol in range(0, int(tollerance) + 1):
        res = wordsPerDist.get(tol,[])
        if not res == []:
            print("tolerancia: " + str(tol) + "\n" + "palabras: " + srt(len(res)))
            print(res)
            print("\n")
#fin de la funcion levenstein_caller

#main
if __name__ == "__main__":
    if len(sys.argv) == 5:
        f = sys.argv[1] #fichero
        k = sys.argv[2] #tolerancia
        to = sys.argv[3] #token
        m = sys.argv[4] #modo
        caller(f,k,to,m)
    else:
        print("argumentos inválidos. Requerido nombre fichero, tolerancia, token y modo")
