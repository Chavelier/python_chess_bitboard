"""
Created on Mon Oct  12 09:31:03 2021

@author: Corto Cristofoli

MAIN
"""

from board import *

B = Board()
# B.print_bb(B.pop_bit(B.Pw,51))
case = B.case_str2int('c7')
block = U64(0)
block = B.set_bit(block,5)
block = B.set_bit(block,13)
block = B.set_bit(block,34)

atk_bb = B.mask_bishop_attack(B.case_str2int("e4"))
# for i in range(4096):
#     B.print_bb(B.set_occupancies(i,B.count_bit(atk_bb),atk_bb))
#     txt = input()

# v = U64(0)
# for i in range(8):
#         v = B.set_bit(v,i*8+6)
# B.print_bb(B.not_ab_file)


for i in range(10000):
    if i % 1000 == 0:
        print(B.count_bit(generate_magic_number()))
    else:
        generate_magic_number()
