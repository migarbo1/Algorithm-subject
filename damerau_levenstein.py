#!/usr/bin/env python
#! -*- encoding utf8

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


def damerau_levenstein_distance(word1, word2):
    #dado que tenemos que acceder a la pposicios -2 en j tenemos que tener 3 filas
    c_row = [none] * (len(word1) + 1)
    p_row = [none] * (len(word1) + 1)
    aux_row = [none] * (len(word1) + 1) #fila para acceder a la pos -2 en j
    c_row[0] = 0 #caso i = j = 1
    for i in range(1, len(word1) + 1): #caso i > 0 j = 0
        c_row[i] = c_row[i - 1] + 1

    p_row,c_row = c_row,p_row
    for i in range(1, len(word1) + 1): #caso j = 1 i > 0
        c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                    p_row[i] + 1, #elemento de abajo en y
                    p_row[i - 1] + (word1[i - 1] != word2[i - 1]))

    for j in range(2, len(word2) + 1):
        aux_row,p_row,c_row = p_row,c_row,aux_row
        c_row[0] = p_row[0] + 1 #esto es para sumarle 1 a la col[0], es decir, simular la insercion completa de la palabra
        for i in range(1, len(word1) + 1):
            if (word1[i -1] == word2[i - 2] and word2[i -1] == word1[i - 2]);
                c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[i - 1]),#elemento anteior en x e y mas si son diferentes (sustitucion por el mismo es 0)
                            (aux_row[i - 2] + 1)) #transposicion
            else:
                c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[i - 1]))

    return c_row[len(word1)]
