# -*- coding: utf-8 -*-
"""
Created on Mon Oct  12 09:22:34 2021

@author: Corto Cristofoli
@co-author : Jeunier Hugo
@secret-author : Lance-Perlick Come

BOARD
"""

from random_generation import *  # numpy est importé dedans


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
        'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
        'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
        'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
        'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
        'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
        'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
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

    piece = ["P","K","Q","B","N","R","p","k","q","b","n","r"]
    piece_print = { "p" : "♙", "k" : "♔", "q" : "♕", "n" : "♘", "b" : "♗", "r" : "♖",
                       "P" : "♟︎", "K" : "♚", "Q" : "♛", "N" : "♞", "B" : "♝", "R" : "♜"}
    castle_side = { "wk" : 1, "wq" : 2, "bk" : 4, "bq" : 8}


    def __init__(self):
        self.init()

    def init(self):

        self.side = True  # False = noir, True = Blanc

        self.bitboard = [
            U64(71776119061217280),
            U64(2**60),
            U64(2**59),
            U64(2**58+2**61),
            U64(2**57+2**62),
            U64(2**56+2**63),
            U64(65280),
            U64(2**4),
            U64(2**3),
            U64(2**2+2**5),
            U64(2**1+2**6),
            U64(2**0+2**7)
            ]
        # ex : bitboard[piece["K"]] -> bitboard du roi blanc

        self.en_passant = -1 # case pour manger en passant, si =-1 pas de case

        self.castle_right = int("0b1111",base = 2) #droits au roque
        # 0001 -> le roi blanc peut roquer à l'aile roi
        # 0010 -> le roi blanc peut roquer à l'aile dame
        # 0100 -> le roi noir peut roquer à l'aile roi
        # 1000 -> le roi noir peut roquer à l'aile dame



        self.init_leaper_attack()
        self.init_magic_numbers()
        # self.init_slider_attack()

        # print(self.bishop_attacks)


    # fonctions sur les bits -----------------------------------------------------------------------

    @staticmethod
    def set_bit(bitboard, case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a mis un 1 sur la case """
        return bitboard | (U64(1) << U64(case))

    @staticmethod
    def pop_bit(bitboard, case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a mis un 0 sur la case """
        return bitboard & ~(U64(1) << U64(case))

    @staticmethod
    def switch_bit(bitboard, case):
        """ U64 , int -> U64
        renvoi le bitboard auquel on a change le bit de la case """
        return bitboard ^ (U64(1) << U64(case))

    @staticmethod
    def get_bit(bitboard, case):
        """ U64 , int -> U64
        renvoi le bit de la case demandee du bitboard """
        return bitboard & (U64(1) << U64(case))

    @staticmethod
    def mult_bb(bb1,bb2):
        """ U64, U64 -> U64
        multiplie 2 bitboards qui seraient trop grand """
        return U64( (int(bb1) * int(bb2)) & (2**64 - 1) )

    @staticmethod
    def count_bit(bitboard):  # verifier efficacite (static inline equivalent)
        """ U64 -> int
        renvoi le nombre de bit du bitboard """  # TODO: on peut ameliorer la fonction
        bb = bitboard
        count = 0
        while bb:
            count += 1
            bb = bb & (bb-U64(1))  # enleve le bit le moins signifiant
        return count

    @staticmethod
    def ls1b_index(bitboard):  # verifier efficacite (static inline equivalent)
        """ U64 -> int
        renvoi l'index du bit le moins signifiant """  # TODO: on peut ameliorer la fonction
        return Board.count_bit((bitboard & -bitboard)-U64(1))

    # affichage / debug ------------------------------------------------------------------------------------

    def case_str2int(self, txt):
        val = self.coord.index(txt)
        return val

    def case_int2str(self, nb):
        val = self.coord[nb]
        return val

    def print_bb(self, bitboard):
        """ U64 -> ()
        affiche le bitboard sous une forme lisible """
        print("val : %s \n" % bitboard)
        for i in range(8):
            ligne = str(8-i)+"   "
            for j in range(8):
                if Board.get_bit(bitboard, 8*i+j):
                    txt = 'x'
                else:
                    txt = '.'
                ligne += txt+" "
            print(ligne)
        print("\n    a b c d e f g h\n")

    # RENVOI AFFICHAGE ######################################################################################

    def print_board(self,unicode=True):
        for x in range(8):
            ligne = str(8-x)+"   "
            for y in range(8):
                case = x * 8 + y

                char = ""
                for i in range(12):
                    if self.get_bit(self.bitboard[i],case):
                        if unicode:
                            char += self.piece_print[self.piece[i]]
                        else:
                            char +=self.piece[i]
                if char == "":
                    char = "."
                ligne += char + " "

            print(ligne)
        print("\n    a b c d e f g h\n")
        if self.side:
            print("Trait : Blancs")
        else:
            print("Trait : Noirs")
        if self.en_passant != -1:
            print("En passant : %s"%self.case_int2str(self.en_passant))
        print("Droits au roque : %s"%bin(self.castle_right)[2:])


    # INITIALISATION DES ATTAQUES ###########################################################################

    def init_leaper_attack(self):
        """ génère les listes d'attaque possible de chaque pièces "sautante" """
        self.pawn_attack = [[], []]
        self.knight_attack = []
        for i in range(64):

            # on initialise les attaques de pion
            self.pawn_attack[0].append(self.mask_pawn_attack(i, False))
            self.pawn_attack[1].append(self.mask_pawn_attack(i, True))

            #on initialise les attaques de cavalier
            self.knight_attack.append(self.mask_knight_attack(i))

            #on initialise les attaques du roi
            self.knight_attack.append(self.mask_king_attack(i))

    def init_slider_attack(self):
        """ génère les mouvements des pièces "glissantes" en fonction de leur position et de l'échequier """
        self.bishop_mask = []
        self.rook_mask = []
        self.bishop_attacks = [[0 for _ in range(512)] for _ in range(64)]
        self.rook_attacks = [[0 for _ in range(4096)] for _ in range(64)]

        for case in range(64):
            # on initialise les masks
            self.bishop_mask.append(self.mask_bishop_attack(case))
            self.rook_mask.append(self.mask_rook_attack(case))


            attack_mask1 = self.bishop_mask[case] # pour le fou
            attack_mask2 = self.rook_mask[case] # pour la tour

            # relevant_bits_count1 = self.count_bit(attack_mask1) # pour le fou
            # relevant_bits_count2 = self.count_bit(attack_mask2) # pour la tour
            relevant_bits_count1 = self.bishop_relevant_bits[case] # pour le fou
            relevant_bits_count2 = self.rook_relevant_bits[case] # pour la tour

            for i in range(1<<relevant_bits_count1):
                occupancy = self.set_occupancy(i, relevant_bits_count1, attack_mask1)

                magic_index = ULL(occupancy * self.bishop_magic_numbers[case]) >> ULL(64-relevant_bits_count1)

                # print(magic_index)
                self.bishop_attacks[case][magic_index] = self.bishop_attack_on_the_fly(case,occupancy)
            for i in range(1<<relevant_bits_count2):
                occupancy = self.set_occupancy(i, relevant_bits_count2, attack_mask2)

                magic_index = ULL(occupancy * self.rook_magic_numbers[case]) >> ULL(64-relevant_bits_count2)

                self.rook_attacks[case][magic_index] = self.rook_attack_on_the_fly(case,occupancy)


    def get_bishop_attack(self,case,occ):
        """ renvoi un bitboard de l'attaque du fou en fonction de l'occupance de l'échéquier """
        bb = U64((occ & self.bishop_mask[case]) * self.bishop_magic_numbers[case]) >> U64(64-self.bishop_relevant_bits[case])
        return self.bishop_attacks[case][bb]
    def get_rook_attack(self,case,occ):
        """ renvoi un bitboard de l'attaque de la tour en fonction de l'occupance de l'échéquier """
        bb = U64((occ & self.rook_mask[case]) * self.rook_magic_numbers[case]) >> U64(64-self.rook_relevant_bits[case])
        return self.rook_attacks[case][bb]


    # ATTAQUES DES PIECES ###############################################################################

    def mask_pawn_attack(self, case, side):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du pion sur la case "case" """

        attack = U64(0)
        bb = Board.set_bit(U64(0), case)  # position du pion en bitboard

        if not side:
            attack = ((bb & self.not_h_file) >> U64(7)) | (
                (bb & self.not_a_file) >> U64(9))
        else:
            attack = ((bb & self.not_a_file) << U64(7)) | (
                (bb & self.not_h_file) << U64(9))

        return attack

    def mask_knight_attack(self, case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du cavalier sur la case "case" """

        attack = U64(0)
        bb = Board.set_bit(U64(0), case)  # position du cavalier en bitboard

        attack = (bb & self.not_h_file) >> U64(15)
        attack = attack | (bb & self.not_a_file) >> U64(17)
        attack = attack | (bb & self.not_ab_file) >> U64(10)
        attack = attack | (bb & self.not_gh_file) >> U64(6)
        attack = attack | (bb & self.not_a_file) << U64(15)
        attack = attack | (bb & self.not_h_file) << U64(17)
        attack = attack | (bb & self.not_gh_file) << U64(10)
        attack = attack | (bb & self.not_ab_file) << U64(6)

        return attack

    def mask_king_attack(self, case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du roi sur la case "case" """

        attack = U64(0)
        bb = Board.set_bit(U64(0), case)  # position du roi en bitboard

        attack = bb >> U64(8) | bb << U64(8)
        if bb & self.not_a_file:
            attack = attack | bb >> U64(1) | bb >> U64(9) | bb << U64(7)
        if bb & self.not_h_file:
            attack = attack | bb << U64(1) | bb << U64(9) | bb >> U64(7)

        return attack

    def mask_bishop_attack(self, case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque du fou sur la case "case" """

        attack = U64(0)

        rank, file = case//8, case % 8  # ligne et colonne de la pieces
        for i in range(1, min(7-rank, 7-file)):
            r, f = rank+i, file+i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1, min(rank, file)):
            r, f = rank-i, file-i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1, min(7-rank, file)):
            r, f = rank+i, file-i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1, min(rank, 7-file)):
            r, f = rank-i, file+i
            attack = attack | U64(1) << U64(r*8 + f)

        return attack

    def mask_rook_attack(self, case):
        """ int , bool -> U64
        renvoi le bitboard de l'attaque de la tour sur la case "case" """

        attack = U64(0)

        rank, file = case//8, case % 8  # ligne et colonne de la pieces
        for i in range(1, 7-rank):
            r, f = rank+i, file
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1, rank):
            r, f = rank-i, file
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1, 7-file):
            r, f = rank, file+i
            attack = attack | U64(1) << U64(r*8 + f)
        for i in range(1, file):
            r, f = rank, file-i
            attack = attack | U64(1) << U64(r*8 + f)

        return attack

    # PIECES GLISSANTES (sliding pieces) "on the fly" #####################################

    def bishop_attack_on_the_fly(self, case, block):
        attack = U64(0)

        rank, file = case//8, case % 8  # ligne et colonne de la pieces
        for i in range(1, min(8-rank, 8-file)):
            r, f = rank+i, file+i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur
        for i in range(1, min(rank+1, file+1)):
            r, f = rank-i, file-i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur
        for i in range(1, min(8-rank, file+1)):
            r, f = rank+i, file-i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur
        for i in range(1, min(rank+1, 8-file)):
            r, f = rank-i, file+i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur

        return attack

    def rook_attack_on_the_fly(self, case, block):
        attack = U64(0)

        rank, file = case//8, case % 8  # ligne et colonne de la pieces
        for i in range(1, 8-rank):
            r, f = rank+i, file
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur
        for i in range(1, rank+1):
            r, f = rank-i, file
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur
        for i in range(1, 8-file):
            r, f = rank, file+i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur
        for i in range(1, file+1):
            r, f = rank, file-i
            b = U64(1) << U64(r*8 + f)
            attack = attack | b
            if b & block:
                break  # on sors de la boucle si on rencontre un bloqueur

        return attack

    # MAGIC NUMBER ####################################################################

    def set_occupancy(self, index, bits_in_mask, attack_mask):
        """ renvoi l'occupance possible des cases
        présentent dans \"attack_mask\" """
        occupancy = U64(0)
        attack_map = attack_mask

        for i in range(bits_in_mask):
            square = Board.ls1b_index(attack_map)
            attack_map = Board.pop_bit(attack_map, square)

            if U64(index) & (U64(1) << U64(i)):
                occupancy = occupancy | (U64(1) << U64(square))

        return occupancy



    def find_magic_number(self, square, relevant_bits, isbishop):
        """ génère un magic number correct par force brute"""
        occupancies = [0 for _ in range(4096)]
        attacks = [0 for _ in range(4096)]

        attack_mask = U64(0)
        if isbishop:
            attack_mask = self.mask_bishop_attack(square)
        else:
            attack_mask = self.mask_rook_attack(square)

        occupancy_index = 1 << relevant_bits
        for i in range(occupancy_index):
            occupancies[i] = self.set_occupancy(i, relevant_bits, attack_mask)

            if isbishop:
                attacks[i] = self.bishop_attack_on_the_fly(
                    square, occupancies[i])
            else:
                attacks[i] = self.rook_attack_on_the_fly(
                    square, occupancies[i])



        # test de possible magic number
        for rdcount in range(10000000): #100000000
            magic_number = generate_magic_number()

            # on passe les mauvais magic number sûr
            if self.count_bit(ULL(attack_mask * magic_number) & ULL(18374686479671623680)) < 6:
                continue

            used_attacks = [0 for _ in range(4096)]

            index = 0
            fail = False
            while index < occupancy_index and not fail:
                magic_index = int(ULL(occupancies[index] * magic_number) >> ULL(64-relevant_bits))
                # print("magic_index : %s"%magic_index)
                if used_attacks[magic_index] == 0:
                    used_attacks[magic_index] = attacks[index]
                # le magic number ne marche pas !
                elif used_attacks[magic_index] != attacks[index]:
                    fail = True
                index += 1

            if not fail:  # le nombre est bien un magic number !
                return magic_number

        print('magic number non trouvé !')
        return U64(0)


    def init_magic_numbers(self):
        """ initialise les magic numbers pour chaque pièces et chaque cases """

        # self.bishop_magic_numbers = []
        # self.rook_magic_numbers = []

        # for case in range(64):
        #     #magic number pour le fou
        #     self.bishop_magic_numbers.append(self.find_magic_number(case, self.bishop_relevant_bits[case], True))
        #     print("%s,"%self.bishop_magic_numbers[case])
        # print('\n ------------------------- \n')
        # for case in range(64):
        #     #magic number pour la tour
        #     self.rook_magic_numbers.append(self.find_magic_number(case, self.rook_relevant_bits[case], False))
        #     print("%s,"%self.rook_magic_numbers[case])

        # print(len(self.bishop_magic_numbers),len(self.rook_magic_numbers))

        self.bishop_magic_numbers = [18018832060792964,
            9011737055478280,
            4531088509108738,
            74316026439016464,
            396616115700105744,
            2382975967281807376,
            1189093273034424848,
            270357282336932352,
            1131414716417028,
            2267763835016,
            2652629010991292674,
            283717117543424,
            4411067728898,
            1127068172552192,
            288591295206670341,
            576743344005317120,
            18016669532684544,
            289358613125825024,
            580966009790284034,
            1126071732805635,
            37440604846162944,
            9295714164029260800,
            4098996805584896,
            9223937205167456514,
            153157607757513217,
            2310364244010471938,
            95143507244753921,
            9015995381846288,
            4611967562677239808,
            9223442680644702210,
            64176571732267010,
            7881574242656384,
            9224533161443066400,
            9521190163130089986,
            2305913523989908488,
            9675423050623352960,
            9223945990515460104,
            2310346920227311616,
            7075155703941370880,
            4755955152091910658,
            146675410564812800,
            4612821438196357120,
            4789475436135424,
            1747403296580175872,
            40541197101432897,
            144397831292092673,
            1883076424731259008,
            9228440811230794258,
            360435373754810368,
            108227545293391872,
            4611688277597225028,
            3458764677302190090,
            577063357723574274,
            9165942875553793,
            6522483364660839184,
            1127033795058692,
            2815853729948160,
            317861208064,
            5765171576804257832,
            9241386607448426752,
            11258999336993284,
            432345702206341696,
            9878791228517523968,
            4616190786973859872,
            ]
        '''self.bishop_magic_numbers = [
            18018831494946945,
            1134767471886336,
            2308095375972630592,
            27308574661148680,
            9404081239914275072,
            4683886618770800641,
            216245358743802048,
            9571253153235970,
            27092002521253381,
            1742811846410792,
            8830470070272,
            9235202921558442240,
            1756410529322199040,
            1127005325142032,
            1152928124311179269,
            2377913937382869017,
            2314850493043704320,
            4684324174200832257,
            77688339246880000,
            74309421802472544,
            8649444578941734912,
            4758897525753456914,
            18168888584831744,
            2463750540959940880,
            9227893366251856128,
            145276341141897348,
            292821938185734161,
            5190965918678714400,
            2419567834477633538,
            2308272929927873024,
            18173279030480900,
            612771170333492228,
            4611976426970161409,
            2270508834359424,
            9223442681551127040,
            144117389281722496,
            1262208579542270208,
            13988180992906560530,
            4649975687305298176,
            9809420809726464128,
            1153222256471056394,
            2901448468860109312,
            40690797321924624,
            4504295814726656,
            299204874469892,
            594838215186186752,
            7210408796106130432,
            144405467744964672,
            145390656058359810,
            1153203537948246016,
            102002796048417802,
            9243919728426124800,
            2455024885924167748,
            72066815467061280,
            325424741529814049,
            1175584649085829253,
            18720594346444812,
            584352516473913920,
            1441151883179198496,
            4919056693802862608,
            1161950831810052608,
            2464735771073020416,
            54610562058947072,
            580611413180448
            ]'''

        self.rook_magic_numbers = [
            9979994641325359136,
            90072129987412032,
            180170925814149121,
            72066458867205152,
            144117387368072224,
            216203568472981512,
            9547631759814820096,
            2341881152152807680,
            140740040605696,
            2316046545841029184,
            72198468973629440,
            81205565149155328,
            146508277415412736,
            703833479054336,
            2450098939073003648,
            576742228899270912,
            36033470048378880,
            72198881818984448,
            1301692025185255936,
            90217678106527746,
            324684134750365696,
            9265030608319430912,
            4616194016369772546,
            2199165886724,
            72127964931719168,
            2323857549994496000,
            9323886521876609,
            9024793588793472,
            562992905192464,
            2201179128832,
            36038160048718082,
            36029097666947201,
            4629700967774814240,
            306244980821723137,
            1161084564161792,
            110340390163316992,
            5770254227613696,
            2341876206435041792,
            82199497949581313,
            144120019947619460,
            324329544062894112,
            1152994210081882112,
            13545987550281792,
            17592739758089,
            2306414759556218884,
            144678687852232706,
            9009398345171200,
            2326183975409811457,
            72339215047754240,
            18155273440989312,
            4613959945983951104,
            145812974690501120,
            281543763820800,
            147495088967385216,
            2969386217113789440,
            19215066297569792,
            180144054896435457,
            2377928092116066437,
            9277424307650174977,
            4621827982418248737,
            563158798583922,
            5066618438763522,
            144221860300195844,
            281752018887682,
            ]
        '''self.rook_magic_numbers = [
            11565248328107303040,
            12123725398701785089,
            900733188335206529,
            72066458867205152,
            144117387368072224,
            216203568472981512,
            9547631759814820096,
            2341881152152807680,
            140740040605696,
            2316046545841029184,
            72198468973629440,
            81205565149155328,
            146508277415412736,
            703833479054336,
            2450098939073003648,
            576742228899270912,
            36033470048378880,
            72198881818984448,
            1301692025185255936,
            90217678106527746,
            324684134750365696,
            9265030608319430912,
            4616194016369772546,
            2199165886724,
            72127964931719168,
            2323857549994496000,
            9323886521876609,
            9024793588793472,
            562992905192464,
            2201179128832,
            36038160048718082,
            36029097666947201,
            4629700967774814240,
            306244980821723137,
            1161084564161792,
            110340390163316992,
            5770254227613696,
            2341876206435041792,
            82199497949581313,
            144120019947619460,
            324329544062894112,
            1152994210081882112,
            13545987550281792,
            17592739758089,
            2306414759556218884,
            144678687852232706,
            9009398345171200,
            2326183975409811457,
            72339215047754240,
            18155273440989312,
            4613959945983951104,
            145812974690501120,
            281543763820800,
            147495088967385216,
            2969386217113789440,
            19215066297569792,
            180144054896435457,
            2377928092116066437,
            9277424307650174977,
            4621827982418248737,
            563158798583922,
            5066618438763522,
            144221860300195844,
            281752018887682
            ]'''
