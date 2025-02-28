import pygame as pg


dico_positions_prises = {}

for i in range(8):
  for j in range(8):
    dico_positions_prises[(i, j)] = -1



class Piece:


  def __init__(self, couleur_name, valeur, x, y):


    self.x = x
    self.y = y
    self.couleur_name = couleur_name
    self.valeur = valeur
    self.couleur = 1 if couleur_name == "white" else 0
    self.image = pg.image.load(f"image/{self.couleur_name}_{self.valeur}.png")
    self.mouvements_autorises = []
    self.deja_bouge = False #sera pratique pour les pions, et les Roques

  def __repr__(self):
    return f'{self.couleur_name} {self.valeur}, {(self.x, self.y)} '

  def __add__(self, pos: tuple):
    self.x += pos[0]
    self.y += pos[1]
    return self
  

  def pos(self):
    return (self.x, self.y)
  
  def clear_mouvements_autorises(self):
     if len(self.mouvements_autorises) > 0:
        self.mouvements_autorises = []
  



class Pawn(Piece):


  def __init__(self, couleur, x, y):
    super().__init__(couleur, "pawn", x, y)
    self.valeur = "pawn"


  def recherche_mouvements_autorises(self, echiquier):
    """
    Renvoie une liste des mouvements autorisés pour la piece 
    """
    self.mouvements_autorises = []
    plateau = echiquier.plateau

    if self.couleur == 1:
        if self.y >= 1:
            if plateau[self.x][self.y-1] == -1:
                self.mouvements_autorises.append((self.x, self.y-1))

                if not self.deja_bouge:
                    if plateau[self.x][self.y-2] == -1:
                        self.mouvements_autorises.append((self.x, self.y-2))

            if self.x-1 >= 0:
                if plateau[self.x-1][self.y-1] != -1:
                    piece = plateau[self.x-1][self.y-1]
                    if piece.couleur != self.couleur:
                        self.mouvements_autorises.append((self.x-1, self.y-1))

            if self.x+1 < 8:
                if plateau[self.x+1][self.y-1] != -1:
                    piece = plateau[self.x+1][self.y-1]
                    if piece.couleur != self.couleur:
                        self.mouvements_autorises.append((self.x+1, self.y-1))

    else:
        if self.y+1 < 8:
            if plateau[self.x][self.y+1] == -1:
                self.mouvements_autorises.append((self.x, self.y+1))

                if not self.deja_bouge:
                    if plateau[self.x][self.y+1] == -1 and plateau[self.x][self.y+2] == -1:
                        self.mouvements_autorises.append((self.x, self.y+2))

            if self.x-1 >= 0:
                if plateau[self.x-1][self.y+1] != -1:
                    piece = plateau[self.x-1][self.y+1]
                    if piece.couleur != self.couleur:
                        self.mouvements_autorises.append((self.x-1, self.y+1))

        if self.x+1 < 8 and self.y+1 < 8:
            if plateau[self.x+1][self.y+1] != -1:
                piece = plateau[self.x+1][self.y+1]
                if piece.couleur != self.couleur:
                    self.mouvements_autorises.append((self.x+1, self.y+1))




    return self.mouvements_autorises




