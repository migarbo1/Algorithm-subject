#!/usr/bin/env python
#! -*- encoding utf8

#distancia de levenstein sin ahorro espacial
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
#fin distancia levenstein 1

#distancia de levenstein con ahorro de espacio
def better_levenstein_distance(word1, word2):
    c_row = [None] * (len(word1) + 1)
    p_row = [None] * (len(word1) + 1)
    c_row[0] = 0
    for i in range(1, len(word1) + 1):
        c_row[i] = c_row[i - 1] + 1
    for j in range(1, len(word2) + 1):
        p_row,c_row = c_row,p_row
        c_row[0] = p_row[0] + 1 #esto es para sumarle 1 a la col[0], es decir, simular la insercion completa de la palabra
        for i in range(1, len(word1) + 1):
            c_row[i] = min(c_row[i - 1] + 1, #elemento anterior en eje x
                            p_row[i] + 1, #elemento de abajo en y
                            p_row[i - 1] + (word1[i - 1] != word2[i - 1]))#elemento anteior en x e y mas si son diferentes (sustitucion por el mismo es 0)
    return c_row[len(word1)]
#fin distancia levenstein con ahorro espacial
