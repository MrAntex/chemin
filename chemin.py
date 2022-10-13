import sys
import numpy as np
import math
import random
from tqdm import tqdm

# Paramètres du script
games = 1000 # Nombres de parties à simuler
maxCards = 4 # Nombre de cartes sur la ligne du milieu
debug = False # Affichage des prints

# Si on a au moins 1 argument
if len(sys.argv) >= 2:
    games = int(sys.argv[1]) # On met à jour le nombre de games
if len(sys.argv) >= 3: # Si 3 arguments
    maxCards = int(sys.argv[2]) # On met à jour le nombre de cartes max


# - - Classe d'un jeu de cartes - -
# Création d'un jeu de 52 cartes
# Possibilité de tirer une carte du jeu
# Affichage des cartes restantes
# Sortie du nombre de cartes restantes
class Jeu:

    remainingCards = []

    # Création du jeu de cartes
    def __init__(self):

        # On redéfinit la variable pour pouvoir
        # reset les instances de classes sans souci
        self.remainingCards = []

        # Pour chaque couleur
        for couleur in ["Coeur", "Carreau", "Pique", "Trèfle"]:
            # On donne une valeur (11=V, 12=D, 13=R, 14=As)
            for valeur in range(2, 15):
                self.remainingCards.append([valeur, couleur])
        # Mélange des cartes, pour éviter des problèmes de récurrence
        random.shuffle(self.remainingCards)
    
    # Choix d'une carte aléatoire et suppression de cette dernière
    # du jeu
    def pickCard(self):
        return self.remainingCards.pop(np.random.randint(0, len(self.remainingCards)))
    
    # Nombre de cartes restantes
    def getCardCount(self):
        return len(self.remainingCards)
    
    def showRemainingCards(self):
        print(self.remainingCards)


# - - Classe du jeu du chemin - -
# Création du chemin
# Inversion du chemin
# Changement auto du sens du chemin en fonction de ses variables
# Affichage
# Affichage de l'inverse (sans inverser le jeu)
# Initialisation du jeu
# Retourner une carte
# Se déplacer sur le chemin
class Chemin:

    etages: int # Nombre de cartes au milieu du chemin
    position = [0,0]

    cartes = [[]]
    currentTurnCards = 0
    currentFigures = 0

    direction = 0

    gorgees = 0
    listeGorgees = []

    # Création du chemin
    def __init__(self, size:int, jeu:Jeu):

        # On redéfinit toutes les variables pour pouvoir
        # reset les instances de classes sans souci
        self.position = [0,0]

        self.cartes = [[]]
        self.currentTurnCards = 0
        self.currentFigures = 0

        self.direction = 0

        self.gorgees = 0
        self.listeGorgees = []

        self.jeu = jeu
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
                if debug: print("Starting bot")
                # On actualise le sens du chemin
                self.setDirection(1)
                return 0
            # Si on commence en haut, idem
            elif pos == "top" or pos == 2:
                if debug: print("starting top")
                self.setDirection(-1)
                return 0
            else:
                print("Wrong argument, got : ", pos)
                return 1
        else:
            if debug: print("Une partie est déja lancée !")
            return 1

    # Retourner une carte
    def checkCard(self):
        if debug: print(f"Position : {self.position}")
        if debug: print(f"La carte est un {self.cartes[self.position[0]][self.position[1]]} !")
        # On a retourné une carte donc on incrémente
        self.currentTurnCards = self.currentTurnCards + 1
        # Si on a retourné une figure
        if self.cartes[self.position[0]][self.position[1]][0] > 10:
            if debug: print("Figure !")
            # On rajoute les gorgées à boire
            self.gorgees = self.gorgees + self.currentTurnCards
            # Logging pour les stats à la fin
            self.listeGorgees.append(self.currentTurnCards)
            self.currentTurnCards = 0 # Reset du nb de cartes retournées
            # On compte la figure retournée
            self.currentFigures = self.currentFigures + 1
            
            
        # Si on est au bout du chemin
        elif self.position[0] == (self.etages-1)*2:
            if debug: print("Le jeu est fini ! (Gagné)")
            #print(f"Gorgées bues : {self.gorgees} en {self.currentFigures} figures, soit ~{self.gorgees/max(self.currentFigures, 1)} gorgées/figure.")
            return 2


        # Si il reste des cartes dans le paquet
        if self.jeu.getCardCount() > 0:
            # On remplace la carte retournée
            self.cartes[self.position[0]][self.position[1]] = self.jeu.pickCard()
            # Si c'est la première carte
            if self.currentTurnCards == 0:
                self.position = [0, 0] # On repart du début
                return 1
            else:
                return 0
        else:
            if debug: print("Le jeu est fini ! (Perdu)")
            #print(f"Gorgées bues : {self.gorgees} en {self.currentFigures} figures, soit ~%.2f gorgées/figure.", self.gorgees/max(self.currentFigures, 1))
            return 3
        
        

    def step(self, d):

        # Pour chaque direction on différencie 3 cas determinés par 2 conditions :
        # Es-ce que la carte en cours est avant l'étage du milieu
        # Si ce n'est pas le cas, es-ce qu'elle est déjà sur le
        # bord du chemin, et ne peut donc pas le dépasser.
        
        # Droite
        if d == 'd' or d == 'D' or d == 'r' or d == 'R' or d == 2:
            if debug: print("Going right")
            # Si on a passé le milieu
            if self.position[0] >= self.etages - 1:
                # Et qu'on est déja tout à droite du chemin
                if self.position[1] == 0:
                    if debug: print("Impossible d'aller à droite")
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
            if debug: print("Going left")
            # Si on a passé le milieu
            if self.position[0] >= self.etages - 1:
                # Et qu'on est déja tout à gauche du chemin
                if self.position[1] == ((self.etages-1)*2)-self.position[0]:
                    if debug: print("Impossible d'aller à gauche")
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

