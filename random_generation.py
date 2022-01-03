# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 09:58:52 2021

@author: Corto Cristofoli

RANDOM NUMBER GENERATION
"""

import numpy as np
U64 = np.uint64 #type utilise pour representer le bitboard (entier de 64 bit non signe)
U32 = np.uint32 #(entier de 32 bit non signe)
ULL = np.ulonglong

random_state = U32(1804289383) #permet la génération aléatoire

def get_U32_random_nb():
    global random_state
    nb = random_state

    nb = nb ^ (nb << U32(13))
    nb = nb ^ (nb >> U32(17))
    nb = nb ^ (nb << U32(5))

    random_state = nb
    return nb

def get_U64_random_nb():

    #on initialise des nombres
    n1 = U64(get_U32_random_nb()) & U64(2**16-1)
    n2 = U64(get_U32_random_nb()) & U64(2**16-1)
    n3 = U64(get_U32_random_nb()) & U64(2**16-1)
    n4 = U64(get_U32_random_nb()) & U64(2**16-1)

    #renvoi nombre aleatoire
    return n1 | (n2 << U64(16)) | (n3 << U64(32)) | (n4 << U64(48))

def generate_magic_number(): #genere un magic number candidat
    return get_U64_random_nb() & get_U64_random_nb() & get_U64_random_nb()
