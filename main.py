"""
Created on Mon Oct  12 09:31:03 2021

@author: Corto Cristofoli

MAIN
"""

from board import *

B = Board()

c = B.case_str2int
occ = U64(0)
occ = B.set_bit(occ, c("e4"))
occ = B.set_bit(occ, c("e5"))
occ = B.set_bit(occ, c("d4"))
occ = B.set_bit(occ, c("d5"))


for case in range(64):
    B.print_bb(B.get_rook_attack(case, occ))
    a = input("...")
    if a == "q":
        break
