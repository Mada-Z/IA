import sys
import math
import time
import os

import stopit as stopit

class NodParcurgere:
#initializare datele necesare
    def __init__(self, date, x, y, insecte, gr_max, gr_c, par, cost, h): 

        self.date = date
        self.x = x
        self.y = y
        self.insecte = insecte
        self.g_max = gr_max
        self.g_c = gr_c
        self.par = par
        self.cost = cost
        self.h = h
        self.f = self.cost + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.par is not None:
            l.insert(0, nod.par)
            nod = nod.par
        return l

    def afisDrum(self, file, timp, nrNoduri = 0, nrMaximNoduri = 0, afisareDetalii = False):
        g = open(file, "a")
        l = self.obtineDrum()

        g.write("1) Broscuta se afla pe frunza initiala " + str(l[0]) + '\n')
        g.write("Greutate broscuta: " + str(l[0].g_c) + '\n')
        i = 2
        for nod in l:
            if nod.par is not None:
                g.write(str(i) + ") Broscuta a sarit de la " + str(nod.par) + " la " + str(nod) + '\n')
                g.write("Broscuta a mancat " + str(nod.insecte) + " insecte. Greutate broscuta: " + str(
                    nod.g_c) + '\n')
                i += 1

        g.write(str(i) + ") Broscuta a ajuns la mal in " + str(len(l)) + " sarituri.\n")

        if afisareDetalii:
            g.write('\n' + "Lungimea drumului: " + str(len(l)) + '\n')
            g.write("Costul drumului: " +  str(len(l)) + '\n')
            g.write("Numarul maxim de noduri existente la un moment dat in memorie: " + str(nrNoduri) + '\n')
            g.write("Numarul total de noduri calculate: " + str(nrMaximNoduri) + '\n')
        g.write("Time: " + str(timp))
        g.write("\n----------------\n\n")
        g.close()

        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.date:
                return True
            nodDrum = nodDrum.par

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.date)
        return sir

    def __str__(self):
        return (str(self.date) + "(" + str(self.x) + "," + str(self.y) + ")")

class Graph:
    def __init__(self, input, output):
        self.output = output

        f = open(input, "r")
        continut_fisier = f.read()
        f.close()

        date_fisier = continut_fisier.split('\n')
        self.raza = int(date_fisier[0])
        self.g = int(date_fisier[1])
        self.date_start = date_fisier[2]
        nod = date_fisier[3].split()
        self.start = (nod[0], int(nod[1]), int(nod[2]), int(nod[3]), int(nod[4]))
        self.noduri = []

        for i in range(4, len(date_fisier)):
            nod = date_fisier[i].split()
            self.noduri.append((nod[0], int(nod[1]), int(nod[2]), int(nod[3]), int(nod[4])))

    def testeaza_scop(self, x, y, g):
     # x-> coordonata pe axa Ox, y-> coordonata pe axa Oy, g -> greutatea curenta
        d = self.raza - math.sqrt(x ** 2 + y ** 2)
        if g / 3 >= d:
            return True
        return False

    def init_fin(self, x, y):
        #daca distanta pana la mal este 0 intoarce True, altfel intoarce False
        dist = self.raza - math.sqrt(x ** 2 + y ** 2)
        if dist == 0:
            return True
        return False

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica_banala"):
        listaSuccesori = []
        for idx in range(len(self.noduri)):
            dist = math.sqrt((nodCurent.x - self.noduri[idx][1]) ** 2 + (nodCurent.y - self.noduri[idx][2]) ** 2)
            if nodCurent.g_c / 3 < dist or nodCurent.g_c - 1 > self.noduri[idx][4]:
                continue
            else:
                for insecte in range(self.noduri[idx][3]+1):
                    if nodCurent.g_c - 1 + insecte > self.noduri[idx][4]:
                        break
                    euristica = self.calculeaza_h(self.noduri[idx][0], self.noduri[idx][1], self.noduri[idx][2], insecte + nodCurent.g_c - 1, tip_euristica )
                    nodNou = NodParcurgere(self.noduri[idx][0],  # date
                                           self.noduri[idx][1],  # x
                                           self.noduri[idx][2],  # y
                                           insecte,
                                           self.noduri[idx][4],  # gr_max
                                           insecte + nodCurent.g_c - 1,  # gr_c
                                           nodCurent,
                                           nodCurent.cost + 1,
                                           euristica)
                    if not nodCurent.contineInDrum(nodNou.date) and nodNou.g_c > 1:
                        listaSuccesori.append(nodNou)

        return listaSuccesori

    def verificaExistentaSolutie(self, g):
        #verifica daca greutatea cureanta este mai mare decat 1
        return g>1

    def calculeaza_h(self, date, x, y, g,  tip_euristica):
        if tip_euristica == "euristica_banala":
            return self.euristica_banala( x, y, g)
        else:
            raise Exception("Aceasta euristica NU este definita!")

    def euristica_banala(self, x, y, g):
        return 0 if self.testeaza_scop(x, y, g) else 1



    def fara_solutie(self, timp,algoritm):
        g = open(self.output, "a")
        g.write( algoritm + "\nNu exista solutii!\n")
        g.write("Timp: " + str(timp))
        g.write("\n----------------\n\n")
        g.close()

    def mal(self,timp,algoritm):
        g = open(self.output, "a")
        g.write(algoritm + "\nBroscuta se afla deja pe mal!\n")
        g.write("Timp: " + str(timp))
        g.write("\n----------------\n\n")
        g.close()


