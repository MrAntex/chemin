from tabnanny import check
from turtle import position
import numpy as np
import string
import math
import random


nbGames = 0
nbGorgees = 0
nbFigures = 0
nbWin = 0
nbLoses = 0

games = 20

# Création d'un jeu de 52 cartes
# Possibilité de tirer une carte du jeu
# Affichage des cartes restantes
class Jeu:

    cleanState = []
    remainingCards = []

    # Création du jeu de cartes
    def __init__(self):
        # Pour chaque couleur
        for couleur in ["Coeur", "Carreau", "Pique", "Trèfle"]:
            # On donne une valeur (11=V, 12=D, 13=R, 14=As)
            for valeur in range(2, 15):
                self.remainingCards.append([valeur, couleur])
        # Mélange des cartes, pour éviter des problèmes de récurrence
        random.shuffle(self.remainingCards)
        self.cleanState = self.remainingCards
    
    # Choix d'une carte aléatoire et suppression de cette dernière
    # du jeu
    def pickCard(self):
        return self.remainingCards.pop(np.random.randint(0, len(self.remainingCards)))
    
    # Nombre de cartes restantes
    def getCardCount(self):
        return len(self.remainingCards)
    
    def showRemainingCards(self):
        print(self.remainingCards)

    def reset(self):
        self.remainingCards = self.cleanState
        random.shuffle(self.remainingCards)


