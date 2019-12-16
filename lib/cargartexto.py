#!/usr/bin/env python
#! -*- encoding utf8

## zona de imports
import re
import sys
import os
import TRie as trie
import levenstein_vs_trie as lvt
import damerau_levenstein_vs_trie as dlvt
import damerau_levenstein as dl


# clean text
clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)
#fin clean text

#funcion que llama para cada palabra del diccionario a la funcion de levenstein
def caller(file, tollerance,token):
    file = open(file,"r")
    text = file.read()
    file.close()
    text = clean_text(text)
    text = text.lower()
    text = text.split()
    text = sorted(text)
    trio = trie.trie()
    for t in text:
        trio.insertarPalabra(t)
    print("sin damerou")
    aux = lvt.levenstein_vs_trie(trio, token, tollerance)
    print(len(aux))
    print(aux)
    #print("++++++++++++++++++++++++con dameury++++++++++++++++++")
    #print(dlvt.damerau_levenstein_vs_trie(trio, token, tollerance))
#fin de la funcion levenstein_caller

#main
if __name__ == "__main__":
    if len(sys.argv) == 4:
        f = sys.argv[1] #fichero
        k = sys.argv[2] #tolerancia
        to = sys.argv[3] #token
        caller(f,int(k),to)
    else:
        print("argumentos invalidos. Requerido nombre fichero, tolerancia, token")
