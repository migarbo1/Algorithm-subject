#!/usr/bin/env python
#! -*- encoding utf8

def damerau_levenstein_distance(word1, word2):
    #dado que tenemos que acceder a la pposicios -2 en j tenemos que tener 3 filas
    c_row = [None] * (len(word1) + 1)
    p_row = [None] * (len(word1) + 1)
    aux_row = [None] * (len(word1) + 1) #fila para acceder a la pos -2 en j
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
            if (word1[i -1] == word2[i - 2] and word2[i -1] == word1[i - 2]):
                c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[i - 1]),#elemento anteior en x e y mas si son diferentes (sustitucion por el mismo es 0)
                            (aux_row[i - 2] + 1)) #transposicion
            else:
                c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[i - 1]))

    return c_row[len(word1)]
