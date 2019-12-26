#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""
Martinez Sanchis, Genis
Garcia Bohigues, Miguel
Piqueres Matoses, Pilar
Giner Vidal, Angel
"""

import json
import pickle
import re
import sys
import os
import ALT_library as libo

# cada doc: {'article': ' ','url' 'date' 'keywords' 'id': '', 'summary': '', 'title':''}, {'article'...
#guardar un objecte(índex) en un fitxer
def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

clean_re = re.compile('\W+')

def clean_text(text):
    return clean_re.sub(' ', text)



def indexer(folder,fitxerGuardat):

    dDocs = {}# Diccionario de documentos (k indice, v path)
    dArticles = {} # Diccionario de articulos(k indice del articulo, v (num documento, posicion dentro del documentos))
    postingListTerms = {} # Diccionario de Terminos (k Termino, v lista de articulos que aparece)
    postingListTitle = {} # diccionario inverso de las palabras de los titulos
    postingListSummary = {} # Diccionario inverso de las palabras del sumario
    postingListKeywords = {} # Diccionario inverso de palabras clave
    postingListDate = {} # Diccionario inverso de fechas

    permutemDicArticle = {} #Diccionari de index permutem per paraula.
    permutemDicDate = {}
    permutemDicTitle = {}
    permutemDicKeywords = {}
    permutemDicSummary = {}

    tri = libo.trie()

    for dirname, subdirs, files in os.walk(folder): #"paseja" per la carpeta
        for filename in files: #agafa els fitxers
            wholeName = os.path.join(dirname,filename)
            with open(wholeName) as json_file:
                ob = json.load(json_file)#carrega el fitxer
            dDocs[len(dDocs)] = wholeName #afig el fitxer al diccionari de fitxers
            pos = 0
            for noti in ob:#para cada noticia dentro del objeto
                tupla = [len(dDocs)-1,pos]#creas la tupla de el articulo
                pos +=1

                dArticles[len(dArticles)] = tupla #insertamos la tupla en el diccionario

                 #seleccion de las secciones a indexar
                text = noti["article"]
                title = noti["title"]
                summary = noti["summary"]
                keywords = noti["keywords"]
                date = noti["date"]

                #paso a minuscula
                text = text.lower()
                title = title.lower()
                summmary = summary.lower()
                keywords = keywords.lower()

                #eliminación de caracteres no alfanumericos
                text = clean_text(text)
                title = clean_text(title)


                #eliminación de saltos de linea y tabuladores
                text = text.replace("\n"," ")
                text = text.replace("\t"," ")
                title = title.replace("\n"," ")
                title = title.replace("\t"," ")
                summary = summary.replace("\n"," ")
                summary = summary.replace("\t"," ")
                keywords = keywords.replace("\n"," ")
                keywords = keywords.replace("\t"," ")

                #separación del texto
                text = text.split()
                title = title.split()
                summary = summary.split()
                keywords = keywords.split(",")

                #inserción en cada diccionario inverso el contenido a indexar
                for simb in text: #para cada temino en el texto
                    postingListTerms[simb] = postingListTerms.get(simb,[])# recuperas el termino
                    if postingListTerms[simb] == [] : # si recuperas nada
                        postingListTerms[simb] = [len(dArticles)-1]
                    else :
                        var = len(postingListTerms[simb])
                        lista = postingListTerms[simb]
                        if len(dArticles)-1 > lista[var-1]: #si el article que estem procesant es major que el ultim inserit vol dir que no esta
                            postingListTerms[simb] = postingListTerms.get(simb) + [len(dArticles)-1]


                for simb in title: #para cada temino en el texto
                    postingListTitle[simb] = postingListTitle.get(simb,[])# recuperas el termino
                    if postingListTitle[simb] == [] : # si recuperas nada
                        postingListTitle[simb] = [len(dArticles)-1]
                    else :
                        var = len(postingListTitle[simb])
                        lista = postingListTitle[simb]
                        if len(dArticles)-1 > lista[var-1]: #si el article que estem procesant es major que el ultim inserit vol dir que no esta
                            postingListTitle[simb] = postingListTitle.get(simb) + [len(dArticles)-1]


                for simb in summary: #para cada temino en el texto
                    postingListSummary[simb] = postingListSummary.get(simb,[])# recuperas el termino
                    if postingListSummary[simb] == [] : # si recuperas nada
                        postingListSummary[simb] = [len(dArticles)-1]
                    else :
                        var = len(postingListSummary[simb])
                        lista = postingListSummary[simb]
                        if len(dArticles)-1 > lista[var-1]: #si el article que estem procesant es major que el ultim inserit vol dir que no esta
                            postingListSummary[simb] = postingListSummary.get(simb) + [len(dArticles)-1]


                for simb in keywords: #para cada temino en el texto
                    postingListKeywords[simb] = postingListKeywords.get(simb,[])# recuperas el termino
                    if postingListKeywords[simb] == [] : # si recuperas nada
                        postingListKeywords[simb] = [len(dArticles)-1]
                    else :
                        var = len(postingListKeywords[simb])
                        lista = postingListKeywords[simb]
                        if len(dArticles)-1 > lista[var-1]: #si el article que estem procesant es major que el ultim inserit vol dir que no esta
                            postingListKeywords[simb] = postingListKeywords.get(simb) + [len(dArticles)-1]

                postingListDate[date] = postingListDate.get(simb,[])# recuperas el termino
                if postingListDate[date] == [] : # si recuperas nada
                    postingListDate[date] = [len(dArticles)-1]
                else :
                    var = len(postingListDate[date])
                    lista = postingListDate[date]
                    if len(dArticles)-1 > lista[var-1]: #si el article que estem procesant es major que el ultim inserit vol dir que no esta
                        postingListDate[date] = postingListDate.get(date) + [len(dArticles)-1]


            for term in postingListTerms:
                index = 0 #per a la posició de les paraules
                cont = 0
                longitud = len(term) #numero de lletres de la paraula
                numComb = longitud -1 #numero de combinacions segons el numero de lletres de cada paraula
                comb = [term] #llistat de combinacions a inserir en el index permutem
                nova = term + "$" #creem l'ultim permuterm
                permutemDicArticle[nova] = term #l'afegim al diccionari
                nova = "$" + term #creem el primer permuterm
                permutemDicArticle[nova] = term #l'afegim al diccionari
                for l in term:  #este bucle hi ha que canviarlo no sé encara com possar-ho
                    if cont != numComb:
                        index = index +1
                        nova = term[index : longitud] + "$" + term[0 : index]
                        permutemDicArticle[nova] = term
                        cont = cont + 1

            for word in postingListTitle:
                index = 0
                cont = 0
                longitud = len(word)
                numComb = longitud -1
                comb = [word]
                nova = word + "$"
                permutemDicTitle[nova] = word
                nova = "$" + word
                permutemDicTitle[nova] = word
                for l in word:
                    if cont != numComb:
                        index = index +1
                        nova = word[index:longitud] + "$" + word[0:index]
                        permutemDicTitle[nova] = word
                        cont = cont+1

            for word in postingListKeywords:
                index = 0
                cont = 0
                longitud = len(word)
                numComb = longitud -1
                comb = [word]
                nova = word + "$"
                permutemDicKeywords[nova] = word
                nova = "$" + word
                permutemDicKeywords[nova] = word
                for l in word:
                    if cont != numComb:
                        index = index +1
                        nova = word[index:longitud] + "$" + word[0:index]
                        permutemDicKeywords[nova] = word
                        cont = cont+1

            for word in postingListDate:
                index = 0
                cont = 0
                longitud = len(word)
                numComb = longitud -1
                comb = [word]
                nova = word + "$"
                permutemDicDate[nova] = word
                nova = "$" + word
                permutemDicDate[nova] = word
                for l in word:
                    if cont != numComb:
                        index = index +1
                        nova = word[index:longitud] + "$" + word[0:index]
                        permutemDicDate[nova] = word
                        cont = cont+1

            for word in postingListSummary:
                index = 0
                cont = 0
                longitud = len(word)
                numComb = longitud -1
                comb = [word]
                nova = word + "$"
                permutemDicSummary[nova] = word
                nova = "$" + word
                permutemDicSummary[nova] = word
                for l in word:
                    if cont != numComb:
                        index = index +1
                        nova = word[index:longitud] + "$" + word[0:index]
                        permutemDicSummary[nova] = word
                        cont = cont+1




        #creación del objeto y guardado del mismo.
    tri.insertarTexto(postingListTerms.keys())
    tri.insertarTexto(postingListTitle.keys())
    tri.insertarTexto(postingListSummary.keys())
    tri.insertarTexto(postingListKeywords.keys())
    tri.guardar("eltrie")
    objecte = [dDocs, dArticles, postingListTerms, postingListTitle, postingListSummary, postingListKeywords, postingListDate, permutemDicSummary,permutemDicDate,permutemDicTitle,permutemDicKeywords,permutemDicArticle]
    save_object(objecte, fitxerGuardat)



'''El fichero invertido puede ser una tabla hash implementada como un diccionario de
    python, indexado por término y que haga referencia a una lista con los newid
    asociados a ese término.'''

'''La mejor forma de guardar los datos de los índices en disco es utilizar la librería pickle
    que permite guardar un objeto python en disco. Si quieres guardar más de un objeto,
    puedes hacer una tupla con ellos, (obj1, obj2, …, objn), y guardar la tupla. Consulta la
    práctica del mono infinito.'''
    #Toda la información necesaria para el recuperador de noticias se guardará en un único
    #fichero en disco.


'''Aceptará dos argumentos de entrada: el primero el directorio donde está la colección
de noticias y el segundo el nombre del fichero donde se guardará el índice.'''
if __name__ == "__main__":
    if len(sys.argv) == 3:
        colNot = ""
        colNot += sys.argv[1]
        savIndx = sys.argv[2]
        indexer(colNot, savIndx)
    else:
        syntax()