# Classe du jeu du chemin
# Création du chemin
# Inversion du chemin
# Affichage
# Initialisation du jeu
# Jouer un tour normal du jeu
class Chemin:

    etages: int # Nombre de cartes au milieu du chemin
    position = [0,0]

    cartes = [[]]
    jeu = Jeu()
    currentTurnCards = 0
    currentFigures = 0

    direction = 0

    gorgees = 0

    # Création du chemin
    def __init__(self, size:int):
        self.etages = size

        # Première moitié
        for i in range(size):
            # On rajoute une ligne de cartes
            self.cartes.append([])
            # Et on ajoute le bon nombre de cartes à cette ligne
            for k in range(i+1):
                self.cartes[i].append(self.jeu.pickCard())

        # Seconde moitié, même principe
        midCursor = size-1
        for g in range(size-1, 0, -1):
            self.cartes.append([])
            midCursor = midCursor+1
            for k in range(g):
                self.cartes[midCursor].append(self.jeu.pickCard())
        
        # On supprime la dernière ligne qui est vide
        # Bug à résoudre dans le futur, pas si grave dans l'état
        self.cartes.pop(len(self.cartes)-1)

    def reset(self, etages:int):

        self.etages = etages

        self.position = [0,0]

        self.cartes = [[]]
        self.jeu.reset()
        self.currentTurnCards = 0
        self.currentFigures = 0

        self.direction = 0

        self.gorgees = 0

        # Première moitié
        for i in range(etages):
            # On rajoute une ligne de cartes
            self.cartes.append([])
            # Et on ajoute le bon nombre de cartes à cette ligne
            for k in range(i+1):
                self.cartes[i].append(self.jeu.pickCard())

        # Seconde moitié, même principe
        midCursor = etages-1
        for g in range(etages-1, 0, -1):
            self.cartes.append([])
            midCursor = midCursor+1
            for k in range(g):
                self.cartes[midCursor].append(self.jeu.pickCard())
        
        # On supprime la dernière ligne qui est vide
        # Bug à résoudre dans le futur, pas si grave dans l'état
        self.cartes.pop(len(self.cartes)-1)

    # Inversion du sens du chemin
    # On crée le miroir de la liste de cartes
    def mirrorCards(self):
        # Pour chaque ligne
        for e in self.cartes:
            # On parcourt la moitié de la ligne
            for i in range(math.floor(len(e)/2)):
                # Et on permute chaque carte avec sa symétrique
                # Sur la ligne
                temp = e[i]
                e[i] = e[len(e)-1-i]
                e[len(e)-1-i] = temp
        
        # Idem en permutant les lignes directement cette fois
        for n in range(math.floor(len(self.cartes)/2)):
            temp = self.cartes[n]
            self.cartes[n] = self.cartes[len(self.cartes)-1-n]
            self.cartes[len(self.cartes)-1-n] = temp
    
    # Affichage des cartes
    def showReversedState(self):
        for e in range(2*(self.etages-1), -1, -1):
            print(self.cartes[e])

    def showState(self):
        for e in range(2*(self.etages-1)+1):
            print(self.cartes[e])

    # Changement du sens du jeu (départ en haut ou en bas)
    def setDirection(self, dir:int):
        if dir != self.direction :
            self.mirrorCards()
        self.direction = dir

    # Début du jeu
    def start(self, pos):
        # Si on est encore au début
        if self.position == [0, 0]:
            # Si on commence en "bas" du chemin
            if pos == "bot" or pos == 1:
                print("Starting bot")
                # On actualise le sens du chemin
                self.setDirection(1)
                return 0
            # Si on commence en haut, idem
            elif pos == "top" or pos == 2:
                print("starting top")
                self.setDirection(-1)
                return 0
            else:
                print("Wrong argument, got : ", pos)
                return 1
        else:
            print("Une partie est déja lancée !")
            return 1

    # Retourner une carte
    def checkCard(self):
        print(f"La carte est un {self.cartes[self.position[0]][self.position[1]]} !")
        # On a retourné une carte donc on incrémente
        self.currentTurnCards = self.currentTurnCards + 1
        # Si on a retourné une figure
        if self.cartes[self.position[0]][self.position[1]][0] > 10:
            print("Figure !")
            # On rajoute les gorgées à boire
            self.gorgees = self.gorgees + self.currentTurnCards
            self.currentTurnCards = 0 # Reset du nb de cartes retournées
            # On compte la figure retournée
            self.currentFigures = self.currentFigures + 1
            
            
        
        # Si on est au bout du chemin
        elif self.position[0] == (self.etages-1)*2:
            print("Le jeu est fini ! (Gagné)")
            #print(f"Gorgées bues : {self.gorgees} en {self.currentFigures} figures, soit ~{self.gorgees/max(self.currentFigures, 1)} gorgées/figure.")
            return 2


        # Si il reste des cartes dans le paquet
        if self.jeu.getCardCount() > 0:
            # On remplace la carte retournée
            self.cartes[self.position[0]][self.position[1]] = self.jeu.pickCard()

            if self.currentTurnCards == 0:
                self.position = [0, 0] # On repart du début
                return 1
            else:
                return 0
        else:
            print("Le jeu est fini ! (Perdu)")
            #print(f"Gorgées bues : {self.gorgees} en {self.currentFigures} figures, soit ~%.2f gorgées/figure.", self.gorgees/max(self.currentFigures, 1))
            return 3
        
        

    def step(self, d):
        
        # Droite
        if d == 'd' or d == 'D' or d == 'r' or d == 'R' or d == 2:
            print("Going right")
            # Si on a passé le milieu
            if self.position[0] >= self.etages - 1:
                # Et qu'on est déja tout à droite du chemin
                if self.position[1] == 0:
                    print("Impossible d'aller à droite")
                    return 1
                # Sinon on peut aller à droite
                else:
                    # Les changements de coordonnées ne sont
                    # Pas les même en fonction de la moitié
                    # Du chemin sur laquelle on se trouve
                    self.position = [self.position[0]+1, self.position[1]-1]
            # Si avant le milieu
            else:
                self.position = [self.position[0]+1, self.position[1]]            
            return 0
        
        # Gauche
        elif d == 'g' or d == 'G' or d == 'l' or d == 'L' or d == 1:
            print("Going left")
            # Si on a passé le milieu
            if self.position[0] >= self.etages - 1:
                # Et qu'on est déja tout à gauche du chemin
                if self.position[1] == ((self.etages-1)*2)-self.position[0]:
                    print("Impossible d'aller à gauche")
                    return 1
                # Sinon on peut aller à gauche
                else:
                    # Les changements de coordonnées ne sont
                    # Pas les même en fonction de la moitié
                    # Du chemin sur laquelle on se trouve
                    self.position = [self.position[0]+1, self.position[1]]
            # Si avant le milieu
            else:
                self.position = [self.position[0]+1, self.position[1]+1]
            return 0
        
        # Si le caractère entré est invalide
        else:
            print("Wrong direction, need (D/R) or (G/L), got ", d)
            return 1


print(f"- - PLAYING {games} GAMES - -")

leChemin = Chemin(4)

while nbGames < games:
    
    if nbGames % 10 == 0:
        print(f"{nbGames} games efffectuées...")

    leChemin.reset(4)
    checkC = 0

    while checkC < 2:
        leChemin.showState()
        direction = np.random.randint(1, 3)

        while leChemin.start(direction) == 1:
            direction = np.random.randint(1, 3)

        checkC = leChemin.checkCard()
        while checkC == 0:

            leChemin.showState()
            
            dg = np.random.randint(1, 3)
            while leChemin.step(dg) == 1:
                dg = np.random.randint(1, 3)
            
            checkC = leChemin.checkCard()
            print(leChemin.position)
    
    nbGames = nbGames + 1

    if checkC == 2:
        nbWin = nbWin + 1

    nbFigures = nbFigures + leChemin.currentFigures
    nbGorgees = nbGorgees + leChemin.gorgees

    



print("")
print("- - RÉSULTATS - -")
print(f"> Parties jouées : {nbGames}")
print(f"> Taux de victoire : %.2f ({nbWin}/{nbGames})", nbWin/nbGames)
print(f"> Gorgées bues : {nbGorgees}")
print("> Moyenne de gorgées par partie : %.2f", nbGorgees/nbGames)

