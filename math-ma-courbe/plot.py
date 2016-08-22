from math import *
from tkinter import *
from PIL import Image, ImageTk

import os

class PlotFrame(Frame):

    """
        Interface graphique pour afficher des courbes via Tkinter.

        *-------------------------------------------------------*
        |*-----------------------------* *---------------------*|
        ||         Bouton Scale        | | Fonction a afficher ||
        |*-----------------------------* | Derivee de fonction ||
        |*-----------------------------* |                     ||
        ||                             | | x_min, x_max, y_amp ||
        ||                             | *---------------------*|
        ||                             | *---------------------*|
        ||            Courbe           | |      Position x     ||
        ||                             | |      Position y     ||
        ||                             | |     Derivee f'(x)   ||
        ||                             | |                     ||
        |*-----------------------------* *---------------------*|
        *-------------------------------------------------------*
    """

    def __init__(self, fenetre, **kwargs):
        """
            Initialisation :
                - des variables utiles a toute l'interface a tout instant dans son utilisation
                - des frames encapsulant des widgets coherents
                - des widgets
        """

        # dimensions du canvas
        self.largeur = 1000
        self.hauteur = 600

        # ref du canvas courbe et positions de la courbe
        self.courbe = None
        self.courbe_points = []

        # autres references du canvas
        self.canvas_legende = None
        self.axe_ordonnee = None

        # preparation des images utiles aux differents canvas
        self.voiture = Image.open('./icones/voiture2.gif').convert('RGBA')

        self.signe = None
        self.plus = ImageTk.PhotoImage(Image.open('./icones/plus.png').convert('RGBA'))
        self.moins = ImageTk.PhotoImage(Image.open('./icones/moins.png').convert('RGBA'))

        self.variation = None
        self.croissant = ImageTk.PhotoImage(Image.open('./icones/croissant.png').convert('RGBA'))
        self.decroissant = ImageTk.PhotoImage(Image.open('./icones/decroissant.png').convert('RGBA'))

        # pointeur de l'item voiture du canvas
        self.tk_voiture = None

        # variable du bouton scale, position horizontale de la voiture
        self.x_pos = StringVar()

        # variables d'affichage
        self.x_valeur = StringVar()
        self.y_valeur = StringVar()
        self.der_valeur = StringVar()

        # variables d'entrees du formulaire
        self.user_fonc = StringVar()
        self.user_der_fonc = StringVar()

        self.x_min = StringVar()
        self.x_max = StringVar()
        self.y_amp = StringVar()

        # intervalle des valeurs reelles de x d'affichage de la courbe
        self.a = 0
        self.b = 0

        # echelle ordonnee reelle / hauteur du pixel (1 ecart vertical de pixels ==> yyyy unites reelles)
        self.y_factor = (self.hauteur - 50) / 2

        # rapport des echelles x / y 
        self.rapport = StringVar()


        ### Initialisation des frames principaux ###

        Frame.__init__(self, fenetre, width=self.largeur, height=self.hauteur+100, **kwargs)
        self.pack(fill=BOTH)

        self.courbe_frame = Frame(self)
        self.courbe_frame.pack(side=LEFT)

        self.form_frame = Frame(self, width=350, borderwidth=2, relief=GROOVE)
        self.form_frame.pack(side=TOP, padx=10, pady=10)

        self.control_frame = Frame(self)
        self.control_frame.pack(side=TOP, expand=True)

        ### ###


        ### Creation du bouton radio ###

        self.x_scale = Scale(self.courbe_frame,
            orient=HORIZONTAL, length=self.largeur, to=self.largeur, showvalue=0, 
            command=self.evenement, variable=self.x_pos, state=DISABLED)
        self.x_scale.pack(padx=5, pady=5)

        ### ###


        # creation du canvas : axe des abscisses fixes ###

        self.canvas = Canvas(self.courbe_frame, width=self.largeur, height=self.hauteur, bg='white')
        self.canvas.pack(padx=5, pady=5)

        self.center = self.hauteur//2
        axe_abscisse = self.canvas.create_line(0, self.center, self.largeur, self.center, fill='black')

        ### ###


        ### Partie formulaire ###

        Label(self.form_frame, text="Fonction a afficher f(x) :").pack(padx=10)

        self.user_fonc_entry = Entry(self.form_frame, textvariable=self.user_fonc, width=30)
        self.user_fonc_entry.pack(padx=10)

        Label(self.form_frame, text="Derivee de la fonction f'(x):").pack()

        self.user_der_fonc_entry = Entry(self.form_frame, textvariable=self.user_der_fonc, width=30)
        self.user_der_fonc_entry.pack(padx=10)

        Label(self.form_frame, text="x min :").pack(padx=10)

        self.x_min_entry = Entry(self.form_frame, textvariable=self.x_min, width=30)
        self.x_min_entry.pack(padx=10)

        Label(self.form_frame, text="x max :").pack(padx=10)

        self.x_max_entry = Entry(self.form_frame, textvariable=self.x_max, width=30)
        self.x_max_entry.pack(padx=10)

        Label(self.form_frame, text="y amplitude :").pack(padx=10)

        self.y_amp_entry = Entry(self.form_frame, textvariable=self.y_amp, width=30)
        self.y_amp_entry.pack(padx=10)

        self.valid_form = Button(self.form_frame, text="Dessiner", command=self.draw)
        self.valid_form.pack(padx=10, pady=10)

        ### ###


        ### Creation de labels d'affichage et de controle pour les positions x et y du curseur-voiture ###

        self.x_frame = Frame(self.control_frame, borderwidth=2, relief=GROOVE)
        self.x_frame.pack(fill=X)
        self.label_x = Label(self.x_frame, text="x = ")
        self.label_x.pack(side=LEFT, padx=7, pady=2)
        self.x_display = Label(self.x_frame, textvariable=self.x_valeur)
        self.x_display.pack(pady=2)

        # Frame image y : f(x), valeur et canvas
        self.y_frame = Frame(self.control_frame, borderwidth=2, relief=GROOVE)
        self.y_frame.pack(fill=X)
        self.label_y = Label(self.y_frame, text="f(x) = ")
        self.label_y.pack(side=LEFT, padx=2, pady=2)
        self.y_display = Label(self.y_frame, textvariable=self.y_valeur)
        self.y_display.pack(pady=2)
        self.canvas_signe = Canvas(self.y_frame, width=26, height=26)
        self.canvas_signe.pack(side=BOTTOM)

        # Frame derivee f'(x), valeur et canvas
        self.der_frame = Frame(self.control_frame, borderwidth=2, relief=GROOVE)
        self.der_frame.pack(fill=X)
        self.label_der = Label(self.der_frame, text="f'(x) = ")
        self.label_der.pack(side=LEFT, padx=2, pady=2)
        self.der_display = Label(self.der_frame, textvariable=self.der_valeur)
        self.der_display.pack()
        self.canvas_variation = Canvas(self.der_frame, width=26, height=26)
        self.canvas_variation.pack(side=BOTTOM)

        self.rapport_frame = Frame(self.control_frame, borderwidth=2, relief=GROOVE)
        self.rapport_frame.pack(fill=X)
        self.label_rapport = Label(self.rapport_frame, text="Rapport echelles x / y :")
        self.label_rapport.pack(side=TOP, padx=2, pady=2)
        self.rapport_display = Label(self.rapport_frame, textvariable=self.rapport)
        self.rapport_display.pack(side=TOP)

        ### ###



    def draw(self):
        """
            Execute la fonction enregistree par l'utilisateur
            Sert pour le calcul des points de la courbe et la valeur de l'image
        """

        # Nettoyage
        self.canvas.delete(self.courbe)
        self.canvas.delete(self.canvas_legende)
        self.canvas.delete(self.axe_ordonnee)
        self.x_scale['state'] = 'active'
        self.courbe_points = []

        # Verification des entrees du formulaire
        if self.check_fonctions() is False or self.check_xy_entrees() is False:
            self.canvas_legende = self.canvas.create_text(100, 20, text="Erreur !")
            self.canvas.delete(self.tk_voiture)
            self.x_scale['state'] = 'disabled'
            return False

        # pour chaque coordonnee x du pixel, calcul de la coorodonnee y du pixel
        for x_pix in range(self.largeur):
            try:
                x_val, y_val, y_pix = self.compute_xy(x_pix)
            except (ZeroDivisionError, ValueError) as exc:
                continue
            else:
                self.courbe_points.append(x_pix)
                self.courbe_points.append(y_pix)

        self.courbe = self.canvas.create_line(self.courbe_points, fill='blue')

        # Tracage de l'axe des ordonnees si x = 0 est dans l'intervalle
        if self.a <= 0 and 0 <= self.b:
            x_zero = (self.largeur * self.a) / (self.a - self.b)
            self.axe_ordonnee = self.canvas.create_line(int(x_zero), 0, int(x_zero), self.hauteur, fill='black')

        ### calcul du rapport x / y
        echelle_x = (self.b - self.a) / self.largeur
        echelle_y = 1 / self.y_factor

        if echelle_x > echelle_y:
            coeff = echelle_y / echelle_x
            self.rapport.set("1 / " + format(coeff, '.3f'))
        else:
            coeff = echelle_x / echelle_y
            self.rapport.set(format(coeff, '.3f') + " / 1")

        self.evenement()


    def evenement(self, param=None):
        """
            Fonction de mouvement de la voiture lorsque le bouton Scale est manipule
        """

        if self.tk_voiture is not None :
            self.canvas.delete(self.tk_voiture)
        if self.signe is not None :
            self.canvas_signe.delete(self.signe)
        if self.variation is not None :
            self.canvas_variation.delete(self.variation)

        # recalcul des positions 
        x_pix = int(self.x_pos.get())
        try:
            x_val, y_val, y_pix = self.compute_xy(x_pix)
            derivee = self.fonction_der_exec(x_val)
        except (ZeroDivisionError, ValueError) as exc:
            self.x_valeur.set("En dehors du domaine de definition")
            self.y_valeur.set("Non défini")
            return False

        # affichage dans les labels de controle
        self.x_valeur.set(format(x_val, '.5f'))
        self.y_valeur.set(format(y_val, '.5f'))
        self.der_valeur.set(format(derivee, '.5f'))

        # recreation de l'image voiture a la bonne orientation
        # angle : arctan(rapport * tan(angle initial a rapport equilibre)) = arctan(rapport * derivee)
        # " * 180 / pi " pour transformer l'angle retournee en radians par atan() en degres
        angle = atan(derivee * eval(self.rapport.get())) * 180 / pi
        self.rot_voiture = ImageTk.PhotoImage(self.voiture.rotate(angle))

        # correction des coordonnees de l'image selon l'angle d'inclinaison
        y_corr = -9 * sqrt( 1 - (angle / 90)**2 )
        x_corr = (14 * sqrt( 1 - (angle / 90)**2 ) - 14) * (angle // abs(angle)) if angle != 0 else 0

        self.tk_voiture = self.canvas.create_image(x_pix + x_corr, y_pix + y_corr, image=self.rot_voiture)
        self.canvas.tag_lower(self.tk_voiture)

        # gestion du signe de l'image
        if y_val > 0 :
            self.signe = self.canvas_signe.create_image(14, 14, image=self.plus)
        elif y_val < 0 :
            self.signe = self.canvas_signe.create_image(14, 14, image=self.moins)

        # gestion de la variation locale
        if derivee > 0 :
            self.variation = self.canvas_variation.create_image(14, 14, image=self.croissant)
        elif derivee < 0 :
            self.variation = self.canvas_variation.create_image(14, 14, image=self.decroissant)



    def check_fonctions(self):
        """
            Evalue les expressions de fonctions entrees par l'utilisateur.
            Retourne un booleen.
        """

        try:
            self.fonction_exec(0)
            self.fonction_der_exec(0)
        except (ZeroDivisionError, ValueError, NameError) as m:
            return True
        except Exception as e:
            return False
        
        return True


    def check_xy_entrees(self):
        """
            Vérifie les champs input x_min, x_max, et y_amp
            Retourne les valeurs, ou des valeurs par defaut.
        """

        self.a = float(self.x_min.get()) if self.x_min.get() != '' else 0
        self.b = float(self.x_max.get()) if self.x_max.get() != '' else self.a + self.largeur / 100

        self.valid_xy_entries = False if self.a > self.b else True

        coeff = float(self.y_amp.get()) if self.y_amp.get() != '' else 1
        self.y_factor = (self.hauteur - 50) / (2 * coeff)

        return self.valid_xy_entries


    def fonction_exec(self, x):
        """
            Execute la fonction enregistree par l'utilisateur
            Sert pour le calcul des points de la courbe et la valeur de l'image
        """

        return eval(self.user_fonc.get())


    def fonction_der_exec(self, x):
        """
            Execute la derivee de la fonction de trace explicitement enregistree par l'utilisateur
            Sert pour le calcul des points de la courbe et la valeur de l'image
        """

        return eval(self.user_der_fonc.get())


    def compute_xy(self, x_init):
        """
            A partir d'une pixel initial, calcule les coordonnees reelles,
            et l'ordonnee du pixel.
            Retourne le tout dans un dictionnaire.
        """
        x_val = self.a + x_init * (self.b - self.a) / self.largeur
        y_val = self.fonction_exec(x_val)
        y_pix = int(self.center - y_val * self.y_factor)

        return (x_val, y_val, y_pix)


fenetre = Tk()
fenetre.title("Maths ma courbe !")

try:
    plot = PlotFrame(fenetre)
    plot.mainloop()
except Exception as e:
    print(str(e))

# Pour Windows
os.system('pause')
# Pour Linux
#raw_input()
