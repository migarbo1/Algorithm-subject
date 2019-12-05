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
    casTransp = False;
    matrix[node.idi, 0] = 0
    res = []

    for ln in range(len(word)+1):
        matrix[node.idi, ln] = ln
 	
    for n in trie.array:
        matrix[n.idi, 0] = n.profundidad
        for ll in range(len(word)+1):
            fills = n.hijos.values();
            for f in fills:
                if(ll < len(word)-1):
                    if(f.letraLlegada == word[ll+1] and word[ll] == n.letraLlegada): 
                        casTransp = True;
                    else: 
                        casTransp = False;
                        				
			
            if(node.idi != n.idi):
                if(casTransp):                    
                    matrix[n.idi, ll] = min(
                            matrix[n.idi, ll-1] + 1, #ins
                            matrix[n.nodoPadre.idi, ll] + 1, #borr
                            matrix[n.nodoPadre.idi, ll - 1] + (word[ll-1] != n.letraLlegada), #sust
                            matrix[n.nodoPadre.idi, ll-2] + 1 #canvi lletres                
                			)
                else:
                    matrix[n.idi, ll] = min(
                            matrix[n.idi, ll-1] + 1, #ins
                            matrix[n.nodoPadre.idi, ll] + 1, #borr
                            matrix[n.nodoPadre.idi, ll - 1] + (word[ll-1] != n.letraLlegada), #sust
                            )
                    
     
    for n in trie.array:
        if(n != node):
            if matrix[n.idi,len(word)] <= toler:
                if n.palabra != None:
                    if n.palabra not in res:
                        res.append(n.palabra)

    return res






    