class Rook(Piece):
   

  def __init__(self, couleur, x, y):
    super().__init__(couleur, "rook", x, y)
    self.valeur = "rook"
    self.roque = None


  def recherche_mouvements_autorises(self, echiquier):

    plateau = echiquier.plateau


    self.clear_mouvements_autorises()
    i, j, k, m = 1, 1, 1, 1


    while self.x + i < 8:
        if plateau[self.x+i][self.y] == -1:
          self.mouvements_autorises.append((self.x + i, self.y))

        else:
          if plateau[self.x + i][self.y].couleur != self.couleur:
            self.mouvements_autorises.append((self.x + i, self.y))
            #Si on tombe sur une pièce de couleur opposée, on s'arrête. On ne voudrait pas passer par dessus !
          break     

        i += 1


    while self.x - j >= 0:

      if plateau[self.x - j][self.y] == -1:
        self.mouvements_autorises.append((self.x - j, self.y))

      else:
        if plateau[self.x - j][self.y].couleur != self.couleur:
          self.mouvements_autorises.append((self.x - j, self.y))
        break

      j += 1


    while self.y + k < 8: 

      if plateau[self.x][self.y + k] == -1:
        self.mouvements_autorises.append((self.x, self.y + k))

      else:
         if plateau[self.x][self.y + k].couleur != self.couleur:
           self.mouvements_autorises.append((self.x, self.y + k))
         break 
      
      k += 1


    while self.y - m >= 0:

      if plateau[self.x][self.y - m] == -1:
        self.mouvements_autorises.append((self.x, self.y - m))

      else:
        if plateau[self.x][self.y - m].couleur != self.couleur:
          self.mouvements_autorises.append((self.x, self.y - m))
        break

      m += 1


    return self.mouvements_autorises



"""
class Bishop(Piece):
   

  def __init__(self, couleur, x, y):
    super().__init__(couleur, "bishop", x, y)
    self.valeur = "bishop"


  def recherche_mouvements_autorises(self, echiquier):

    plateau = echiquier.plateau
    i, j, k, m = 1, 1, 1, 1


    while self.x + i < 8 and self.y + i < 8:
      
        
        if plateau[self.x+i][self.y+i] == -1:
          self.mouvements_autorises.append((self.x + i, self.y+i))

        else:
          if plateau[self.x + i][self.y+i].couleur != self.couleur:
            self.mouvements_autorises.append((self.x + i, self.y+i))
            #Si on tombe sur une pièce de couleur opposée, on s'arrête. On ne voudrait pas passer par dessus !
          break     

        i += 1


    while self.x - j >= 0 and self.y - j >= 0:
      if plateau[self.x - j][self.y-j] == -1:
        self.mouvements_autorises.append((self.x - j, self.y-j))

      else:
        if plateau[self.x - j][self.y-j].couleur != self.couleur:
          self.mouvements_autorises.append((self.x - j, self.y-j))
        break

      j += 1


    while self.y + k < 8 and self.x - k >= 0: 
      if plateau[self.x-k][self.y + k] == -1:
        self.mouvements_autorises.append((self.x-k, self.y + k))

      else:
         if plateau[self.x-k][self.y + k].couleur != self.couleur:
           self.mouvements_autorises.append((self.x-k, self.y + k))
         break 
      
      k += 1


    while self.y - m >= 0 and self.x + m < 8:
      if plateau[self.x+m][self.y - m] == -1:
        self.mouvements_autorises.append((self.x+m, self.y - m))

      else:
        if plateau[self.x+m][self.y - m].couleur != self.couleur:
          self.mouvements_autorises.append((self.x+m, self.y - m))
        break

      m += 1


    return self.mouvements_autorises
"""

