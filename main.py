"""
Created on Mon Oct  12 09:31:03 2021

@author: Corto Cristofoli
@co-author : Jeunier Hugo
@secret-author : Lance-Perlick Come

MAIN
"""

from board import *

B = Board()

c = B.case_str2int
B.print_board(False)
# occ = U64(0)
# occ = B.set_bit(occ,c("e4"))
# occ = B.set_bit(occ,c("d4"))
# occ = B.set_bit(occ,c("e5"))
# occ = B.set_bit(occ,c("d5"))
# B.print_bb(occ)
#
#
# for case in range(64):
#     # B.print_bb(B.rook_attack_on_the_fly(case,occ))
#     B.print_bb(B.get_rook_attack(case, occ))
#     a = input("...")
#     if a == "q":
#         break
