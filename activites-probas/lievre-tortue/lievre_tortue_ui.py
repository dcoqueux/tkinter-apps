from math import *
from random import *
from tkinter import *

import os
import time

def tracer_rectangles():

    global cases_plateau
    global num_tour
    
    global nb_total_simu
    global nb_victoires_tortue

    # redimensionnement du canvas
    canvas.config(width=(40+60*(nb_cases.get()+1)))

    # nettoyage préalable
    for case in cases_plateau :
        canvas.delete(case)

    # plateau de la tortue
    for i in range(0, nb_cases.get()):   
        cases_plateau.append(canvas.create_rectangle(80 + 60*i, 30, 140 + 60*i, 90))
    
    # plateau du lievre
    cases_plateau.append(canvas.create_rectangle(80 + 60*i, 120, 140 + 60*i, 180))

    num_tour = nb_cases.get()
    nb_total_simu = 0
    nb_victoires_tortue = 0
    freq_vict.set(0.0)
    proba_vict.set(round((5/6.0) ** nb_cases.get(), 5))


# procedure principale de l'application, lancee au clic du bouton "Jouer"
def simulation():

    # quand le lievre et la tortue sont sur la ligne de départ, le numéro du tour est 0
    # tant que le score n'est pas favorable au lievre, on incrémente le numéro de tour de 1
    # si le lievre gagne quelle que soit la progression de la tortue, le numéro du tour est 5
    global num_tour

    # variables symbolisant les images du lievre et de la tortue a manipuler sur le canvas
    global canvas_tortue
    global canvas_lapin

    global nb_simu
    global nb_total_simu
    global nb_victoires_tortue
    global freq_vict

    # on met à jour le nombre de tours nécessaires pour gagner
    num_tour_gagnant = nb_cases.get()

    if num_tour == num_tour_gagnant :
        # à l'appel précédent, l'epreuve avait un gagnant.
        # on reinitialise tout
        canvas.delete(canvas_tortue)
        canvas.delete(canvas_lapin)
        canvas_tortue = canvas.create_image(50, 60, image=tortue)
        canvas_lapin = canvas.create_image(50, 150, image=lapin)
        num_tour = 0

        # on redemarre aussitot
        print('')
        interface.after(100, simulation)
        return

    # lancer du dé
    score = randint(1, 6)
    if score == 6 :
        # VICTOIRE LIEVRE
        canvas.move(canvas_lapin, num_tour_gagnant * 60, 0)
        num_tour = num_tour_gagnant
        color_frame.config(bg='red')
    else :
        # VICTOIRE TORTUE
        canvas.move(canvas_tortue, 60, 0)
        num_tour += 1
        if num_tour == num_tour_gagnant :
            nb_victoires_tortue += 1
            color_frame.config(bg='green')

    time.sleep(0.200)
    print('score du dé = ' + str(score))

    # tant qu'il n'y a pas de gagnant, on relance le dé => rappel de la fonction
    if num_tour < num_tour_gagnant :
        interface.after(100, simulation)
    # sinon, on ne rappelle la fonction de simulation que si le nombre d'épreuves
    # à réaliser n'est pas épuisé
    else:
        # mise à jour des données de l'expérience
        nb_total_simu += 1
        print('Simulations : ' + str(nb_total_simu) 
            + ', victoires de la tortue : ' + str(nb_victoires_tortue))
        freq_vict.set(round(nb_victoires_tortue / nb_total_simu, 5))

        if nb_simu.get() > 1:
            nb_simu.set(nb_simu.get() - 1)
            interface.after(100, simulation)

cases_plateau = []

num_tour = 0
nb_victoires_tortue = 0
nb_total_simu = 0

interface = Tk()
interface.title("Jeu du lièvre et de la tortue")

### CANVAS

canvas = Canvas(interface, width=(40+6*60) , height=200, bg='white')
canvas.pack(padx=5, pady=5)

tortue = PhotoImage(file="tortue.png")
lapin = PhotoImage(file="lapin.png")

canvas_tortue = canvas.create_image(50, 60, image=tortue)
canvas_lapin = canvas.create_image(50, 150, image=lapin)

### FORMULAIRE

# Cadre "Nombre de simulations"

nb_simu = IntVar()
nb_simu.set(1)

simu_frame = Frame(interface, borderwidth=2, relief=GROOVE)
nb_simu_label = Label(simu_frame, text="Nombre de simulations ?")
nb_simu_entry = Entry(simu_frame, textvariable=nb_simu, width=10)
valid_form = Button(simu_frame, text="Jouer !", command=simulation)

simu_frame.pack(fill=X, padx=5, pady=5)
nb_simu_label.pack(side=LEFT, padx=5, pady=5)
nb_simu_entry.pack(side=LEFT, padx=5, pady=5)
valid_form.pack(pady=5)

# Cadre "Plateau de jeu"

nb_cases = IntVar()
nb_cases.set(5)

setup_frame = Frame(interface, borderwidth=2, relief=GROOVE)
nb_cases_label = Label(setup_frame, text="Nombre de cases pour la tortue ?")
nb_cases_entry = Entry(setup_frame, textvariable=nb_cases, width=10)
valid_setup = Button(setup_frame, text="Mettre à jour", command=tracer_rectangles)

setup_frame.pack(fill=X, padx=5, pady=5)
nb_cases_label.pack(side=LEFT, padx=5, pady=5)
nb_cases_entry.pack(side=LEFT, padx=5, pady=5)
valid_setup.pack(pady=5)

### VOYANT (VERT / ROUGE)

color_frame = Frame(interface, borderwidth=2, relief=GROOVE, height=20)
color_frame.pack(fill=X, padx=5)

### RESULTAT

# Fréquence de victoires dans les simulations
freq_vict = DoubleVar()

result_frame = Frame(interface, borderwidth=2, relief=GROOVE)
result_label = Label(result_frame, text="Fréquence de victoires de la tortue : ")
result_val = Label(result_frame, textvariable=freq_vict)

result_frame.pack(fill=X, padx=5, pady=5)
result_label.pack(side=LEFT, padx=7, pady=5)
result_val.pack(pady=5)

# Probabilité théorique de victoires
proba_vict = DoubleVar()

theoric_frame = Frame(interface, borderwidth=2, relief=GROOVE)
theoric_label = Label(theoric_frame, text="Probabilité théorique de victoires de la tortue : ")
theoric_val = Label(theoric_frame, textvariable=proba_vict)

theoric_frame.pack(fill=X, padx=5, pady=5)
theoric_label.pack(side=LEFT, padx=7, pady=5)
theoric_val.pack(pady=5)

### EXECUTION

tracer_rectangles()

try:
    interface.mainloop()
except Exception as e:
    print(str(e))

# Pour Windows
os.system('pause')
# Pour Linux
#raw_input()
