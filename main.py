from board import *

B = Board()
# B.print_bb(B.pop_bit(B.Pw,51))
case = B.case_str2int('e1')
B.print_bb(B.mask_pawn_attack(case,True))


# v = U64(0)
# for i in range(8):
#         v = B.set_bit(v,i*8+6)
# B.print_bb(B.not_ab_file)
