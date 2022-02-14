import pygame
from enum import Enum

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

#Création d'un tableau : 0 = case VIDE, 1 = MUR, 2 = DEPART, 3 = ARRIVE
tableau = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 1, 0, 0, 3, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

class Case():
	"""Classe définissant une case caractérisée par :
	- sa distance G par rapport à la case de départ
	- sa distance H par rapport à la case d'arrivée
	- la distance entre la case de départ et la case d'arrivée en passant par cette case 
	F (F = G + H)
	"""
	def __init__(self):
		"""    Constructeur de la classe Case     """

		self.g = 0
		self.h = 0
		self.f = 0
		self.type = "" # les types de cases : vide, mur, départ, arrivée, évaluée, non-évaluée



def main(tableau, largeur, hauteur):

	LARGEUR = largeur
	HAUTEUR = hauteur

	#création de la fenêtre
	screen = pygame.display.set_mode((largeur, hauteur))
	pygame.display.set_caption("Pathfinding program")

	#initialisation et affichage du tableau
	case = Case()
	tableau_initialise = [[case for j in range(len(tableau[0]))] for i in range(len(tableau))]
	for i in range(len(tableau)):
		for j in range(len(tableau[0])):
			if tableau[i][j] == 0:
				tableau_initialise[i][j].type = 0
			if tableau[i][j] == 1:
				tableau_initialise[i][j].type = 1
			if tableau[i][j] == 2:
				tableau_initialise[i][j].type = 2
			if tableau[i][j] == 3:
				tableau_initialise[i][j].type = 3

	clock = pygame.time.Clock()
	FPS = 60  # Frames per second.
	BLACK = (0, 0, 0)

	#création du tableau de surfaces pour blit
	tableau_rect = [[pygame.Rect((LARGEUR/10,HAUTEUR/10), (LARGEUR/10, HAUTEUR/10)) for j in range (len(tableau_initialise[0]))] for i in range(len(tableau_initialise))]
	for i in range(len(tableau_initialise)):
		for j in range(len(tableau_initialise[0])):
			tableau_rect[i][j] = pygame.Rect((j*LARGEUR/10, i*HAUTEUR/10), (LARGEUR/10, HAUTEUR/10))

	#importation et redimensionnement des images pour les cases
	case_depart = pygame.image.load("case_bleue.png")
	case_depart = case_depart.convert()
	case_depart = pygame.transform.scale(case_depart, (int(LARGEUR/10), int(HAUTEUR/10)))
	case_evaluee = pygame.image.load("case_rouge.png")
	case_evaluee = case_evaluee.convert()
	case_evaluee = pygame.transform.scale(case_evaluee, (int(LARGEUR/10), int(HAUTEUR/10)))
	case_non_evaluee = pygame.image.load("case_verte.png")
	case_non_evaluee = case_non_evaluee.convert()
	case_non_evaluee = pygame.transform.scale(case_non_evaluee, (int(LARGEUR/10), int(HAUTEUR/10)))
	case_arrivee = pygame.image.load("case_orange.png")
	case_arrivee = case_arrivee.convert()
	case_arrivee = pygame.transform.scale(case_arrivee, (int(LARGEUR/10), int(HAUTEUR/10)))
	case_mur = pygame.image.load("case_noire.png")
	case_mur = case_mur.convert()
	case_mur = pygame.transform.scale(case_mur, (int(LARGEUR/10), int(HAUTEUR/10)))
	case_vide = pygame.image.load("case_grise.png")
	case_vide = case_vide.convert()
	case_vide = pygame.transform.scale(case_vide, (int(LARGEUR/10), int(HAUTEUR/10)))

	screen.fill(BLACK)

	for i in range(len(tableau_initialise)):
			for j in range(len(tableau_initialise[0])):
				if tableau_initialise[i][j].type == 0:
					screen.blit(case_vide, tableau_rect[i][j])

				if tableau_initialise[i][j].type == 1:
					screen.blit(case_mur, tableau_rect[i][j])

				if tableau_initialise[i][j].type == 2:
					screen.blit(case_depart, tableau_rect[i][j])

				if tableau_initialise[i][j].type == 3:
					screen.blit(case_arrivee, tableau_rect[i][j])

				if tableau_initialise[i][j].type == 4:
					screen.blit(case_evaluee, tableau_rect[i][j])

				if tableau_initialise[i][j].type == 5:
					screen.blit(case_non_evaluee, tableau_rect[i][j])

	pygame.display.update()

	while True:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

main(tableau, 720, 720)