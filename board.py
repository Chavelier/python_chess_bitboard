import numpy as np
U64 = np.uint64 #type utilise pour representer le bitboard (entier de 64 bit non signe)

class Board:
    """gere tout l'echequier, les pieces, les coups,..."""

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

    coord = [
    'a8','b8','c8','d8','e8','f8','g8','h8',
    'a7','b7','c7','d7','e7','f7','g7','h7',
    'a6','b6','c6','d6','e6','f6','g6','h6',
    'a5','b5','c5','d5','e5','f5','g5','h5',
    'a4','b4','c4','d4','e4','f4','g4','h4',
    'a3','b3','c3','d3','e3','f3','g3','h3',
    'a2','b2','c2','d2','e2','f2','g2','h2',
    'a1','b1','c1','d1','e1','f1','g1','h1'
    ]

    #constantes
    a_file = U64(72340172838076673)
    b_file = U64(144680345676153346)
    g_file = U64(4629771061636907072)
    h_file = U64(9259542123273814144)
    not_a_file = ~a_file
    not_h_file = ~h_file
    not_ab_file = ~(a_file | b_file)
    not_gh_file = ~(g_file | h_file)


    def __init__(self):
        self.init()

    def init(self):

        self.side = False #False = blanc, True = noir

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

        # self.bb_white = self.Pw | self.Kw | self.Qw | self.Bw | self.Rw | self.Nw
        # self.bb_black = self.Pb | self.Kb | self.Qb | self.Bb | self.Rb | self.Nb
        self.init_leaper_attack()



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


    # affichage / debug ------------------------------------------------------------------------------------
    def case_str2int(self,txt):
        val = self.coord.index(txt)
        return val
    def print_bb(self,bitboard):
        print("val : %s \n"%bitboard)
        for i in range(8):
            ligne = str(8-i)+"   "
            for j in range(8):
                txt = str(int(self.bit_state(bitboard,8*i+j)))
                ligne += txt+" "
            print(ligne)
        print("\n    a b c d e f g h\n")


    # INITIALISATION DES ATTAQUES ###########################################################################

    def init_leaper_attack(self):
        self.pawn_attack = {}
        for i in range(64):
            self.pawn_attack['blanc'].append(self.mask_pawn_attack(i,False))
            self.pawn_attack['noir'].append(self.mask_pawn_attack(i,True))

    # ATTAQUES DES PIECES ###############################################################################

    def mask_pawn_attack(self,case,side):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du pion sur la case """

        attack = U64(0)
        bb = self.set_bit(U64(0),case) #position du pion en bitboard

        if not side:
            attack = ((bb & self.not_h_file) >> U64(7)) | ((bb & self.not_a_file) >> U64(9))
        else:
            attack = ((bb & self.not_a_file) << U64(7)) | ((bb & self.not_h_file) << U64(9))

        return attack
