from tkinter import *
import random
import math

LARGEUR = 750
HAUTEUR = 750

arm = [0]
lenght_arm = [0] + [3 for i in range(250)]
angles_arm = [0]*len(lenght_arm)
step = 0.01

X = 0
Y = 0

def clik(event):
    global X, Y

    # position of the mouse pointer
    X = event.x
    Y = event.y
    #print("mouse pointer -> ", X, Y)

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
    global arm, X, Y, LARGEUR, HAUTEUR

    #for i in range(1, len(arm)): # arm normal

    for i in range(len(arm)-1, 0, -1): # corde

    #t = list(range(1, len(arm))) # mouvement brownien
    #random.shuffle(t)
    #for i in t: # corde

        # the offset of the front arms is calculated
        # the offset of the base
        xoffset_before = LARGEUR/2
        yoffset_before = HAUTEUR/2
        for j in range(i):
            xoffset_before += math.cos(angles_arm[j]) * lenght_arm[j]
            yoffset_before += math.sin(angles_arm[j]) * lenght_arm[j]

        # the offset of the arms is calculated after
        xoffset_after = 0
        yoffset_after = 0
        for j in range(i+1, len(arm)):
            xoffset_after += math.cos(angles_arm[j]) * lenght_arm[j]
            yoffset_after += math.sin(angles_arm[j]) * lenght_arm[j]

        # on calcule a et b
        a = X - (xoffset_before + xoffset_after)
        b = Y - (yoffset_before + yoffset_after)

        x = zero_approximately(a, b)

        # to avoid bugs
        if b < 0:
            x += math.pi

        #print(a, b, x)
        angles_arm[i] = x

        Canevas.coords(arm[i], xoffset_before, yoffset_before, xoffset_before + math.cos(angles_arm[i]) * lenght_arm[i], yoffset_before + math.sin(angles_arm[i]) * lenght_arm[i])

    # update every 16 ms (60FPS)
    root.after(16, deplacement)


# creating the main window
root = Tk()
root.title("Simulation arm robot")

# creation of a Canvas widget
Canevas = Canvas(root, height = HAUTEUR, width = LARGEUR, bg='white')
Canevas.pack(padx=5,pady=5)

# creation of the base (aesthetics)
Canevas.create_oval(LARGEUR/2-5, HAUTEUR/2-5, LARGEUR/2+5, HAUTEUR/2+5, fill="green")

# creation of the arms
for i in range(1, len(lenght_arm)):
    arm.append(Canevas.create_line(LARGEUR/2, HAUTEUR/2, LARGEUR/2, HAUTEUR/2+lenght_arm[i-1]+lenght_arm[i], fill="black"))

# creation of a Button widget (Quit button)
BoutonQuitter = Button(root, text = "Quitter", command = root.destroy)
BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)

Canevas.bind("<Button-1>", clik) # event left clikk (press)
Canevas.bind("<B1-Motion>", clik) # event left button down (hold down)
deplacement()

root.mainloop()