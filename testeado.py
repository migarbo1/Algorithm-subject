#!/usr/bin/env python
#! -*- encoding utf8 -*-

import ALT_library as libo
import time

text = libo.leer_texto("quijote.txt")
tri = libo.trie()
tri.insertarTexto(text)
print("Texto cargado")

print("Tiempos de aplicación de Levenstein: ")

############### cadena vs cadena ####################

start = time.time()
for t in text:
    libo.better_levenstein_distance(t,"xi")
end = time.time()
tim = (end-start)
print("Levenstein cadena vs cadena: palabra xi : " + str(tim))

start = time.time()
for t in text:
    libo.better_levenstein_distance(t,"casa")
end = time.time()
tim = (end-start)
print("Levenstein cadena vs cadena: palabra casa : " + str(tim))

start = time.time()
for t in text:
    libo.better_levenstein_distance(t,"constitución")
end = time.time()
tim = (end-start)
print("Levenstein cadena vs cadena: palabra constitución : " + str(tim))

################# trie básico ####################
for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie(tri,"xi",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE: Palabra xi, Tolerancia " + str(i) + " : " + str(tim))


for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie(tri,"casa",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE: Palabra casa, Tolerancia " + str(i) + " : " + str(tim))


for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie(tri,"constitución",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE: Palabra constitución, Tolerancia " + str(i) + " : " + str(tim))

################# trie con ramificación ###################

for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie_ramificacion(tri,"xi",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE con ramificación de estados: Palabra xi, Tolerancia " + str(i) + " : " + str(tim))

for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie_ramificacion(tri,"casa",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE con ramificación de estados: Palabra casa, Tolerancia " + str(i) + " : " + str(tim))

for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie_ramificacion(tri,"constitución",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE con ramificación de estados: Palabra constitución, Tolerancia " + str(i) + " : " + str(tim))

##################################################################################################################################
##################################################################################################################################

print("Tiempos de aplicación de Damerau-Leventein")

############### cadena vs cadena ####################

start = time.time()
for t in text:
    libo.damerau_levenstein_distance(t,"xi")
end = time.time()
tim = (end-start)
print("Damerau-Levenstein cadena vs cadena: palabra xi : " + str(tim))


start = time.time()
for t in text:
    libo.damerau_levenstein_distance(t,"casa")
end = time.time()
tim = (end-start)
print("Damerau-Levenstein cadena vs cadena: palabra casa : " + str(tim))


start = time.time()
for t in text:
    libo.damerau_levenstein_distance(t,"constitución")
end = time.time()
tim = (end-start)
print("Damerau-Levenstein cadena vs cadena: palabra constitución : " + str(tim))

################# trie básico ####################

for i in range(0,5):
    start = time.time()
    libo.damerau_levenstein_vs_trie(tri,"xi",i)
    end = time.time()
    tim = (end-start)
    print("DAMEROU-LEVENSTEIN VS TRIE: palabra xi, TOlerancia " + str(i) + " : " + str(tim))

for i in range(0,5):
    start = time.time()
    libo.damerau_levenstein_vs_trie(tri,"casa",i)
    end = time.time()
    tim = (end-start)
    print("DAMEROU-LEVENSTEIN VS TRIE: palabra casa, TOlerancia " + str(i) + " : " + str(tim))

for i in range(0,5):
    start = time.time()
    libo.damerau_levenstein_vs_trie(tri,"constitución",i)
    end = time.time()
    tim = (end-start)
    print("DAMEROU-LEVENSTEIN VS TRIE: palabra constitución, TOlerancia " + str(i) + " : " + str(tim))

################# trie con ramificación ###################

for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie_ramificacionD(tri,"xi",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE con ramificación de estados: Palabra xi, Tolerancia " + str(i) + " : " + str(tim))

for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie_ramificacionD(tri,"casa",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE con ramificación de estados: Palabra casa, Tolerancia " + str(i) + " : " + str(tim))

for i in range(0,5):
    start = time.time()
    libo.levenstein_vs_trie_ramificacionD(tri,"constitución",i)
    end = time.time()
    tim = (end-start)
    print("LEVENSTEIN VS TRIE con ramificación de estados: Palabra constitución, Tolerancia " + str(i) + " : " + str(tim))