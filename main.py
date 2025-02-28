from piece import *
from plateau import *
from moteur import *

import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 80, 80
LIGNES, COLONNES = 8, 8
TAILLE_ECHIQUIER = (HAUTEUR * LIGNES, LARGEUR * COLONNES)
RED = (255, 0, 0)

screen = pg.display.set_mode(TAILLE_ECHIQUIER)
screen_color = (255, 255, 255)


if __name__ == "__main__":
    # Initialisation de Pygame
    pg.init()
    running = True
    fin_du_jeu = False

    game = Jeu(LARGEUR, HAUTEUR, COLONNES, LIGNES, screen, None)
    game.Plateau.generer_plateau()
    game_over = False

    while running:
        screen.fill(screen_color)

        game.mettre_a_jour_fenetre()
        if game.verifier_jeu():
            game_over = True
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()


            if event.type == pg.KEYDOWN and game_over:
                if event.key == pg.K_SPACE and game_over:
                    game.reinitialiser()




            if event.type == pg.MOUSEBUTTONDOWN and not game_over:


                if pg.mouse.get_pressed()[0]:
                    location = pg.mouse.get_pos()
                    row,col = (location[0]//LARGEUR,location[1]//HAUTEUR)
                    game.selectionner(row,col)


        pg.display.update()

    pg.quit()
