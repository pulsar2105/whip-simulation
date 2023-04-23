from tkinter import *
import random
import math

LARGEUR = 750
HAUTEUR = 750

bras = [0]
lenght_bras = [0] + [3 for i in range(250)]
angles_bras = [0]*len(lenght_bras)
step = 0.01

X = 0
Y = 0

def Clic(event):
    """ Gestion de l"événement Clic gauche """
    global X, Y

    # position du pointeur de la souris
    X = event.x
    Y = event.y
    #print("position du clic -> ", X, Y)

def d_prime(x, a, b):
    return (a*math.sin(x) - b*math.cos(x)) #/ math.sqrt((a-math.cos(x))**2 + (b-math.sin(x))**2)

def zero_approximately(a, b):
    sample = 5
    step_search = 1.28
    x = 0

    for s in range(sample):
        while d_prime(x, a, b) * d_prime(x + step_search, a, b) > 0 :
            x = x + step_search
        step_search = step_search / 10

    return x

def deplacement():
    """ Déplacement des bras robotiques """
    global bras, X, Y, LARGEUR, HAUTEUR

    #for i in range(1, len(bras)): # bras normal
    for i in range(len(bras)-1, 0, -1): # corde
    #t = list(range(1, len(bras))) # mouvement brownien
    #random.shuffle(t)
    #for i in t: # corde

        # on calcule le décalage des bras avant
        # l'offset de la base
        xoffset_before = LARGEUR/2
        yoffset_before = HAUTEUR/2
        for j in range(i):
            xoffset_before += math.cos(angles_bras[j]) * lenght_bras[j]
            yoffset_before += math.sin(angles_bras[j]) * lenght_bras[j]

        # on calcule le décalage des bras après
        xoffset_after = 0
        yoffset_after = 0
        for j in range(i+1, len(bras)):
            xoffset_after += math.cos(angles_bras[j]) * lenght_bras[j]
            yoffset_after += math.sin(angles_bras[j]) * lenght_bras[j]

        # on calcule a et b
        a = X - (xoffset_before + xoffset_after)
        b = Y - (yoffset_before + yoffset_after)

        x = zero_approximately(a, b)

        # pour éviter les bugs
        if b < 0:
            x += math.pi

        #print(a, b, x)
        angles_bras[i] = x

        Canevas.coords(bras[i], xoffset_before, yoffset_before, xoffset_before + math.cos(angles_bras[i]) * lenght_bras[i], yoffset_before + math.sin(angles_bras[i]) * lenght_bras[i])

    # mise à jour toutes les 16 ms (60FPS)
    Mafenetre.after(16, deplacement)


# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title("Simulation bras robot")

# Création d'un widget Canvas
Canevas = Canvas(Mafenetre, height = HAUTEUR, width = LARGEUR, bg='white')
Canevas.pack(padx=5,pady=5)

# création de la base (esthétique)
Canevas.create_oval(LARGEUR/2-5, HAUTEUR/2-5, LARGEUR/2+5, HAUTEUR/2+5, fill="green")

# création des bras
for i in range(1, len(lenght_bras)):
    bras.append(Canevas.create_line(LARGEUR/2, HAUTEUR/2, LARGEUR/2, HAUTEUR/2+lenght_bras[i-1]+lenght_bras[i], fill="black"))

# Création d'un widget Button (bouton Quitter)
BoutonQuitter = Button(Mafenetre, text = "Quitter", command = Mafenetre.destroy)
BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)

Canevas.bind("<Button-1>", Clic) # évévement clic gauche (press)
Canevas.bind("<B1-Motion>", Clic) # événement bouton gauche enfoncé (hold down)
deplacement()

Mafenetre.mainloop()