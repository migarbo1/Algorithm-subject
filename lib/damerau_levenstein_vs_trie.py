#import
import numpy as np
import TRie
 
 #tenim el trie, paraula i tolereancia
 #hem d'anar recorrent la paraula per el trie i calculant damerau_levenstein
 #cas base node arrel - 0 lletres = 0
 #cas 2 node arrel >0 lletres: hem de "inserir tot" la distancia de d_l serà la pos de la lletra en la paraula
 #cas 3 node X 0 lletres = profundidad ATRIBUTO // hem de tornar "la quantitat de voltes que hem inserit" això ve donat per la capa en la que esta i de ahi profundidad
 #cas general node X lletra 1-len(paraula) -> min entre la tipica + lletra actual = node fill // lletra següent = node actual

def damerau_levenstein_vs_trie(trie, word, toler):
 	
    nodo = trie.nodoRaiz
    matrix= np.zeros(dtype = np.int8,shape = (len(trie.array)+1, len(word)+1))
    res = []

    matrix[nodo.idi, 0] = 0 #case 1

    for ln in range(1, len(word)+1): #case 2
        matrix[nodo.idi, ln] = ln
 	
    for n in trie.array:
        if n != nodo:
            matrix[n.idi,0] = n.profundidad #case 3
            for i in range (1,len(word) + 1):
                if (word[i-1] == n.nodoPadre.letraLlegada and word[i-2] == n.letraLlegada) and n.nodoPadre.nodoPadre != None:
                    matrix[n.idi,i] = min(
                        matrix[n.idi,i - 1] + 1,
                        matrix[n.nodoPadre.idi,i] + 1,
                        matrix[n.nodoPadre.idi,i - 1] + (word[i-1] != n.letraLlegada),
                        matrix[n.nodoPadre.nodoPadre.idi,i - 2] + 1
                    )
                else:
                    matrix[n.idi,i] = min(
                        matrix[n.idi,i - 1] + 1,
                        matrix[n.nodoPadre.idi,i] + 1,
                        matrix[n.nodoPadre.idi,i - 1] + (word[i-1] != n.letraLlegada)
                    )
     
    for n in trie.array:
        if(n != nodo):
            if matrix[n.idi,-1] <= toler:
                if n.palabra != None:
                    if n.palabra not in res:
                        res.append(n.palabra)

    return res