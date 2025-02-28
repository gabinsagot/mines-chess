from piece import *
import pygame as pg


class Plateau:



    def __init__(self, LARGEUR, HAUTEUR, COLONNES, LIGNES, screen):

        self.LARGEUR = LARGEUR
        self.HAUTEUR = HAUTEUR
        self.COLONNES = COLONNES
        self.LIGNES = LIGNES

        self.plateau = [] 
        self.casesASurligner = []
        self.piecesPresentes = []
        self.screen = screen
        #On utilise une liste car on ne peut pas remplir 
        #un np.ndarray avec des instances de la classe Piece
        self.dico_positions_prises = {}
        


    def generer_plateau(self):
        
        for colonne in range(8):
            self.plateau.append([-1 for i in range(8)])


        for i in range(8):


            self.plateau[i][6] = Pawn("white", i, 6)
            self.plateau[i][1] = Pawn("black", i, 1)


            self.plateau[0][7] = Rook("white", 0, 7)
            self.plateau[7][7] = Rook("white", 7, 7)
            self.plateau[0][0] = Rook("black", 0, 0)
            self.plateau[7][0] = Rook("black", 7, 0)


            self.plateau[1][7] = Knight("white", 1, 7)
            self.plateau[6][7] = Knight("white", 6, 7)
            self.plateau[1][0] = Knight("black", 1, 0)
            self.plateau[6][0] = Knight("black", 6, 0)


            self.plateau[2][7] = Bishop("white", 2, 7)
            self.plateau[5][7] = Bishop("white", 5, 7)
            self.plateau[2][0] = Bishop("black", 2, 0)
            self.plateau[5][0] = Bishop("black", 5, 0)


            self.plateau[4][7] = King("white", 4, 7)
            self.plateau[4][0] = King("black", 4, 0)

            self.plateau[3][7] = Queen("white", 3, 7)
            self.plateau[3][0] = Queen("black", 3, 0)



    def tracerPlateau(self):

        for i in range(self.LIGNES):
            for j in range(self.COLONNES):

                x = i * self.LARGEUR
                y = j * self.HAUTEUR
                rect = pg.Rect(x, y, self.LARGEUR, self.HAUTEUR)
                    
                if (i + j) % 2 == 1:
                    pg.draw.rect(self.screen, (60, 25, 25), rect)

            


    def case(self, ligne, colonne):
        return self.plateau[colonne][ligne]
    

    def obtenirPiecesPlateau(self):
        """
        Renvoie la liste des pieces présentes dans le plateau
        """
        self.piecesPresentes = []
        for col in self.plateau:
            for piece in col:
                if piece != -1:
                    self.piecesPresentes.append(piece)

        return self.piecesPresentes


    def tracerPieces(self):
        for piece in self.obtenirPiecesPlateau():
            self.screen.blit(piece.image, (piece.x * self.LARGEUR, piece.y * self.HAUTEUR))


    def __str__(self):
        return str(self.plateau)


    def __iter__(self):
        return iter(self.plateau)
    

B = Plateau(80, 80, 8, 8, pg.display.set_mode((640, 640)))
B.generer_plateau()
B.plateau[4][4] = Bishop("black", 4, 4)
B.obtenirPiecesPlateau()
print(B.plateau[4][4].recherche_mouvements_autorises(B))
#print(B.piecesPresentes)