# Fonctionnement normal
print(f"- - PLAYING {games} GAMES - -")

# Variables pour les stats
nbGames = 0
nbGorgees = 0
nbFigures = 0
nbWin = 0
nbLoses = 0
nbGorgeesParLigne = []

# Initialisation du jeu de cartes et du chemin
jeu = Jeu()
leChemin = Chemin(4, jeu)

# tqdm pour avoir une barre de progression
for k in tqdm(range(games)):
   
    checkC = 0 # Permet de savoir si la partie en cours est finie

    while checkC < 2: # Tant que la partie n'est pas finie
        if debug: leChemin.showState()
        # On prend un sens au hasard
        direction = np.random.randint(1, 3)

        # Et on continue d'en prendre un au hasard tant
        # qu'elle n'est pas valide
        while leChemin.start(direction) == 1:
            direction = np.random.randint(1, 3)

        # On retourne la carte choisie, en mettant à jour le flag
        checkC = leChemin.checkCard()

        # Et tant qu'on ne tombe pas sur une figure on avance
        while checkC == 0:

            if debug: leChemin.showState()
            # Choix d'une direction au hasard
            dg = np.random.randint(1, 3)
            # Et on continue d'en prendre une au hasard
            # tant qu'elle n'est pas valide
            while leChemin.step(dg) == 1:
                dg = np.random.randint(1, 3)
            
            # On retourne la carte en mettant à jour le flag
            checkC = leChemin.checkCard()
            if debug: print(leChemin.position)
    
    # Si on a gagné
    if checkC == 2:
        nbWin = nbWin + 1 # Màj du nb de victoires

    # Màj des compteurs pour les stats
    nbFigures = nbFigures + leChemin.currentFigures
    nbGorgees = nbGorgees + leChemin.gorgees
    nbGorgeesParLigne.append(leChemin.listeGorgees)

    # Reset du jeu de cartes et du chemin
    jeu = Jeu()
    leChemin = Chemin(maxCards, jeu)

    
# Calcul des stats des parties
avgWin = nbWin/games # Taux de victoire
avgGorgees = nbGorgees/games # Moyenne des gorgées / partie
nbLignes = 0

# Calcul du nombre de lignes
for game in nbGorgeesParLigne:
    nbLignes = nbLignes + len(game)

avgLignePerGame = nbLignes / games # Moy du nb de lignes / partie
avgGorPerLigne = nbGorgees / nbLignes # Moy du nb de gorgées / ligne

# Output
print("")
print("- - RÉSULTATS - -")
print(f"> Parties jouées : {games}")
print('> Taux de victoire : %5.2f (%2d/%2d)' % (avgWin, nbWin, games))
print(f"> Gorgées bues : {nbGorgees}")
print("> Moyenne de gorgées par partie : %5.2f" % (avgGorgees))
print("> Moyenne de lignes faites par partie : %5.2f" % avgLignePerGame)
print("> Moyenne de gorgees par ligne : %5.2f" % avgGorPerLigne)

