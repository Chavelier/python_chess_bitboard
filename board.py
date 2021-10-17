import numpy as np
U64 = np.uint64 #type utilise pour representer le bitboard (entier de 64 bit non signe)

class Board:
    """gere tout l'echequier, les pieces, les coups,..."""

    # U64 = U64(2**63)
    """
    bitboard echequier representation :

    8   0  1  2  3  4  5  6  7
    7   8  9  10 11 12 13 14 15
    6   16 17 18 19 20 21 22 23
    5   24 25 26 27 28 29 30 31
    4   32 33 34 35 36 37 38 39
    3   40 41 42 43 44 45 46 47
    2   48 49 50 51 52 53 54 55
    1   56 57 58 59 60 61 62 63

        A  B  C  D  E  F  G  H

    ex: case E4 a comme id 36 et comme représentation en bitboard 2**36
    """


    def __init__(self):
        self.init()

    def init(self):
        self.Pw = U64(71776119061217280)
        self.Kw = U64(2**60)
        self.Qw = U64(2**59)
        self.Bw = U64(2**58+2**61)
        self.Nw = U64(2**57+2**62)
        self.Rw = U64(2**56+2**63)
        self.Pb = U64(65280)
        self.Kb = U64(2**4)
        self.Qb = U64(2**3)
        self.Rb = U64(2**0+2**7)
        self.Nb = U64(2**1+2**6)
        self.Bb = U64(2**2+2**5)

        self.bb_white = self.Pw | self.Kw | self.Qw | self.Bw | self.Rw | self.Nw
        self.bb_black = self.Pb | self.Kb | self.Qb | self.Bb | self.Rb | self.Nb


    # fonctions sur les bits -----------------------------------------------------------------------

    def set_bit(self,bitboard,case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a mis un 1 sur la case """
        return bitboard | (U64(1) << U64(case))
    def pop_bit(self,bitboard,case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a mis un 0 sur la case """
        return bitboard & ~(U64(1) << U64(case))
    def switch_bit(self,bitboard,case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a change le bit de la case """
        return bitboard ^ (U64(1) << U64(case))
    def get_bit(self,bitboard,case):
        """ U64 , int -> U64
        renvoi le bit de la case demandee du bitboard """
        return bitboard & (U64(1) << U64(case))
    def bit_state(self,bitboard,case):
        """ U64 , int -> bool
        renvoi l'etat actuel de la case du bitboard """
        return self.get_bit(bitboard,case) != 0

    # -------------------------------------------------------------------------------------------------



    def print_bb(self,bitboard):
        for i in range(8):
            ligne = str(i+1)+"   "
            for j in range(8):
                txt = str(int(self.bit_state(bitboard,8*i+j)))
                ligne += txt+" "
            print(ligne)
        print("\n    a b c d e f g h\n")


B = Board()
B.print_bb(B.pop_bit(B.Pw,54))
