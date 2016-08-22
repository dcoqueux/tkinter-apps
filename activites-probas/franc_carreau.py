from math import *
from random import *
from tkinter import *

import os
import time

## détermine si la coordonnée x ou y du centre de la piece
## est trop proche d'une rayure entre carreaux 
def touche_limite(x):
    global rayon
    proche_centaine = round(x / 100.0) * 100
    return (abs(x - proche_centaine) < rayon)


## procedure principale de l'application, lancee au clic du bouton "Jouer"
def simulation():

    global nb_simu
    global nb_total_simu
    global nb_victoires
    global freq_vict
    global rayon


    # tirage aléatoire uniforme des coordonnées réelles entre 0 et 400
    x = uniform(0, 400)
    y = uniform(0, 400)


    # message en console, et creation d'une piece pour le canvas
    print("x = " + format(x, '.2f') + ", y = " + format(y, '.2f'))
    piece = canvas.create_oval(
        round(x - rayon, 0), round(y - rayon, 0),
        round(x + rayon, 0), round(y + rayon, 0),
        fill='gold')


    # mise à jour des données de l'expérience
    if touche_limite(x) or touche_limite(y) :
        color_frame.config(bg='red')
    else :
        nb_victoires += 1
        color_frame.config(bg='green')

    nb_total_simu += 1
    print('Simulations : ' + str(nb_total_simu) + ', nombres de succes : ' + str(nb_victoires))
    print('')
    freq_vict.set(round(nb_victoires / nb_total_simu, 5))


    # la fonction demande a Python de la rappeler apres 300 millisecondes,
    # le temps d'envoyer un signal de terminaison a Tkinter pour mettre à jour le canvas
    if nb_simu.get() > 1:
        nb_simu.set(nb_simu.get() - 1)
        interface.after(300, simulation)

## variables globales
rayon = 10
nb_victoires = 0
nb_total_simu = 0

## interface graphique
interface = Tk()
interface.title("Jeu du franc carreau")

### CANVAS

taille = 400
canvas = Canvas(interface, width=taille, height=taille, bg='white')
canvas.pack(padx=5, pady=5)

# creation des lignes séparant les carreaux
for i in range(1, taille//100) : 
    canvas.create_line(100 * i, 0, 100 * i, taille)
    canvas.create_line(0, 100 * i, taille, 100 * i)

### ENCADRE FORMULAIRE (et widgets qui y appartiennent) 

# Pour que le programme Python de base puisse manipuler les entrées de l'interface
# Tkinter, il faut un type de variable "objet" spécifique (IntVar, DoubleVar, StringVar),
# et utiliser les fonctions set et get de l'objet pour modifier ou récupérer la valeur.
nb_simu = IntVar()
nb_simu.set(1)

form_frame = Frame(interface, borderwidth=2, relief=GROOVE)
nb_simu_label = Label(form_frame, text="Nombre de simulations ?")
nb_simu_entry = Entry(form_frame, textvariable=nb_simu, width=10)
valid_form = Button(form_frame, text="Jouer !", command=simulation)

form_frame.pack(fill=X, padx=5, pady=5)
nb_simu_label.pack(side=LEFT, padx=5)
nb_simu_entry.pack(side=LEFT, padx=5)
valid_form.pack(padx=10, pady=5)

### VOYANT (VERT / ROUGE)

color_frame = Frame(interface, borderwidth=2, relief=GROOVE, height=20)
color_frame.pack(fill=X, padx=5)

### ENCADRE RESULTAT (et widgets qui y appartiennent) 

freq_vict = DoubleVar()

result_frame = Frame(interface, borderwidth=2, relief=GROOVE)
result_label = Label(result_frame, text="Fréquence de lancers gagnants : ")
result_val = Label(result_frame, textvariable=freq_vict)

result_frame.pack(fill=X, padx=5, pady=5)
result_label.pack(side=LEFT, padx=7, pady=5)
result_val.pack(pady=5)

# une fois que tout a été mis en place (définition des procédures,
# et organisation des éléments de la fenetre graphique), on démarre le programme
try:
    interface.mainloop()
except Exception as e:
    print(str(e))

# Pour Windows
os.system('pause')
# Pour Linux
#raw_input()