@stopit.threading_timeoutable(default="Functie oprita")
def a_star(gr, nrSolutiiCautate, tip_euristica):
    start = time.time()
    existaSolutii = False
    if not gr.verificaExistentaSolutie(gr.g):
        stop = time.time()
        timp = stop - start
        gr.fara_solutie(timp,"A*")
        return
    if gr.init_fin(gr.start[1], gr.start[2]):
        stop = time.time()
        timp = stop - start
        gr.mal(timp,"A*")
        return
    maxNoduri = 0
    nrTotalNoduri = 0
    c = [NodParcurgere(gr.start[0],
                       gr.start[1],
                       gr.start[2],
                       gr.start[3],
                       gr.start[4],
                       gr.g,
                       None,
                       0,
                       0)]

    while len(c) > 0:

        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent.x, nodCurent.y, nodCurent.g_c):
            existaSolutii = True
            stop = time.time()
            timp = stop - start
            g = open(gr.output, "a")
            g.write("Solutie A* (" + tip_euristica + ")\n\n")
            g.close()
            nodCurent.afisDrum(gr.output, timp,maxNoduri, nrTotalNoduri, True)
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        nrTotalNoduri += len(lSuccesori)
        maxNoduri = max(maxNoduri, len(lSuccesori))
        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)
    if existaSolutii == False:
        stop = time.time()
        timp = stop - start
        gr.fara_solutie(timp,"A*")

@stopit.threading_timeoutable(default="Functie oprita")
def uniform_cost(gr, nrSolutiiCautate=1):
    start = time.time()
    existaSolutii = False
    if not gr.verificaExistentaSolutie(gr.g):
        stop = time.time()
        timp = stop - start
        gr.fara_solutie(timp,"UCS")
        return
    if gr.init_fin(gr.start[1], gr.start[2]):
        stop = time.time()
        timp = stop - start
        gr.mal(timp,"UCS")
        return
    maxNoduri = 0
    nrTotalNoduri = 0
    c = [NodParcurgere(gr.start[0],
                       gr.start[1],
                       gr.start[2],
                       gr.start[3],
                       gr.start[4],
                       gr.g,
                       None,
                       0,
                       0)]

    while len(c) > 0:

        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent.x, nodCurent.y, nodCurent.g_c):
            existaSolutii = True
            stop = time.time()
            timp = stop - start
            g = open(gr.output, "a")
            g.write("Solutie UCS: \n\n")
            g.close()
            nodCurent.afisDrum(gr.output, timp,maxNoduri, nrTotalNoduri, True)
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        nrTotalNoduri += len(lSuccesori)
        maxNoduri = max(maxNoduri, len(lSuccesori))
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].cost > s.cost:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
    if existaSolutii == False:
        stop = time.time()
        timp = stop - start
        gr.fara_solutie(timp,"UCS")

    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
    nrTotalNoduri += len(lSuccesori)
    maxNoduri = max(maxNoduri, len(lSuccesori))

    minim = float("inf")
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, start, maxNoduri, nrTotalNoduri, tip_euristica)
        if rez == "gata":
            return nrSolutiiCautate, "gata"

        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim

def verif_input(fisier):
    f = open(fisier, "r")
    continut_fisier = f.read()
    f.close()

    date_fisier = continut_fisier.split('\n')

    if date_fisier[0].lstrip('+').isdigit() == False:
        return False

    if date_fisier[1].lstrip('+').isdigit() == False:
        return False

    nod = date_fisier[3].split()
    if date_fisier[2] != nod[0]:
        return False
    l = []
    for i in range(3, len(date_fisier)):
        nod = date_fisier[i].split()
        l.append(nod[0])
        if len(nod) != 5:
            return False
        if nod[1].lstrip('-+').isdigit() == False:
            return False
        if nod[2].lstrip('-+').isdigit() == False:
            return False
        if nod[3].lstrip('+').isdigit() == False:
                   return False
        if nod[4].lstrip('+').isdigit() == False:
                   return False

    if len(l) != len(set(l)):
        return False
    return True


# argumente input
folderInput = sys.argv[1]
folderOutput = sys.argv[2]
nrSolutiiCautate = int(sys.argv[3])
timeOut = float(sys.argv[4])
euristica = "euristica_banala"
# daca nu exista folderul Output
if not os.path.exists(folderOutput):
    os.mkdir(folderOutput)

for input in os.listdir(folderInput):
    output = "output_" + input
    f = open(folderOutput + '/' + output, "w")
    f.close()

    if verif_input(folderInput + '/' + input) == True:
        gr = Graph(folderInput + '/' + input, folderOutput + '/' + output)
        a_star(gr, nrSolutiiCautate, euristica, timeout = timeOut)
        uniform_cost(gr, nrSolutiiCautate, timeout = timeOut)
    else:
        f = open(folderOutput + '/' + output, "w")
        f.write("Formatul sau datele fisierului de intrare nu sunt corecte!")
        f.close()