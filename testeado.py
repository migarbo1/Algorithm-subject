#!/usr/bin/env python
#! -*- encoding utf8 -*-

import ALT_library as libo
import time

text = libo.leer_texto("quijote.txt")
tri = libo.trie()
tri.insertarTexto(text)
print("Texto cargado")

start = time.time()
libo.levenstein_vs_trie(tri,"casa",1)
end = time.time()
tim = (end-start)
print("LEVENSTEIN VS TRIE 1: ", tim)

start = time.time()
libo.levenstein_vs_trie(tri,"casa",2)
end = time.time()
tim = (end-start)
print("LEVENSTEIN VS TRIE 2: ", tim)

start = time.time()
libo.levenstein_vs_trie(tri,"casa",3)
end = time.time()
tim = (end-start)
print("LEVENSTEIN VS TRIE 3: ", tim)

start = time.time()
libo.levenstein_vs_trie(tri,"casa",4)
end = time.time()
tim = (end-start)
print("LEVENSTEIN VS TRIE 4: ", tim)

start = time.time()
libo.levenstein_vs_trie(tri,"casa",5)
end = time.time()
tim = (end-start)
print("LEVENSTEIN VS TRIE 5: ", tim)


start = time.time()
libo.damerau_levenstein_vs_trie(tri,"casa",1)
end = time.time()
tim = (end-start)
print("DAMEROU-LEVENSTEIN VS TRIE 1: ", tim)

start = time.time()
libo.damerau_levenstein_vs_trie(tri,"casa",2)
end = time.time()
tim = (end-start)
print("DAMEROU-LEVENSTEIN VS TRIE 2: ", tim)

start = time.time()
libo.damerau_levenstein_vs_trie(tri,"casa",3)
end = time.time()
tim = (end-start)
print("DAMEROU-LEVENSTEIN VS TRIE 3: ", tim)

start = time.time()
libo.damerau_levenstein_vs_trie(tri,"casa",4)
end = time.time()
tim = (end-start)
print("DAMEROU-LEVENSTEIN VS TRIE 4: ", tim)

start = time.time()
libo.damerau_levenstein_vs_trie(tri,"casa",5)
end = time.time()
tim = (end-start)
print("DAMEROU-LEVENSTEIN VS TRIE 5: ", tim)
