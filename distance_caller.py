#!/usr/bin/env python
#! -*- encoding utf8

## zona de imports
import numpy as np
import re
import sys
import os
from levenstein_distance import levenstein_caller
from damerau_levenstein import damerau_caller
##

# clean text
clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)
#fin clean text


#main
if __name__ == "__main__":
    if len(sys.argv) == 5:
        f = sys.argv[1]
        k = sys.argv[2]
        to = sys.argv[3]
        mode = sys.argv[4]
        if mode == 1:
            levenstein_caller(f,k,to)
        else:
            damerau_caller(f,k,to)
    else:
        syntax()
