import math
import turtle

# =====================================================================
# ÉTAPE 1 : paramètres (modifiables)
# =====================================================================
ANGLE_INITIAL = 45          # 45° => arbre symétrique (c1 = c2)
PROFONDEUR_INITIALE = 10    # nombre de niveaux de carrés
COTE_TRONC = 100            # côté du carré de départ (en pixels)

COULEUR_FOND = "#101820"
COULEUR_TRONC = (110, 70, 35)     # marron (niveau 1)
COULEUR_FEUILLE = (60, 210, 70)   # vert (dernier niveau)


# =====================================================================
# ÉTAPE 2 : couleur selon le niveau (dégradé tronc -> feuilles)
# =====================================================================
def couleur_niveau(niveau, profondeur):
    """
    niveau = profondeur au tronc, puis diminue jusqu'à 1 aux feuilles.
    On mélange linéairement marron et vert :  t = 0 (tronc) ... 1 (feuilles).
    """
    t = (profondeur - niveau) / max(1, profondeur - 1)
    return tuple(int(a + t * (b - a))
                 for a, b in zip(COULEUR_TRONC, COULEUR_FEUILLE))


# =====================================================================
# ÉTAPE 3 : dessiner UN carré
# =====================================================================
def dessiner_carre(t, cote, couleur):
    """
    Dessine un carré rempli. La tortue part du coin bas-gauche, dirigée
    vers la droite. Elle tourne à gauche : le carré est donc à gauche
    de sa direction. À la fin, elle revient au point de départ, dans
    la même direction.
    """
    t.fillcolor(couleur)
    t.begin_fill()
    for _ in range(4):
        t.forward(cote)
        t.left(90)
    t.end_fill()


# =====================================================================
# ÉTAPE 4 : la fonction RÉCURSIVE
# =====================================================================
def arbre(t, cote, niveau, profondeur, angle_deg):
    """
    Dessine un carré, puis deux sous-arbres sur les cathètes du triangle.

    t          : la tortue (au coin bas-gauche du carré, direction = base)
    cote       : côté du carré courant
    niveau     : niveau restant (cas d'arrêt : niveau = 0)
    profondeur : niveau total (sert uniquement pour la couleur)
    angle_deg  : angle du triangle côté gauche
    """
    # --- cas d'arrêt : plus de niveau, ou carré trop petit pour être vu
    if niveau == 0 or cote < 1:
        return

    # --- 4a. on dessine le carré courant
    dessiner_carre(t, cote, couleur_niveau(niveau, profondeur))

    # --- 4b. longueurs des deux cathètes (trigonométrie)
    a = math.radians(angle_deg)
    c1 = cote * math.cos(a)        # cathète gauche
    c2 = cote * math.sin(a)        # cathète droite

    # --- 4c. on monte au coin haut-gauche du carré
    t.left(90)
    t.forward(cote)
    t.right(90)

    # --- 4d. sous-arbre GAUCHE : le carré est posé sur la cathète c1.
    #         La cathète part du coin haut-gauche avec un angle a.
    t.left(angle_deg)
    arbre(t, c1, niveau - 1, profondeur, angle_deg)

    # --- 4e. sous-arbre DROIT : on avance jusqu'au sommet du triangle
    #         (l'angle droit), puis on tourne de 90° pour suivre c2.
    t.forward(c1)
    t.right(90)
    arbre(t, c2, niveau - 1, profondeur, angle_deg)

    # --- 4f. retour exact au point de départ (on annule tout à l'envers)
    t.left(90)
    t.backward(c1)
    t.right(angle_deg)
    t.left(90)
    t.backward(cote)
    t.right(90)


# =====================================================================
# ÉTAPE 5 : fenêtre, état et dessin complet
# =====================================================================
def main():
    ecran = turtle.Screen()
    ecran.setup(width=900, height=700)
    ecran.bgcolor(COULEUR_FOND)
    ecran.colormode(255)       # pour utiliser des couleurs (r, g, b)
    ecran.tracer(0)            # pas d'animation : dessin instantané

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pencolor(COULEUR_FOND)   # contour de la couleur du fond = joints nets
    t.pensize(1)

    etat = {"angle": ANGLE_INITIAL, "profondeur": PROFONDEUR_INITIALE}

    def dessiner():
        t.clear()
        t.penup()
        t.goto(-COTE_TRONC / 2, -300)   # coin bas-gauche du tronc
        t.setheading(0)                 # direction : vers la droite
        t.pendown()
        arbre(t, COTE_TRONC, etat["profondeur"],
              etat["profondeur"], etat["angle"])
        ecran.title(f"Arbre de Pythagore - angle {etat['angle']}° "
                    f"- profondeur {etat['profondeur']}")
        ecran.update()

    # --- ÉTAPE 6 : commandes clavier
    def plus_angle():
        etat["angle"] = min(85, etat["angle"] + 5)
        dessiner()

    def moins_angle():
        etat["angle"] = max(5, etat["angle"] - 5)
        dessiner()

    def plus_profond():
        etat["profondeur"] = min(12, etat["profondeur"] + 1)
        dessiner()

    def moins_profond():
        etat["profondeur"] = max(1, etat["profondeur"] - 1)
        dessiner()

    ecran.onkeypress(plus_angle, "Right")
    ecran.onkeypress(moins_angle, "Left")
    ecran.onkeypress(plus_profond, "Up")
    ecran.onkeypress(moins_profond, "Down")
    ecran.listen()

    dessiner()
    ecran.mainloop()


if __name__ == "__main__":
    main()