class Bishop(Piece):
  def __init__(self, couleur, x, y):
    super().__init__(couleur, "bishop", x, y)
    self.valeur = "bishop"

  def recherche_mouvements_autorises(self, echiquier):
    self.clear_mouvements_autorises()
    plateau = echiquier.plateau

    row = self.y
    col = self.x

    # Diagonal up-right
    row_i = row + 1
    col_i = col + 1
    while row_i <= 7 and col_i <= 7:
      if plateau[col_i][row_i] == -1:
        self.mouvements_autorises.append((col_i, row_i))
        row_i += 1
        col_i += 1
      else:
        if plateau[col_i][row_i].couleur != self.couleur:
          self.mouvements_autorises.append((col_i, row_i))
        break

    # Diagonal down-left
    row_i = row - 1
    col_i = col - 1
    while row_i >= 0 and col_i >= 0:
      if plateau[col_i][row_i] == -1:
        self.mouvements_autorises.append((col_i, row_i))
        row_i -= 1
        col_i -= 1
      else:
        if plateau[col_i][row_i].couleur != self.couleur:
          self.mouvements_autorises.append((col_i, row_i))
        break

    # Diagonal up-left
    row_i = row - 1
    col_i = col + 1
    while row_i >= 0 and col_i <= 7:
      if plateau[col_i][row_i] == -1:
        self.mouvements_autorises.append((col_i, row_i))
        row_i -= 1
        col_i += 1
      else:
        if plateau[col_i][row_i].couleur != self.couleur:
          self.mouvements_autorises.append((col_i, row_i))
        break

    # Diagonal down-right
    row_i = row + 1
    col_i = col - 1
    while row_i <= 7 and col_i >= 0:
      if plateau[col_i][row_i] == -1:
        self.mouvements_autorises.append((col_i, row_i))
        row_i += 1
        col_i -= 1
      else:
        if plateau[col_i][row_i].couleur != self.couleur:
          self.mouvements_autorises.append((col_i, row_i))
        break

    return self.mouvements_autorises

class Knight(Piece):
   
  def __init__(self, couleur, x, y):
      super().__init__(couleur, "knight", x, y)
      self.valeur = "knight"

  def recherche_mouvements_autorises(self, echiquier):

    plateau = echiquier.plateau
    self.clear_mouvements_autorises()


    for i in range(-2, 3):

      for j in range(-2, 3):

        if abs(i) + abs(j) == 3 and 0 <= self.x + i < 8 and 0 <= self.y + j < 8:
          #Le cavalier se déplace de trois cases au total, et de maximum 2 cases par direction
          if plateau[self.x + i][self.y + j] == -1 or plateau[self.x + i][self.y + j].couleur != self.couleur:
            self.mouvements_autorises.append((self.x + i, self.y + j))

          
    return self.mouvements_autorises
  


class King(Piece):
   
  def __init__(self, couleur, x, y):
    super().__init__(couleur, "king", x, y)
    self.valeur = "king"
    self.echec = False
    self.mat = False

  def recherche_mouvements_autorises(self, echiquier):
    plateau = echiquier.plateau
    self.clear_mouvements_autorises()
    
    for i in range(-1, 2):
        for j in range(-1, 2):
        
            if 0 <= self.x + i < 8 and 0 <= self.y + j < 8:
            
                if plateau[self.x + i][self.y + j] == -1 or plateau[self.x + i][self.y + j].couleur != self.couleur:
                    self.mouvements_autorises.append((self.x + i, self.y + j))
    
    # Castling
    if not self.deja_bouge:
        # Petit Roque
        if self.x + 2 < 8:
          if plateau[self.x + 1][self.y] == -1 and plateau[self.x + 2][self.y] == -1:
              rook = plateau[self.x + 3][self.y]
              if isinstance(rook, Rook) and not rook.deja_bouge:
                  self.mouvements_autorises.append((self.x + 2, self.y))
        
        # Grand Roque
        if self.x-2 >= 0:
          if plateau[self.x - 1][self.y] == -1 and plateau[self.x - 2][self.y] == -1 and plateau[self.x - 3][self.y] == -1:
              rook = plateau[self.x - 4][self.y]
              if isinstance(rook, Rook) and not rook.deja_bouge:
                  self.mouvements_autorises.append((self.x - 2, self.y))
  
    return self.mouvements_autorises
  


class Queen(Piece):
   

  def __init__(self, couleur, x, y):
      super().__init__(couleur, "queen", x, y)
      self.valeur = "queen"


  def recherche_mouvements_autorises(self, echiquier):

    tour_fictive = Rook(self.couleur_name, self.x, self.y)
    fou_fictif = Bishop(self.couleur_name, self.x, self.y)

    self.mouvements_autorises = tour_fictive.recherche_mouvements_autorises(echiquier) + fou_fictif.recherche_mouvements_autorises(echiquier)
    return self.mouvements_autorises


     


