#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""
Martinez Sanchis, Genis
Garcia Bohigues, Miguel
Piqueres Matoses, Pilar
Giner Vidal, Angel
"""

import re
import sys
import json
import pickle
import ALT_library as libo

termsnip = [] #lista e terminos que usaremos para generar el snippset
conparent = []
numparent = 0
findi = None #Objeto indice

clean_re = re.compile('\W+')

def clean_text(text): #limpia el texto
    return clean_re.sub(' ', text)

def load_object(file_name):
    with open (file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj

def load_json(filename):
    with open(filename) as fh:
        obj = json.load(fh)
    return obj

def gensnippet(ar): #genera snippsets
    listindi = [] #Lista donde se guardan los indices de los terminos de la querry
    ressnip = "" # resultado
    #pasamos a minuscula limpiamos, quitamos tabueladores y finales de linea
    ar = ar.lower()
    ar = clean_text(ar)
    ar = ar.replace("\n"," ")
    ar = ar.replace("\t"," ")
    ar = ar.split()# Separamos el articulo en una lista de plabras
    for t in termsnip:# Para cada termino de la querry obtenermos su primer indice en el articulo
        try:
            listindi.append(ar.index(t))
        except:
            pass
    listindi.sort() # ordenamos los indices
    for x in listindi:# Creamos el snippet obteniendo pedazos de texto de longitud 9 teniendo los terminos en el medio
        inn = max((x-4),0)# Evitamos salirnos del array
        fi = min((x+5),len(ar))# Evitamos salirnos del array
        ressnip = ressnip + " " + "..." + " ".join(ar[inn:fi]) + "..." # generamos el snippet
    return ressnip

def parsequerry(que):#Pasamos a minuscula y semaparamos la querry
    que = que.lower()
    que = que.split()
    #procedemos a encontrar segmentos de la querry que esten entre comillas y juntarlos en un solo termino
    auxque = []
    inn = -1 #posicion de la primera comilla
    cun = 0 #contador
    for e in que: #recorremmos todods los terminos
        if '"' in e: #si el termino contiene comillas
            if inn == -1: #y no se ha encontrado ninguna comilla
                inn = cun
            else: #en el casos de que si se haya encontrado una comilla antes creamos el termino conjunto
                auxque.append(" ".join(que[inn:cun+1]))
                inn = -1 #restablecemos la posicion para mas posibles comillas
        else:
            if inn == -1: # en el caso de que inn != -1 significa que el terino esta entre comillas asi que no se añade
                auxque.append(e)
        cun += 1
    que = auxque
    return que

"""
Recorremos la querry en busca de parentesis, si encontramos alguno obtenemos una query secundaria de el
y realizamos la consuta de esa querry buardando el resultado en una lista auxuliar y sustituyendo los Terminos
entre parentesis por una palabra clave con la posicion de los resultados en la lista auxiliara para su posterior uso
Ejemplo: casa or (cosa and coche) -> casa or rexultadio0 estando en la posicion 0 de la lista auxiliar el
resultado de la subquerry cosa and coche.
"""
def parentesis(quensulta):
    primer = -1
    ulti = -1
    cont = 0
    while cont < len(quensulta) and ulti == -1: # obtenemos el congunto de parentesis mas interiorores posible
        if (quensulta[cont] == "("):
            primer = cont
        if (quensulta[cont] == ")"):
            ulti = cont
        cont += 1
    if primer == -1: # si no se ha encontrado ninguno se devuelve la querry tal y como esta
        return quensulta, 1
    nuevaq = quensulta[primer+1:ulti] #se generra la subquerry
    cambio = "rexultadio" + str(len(conparent)) #generamos la plabra clave que sustuira al los parentesis
    conparent.append(consulta(findi, nuevaq)) #colocamos el resultado de la subquerry en la lista
    quensulta = quensulta.replace(quensulta[primer:ulti+1], cambio) #realizamos los parentesis por la palabra clave
    return quensulta, 0

"""
Se obtiene el resultado de una consuta posicional reescribiendo el termino en una subquerry
compuesta por ands, para cada resultado de la consulta de la subquerry se accedera y se buscara
el termino como tal y se devolvera solo los que contengan ese termino.
Ejemplo title:"fin de semana" -> title:fin and title:de and title:semana
"""
def posicional(ttt,lugbuss):
    #transformamos el termino en una querry compuesta por ands y el lubar de busqueda
    precosas = ["","","article","title","summary","keywords","date"]
    ttt = ttt.replace('"', "")
    ttta = precosas[lugbuss] + ":" + ttt
    ttta = ttta.replace(" ", " and " + precosas[lugbuss] + ":")
    rrr = consulta(findi, ttta)# realizamos la consuta de la subquerry
    k = len(rrr)
    dicDoc = findi[0]
    dicArt = findi[1]
    c = 0
    resulteido = []
    #recorre los resultados y comprueba cuales contienen el termino entero
    while c < k:
        ndoc,posdoc = dicArt[rrr[c]]
        with open(dicDoc[ndoc]) as json_file:
            ob = json.load(json_file)
        arti = ob[posdoc]
        if ttt in arti[precosas[lugbuss]].lower():
            resulteido.append(rrr[c])
        c += 1
    return resulteido
"""
Devuelve el temino limpio ellugar de busqueda como un numero
"""
def procesarTermino(tt):
    if "article:" in tt:
        return tt.replace("article:",""), 2
    if "title:" in tt:
        return tt.replace("title:",""), 3
    if "summary:" in tt:
        return tt.replace("summary:",""), 4
    if "keywords:" in tt:
        return tt.replace("keywords:",""), 5
    if "date:" in tt:
        return tt.replace("date:",""), 6
    return tt, 2

def procesodist(laque):
    laques = laque.lower()
    laques = laques.split()
    for indx in len(laques):
        j = laques[indx]
        if '%' in j:
            elresult = libo.levenstein_vs_trie_ramificacion(tri,j[0:j.find('%')],int(j[j.find('%')+1]))
            elresult = ' or '.join(elresult)
            elresult  = '( ' + elresult + ' )'
            laques[indx] = elresult
        elif '@' in j:
            elresult = libo.levenstein_vs_trie_ramificacionD(tri,j[0:j.find('@')],int(j[j.find('@')+1]))
            elresult = ' or '.join(elresult)
            elresult  = '( ' + elresult + ' )'
            laques[indx] = elresult
    return ' '.join(laques)

"""
Se recorrera la querry detectando los operadores booleanos y realizando las
operaciones interseccion, union y diferencia requeridas.
1 = and, 2 = or, 3 = not, 10 = and not, 20 = or not
Cuando se encuentre un termino que no sea boleano se transferira a el metodo
correspondiete dependiendo si esun palabra clave de los parentesis, si tiene ""
, si tiene * o ?, o si es un termino normal.
se han realizado diferentes if por si el termino es el primero, vaseguido de un
and, or, not o culaquier combinacion.
"""
def consulta(ind, q):
    #aplicamos el preproceso pra transformal la palabeas co @ y % en un conjunto de palabras

    print("Antes del proceso: ", q)
    q = procesodist(q)
    print("Despues del proceso: ", q)
    aux = None
    flag = 0
    while flag == 0: # se aplica parentesis hasta que se hayan sustituido todos por palabras clave
        q,flag = parentesis(q)
    operador = -1
    res = []
    inda = ind[1]
    q = parsequerry(q)
    for t in q:# Recorrremos la querry
        #print("TERMINO: ", t)
        t,lugbus = procesarTermino(t) # te devuelve el termino limpio y el diccionario en el que tienes que bucar

        if len(res) == 0 and not t == "not" and not t == "and" and not t == "or" and operador == -1:
            #print("PRIMER TERMINO")
            if "rexultadio" in t:
                aux = conparent[int(t.replace("rexultadio",""))]
            elif '"' in t:
                aux = posicional(t,lugbus)
            elif '*' in t or '?' in t:
                aux = consulta(findi,get_term_from_permuterm(t,findi,lugbus))
            else:
                aux = ind[lugbus].get(t,[]) #************************************************
            if aux is not []:
                res += aux
                if "rexultadio" not in t:
                    termsnip.append(t)
        else:
            if(t == "and" or t == "or" or t == "not"):
                if t == "and": #es una and
                    #print("HE ENCONTRADO UN AND")
                    operador = 1
                if t == "or":
                    #print("HE ENCONTRADO UN OR")
                    operador = 2
                if t == "not":
                    #print("HE ENCONTRADO UN NOT")
                    if operador > 0:
                        #print("NOT DOBLE")
                        operador = operador*10
                    else:
                        #print("NOT SIMPLE")
                        operador = 3
            else:
                if operador == 1:
                    #print("HE APLICADO UN AND")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t,lugbus)
                    elif '*' in t or '?' in t:
                        aux = consulta(findi,get_term_from_permuterm(t,findi,lugbus))
                    else:
                        aux = ind[lugbus].get(t,[]) #*******************************************************************
                    if aux is not []:
                        termsnip.append(t)
                    res = intersection(res, aux)
                if operador == 2:
                    #print("HE APLICADO UN OR")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t,lugbus)
                    elif '*' in t or '?' in t:
                        aux = consulta(findi,get_term_from_permuterm(t,findi,lugbus))
                    else:
                        aux = ind[lugbus].get(t,[]) #********************************************************************
                    if aux is not []:
                        termsnip.append(t)
                    res = union(res, aux)
                if operador == 3:
                    #print("HE APLICADO UN NOT")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t,lugbus)
                    elif '*' in t or '?' in t:
                        aux = consulta(findi,get_term_from_permuterm(t,findi,lugbus))
                    else:
                        aux = ind[lugbus].get(t,[]) #*********************************************************************
                    res = diferencia(inda, aux)
                if operador == 10:
                    #print("HE APLICADO UN AND NOT")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t,lugbus)
                    elif '*' in t or '?' in t:
                        aux = consulta(findi,get_term_from_permuterm(t,findi,lugbus))
                    else:
                        aux = ind[lugbus].get(t,[]) #*********************************************************************
                    aux = diferencia(inda, aux)
                    res = intersection(res, aux)
                if operador == 20:
                    #print("HE APLICADO UN OR NOT")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t,lugbus)
                    elif '*' in t or '?' in t:
                        aux = consulta(findi,get_term_from_permuterm(t,findi,lugbus))
                    else:
                        aux = ind[lugbus].get(t,[]) #**********************************************************************
                    aux = diferencia(inda, aux)
                    res = union(res, aux)
                operador = -1
    return res

"""
Dado un termino con wildcard se procesa y se obtiene, de losindices permuten
correspondietes las palabras que lo cumplen y se guenera un a subquerry
compuesta por esas plabras con ors
Ejemplo title:c*sa -> title:casa or title:cosa or title:carrascosa or .....
"""
def get_term_from_permuterm(que,findi,where_to_search):
    donde = ""
    astointe = -1
    longi = len(que)
    # obtenemos el indice donce buscar
    if where_to_search == 2:
        pos_dict = -1 #diccionario de articles
        donde = "article:"
    elif where_to_search == 5:
        pos_dict = -2 #diccionario keywords
        donde = "keywords:"
    elif where_to_search == 3:
        pos_dict = -3 #diccionario de tituls
        donde = "title:"
    elif where_to_search == 6:
        pos_dict = -4 # diccionario de dates
        donde = "dates:"
    elif where_to_search == 4:
        pos_dict = -5 # diccionario de dates
        donde = "summary:"

    dicPerm = findi[pos_dict] #diccionario permuterm de articulos
    keys = dicPerm.keys() #recuperas las claves
    res = "" #cadena de paraules que compleixen la query ex casa cosa amb query c*a
    ##########traduim la query##########
    if '*' in que:
        indirisco = que.index("*")
        astointe = 0
    else:
        indirisco = que.index("?")
        astointe = 1
    aux = que + "$"
    aux = aux[indirisco+1:len(aux)] + aux[0:indirisco]

    for k in keys: # per a cada clau dins del diccionari
        if k.startswith(aux): # si dita clau comensa per la query traduida
            if len(res) == 0: # si es la primera que afegixes no te or
                if astointe == 1 and len(dicPerm[k]) == longi:
                    res += donde + dicPerm[k]
                elif astointe == 0:
                    res += donde + dicPerm[k]
            else: # si no es la primera si.
                if astointe == 1 and len(dicPerm[k]) == longi:
                    res += " or " + donde + dicPerm[k]
                elif astointe == 0:
                    res += " or " + donde + dicPerm[k]
    return res

def intersection(p1,p2):
    res = []
    i = 0
    j = 0
    p1.sort()
    p2.sort()
    while i < len(p1) and  j < len(p2):
        ep1 = p1[i]
        ep2 = p2[j]
        if ep1 == ep2:
            res.append(ep1)
            i+=1
            j+=1
        else:
            if ep1 < ep2:
                i+=1
            else:
                j+=1
    return res

def union(p1,p2):
    res = []
    i = 0
    j = 0
    p1.sort()
    p2.sort()
    while i < len(p1) and  j < len(p2):
        ep1 = p1[i]
        ep2 = p2[j]
        if ep1 == ep2:
            res.append(ep1)
            i+=1
            j+=1
        else:
            if ep1 < ep2:
                res.append(ep1)
                i+=1
            else:
                res.append(ep2)
                j+=1
    while i < len(p1):
        ep1 = p1[i]
        res.append(ep1)
        i+=1
    while j < len(p2):
        ep2 = p2[j]
        res.append(ep2)
        j+=1
    return  res

def diferencia(dic,p2):
    res = []
    for k,_ in dic.items():
        if k not in p2:
                res.append(k)
    return res

"""
dado un conjunto de resusltados y el indice los muestra segun la cantida de resultados
"""
def mostrar(r, ind):
    dicDoc = ind[0]
    dicArt = ind[1]
    m = (0,0,0,0,0) #{fecha, titulo ,keywords, cuerpo, snippet} sirve para saber que es lo que mostramos qy que no
    k = len(r)
    if(k == 0):
        print("No se han encontrado resultados\n")
    if(k == 1 or k == 2):# si hay 1 o 2 resultados
        m = (1,1,1,1,0)
    if(3 <= k and k <= 5): # si hay entre 3 y 5
        m = (1,1,1,0,1)
    if(5 < k): # si hay mas de 5
        k = min(len(r), 10) # com maximo mostramos 10
        m = (1,1,1,0,0)
    c = 0
    fgh = ""
    while c < k: # para cada artiulo imprimimos loq eue tenemos indicado en m
        ndoc,posdoc = dicArt[r[c]]
        with open(dicDoc[ndoc]) as json_file:
            ob = json.load(json_file)
        arti = ob[posdoc]
        fgh = fgh + dicDoc[ndoc] + "\n"
        p = ""
        if m[0]:
            p = p + arti["date"] + " "
        if m[1]:
            p = p + arti["title"] + " "
        if m[2]:
            p = p + "[" + arti["keywords"] + "]" + " "
        if m[3]:
            p = p + arti["article"] + " "
        if m[4]:
            p = p + gensnippet(arti["article"]) + " "
        print(p, "\n")
        c = c+1
    print("Numero de resultados: ", len(r), "\n")

    print("Rutas de los resultados:", "\n")

    print(fgh)

if __name__ == "__main__":
    querry = None
    resultado = None
    if len(sys.argv) >= 2:
        findi = sys.argv[1] #indice
        findi = load_object(findi)#(diccionario de documentos, diccionario de articulos, diccionario de terminos)
        tri = load_object("eltrie")
        if len(sys.argv) >= 3:
            querry = sys.argv[2] #querry
        if querry != None:
            if '"' in querry:
                print("yes")
            resultado = consulta(findi, querry)
            mostrar(resultado, findi)
        else:
            while True:
                termsnip = []
                conparent = []
                numparent = 0
                text = input("Dime:")
                if len(text) == 0:
                    break
                querry = text
                #print(querry)
                resultado = consulta(findi, querry)
                mostrar(resultado, findi)
