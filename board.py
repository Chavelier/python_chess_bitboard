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

    bishop_relevant_bits = [
    6, 5, 5, 5, 5, 5, 5, 6,
    5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 7, 7, 7, 7, 5, 5,
    5, 5, 7, 9, 9, 7, 5, 5,
    5, 5, 7, 9, 9, 7, 5, 5,
    5, 5, 7, 7, 7, 7, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5,
    6, 5, 5, 5, 5, 5, 5, 6
    ]
    rook_relevant_bits = [
    12, 11, 11, 11, 11, 11, 11, 12,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    12, 11, 11, 11, 11, 11, 11, 12
    ]

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
    @staticmethod
    def set_bit(bitboard,case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a mis un 1 sur la case """
        return bitboard | (U64(1) << U64(case))
    @staticmethod
    def pop_bit(bitboard,case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a mis un 0 sur la case """
        return bitboard & ~(U64(1) << U64(case))
    @staticmethod
    def switch_bit(bitboard,case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a change le bit de la case """
        return bitboard ^ (U64(1) << U64(case))
    @staticmethod
    def get_bit(bitboard,case):
        """ U64 , int -> U64
        renvoi le bit de la case demandee du bitboard """
        return bitboard & (U64(1) << U64(case))

    @staticmethod
    def count_bit(bitboard): #verifier efficacite (static inline equivalent)
        """ U64 -> int
        renvoi le nombre de bit du bitboard """ # TODO: on peut ameliorer la fonction
        bb = bitboard
        count = 0
        while bb:
            count += 1
            bb = bb & (bb-U64(1)) # enleve le bit le moins signifiant
        return count
    @staticmethod
    def ls1b_index(bitboard): #verifier efficacite (static inline equivalent)
        """ U64 -> int
        renvoi l'index du bit le moins signifiant """ # TODO: on peut ameliorer la fonction
        return Board.count_bit((bitboard & -bitboard)-U64(1))



    # affichage / debug ------------------------------------------------------------------------------------
    def case_str2int(self,txt):
        val = self.coord.index(txt)
        return val
    def case_int2str(self,nb):
        val = self.coord[nb]
        return val
    def print_bb(self,bitboard):
        print("val : %s \n"%bitboard)
        for i in range(8):
            ligne = str(8-i)+"   "
            for j in range(8):
                txt = str(int(Board.get_bit(bitboard,8*i+j)!=0))
                ligne += txt+" "
            print(ligne)
        print("\n    a b c d e f g h\n")


    # INITIALISATION DES ATTAQUES ###########################################################################

    def init_leaper_attack(self):
        self.pawn_attack = [[],[]]
        self.knight_attack = []
        for i in range(64):

            # on initialise les attaques de pion
            self.pawn_attack[0].append(self.mask_pawn_attack(i,False))
            self.pawn_attack[1].append(self.mask_pawn_attack(i,True))

            #on initialise les attaques de cavalier
            self.knight_attack.append(self.mask_knight_attack(i))

            #on initialise les attaques du roi
            self.knight_attack.append(self.mask_king_attack(i))

    # ATTAQUES DES PIECES ###############################################################################

    def mask_pawn_attack(self,case,side):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du pion sur la case "case" """

        attack = U64(0)
        bb = Board.set_bit(U64(0),case) #position du pion en bitboard

        if not side:
            attack = ((bb & self.not_h_file) >> U64(7)) | ((bb & self.not_a_file) >> U64(9))
        else:
            attack = ((bb & self.not_a_file) << U64(7)) | ((bb & self.not_h_file) << U64(9))

        return attack

    def mask_knight_attack(self,case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du cavalier sur la case "case" """

        attack = U64(0)
        bb = Board.set_bit(U64(0),case) #position du cavalier en bitboard

        attack = (bb & self.not_h_file) >> U64(15)
        attack = attack | (bb & self.not_a_file) >> U64(17)
        attack = attack | (bb & self.not_ab_file) >> U64(10)
        attack = attack | (bb & self.not_gh_file) >> U64(6)
        attack = attack | (bb & self.not_a_file) << U64(15)
        attack = attack | (bb & self.not_h_file) << U64(17)
        attack = attack | (bb & self.not_gh_file) << U64(10)
        attack = attack | (bb & self.not_ab_file) << U64(6)

        return attack

    def mask_king_attack(self,case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du roi sur la case "case" """

        attack = U64(0)
        bb = Board.set_bit(U64(0),case) #position du roi en bitboard

        attack = bb >> U64(8) | bb << U64(8)
        if bb & self.not_a_file: attack = attack | bb >> U64(1) | bb >> U64(9) | bb << U64(7)
        if bb & self.not_h_file: attack = attack | bb << U64(1) | bb << U64(9) | bb >> U64(7)

        return attack

    def mask_bishop_attack(self,case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du fou sur la case "case" """

        attack = U64(0)

        rank,file = case//8, case%8 # ligne et colonne de la pieces
        for i in range(1,min(7-rank,7-file)):
            r,f = rank+i,file+i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1,min(rank,file)):
            r,f = rank-i,file-i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1,min(7-rank,file)):
            r,f = rank+i,file-i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1,min(rank,7-file)):
            r,f = rank-i,file+i
            attack = attack | U64(1) << U64(r*8 + f)

        return attack

    def mask_rook_attack(self,case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque de la tour sur la case "case" """

        attack = U64(0)

        rank,file = case//8, case%8 # ligne et colonne de la pieces
        for i in range(1,7-rank):
            r,f = rank+i,file
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1,rank):
            r,f = rank-i,file
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1,7-file):
            r,f = rank,file+i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1,file):
            r,f = rank,file-i
            attack = attack | U64(1) << U64(r*8 + f)

        return attack

    # PIECES GLISSANTES (sliding pieces) "on the fly" #####################################

    def bishop_attack_on_the_fly(self,case,block):
        attack = U64(0)

        rank,file = case//8, case%8 # ligne et colonne de la pieces
        for i in range(1,min(8-rank,8-file)):
            r,f = rank+i,file+i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur
        for i in range(1,min(rank+1,file+1)):
            r,f = rank-i,file-i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur
        for i in range(1,min(8-rank,file+1)):
            r,f = rank+i,file-i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur
        for i in range(1,min(rank+1,8-file)):
            r,f = rank-i,file+i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur

        return attack

    def rook_attack_on_the_fly(self,case,block):
        attack = U64(0)

        rank,file = case//8, case%8 # ligne et colonne de la pieces
        for i in range(1,8-rank):
            r,f = rank+i,file
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur
        for i in range(1,rank+1):
            r,f = rank-i,file
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur
        for i in range(1,8-file):
            r,f = rank,file+i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur
        for i in range(1,file+1):
            r,f = rank,file-i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block: break #on sors de la boucle si on rencontre un bloqueur

        return attack

    # MAGIC bitboard function

    def set_occupancies(self,index, bits_in_mask, attack_mask):
        """pas encore trop compris ce que ça fait..."""
        occupancy = U64(0)
        attack_map = attack_mask

        for i in range(bits_in_mask):
            square = Board.ls1b_index(attack_map)
            attack_map = Board.pop_bit(attack_map,square)

            if U64(index) & (U64(1)<<U64(i)):
                occupancy = occupancy | (U64(1)<<U64(square))

        return occupancy
