import timeit
# classe Noeud
class Noeud:
    def __init__(self, valeur, gauche = None, droit = None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit

        
    def __str__(self):
        return str(self.valeur)
    
# fonction hauteur
# la hauteur de la racine est ici de 1
# remplacer 0 par -1 si on souhaite une hauteur de 0 pour la racine
def hauteur(arbre):
    if arbre is None:
        return 0
    else:
        return 1 + max(hauteur(arbre.gauche), hauteur(arbre.droit))
    
#################### Code pour afficher l'arbre
import networkx as nx
import matplotlib.pyplot as plt

def repr_graph(arbre, size=(8,8), null_node=False):
    """
    size : tuple de 2 entiers. Si size est int -> (size, size)
    null_node : si True, trace les liaisons vers les sous-arbres vides
    """
    def parkour(arbre, noeuds, branches, labels, positions, profondeur, pos_courante, pos_parent, null_node):
        if arbre is not None:
            noeuds[0].append(pos_courante)
            positions[pos_courante] = (pos_courante, profondeur)
            profondeur -= 1
            labels[pos_courante] = str(arbre.valeur)
            branches[0].append((pos_courante, pos_parent))
            pos_gauche = pos_courante - 2**profondeur
            parkour(arbre.gauche, noeuds, branches, labels, positions, profondeur, pos_gauche, pos_courante, null_node)
            pos_droit = pos_courante + 2**profondeur
            parkour(arbre.droit, noeuds, branches, labels, positions, profondeur, pos_droit, pos_courante, null_node)
        elif null_node:
            noeuds[1].append(pos_courante)
            positions[pos_courante] = (pos_courante, profondeur)
            branches[1].append((pos_courante, pos_parent))
    
    
    if arbre is None:
        return
    
    branches = [[]]
    profondeur = hauteur(arbre)
    pos_courante = 2**profondeur
    noeuds = [[pos_courante]]
    positions = {pos_courante: (pos_courante, profondeur)} 
    labels = {pos_courante: str(arbre.valeur)}
    
    if null_node:
        branches.append([])
        noeuds.append([])
        
    profondeur -= 1
    parkour(arbre.gauche, noeuds, branches, labels, positions, profondeur, pos_courante - 2**profondeur, pos_courante, null_node)
    parkour(arbre.droit, noeuds, branches, labels, positions, profondeur, pos_courante + 2**profondeur, pos_courante, null_node) 

    mon_arbre = nx.Graph()
    
    if type(size) == int:
        size = (size, size)    
    plt.figure(figsize=size)
    
    nx.draw_networkx_nodes(mon_arbre, positions, nodelist=noeuds[0], node_color="white", node_size=1000, edgecolors="blue")
    nx.draw_networkx_edges(mon_arbre, positions, edgelist=branches[0], edge_color="black", width=2)
    nx.draw_networkx_labels(mon_arbre, positions, labels)

    if null_node:
        nx.draw_networkx_nodes(mon_arbre, positions, nodelist=noeuds[1], node_color="white", node_size=50, edgecolors="grey")
        nx.draw_networkx_edges(mon_arbre, positions, edgelist=branches[1], edge_color="grey", width=1)

    ax = plt.gca()
    ax.margins(0.1)
    plt.axis("off")
    plt.show()
    plt.close()

# nom de la lettre = Noeud('nom de la lettre', fils gauche, fils droit)
o = Noeud('o',None,None)
q = Noeud('q',None,None)
z = Noeud('z',None,None)
g = Noeud('g',z,q)
m = Noeud('m',g,o)
y = Noeud('y',None,None)
c = Noeud('c',None,None)
x = Noeud('x',None,None)
b = Noeud('b',None,None)
k = Noeud('k',c,y)
d = Noeud('d',b,x)
n = Noeud('n',d,k)

j = Noeud('j',None,None)
p = Noeud('p',None,None)
l = Noeud('l',None,None)
f = Noeud('f',None,None)
v = Noeud('v',None,None)
h = Noeud('h',None,None)
w = Noeud('w',p,j)
r = Noeud('r',l,None)
u = Noeud('u',f,None)
s = Noeud('s',h,v)
a = Noeud('a',r,w)
i = Noeud('i',s,u)
rg = Noeud('e',i,a) # racine gauche
rd= Noeud('t',n,m) # racine droite
arbre1 = Noeud('start',rg,rd) # racine de l'arbre
#repr_graph(arbre1,(15,5),True)

def decode_lettre(arbre,code):
    """Fonction qui traduit une lettre en morse en une lettre de l'alphabet et la retourne

    Args:
        arbre: arbre binaire
        code: code morse de la lettre

    Returns:
        str: lettre décodée
    """
    L = list(code) # chaque caractère de 'code' devient un élément individuel de L
    if L == []: # si 'code' et donc L est vide
        y = arbre.valeur # prend la valeur de l'arbre sur lequel la fonction est
        return y
    el = L.pop(0) # enlève la première valeur de la liste et la garde
    if el == '.':
        return(decode_lettre(arbre.gauche,L)) # va à gauche dans l'arbre binaire
    elif el == '-':
        return(decode_lettre(arbre.droit,L)) # va à droite dans l'arbre binaire

def encode_lettre(lettre,chemin,arbre):
    """Fonction qui prend une lettre de l'alphabet et la traduit en morse

    Args:
        lettre (str): La lettre qu'on veut traduire
        chemin (_type_): Le parcours dans l'arbre binaire qu'il faut faire pour trouver la lettre
        arbre: arbre binaire

    Returns:
        str: Le code morse qui représente la lettre demandée
    """
    if arbre is None: # si la cellulle qu'on regarde couramment n'a pas de feuilles, sortir de cette partie de la fonction récursive
        return "" # remonte de une cellule dans l'arbre
    elif arbre.valeur == lettre: # si la lettre de la cellulle sur laquelle on est correspond à ce qu'on cherche
        return chemin # retourne le parours nécessaire pour trouver la lettre dans l'arbre
    else:
        chg = encode_lettre(lettre, chemin + ".", arbre.gauche) # aller à gauche dans l'arbre et ajouter un '.' au parcours
        chd = encode_lettre(lettre, chemin + "-", arbre.droit) # aller à droite dans l'arbre et ajouter un '.' au parcours
    return chg + chd # soit chg soit chd sera égal à 0 donc c'est une méthode plus efficace d'afficher le résultat 

#print(encode_lettre('p',"",arbre1))

def encode_message(message,code,arbre):
    """Fonction qui prend une phrase normale et la traduit en code morse

    Args:
        message (str): le message qu'on veut traduire
        code (str): string vide où on mettra le message traduit
        arbre: arbre binaire

    Returns:
        str: phrase en code morse. Les lettres sont distinguées les une des autres par des '*' et les mots sont distingués les uns des autres par des "/"
    """
    phrase = list(message) # transforme le message en liste de caractères (espaces inclus)
    if phrase: # si il a des éléments dans la liste
        val = phrase.pop(0)
        val = val.casefold() # convertit tous les caractère en minuscule
        if val != " ": # si le premier élément de la liste n'est pas un espace
            tmp = encode_lettre(val,"",arbre) # prend ce premier élément et le traduit en morse
            if phrase and phrase[0] != " ": # verifie si le prochain élément n'est pas un espace
                tmp += "*" # ajoute un '*' pour distinguer deux lettres
            code = encode_message(phrase,code+tmp,arbre)
        else:
            code = encode_message(phrase,code+"/",arbre) # ajoute un '/' pour dire qu'il y a une espace entre deux mots
    return code
    
#print(encode_message("this is a test","",arbre1))

def decode_message(message_code,arbre):
    """Fonciton qui prend une phrase en code morse et la traduit

    Args:
        message_code (str): Le code en morse que l'on veut traduire
        arbre: arbre binaire

    Returns:
        str: phrase traduite
    """
    code = ""
    a = list(message_code.split("/")) # sépare chaque mot comme un élément de la lsite
    b = []
    for i in range(len(a)):
        b.append(list(a[i].split("*"))) # ajoute à la nouvelle liste chaque lettre comme élément individuel
    if b == []:
        return code
    else:
        for i in range(len(b)):
            for j in range(len(b[i])):
                lettre = b[i].pop(0)
                code += decode_lettre(arbre, lettre)
            code += " "
    return code

#
# decode_message("-*....*..*.../..*.../.-/-*.*...*-",arbre1)



# ------------------------------------
#Encodage à l'aide d'un dictionnaire et non d'un arbre

def dictionnaire(arbre,chemin,dico):
    if arbre is not None:
        if arbre.valeur != "":
            dico[arbre.valeur] = chemin
        dictionnaire(arbre.gauche,chemin + "°",dico)
        dictionnaire(arbre.droit,chemin + "-",dico)
    return dico

dico_morse = dictionnaire(arbre1,'',{})
#print(dico_morse)

def decode_lettre_dico(code, dico):
    """Fonction qui traduit une lettre en morse en une lettre de l'alphabet et la retourne

    Args:
        code: code morse de la lettre
        dico: dictionnaire associant le code morse à sa lettre

    Returns:
        str: lettre décodée
    """
    for cle, val in dico.items(): #pour toutes cles et leurs valeurs dans le dictionnaire
        if code == val: #on teste si le code morse renseigné correspond a un code existant dans les valuers du dictionnaire  
            return cle #si oui on renvoie la cle de ce code, qui est la lettre qui lui correspond
    return

#print(decode_lettre_dico("°°°", dico_morse))

def encode_lettre_dico(lettre, dico):
    """Fonction qui prend une lettre de l'alphabet et la traduit en morse

    Args:
        lettre (str): La lettre qu'on veut traduire
        dico: dictionnaire associant le code morse à sa lettre
        
    Returns:
        str: Le code morse qui représente la lettre demandée
    """
    for cle, val in dico.items(): #pour toutes cles et leurs valeurs dans le dictionnaire
        if lettre == cle: #on teste si la lettre renseigné correspond a une lettre existante dans les cles du dictionnaire
            return val #si oui on renvoie la valeur de cette lettre, qui est le code morse qui lui correspond
    return

#print(encode_lettre_dico("s", dico_morse))

def encode_message_dico(message, dico):
    """Fonction qui prend une phrase normale et la traduit en code morse

    Args:
        message (str): le message qu'on veut traduire
        dico: dictionnaire associant le code morse à sa lettre

    Returns:
        str: phrase en code morse. Les lettres sont distinguées les une des autres par des '*' et les mots sont distingués les uns des autres par des "/"
    """
    phrase = list(message) #phrase est une liste de toute les lettres constituant le message
    code = ""
    for i in range(len(phrase)): #pour la taille de caracteres de la phrase
        lettre = phrase.pop(0) #lettre prend la premiere lettre de la phrase et l'enleve de la liste "phrase"
        lettre = lettre.casefold() #on ignore si la lettre et majuscule ou minuscule
        if lettre != " ": #si il s'agit bien d'une lettre et non d'un espace
            code += encode_lettre_dico(lettre, dico) #on ajoute le code de la lettre a notre code finale
            if phrase and phrase[0] != " ": #apres la derniere lettre d'un mot (qui n'est pas le dernier mot du message)
                code += "*" #on ajoute "*" pour separer les codes morse d'une lettre et de la suivante
        else: #si on a un espace
            code += "/" #on ajoute "/" pour separer les codes morse d'un mot et du suivant
    return code #on renvoie le code morse correspondant au message renseigné

#print(encode_message_dico("Ceci est un test pour tester", dico_morse))  


def decode_message_dico(message_code, dico):
    """Fonction qui prend une phrase en code morse et la traduit

    Args:
        message_code (str): Le code en morse que l'on veut traduire
        dico: dictionnaire associant le code morse à sa lettre

    Returns:
        str: phrase traduite
    """
    message = ""
    a = list(message_code.split("/")) #a est une liste de chaque code morse d'un mot du message_code
    b = []
    for i in range(len(a)):
        b.append(list(a[i].split("*"))) #b devient une liste de liste de chaque code morse d'une lettre du message_code
    if b == []: #si aucun message de code morse n'est renseigné
        return message
    else: #si on a bien un message
        for i in range(len(b)): #on parcours chaque mots codé en morse
            for j in range(len(b[i])): # on parcours chaque lettre de chaque mot codé en morse
                c = b[i].pop(0) #c admet le code morse de la premiere lettre, en l'enlevant de la liste b
                message += decode_lettre_dico(c, dico) #on ajoute au message finale la lettre du code c 
            message += " " #on met un espace entre chaque mot décodé
    return message #on renvoie le message correspondant au code morse renseigné

#print(decode_message_dico("-°-°*°*-°-°*°°/°*°°°*-/°°-*-°/-*°*°°°*-/°--°*---*°°-*°-°/-*°*°°°*-*°*°-°", dico_morse))



# ------------------------------------
# interface utilisateur qui permet d'accéder à toutes les commandes
import time

def interface():
    print("""--------------------------------------------------------------------------------------------------------------------
Bonjour! Ce programme encode et décode le morse. Il y a plusieurs commandes qui peuvent être faites.""")
    time.sleep(1)
    print("Voulez vous décoder ou encoder? Ecrivez 'exit' pour quitter le programme.")
    fromage = input(">>> ")
    fromage = fromage.casefold() #convertit en minuscule
    if fromage == "decoder" or fromage == "décoder":
        time.sleep(1)
        print("Voulez vous décoder un mot ou une lettre? Ecrivez annuler pour retourner au menu principal.")
        gruyere = input(">>> ")
        gruyere = gruyere.casefold() #convertit en minuscule
        if gruyere == "mot":
            time.sleep(1)
            print("Quel message voulez vous décoder?")
            time.sleep(1)
            print("""NOTE: Impulsions courtes = '.'
Impulsions longues = '-'
Espaces entre lettres = '*'
Espaces entre mots = '/'""")
            message = input(">>> ")
            print("Le message traduit est:",decode_message(message,arbre1))
            time.sleep(1)
            return interface()
        elif gruyere == "lettre":
            time.sleep(1)
            print("Quel lettre voulez vous décoder?")
            time.sleep(1)
            print("""NOTE: Impulsions courtes = '.'
Impulsions longues = '-'""")
            message = input(">>> ")
            print("La lettre traduite est:",decode_lettre(message,arbre1))
            time.sleep(1)
            return interface()
        elif gruyere == "annuler":
            return interface()
    elif fromage == "encoder":
        time.sleep(1)
        print("Voulez vous encoder un mot ou une lettre? Ecrivez annuler pour retourner au menu principal.")
        gruyere = input(">>> ")
        gruyere = gruyere.casefold()
        if gruyere == "mot":
            time.sleep(1)
            print("Quel message voulez vous encoder?")
            message = input(">>> ")
            print("Le message traduit est:", encode_message(message,"",arbre1))
            time.sleep(1)
            return interface()
        elif gruyere == "lettre":
            time.sleep(1)
            print("Quel lettre voulez vous encoder?")
            message = input(">>> ")
            print("La lettre traduite est:", encode_lettre(message,"",arbre1))
            time.sleep(1)
            return interface()
        elif gruyere == "annuler":
            return interface()
    elif fromage == "exit":
        exit()
    

##### Test de mesures :
# avec un arbre :
##decoder :
print("--------------------------------")
print("AVEC UN ARBRE :")
print(">>>decoder une lettre :")
debut = timeit.default_timer()
a = decode_lettre(arbre1,'-.-.')
fin = timeit.default_timer()
total = fin-debut
print("Vous avez decodé la lettre", a,"en ",total, "secondes")

## encoder :
print(" ")
print(">>>encoder une lettre :")
debut = timeit.default_timer()
a = encode_lettre('p',"",arbre1)
fin = timeit.default_timer()
total = fin-debut
print("Vous avez encodé la lettre", a, "en ",total, "secondes")

## encoder message
print(" ")
print(">>>encoder un message :")
debut = timeit.default_timer()
a = encode_message("this is a test","",arbre1)
fin = timeit.default_timer()
total = fin-debut
print("Vous avez encodé le message", a, "en ",total, "secondes")

## decoder message
print(" ")
print(">>>decoder un message :")
debut = timeit.default_timer()
a = decode_message("-*....*..*.../..*.../.-/-*.*...*-",arbre1)
fin = timeit.default_timer()
total = fin-debut
print("Vous avez decodé le message :", a, "en ",total, "secondes")


# AVEC DICTIONNAIRE :
##decoder :
print("--------------------------------")
print("AVEC UN DICTIONNAIRE :")
print(">>>decoder une lettre :")
debut = timeit.default_timer()
a = decode_lettre_dico("°°°", dico_morse)
fin = timeit.default_timer()
total = fin-debut
print("Vous avez decodé la lettre", a,"en ",total, "secondes")

## encoder :
print(" ")
print(">>>encoder une lettre :")
debut = timeit.default_timer()
a = encode_lettre_dico("s", dico_morse)
fin = timeit.default_timer()
total = fin-debut
print("Vous avez encodé la lettre", a, "en ",total, "secondes")

## encoder message
print(" ")
print(">>>encoder un message :")
debut = timeit.default_timer()
a = encode_message_dico("Ceci est un test pour tester", dico_morse)
fin = timeit.default_timer()
total = fin-debut
print("Vous avez encodé le message", a, "en ",total, "secondes")

## decoder message
print(" ")
print(">>>decoder un message :")
debut = timeit.default_timer()
a = decode_message("-*....*..*.../..*.../.-/-*.*...*-",arbre1)
fin = timeit.default_timer()
total = fin-debut
print("Le decodage du message :", a, ", a été fait en ",total, "secondes")


interface()