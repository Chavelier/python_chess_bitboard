"""
Created on Mon Oct  12 09:31:03 2021

@author: Corto Cristofoli
@co-author : Jeunier Hugo
@secret-author : Lance-Perlick Come

MAIN
"""

from board import *

B = Board()

B.print_board(True)
# occ = U64(0)
# occ = B.set_bit(occ,B.E4)
# occ = B.set_bit(occ,B.D4)
# occ = B.set_bit(occ,B.E5)
# occ = B.set_bit(occ,B.D5)
# B.print_bb(occ)

B.print_bb(B.attacked_bitboard(B.White))
# B.print_bb(B.pawn_attack[1][B.C3])
# B.print_bb(B.bitboard[B.P])
