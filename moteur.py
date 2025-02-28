from plateau import Plateau
from piece import King, Rook, Pawn, Queen, Bishop, Knight
import pygame as pg

class Jeu:

    def __init__(self, LARGEUR, HAUTEUR, COLONNES, LIGNES, ecran, Victoire):
        self.Victoire = Victoire
        self.Plateau = Plateau(LARGEUR, HAUTEUR, COLONNES, LIGNES, ecran)
        self.selectionne = None
        self.tour = 1
        self.mouvements_valides = []
        self.pieces_noires_restantes = 16
        self.pieces_blanches_restantes = 16
        self.LARGEUR = LARGEUR
        self.HAUTEUR = HAUTEUR
        self.COLONNES = COLONNES
        self.LIGNES = LIGNES
        self.ecran = ecran

    def mettre_a_jour_fenetre(self):
        self.Plateau.tracerPlateau()
        self.Plateau.tracerPieces()
        self.colorier_roi_en_echec_ou_mat()
        self.tracer_mouvements_possibles()
        pg.display.update()

    def reinitialiser(self):
        self.Plateau = Plateau(self.LARGEUR, self.HAUTEUR, self.COLONNES, self.LIGNES, self.ecran)
        self.selectionne = None

    def verifier_jeu(self):
        if self.pieces_noires_restantes == 0:
            print("Les Blancs gagnent")
            return True

        if self.pieces_blanches_restantes == 0:
            print("Les Noirs gagnent")
            return True

        if self.echec_et_mat(self.Plateau):
            if self.tour == 1:
                print("Les Noirs gagnent")
                return True
            else:
                print("Les Blancs gagnent")
                return True

    def mouvements_ennemis(self, piece, Plateau):
        mouvements_ennemis = []
        for r in range(len(Plateau.plateau)):
            for c in range(len(Plateau.plateau[r])):
                if Plateau.plateau[r][c] != -1:
                    if Plateau.plateau[r][c].couleur != piece.couleur:
                        mouvements = Plateau.plateau[r][c].recherche_mouvements_autorises(Plateau)
                        for mouvement in mouvements:
                            mouvements_ennemis.append(mouvement)
        return mouvements_ennemis

    def obtenir_position_roi(self, Plateau):
        for colonne in Plateau.plateau:
            for piece in colonne:
                if piece != -1:
                    if piece.valeur == "king" and piece.couleur == self.tour:
                        return (piece.x, piece.y)

    def simuler_mouvement(self, piece, ligne, colonne):
        ligne_piece, colonne_piece = piece.x, piece.y
        piece_sauvegardee = self.Plateau.plateau[ligne][colonne]
        if self.Plateau.plateau[ligne][colonne] != -1:
            self.Plateau.plateau[ligne][colonne] = -1

        self.Plateau.plateau[piece.x][piece.y], self.Plateau.plateau[ligne][colonne] = self.Plateau.plateau[ligne][colonne], self.Plateau.plateau[piece.x][piece.y]

        position_roi = self.obtenir_position_roi(self.Plateau)
        if position_roi in self.mouvements_ennemis(piece, self.Plateau):
            piece.x, piece.y = ligne_piece, colonne_piece
            self.Plateau.plateau[ligne_piece][colonne_piece] = piece
            self.Plateau.plateau[ligne][colonne] = piece_sauvegardee
            return False

        piece.x, piece.y = ligne_piece, colonne_piece
        self.Plateau.plateau[ligne_piece][colonne_piece] = piece
        self.Plateau.plateau[ligne][colonne] = piece_sauvegardee
        return True

    def mouvements_possibles(self, Plateau):
        mouvements_possibles = []
        for r in range(len(Plateau.plateau)):
            for c in range(len(Plateau.plateau[r])):
                if Plateau.plateau[c][r] != -1:
                    if Plateau.plateau[c][r].couleur == self.tour and Plateau.plateau[c][r].valeur != "roi":
                        mouvements = Plateau.plateau[c][r].recherche_mouvements_autorises(Plateau)
                        for mouvement in mouvements:
                            mouvements_possibles.append(mouvement)
        return mouvements_possibles

    def echec_et_mat(self, Plateau):
        position_roi = self.obtenir_position_roi(Plateau)
        if position_roi is None:
            return False
        roi = Plateau.plateau[position_roi[0]][position_roi[1]]
        mouvements_disponibles_roi = set(roi.recherche_mouvements_autorises(Plateau))
        mouvements_ennemis_set = set(self.mouvements_ennemis(roi, Plateau))
        mouvements_roi = mouvements_disponibles_roi - mouvements_ennemis_set
        set1 = mouvements_disponibles_roi.intersection(mouvements_ennemis_set)
        mouvements_possibles_defense = set1.intersection(self.mouvements_possibles(Plateau))
        if len(mouvements_roi) == 0 and len(mouvements_disponibles_roi) != 0 and len(mouvements_possibles_defense) == 0:
            roi.mat = True
            return True
        return False

    def changer_tour(self):
        self.tour = 1 - self.tour

    def selectionner(self, ligne, colonne):
        if self.selectionne:
            mouvement = self._deplacer(ligne, colonne)
            if not mouvement:
                self.selectionne = None
                self.selectionner(ligne, colonne)

        piece = self.Plateau.plateau[ligne][colonne]
        print(piece)
        if piece != -1 and self.tour == piece.couleur:
            self.selectionne = piece
            tous_mouvements_valides = piece.recherche_mouvements_autorises(self.Plateau)
            self.mouvements_valides = [mouvement for mouvement in tous_mouvements_valides if self.simuler_mouvement(piece, mouvement[0], mouvement[1])]
            print("self mouvements_valides", self.mouvements_valides)

    def _deplacer(self, ligne, colonne):
        piece = self.Plateau.plateau[ligne][colonne]

        if self.selectionne and isinstance(self.selectionne, King) and abs(self.selectionne.x - ligne) == 2:
                print("ROQUE")
                # Mouvement de roque
                if colonne == self.selectionne.y:
                    if ligne == self.selectionne.x + 2:

                        # Roque côté roi
                        tour = self.Plateau.plateau[self.selectionne.x + 3][self.selectionne.y]
                        if isinstance(tour, Rook) and not tour.deja_bouge:
                            self.Plateau.plateau[self.selectionne.x + 1][self.selectionne.y], self.Plateau.plateau[self.selectionne.x + 3][self.selectionne.y] = tour, -1
                            tour.x, tour.y = self.selectionne.x + 1, self.selectionne.y
                    elif ligne == self.selectionne.x - 2:

                        # Roque côté dame
                        tour = self.Plateau.plateau[self.selectionne.x - 4][self.selectionne.y]
                        if isinstance(tour, Rook) and not tour.deja_bouge:
                            self.Plateau.plateau[self.selectionne.x - 1][self.selectionne.y], self.Plateau.plateau[self.selectionne.x - 4][self.selectionne.y] = tour, -1
                            tour.x, tour.y = self.selectionne.x - 1, self.selectionne.y
                    self.Plateau.plateau[self.selectionne.x][self.selectionne.y], self.Plateau.plateau[ligne][colonne] = -1, self.selectionne
                    self.selectionne.x, self.selectionne.y = ligne, colonne  # Mettre à jour la position de la pièce
                    self.Plateau.obtenirPiecesPlateau()  # Mettre à jour les pièces du plateau
                    print(self.Plateau.obtenirPiecesPlateau())
                    self.changer_tour()
                    self.mouvements_valides = []
                    self.selectionne = None
                    return True
                return False

        elif self.selectionne and (ligne, colonne) in self.mouvements_valides:
            if piece == -1 or piece.couleur != self.selectionne.couleur:
                if self.simuler_mouvement(self.selectionne, ligne, colonne):
                    self.enlever(self.Plateau.plateau, piece, ligne, colonne)
                    self.Plateau.plateau[self.selectionne.x][self.selectionne.y], self.Plateau.plateau[ligne][colonne] = -1, self.selectionne
                    self.selectionne.x, self.selectionne.y = ligne, colonne  # Mettre à jour la position de la pièce
                    self.selectionne.deja_bouge = True
                    self.Plateau.obtenirPiecesPlateau()  # Mettre à jour les pièces du plateau
                    self.verifier_promotion_pion(ligne, colonne)  # Vérifier la promotion du pion
                    self.changer_tour()
                    self.mouvements_valides = []
                    self.selectionne = None
                    return True
                return False

    def verifier_promotion_pion(self, ligne, colonne):
        piece = self.Plateau.plateau[ligne][colonne]
        if isinstance(piece, Pawn) and (colonne == 0 or colonne == self.COLONNES - 1):
            self.promouvoir_pion(piece, ligne, colonne)

    def promouvoir_pion(self, pion, ligne, colonne):
        # Ceci est un exemple simple, vous pourriez vouloir créer une interface utilisateur appropriée pour cela
        choix_promotion = input("Promouvoir en (r)eine, (t)our, (f)ou ou (c)avalier: ").lower()
        if choix_promotion == 'r':
            self.Plateau.plateau[ligne][colonne] = Queen(pion.couleur_name, ligne, colonne)
        elif choix_promotion == 't':
            self.Plateau.plateau[ligne][colonne] = Rook(pion.couleur_name, ligne, colonne)
        elif choix_promotion == 'f':
            self.Plateau.plateau[ligne][colonne] = Bishop(pion.couleur_name, ligne, colonne)
        elif choix_promotion == 'c':
            self.Plateau.plateau[ligne][colonne] = Knight(pion.couleur_name, ligne, colonne)

    def enlever(self, plateau, piece, ligne, colonne):
        if piece != -1:
            plateau[ligne][colonne] = -1
            if piece.couleur == 1:
                self.pieces_blanches_restantes -= 1
            else:
                self.pieces_noires_restantes -= 1
        print("pieces_blanches_restantes : ", self.pieces_blanches_restantes)
        print("pieces_noires_restantes : ", self.pieces_noires_restantes)

    def colorier_roi_en_echec_ou_mat(self):
        for r in range(len(self.Plateau.plateau)):
            for c in range(len(self.Plateau.plateau[r])):
                piece = self.Plateau.plateau[r][c]
                if piece != -1 and isinstance(piece, King):
                    if piece.echec:
                        rect = pg.Rect(c * self.Plateau.LARGEUR, r * self.Plateau.HAUTEUR, self.Plateau.LARGEUR, self.Plateau.HAUTEUR)
                        pg.draw.rect(self.Plateau.screen, (255, 165, 0), rect)  # Orange pour échec
                    if piece.mat:
                        rect = pg.Rect(c * self.Plateau.LARGEUR, r * self.Plateau.HAUTEUR, self.Plateau.LARGEUR, self.Plateau.HAUTEUR)
                        pg.draw.rect(self.Plateau.screen, (255, 0, 0), rect)  # Rouge pour échec et mat

    def tracer_mouvements_possibles(self):
        if len(self.mouvements_valides) > 0:
            for pos in self.mouvements_valides:
                ligne, colonne = pos[0], pos[1]
                rect = pg.Rect(ligne * self.Plateau.LARGEUR, colonne * self.Plateau.HAUTEUR, self.Plateau.LARGEUR, self.Plateau.HAUTEUR)
                pg.draw.rect(self.Plateau.screen, (128, 128, 128), rect)  # Surligner en gris

    def obtenir_plateau(self):
        return self.Plateau


game = Jeu(80, 80, 8, 8, pg.display.set_mode((640, 640)), None)
game.Plateau.generer_plateau()
