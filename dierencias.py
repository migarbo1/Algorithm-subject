#!/usr/bin/env python
#! -*- encoding utf8 -*-
import re
import sys
import os
import copy

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

mal = open("mal","r") # se abre el fichero
bien = open("bien","r") # se abre el fichero
textm = mal.read() # leemos el fichero
textb = bien.read() # leemos el fichero
mal.close() # lo cerramos
bien.close() # lo cerramos
textm = textm.split() #
textb = textb.split() #
textm = sorted(textm)
textb = sorted(textb)
puta = diff(textb,textm)
print(puta)
print(len(puta))
