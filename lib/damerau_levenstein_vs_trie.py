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
 	
    node = trie.root()
    matrix= np.zeros(dtype = np.int8,shape = (len(trie.array)+1, len(word)+1))
    cont = 0
    casTransp = False;
    matrix[node.idi, 0] = 0
    aux = 3000

    for l in word:
        matrix[node.idi, l] = l
 	
    for n in trie.array:
        matrix[n.idi, 0] = trie.profundidad
        for ll in range(word):
            fills = n.hijos;
            for f in fills:
                if(f.char == ll and word[cont + 1] == n.char):
                    casTransp = True;
				
			
            if(node.idi != n.idi):
                if(casTransp):
                   aux = matrix[n.parent().idi, ll-2] #canvi lletres
                matrix[n.idi, ll] = min(
                        matrix[n.idi, ll-1] + 1, #ins
                        matrix[n.parent().idi, ll + 1], #borr
                        matrix[n.parent().idi, ll - 1] + (word[ll] != n.char()), #sust
                        aux               
            			)            
        cont += 1







    

