"""

Programme pathfinding
Auteur : Adrien Louvrier
Date de création : 05/11/2020

entrée : tableau composé :
	-de cases vides(0),
	-de murs(1), 
	-d'une case de départ(2)
	-d'une case d'arrivée(3)

sortie : affichage d'un tableau avec le chemin le plus court reliant la case de départ 
avec la case d'arrivée

Objectif : créer un programme permettant de trouver le chemin le plus court 
entre 2 case dans un tableau

"""

import pygame
from math import *
from random import *

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

pygame.font.init()

#Création d'un tableau : 0 = case VIDE, 1 = MUR, 2 = DEPART, 3 = ARRIVE
tableau = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

depart_x = randint(0,len(tableau))
depart_y = randint(0, len(tableau[0]))

arrivee_x = randint(0, len(tableau))
arrivee_y = randint(0, len(tableau[0]))

for i in range(len(tableau)):
	for j in range(len(tableau[0])):
		tableau[i][j] = randint(0,1)

tableau[5][6] = 2
tableau[10][25] = 3

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
		self.x = 0
		self.y = 0
		self.type = "" # les types de cases : vide, mur, départ, arrivée, évaluée, non-évaluée


def main(tableau):
	"""Fonction principale du programme"""

	if len(tableau) >= len(tableau[0]):
		LARGEUR = int(1008/len(tableau))*len(tableau[0])
		HAUTEUR = int(1008/len(tableau))*len(tableau)
	elif len(tableau) < len(tableau[0]):
		LARGEUR = int(1008/len(tableau[0]))*len(tableau[0])
		HAUTEUR = int(1008/len(tableau[0]))*len(tableau)

	taille_case = HAUTEUR/len(tableau)

	lignes = len(tableau)
	colonnes = len(tableau[0])

	#création de la fenêtre
	screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
	pygame.display.set_caption("Pathfinding program")

	#initialisation et affichage du tableau
	tableau_initialise = initialiser_tableau(tableau)

	clock = pygame.time.Clock()
	FPS = 60  # Frames per second.
	BLACK = (0, 0, 0)
	cases_a_evaluer = []
	cases_evaluees = []
	current = Case()
	debut = False
	chemin_trouve = False
	afficher_valeur = False
	fin = False

	font1 = pygame.font.SysFont('Arial', int((1/4)*(1152/max(len(tableau),len(tableau[0])))))
	font2 = pygame.font.SysFont('Arial', int((1/6)*(1152/max(len(tableau),len(tableau[0])))))

	#création du tableau de surfaces pour blit
	tableau_rect = [[pygame.Rect((LARGEUR/colonnes,HAUTEUR/lignes), (LARGEUR/colonnes, HAUTEUR/lignes)) for j in range (len(tableau_initialise[0]))] for i in range(len(tableau_initialise))]
	for i in range(len(tableau_initialise)):
		for j in range(len(tableau_initialise[0])):
			tableau_rect[i][j] = pygame.Rect((j*LARGEUR/colonnes, i*HAUTEUR/lignes), (LARGEUR/colonnes, HAUTEUR/lignes))

	#importation et redimensionnement des images pour les cases
	case_depart = pygame.image.load("case_bleue.png")
	case_depart = case_depart.convert()
	case_depart = pygame.transform.scale(case_depart, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	case_evaluee = pygame.image.load("case_rouge.png")
	case_evaluee = case_evaluee.convert()
	case_evaluee = pygame.transform.scale(case_evaluee, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	case_non_evaluee = pygame.image.load("case_verte.png")
	case_non_evaluee = case_non_evaluee.convert()
	case_non_evaluee = pygame.transform.scale(case_non_evaluee, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	case_arrivee = pygame.image.load("case_orange.png")
	case_arrivee = case_arrivee.convert()
	case_arrivee = pygame.transform.scale(case_arrivee, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	case_mur = pygame.image.load("case_noire.png")
	case_mur = case_mur.convert()
	case_mur = pygame.transform.scale(case_mur, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	case_vide = pygame.image.load("case_grise.png")
	case_vide = case_vide.convert()
	case_vide = pygame.transform.scale(case_vide, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	case_chemin = pygame.image.load("case_cyan.png")
	case_chemin = case_chemin.convert()
	case_chemin = pygame.transform.scale(case_chemin, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	case_current = pygame.image.load("case_rose.png")
	case_current = case_current.convert()
	case_current = pygame.transform.scale(case_current, (int(LARGEUR/colonnes), int(HAUTEUR/lignes)))

	screen.fill(BLACK)

	#On affiche le tableau initialisé
	for i in range(len(tableau_initialise)):
			for j in range(len(tableau_initialise[0])):
				if tableau_initialise[i][j].type == "case_vide":
					screen.blit(case_vide, tableau_rect[i][j])

				if tableau_initialise[i][j].type == "case_mur":
					screen.blit(case_mur, tableau_rect[i][j])

				if tableau_initialise[i][j].type == "case_depart":
					screen.blit(case_depart, tableau_rect[i][j])
					#screen.blit(font1.render("A", False, (0, 0, 0)), (j*taille_case+(1/2)*taille_case, i*taille_case+(2/3)*taille_case))

				if tableau_initialise[i][j].type == "case_arrivee":
					screen.blit(case_arrivee, tableau_rect[i][j])
					#screen.blit(font1.render("B", False, (0, 0, 0)), (j*taille_case+(1/2)*taille_case, i*taille_case+(2/3)*taille_case))

	pygame.display.update()

	while True:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					
					while not(fin):

						#Identification de la case de départ et de la case d'arrivée
						if not(debut):
							for i in range(len(tableau_initialise)):
								for j in range(len(tableau_initialise[0])):
									if tableau_initialise[i][j].type == "case_depart":
										case_depart_case = tableau_initialise[i][j]
										cases_a_evaluer.append(case_depart_case)
									if tableau_initialise[i][j].type == "case_arrivee":
										case_arrivee_case = tableau_initialise[i][j]
							debut = True

						if not(chemin_trouve or fin):
							if (len(cases_a_evaluer) == 0):
								print("Impossible situation")
								fin = True

							else:
							
								current = lowest_f_cost_case(cases_a_evaluer)
								del cases_a_evaluer[lowest_f_cost_case_index(cases_a_evaluer)]
								cases_evaluees.append(current)	
								if current.type != "case_depart" and current.type != "case_arrivee":
									current.type = "case_current"

								if current.type == "case_arrivee":
									chemin_trouve = True
									determiner_chemin(tableau_initialise)

								if not(chemin_trouve):

									for i in (-1, 0, 1):
										for j in (-1, 0, 1):
											if not(i == 0 and j == 0) and current.x + i < lignes and current.y + j < colonnes and current.x + i >= 0 and current.y + j >= 0:
												tableau_initialise[current.x+i][current.y+j].g = calcul_g(tableau_initialise[current.x+i][current.y+j], current)
												tableau_initialise[current.x+i][current.y+j].h = calcul_h(tableau_initialise[current.x+i][current.y+j], case_arrivee_case)
												tableau_initialise[current.x+i][current.y+j].f = calcul_f(tableau_initialise[current.x+i][current.y+j])
												if tableau_initialise[current.x+i][current.y+j].type == "case_vide":
													cases_a_evaluer.append(tableau_initialise[current.x+i][current.y+j])
													tableau_initialise[current.x+i][current.y+j].type = "case_non_evaluee"
												if tableau_initialise[current.x+i][current.y+j].type == "case_arrivee":
													afficher_valeur = True
													cases_a_evaluer.append(tableau_initialise[current.x+i][current.y+j])
												

								for i in range(len(tableau_initialise)):
									for j in range(len(tableau_initialise[0])):

										if tableau_initialise[i][j].type == "case_vide":
											screen.blit(case_vide, tableau_rect[i][j])

										if tableau_initialise[i][j].type == "case_mur":
											screen.blit(case_mur, tableau_rect[i][j])

										if tableau_initialise[i][j].type == "case_depart":
											screen.blit(case_depart, tableau_rect[i][j])
											"""screen.blit(font1.render("A", False, (0, 0, 0)), (j*taille_case+(1/2)*taille_case, i*taille_case+(2/3)*taille_case))"""

										if tableau_initialise[i][j].type == "case_arrivee":
											screen.blit(case_arrivee, tableau_rect[i][j])
											"""if afficher_valeur:
												screen.blit(font1.render(str(tableau_initialise[i][j].f), False, (0, 0, 0)), (j*taille_case+(1/3)*taille_case, i*taille_case+(2/3)*taille_case))
												screen.blit(font2.render(str(tableau_initialise[i][j].g), False, (0, 0, 0)), (j*taille_case + (1/8)*taille_case, i*taille_case + (1/8)*taille_case))
												screen.blit(font2.render(str(tableau_initialise[i][j].h), False, (0, 0, 0)), (j*taille_case + (5/8)*taille_case, i*taille_case + (1/8)*taille_case))
											else:
												screen.blit(font1.render("B", False, (0, 0, 0)), (j*taille_case+(1/2)*taille_case, i*taille_case+(2/3)*taille_case))"""
											
										if tableau_initialise[i][j].type == "case_evaluee":
											screen.blit(case_evaluee, tableau_rect[i][j])
											"""screen.blit(font1.render(str(tableau_initialise[i][j].f), False, (0, 0, 0)), (j*taille_case+(1/3)*taille_case, i*taille_case+(2/3)*taille_case))
											screen.blit(font2.render(str(tableau_initialise[i][j].g), False, (0, 0, 0)), (j*taille_case + (1/8)*taille_case, i*taille_case + (1/8)*taille_case))
											screen.blit(font2.render(str(tableau_initialise[i][j].h), False, (0, 0, 0)), (j*taille_case + (5/8)*taille_case, i*taille_case + (1/8)*taille_case))"""

										if tableau_initialise[i][j].type == "case_non_evaluee":
											screen.blit(case_non_evaluee, tableau_rect[i][j])
											"""screen.blit(font1.render(str(tableau_initialise[i][j].f), False, (0, 0, 0)), (j*taille_case+(1/3)*taille_case, i*taille_case+(2/3)*taille_case))
											screen.blit(font2.render(str(tableau_initialise[i][j].g), False, (0, 0, 0)), (j*taille_case + (1/8)*taille_case, i*taille_case + (1/8)*taille_case))
											screen.blit(font2.render(str(tableau_initialise[i][j].h), False, (0, 0, 0)), (j*taille_case + (5/8)*taille_case, i*taille_case + (1/8)*taille_case))"""

										if tableau_initialise[i][j].type == "case_current":
											screen.blit(case_current, tableau_rect[i][j])
											"""screen.blit(font1.render(str(tableau_initialise[i][j].f), False, (0, 0, 0)), (j*taille_case+(1/3)*taille_case, i*taille_case+(2/3)*taille_case))
											screen.blit(font2.render(str(tableau_initialise[i][j].g), False, (0, 0, 0)), (j*taille_case + (1/8)*taille_case, i*taille_case + (1/8)*taille_case))
											screen.blit(font2.render(str(tableau_initialise[i][j].h), False, (0, 0, 0)), (j*taille_case + (5/8)*taille_case, i*taille_case + (1/8)*taille_case))"""

								if current.type != "case_depart" and current.type != "case_arrivee":
									current.type = "case_evaluee" 

						else:
							fin = True				
							for i in range(len(tableau_initialise)):
								for j in range(len(tableau_initialise[0])):
									if tableau_initialise[i][j].type == "case_depart" or tableau_initialise[i][j].type == "case_arrivee":
											tableau_initialise[i][j].type = "case_chemin"
									if tableau_initialise[i][j].type == "case_chemin":
										screen.blit(case_chemin, tableau_rect[i][j])
										"""screen.blit(font1.render(str(tableau_initialise[i][j].f), False, (0, 0, 0)), (j*taille_case+(1/3)*taille_case, i*taille_case+(2/3)*taille_case))
										screen.blit(font2.render(str(tableau_initialise[i][j].g), False, (0, 0, 0)), (j*taille_case + (1/8)*taille_case, i*taille_case + (1/8)*taille_case))
										screen.blit(font2.render(str(tableau_initialise[i][j].h), False, (0, 0, 0)), (j*taille_case + (5/8)*taille_case, i*taille_case + (1/8)*taille_case))"""

						pygame.time.wait(50)

						pygame.display.update()

def initialiser_tableau(tableau):
	"""Fonction permettant d'initialiser un tableau pour l'algorithme à partir d'un tableau"""

	#Création du tableau initialisé
	tableau_initialise = [tableau[0][:] for i in range(len(tableau))]
	for i in range(len(tableau_initialise)):
		for j in range(len(tableau_initialise[0])):
			tableau_initialise[i][j] = Case()

	#Affectation des valeurs
	for i in range(len(tableau_initialise)):
		for j in range(len(tableau_initialise[0])):
			if tableau[i][j] == 0:
				tableau_initialise[i][j].type = "case_vide"

			if tableau[i][j] == 1:
				tableau_initialise[i][j].type = "case_mur"

			if tableau[i][j] == 2:
				tableau_initialise[i][j].type = "case_depart"

			if tableau[i][j] == 3:
				tableau_initialise[i][j].type = "case_arrivee"

			tableau_initialise[i][j].x = i
			tableau_initialise[i][j].y = j

	return tableau_initialise

def lowest_f_cost_case(cases_a_evaluer):
	f_cost_min_nodes = []
	f_cost_min_node = cases_a_evaluer[0]
	f_cost_min = cases_a_evaluer[0].f
	if len(cases_a_evaluer) > 1:
		for i in range(len(cases_a_evaluer)):
			if cases_a_evaluer[i].f < f_cost_min:
				f_cost_min = cases_a_evaluer[i].f

		for i in range(len(cases_a_evaluer)):
			if cases_a_evaluer[i].f == f_cost_min:
				f_cost_min_nodes.append(cases_a_evaluer[i])

		h_cost_min = f_cost_min_nodes[0].h
		f_cost_min_node = f_cost_min_nodes[0]

		for i in range(len(f_cost_min_nodes)):
			if f_cost_min_nodes[i].h < h_cost_min:
				h_cost_min = f_cost_min_nodes[i].h
				f_cost_min_node = f_cost_min_nodes[i]

	return f_cost_min_node

def lowest_f_cost_case_index(cases_a_evaluer):
	index = 0
	case = lowest_f_cost_case(cases_a_evaluer)

	for i in range(len(cases_a_evaluer)):
		if cases_a_evaluer[i].x == case.x and cases_a_evaluer[i].y == case.y:
			index = i

	return index

def calcul_g(case_evaluee, case_mere):
	if case_mere.type == "case_depart":
		if case_evaluee.x == case_mere.x or case_evaluee.y == case_mere.y:
			g_cost = 10
		else:
			g_cost = 14
	elif (case_evaluee.x == case_mere.x or case_evaluee.y == case_mere.y) and (case_mere.g + 10 < case_evaluee.g or case_evaluee.type == "case_vide" or case_evaluee.type == "case_arrivee"):
		g_cost = case_mere.g + 10
	elif not(case_evaluee.x == case_mere.x or case_evaluee.y == case_mere.y) and (case_mere.g + 14 < case_evaluee.g or case_evaluee.type == "case_vide" or case_evaluee.type == "case_arrivee"):
		g_cost = case_mere.g + 14
	else:
		g_cost = case_evaluee.g
	return g_cost

def calcul_h(case_evaluee, case_arrivee):
	if case_evaluee.x == case_arrivee.x:
		h_cost = fabs(case_evaluee.y-case_arrivee.y)*10

	if case_evaluee.y == case_arrivee.y:
		h_cost = fabs(case_evaluee.x-case_arrivee.x)*10

	else:
		h_cost = min(fabs(case_evaluee.x - case_arrivee.x),fabs(case_evaluee.y-case_arrivee.y))*14 + (fabs(case_evaluee.x - case_arrivee.x)-min(fabs(case_evaluee.x - case_arrivee.x),fabs(case_evaluee.y-case_arrivee.y)))*10 + (fabs(case_evaluee.y - case_arrivee.y)-min(fabs(case_evaluee.x - case_arrivee.x),fabs(case_evaluee.y-case_arrivee.y)))*10
	return int(h_cost)

def calcul_f(current):
	return current.g + current.h

def lowest_f_cost_case_chemin(cases_a_evaluer):
	f_cost_min_nodes = []
	f_cost_min_node = cases_a_evaluer[0]
	f_cost_min = cases_a_evaluer[0].f
	if len(cases_a_evaluer) > 1:
		for i in range(len(cases_a_evaluer)):
			if cases_a_evaluer[i].f < f_cost_min:
				f_cost_min = cases_a_evaluer[i].f

		for i in range(len(cases_a_evaluer)):
			if cases_a_evaluer[i].f == f_cost_min:
				f_cost_min_nodes.append(cases_a_evaluer[i])

		g_cost_min = f_cost_min_nodes[0].g
		f_cost_min_node = f_cost_min_nodes[0]

		for i in range(len(f_cost_min_nodes)):
			if f_cost_min_nodes[i].g < g_cost_min:
				g_cost_min = f_cost_min_nodes[i].g
				f_cost_min_node = f_cost_min_nodes[i]

	return f_cost_min_node

def determiner_chemin(tableau):
	current = tableau[0][0]
	voisins = []
	for i in range(len(tableau)):
		for j in range(len(tableau[0])):
			if tableau[i][j].type == "case_arrivee":
				current = tableau[i][j]

	while not(current.type == "case_depart"):
		for i in(-1,0,1):
			for j in (-1,0,1):
				if not(i == 0 and j == 0) and current.x + i >= 0 and current.y + j >= 0 and current.x + i < len(tableau) and current.y + j < len(tableau[0]) and tableau[current.x+i][current.y+j].type == "case_evaluee" or tableau[current.x+i][current.y+j].type == "case_depart":
					if tableau[current.x+i][current.y+j].type == "case_depart":
						voisins = []
						voisins.append(tableau[current.x+i][current.y+j])
						break
					else:
						voisins.append(tableau[current.x+i][current.y+j])

		current = lowest_f_cost_case_chemin(voisins)
		if current.type != "case_depart":
			current.type = "case_chemin"
		voisins = []

def is_in(liste):
	booleen = False
	for i in range(len(liste)):
		if liste[i].x == 6 and liste[i].y == 2:
			booleen = True
	return booleen

main(tableau)