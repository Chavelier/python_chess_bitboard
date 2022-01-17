"""
Created on Mon Oct  12 09:31:03 2021

@author: Corto Cristofoli
@co-author : Jeunier Hugo
@secret-author : Lance-Perlick Come

MAIN
"""

from board import *

B = Board()

B.print_board(False)
occ = U64(0)
occ = B.set_bit(occ,B.E4)
occ = B.set_bit(occ,B.D4)
occ = B.set_bit(occ,B.E5)
occ = B.set_bit(occ,B.D5)
B.print_bb(occ)


for case in range(64):
    # B.print_bb(B.rook_attack_on_the_fly(case,occ))
    B.print_bb(B.get_bishop_attack(case, occ))
    a = input("...")
    if a == "q":
        break

