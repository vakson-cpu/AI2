from codecs import getwriter
from glob import glob
import math
import json
from pickle import FALSE
from tabnanny import check
from tkinter import W, Grid
from webbrowser import get
from xml.etree.ElementTree import PI
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import random
# Create your views here.
Gridara = ["_"]*11
DobreHor = ["_"]*11
DobreVer = ["_"]*11
DobreDDiag = ["_"]*11
DobreLDiag = ["_"]*11
InicijalnoStanje = 0
inicijalnoW = 0
for i in range(11):
    Gridara[i] = ["_"]*11
    DobreHor[i] = ["_"]*11
    DobreVer[i] = ["_"]*11
    DobreDDiag[i] = ["_"]*11
    DobreLDiag[i] = ["_"]*11


def FullBoard():
    k = False
    for i in range(1, 11):
        for j in range(1, 11):
            if Gridara[i][j] != "_":
                k = True
    if k == False:
        return True
    return False


def Ispis():
    ispis = ""
    for i in range(1, 11):
        ispis += "\n"
        for j in range(1, 11):
            ispis += " " + Gridara[i][j]
    print(ispis)

# Za Globalne koje cuvaju proslu promenljivu


class Allowed:
    def __init__(self, pom1, pom2):
        self.pom1 = pom1
        self.pom2 = pom2


P = Allowed(0, 0)
turn = False

# Provera Needed


def Provera(i, j, a, b):
    # print("Pom1:{0},Pom2:{1},zeljeno mesto:{2} {3}".format(a,b,i,j))
    if(Gridara[i][j] == "_" and ((i == a - 1 and j == b + 1) or (i == a - 1 and j == b - 1) or (i == a + 1 and j == b - 1) or (i == a + 1 and j == b + 1) or (a == i and b == j + 1) or (a == i and b == j - 1) or (a == i + 1 and b == j) or (a == i - 1 and b == j))):
        # print("Provera ok")
        return True
    return False


DaLi = False

P2 = Allowed(0, 0)


def InsertPosition(i, j, val, lastMove1, lastMove2):
    global DaLi
    if(Provera(i, j, lastMove1, lastMove2) == True):
        if Gridara[i][j] == "_":
            Gridara[i][j] = val
            DaLi = True
    else:
        print("BIO JE FALSE!!!")
        DaLi = False


def InsertDirect(i, j, val):
    if Gridara[i][j] == "_":
        Gridara[i][j] = val
    P.pom1 = i
    P.pom2 = j


def Kontejna(P1, P2, P3, P4, val1):
    if P1 == val1 and P2 == val1 and P3 == val1 and P4 == val1:
        return True
    return False


# Horizontala val1-color//Vraca nam 4 u horizontalu
def AddCheckedHors(i, j, val1):
    DobreHor[i][j] = val1
    DobreHor[i][j+1] = val1
    DobreHor[i][j+2] = val1
    DobreHor[i][j+3] = val1


def RemoveCheckedHors(i, j):
    DobreHor[i][j] = "_"
    DobreHor[i][j+1] = "_"
    DobreHor[i][j+2] = "_"
    DobreHor[i][j+3] = "_"


def HoriPom(i, j, val1):
    P1 = Gridara[i][j]
    P2 = Gridara[i][j+1]
    P3 = Gridara[i][j+2]
    P4 = Gridara[i][j+3]
    P5 = "_"
    if(j != 1):
        P5 = Gridara[i][j-1]
    else:
        P5 = None

    if(Kontejna(P1, P2, P3, P4, val1) == True):
        if j != 1:
            if P5 != None:
                if P5 == val1:
                    RemoveCheckedHors(i,j)
                    return False
                else:
                    if j+4 <= 10:
                        if Gridara[i][j+4] != "_":
                            pp = Gridara[i][j+4]
                            if pp == val1:
                                RemoveCheckedHors(i,j)
                                return False
                            AddCheckedHors(i, j, val1)
                            return True
                    AddCheckedHors(i, j, val1)
                    return True
            else:
                if j+4 <= 10:
                    if Gridara[i][j+4] != "_":
                        pp = Gridara[i][j+4]
                        if pp == val1:
                            RemoveCheckedHors(i,j)                            
                            return False
                AddCheckedHors(i, j, val1)
                return True
        else:
            if j+4 <= 10:
                if Gridara[i][j+4] != "_":
                    pp = Gridara[i][j+4]
                    if pp == val1:
                        RemoveCheckedHors(i,j)
                        return False
                    AddCheckedHors(i, j, val1)
                    return True
        AddCheckedHors(i, j, val1)
        return True
    return False


def Horizontala(i, j, val1):
    if j <= 7:
        if (Gridara[i][j] == val1 and Gridara[i][j+1] != "_" and Gridara[i][j+2] != "_" and Gridara[i][j+3] != "_"):
            return HoriPom(i, j, val1)
        else:
            return False
    return False
# Vertikala


def AddCheckersVert(i, j, val1):
    DobreVer[i][j] = val1
    DobreVer[i+1][j] = val1
    DobreVer[i+2][j] = val1
    DobreVer[i+3][j] = val1


def VertikalaPom(i, j, val1):
    P5 = None
    if i-1 >= 1:
        P5 = Gridara[i-1][j]
    else:
        P5 = None
    if(Kontejna(Gridara[i + 1][j], Gridara[i + 2][j], Gridara[i + 3][j], Gridara[i][j], val1) == True):
        if i-1 >= 1:
            if P5 == val1:
                return False
            if P5 == None:
                if i+4 <= 10:
                    if Gridara[i+4][j] > 0:
                        pp = Gridara[i+4][j]
                        if pp == val1:
                            return False
                    AddCheckersVert(i, j, val1)
                    return True
            else:
                if i+4 <= 10:
                    if Gridara[i+4][j] == val1:
                        return False
                AddCheckersVert(i, j, val1)
                return True
        else:
            if i+4 <= 10:
                if Gridara[i+4][j] == val1:
                    return False
            AddCheckersVert(i, j, val1)
            return True
    return False


def Vertikala(i, j, val1):
    if i <= 7:
        if(Gridara[i][j] == val1 and Gridara[i+1][j] != "_" and Gridara[i+2][j] != "_" and Gridara[i+3][j] != "_"):
            return VertikalaPom(i, j, val1)
        else:
            return False
    return False
# Desna Dijagonala


def AddCheckersDDijag(i, j, val1):
    DobreDDiag[i][j] = val1
    DobreDDiag[i-1][j+1] = val1
    DobreDDiag[i-2][j+2] = val1
    DobreDDiag[i-3][j+3] = val1
def RemoveCheckedDD(i, j):
    DobreDDiag[i][j] = "_"
    DobreDDiag[i-1][j+1] = "_"
    DobreDDiag[i-2][j+2] = "_"
    DobreDDiag[i-3][j+3] = "_"


def DDpom(i, j, val1):
    P5 = None
    if(i-4 >= 1 and j+4 <= 10):
        P5 = Gridara[i-4][j+4]
    if(Kontejna(Gridara[i-1][j+1], Gridara[i-2][j+2], Gridara[i-3][j+3], Gridara[i][j], val1) == True):
        if i != 4:
            if P5 != None:
                if P5 == val1:
                    return False
                if P5 != val1 and j > 1 and i < 10:
                    if Gridara[i+1][j-1] == val1:
                        RemoveCheckedDD(i,j)
                        return False
                    AddCheckersDDijag(i, j, val1)
                    return True
            else:
                if i+1 <= 10 and j-1 >= 1:
                    if Gridara[i+1][j-1] == val1:
                        RemoveCheckedDD(i,j)
                        return False
                AddCheckersDDijag(i, j, val1)
                return True
        else:
            if i+1 <= 10 and j-1 >= 1:
                if Gridara[i+1][j-1] == val1:
                    RemoveCheckedDD(i,j)
                    return False
                AddCheckersDDijag(i, j, val1)
                return True
        AddCheckersDDijag(i, j, val1)
        return True
    return False


def DijagonalaDesna(i, j, val1):
    if (j <= 7 and i >= 4):
        if(Gridara[i][j] == val1 and Gridara[i-1][j+1] != "_" and Gridara[i-2][j+2] != "_" and Gridara[i-3][j+3] != "_"):
            return DDpom(i, j, val1)
        else:
            return False
    return False
# Leva Dijagonala


def AddCheckersLDijag(i, j, val1):
    DobreLDiag[i][j] = val1
    DobreLDiag[i-1][j-1] = val1
    DobreLDiag[i-2][j-2] = val1
    DobreLDiag[i-3][j-3] = val1
    
def RemoveCheckedLD(i, j):
    DobreLDiag[i][j] = "_"
    DobreLDiag[i-1][j-1] = "_"
    DobreLDiag[i-2][j-2] = "_"
    DobreLDiag[i-3][j-3] = "_"


def LDpom(i, j, val1):
    P5 = None
    if(i-4 >= 1 and j-4 >= 1):
        P5 = Gridara[i-4][j-4]
    if(Kontejna(Gridara[i][j], Gridara[i-1][j-1], Gridara[i-2][j-2], Gridara[j-3][j-3], val1) == True):
        if(i != 4):
            if(P5 != "_"):
                if(P5 == val1):
                    return False
                if(i < 10 and j < 10):
                    if(Gridara[i+1][j+1] == val1):
                        RemoveCheckedLD(i,j)
                        return False
                    AddCheckersLDijag(i, j, val1)
                    return True
            else:
                if (i+1 <= 10 and j+1 <= 10):
                    if(Gridara[i+1][j+1] == val1):
                        RemoveCheckedLD(i,j)
                        return False
                    AddCheckersLDijag(i, j, val1)
                    return True
                AddCheckersLDijag(i, j, val1)
                return True
        else:
            if(i+1 <= 10 and j+1 <= 10):
                if(Gridara[i+1][j+1] == val1):
                    RemoveCheckedLD(i,j)
                    return False
                AddCheckersLDijag(i, j, val1)
                return True
            AddCheckersLDijag(i, j, val1)
            return True
    else:
        return False


def LevaDijagonala(i, j, val1):
    if(j > 3 and i > 3):
        if(Gridara[i][j] == val1 and Gridara[i-1][j-1] != "_" and Gridara[i-2][j-2] != "_" and Gridara[i-3][j-3] != "_"):
            return LDpom(i, j, val1)
        else:
            return False
    return False


Ispis()


def getRandoWmInt(m):
    return random.randint(0, m)

# Vraca Slobodna polja


def AllFreeSpaces():
    Slobodni = []
    for i in range(1, 11):
        for j in range(1, 11):
            if(Gridara[i][j] == "_"):
                A = Allowed(i, j)
                Slobodni.append(A)
    return Slobodni


def anywhere():
    Slobodni = []
    for i in range(1, 11):
        for j in range(1, 11):
            if(Gridara[i][j] == "_"):
                A = Allowed(i, j)
                Slobodni.append(A)
    br = getRandoWmInt(len(Slobodni)-1)
    return Slobodni[br]


# Vraca Listu Susjeda


def clear():
    for i in range(1, 11):
        for j in range(1, 11):
            DobreLDiag[i][j] = "_"
            DobreHor[i][j] = "_"
            DobreVer[i][j] = "_"
            DobreDDiag[i][j] = "_"


def listaPolja(a, b):
    Objekat = []
    if a < 10:  # dole
        i = a+1
        j = b
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    if a > 1:  # Gore
        i = a-1
        j = b
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    if b > 1:  # lijevo
        i = a
        j = b-1
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    if b < 10:  # Desno
        i = a
        j = b+1
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    if a > 1 and b > 1:  # Nalevo dijagonala
        i = a-1
        j = b-1
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    if a > 1 and b < 10:  # Nadesno dijagonala
        i = a-1
        j = b+1
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    if a < 10 and b < 10:  # dole Desno
        i = a+1
        j = b+1
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    if a < 10 and b > 1:
        i = a+1
        j = b-1
        if Gridara[i][j] == "_":
            h = Allowed(i, j)
            Objekat.append(h)
    return Objekat


def PraznaTabla():
    semafor = False
    for i in range(1, 11):
        for j in range(1, 11):
            if(Gridara[i][j] == "_"):
                semafor = True
    return semafor


def InicijalizacijaBrojaca(val1):
    globz = 0
    for i in range(1, 11):
        for j in range(1, 11):
            if(DobreHor[i][j] == val1):
                globz += 1
            if(DobreVer[i][j] == val1):
                globz += 1
            if(DobreDDiag[i][j] == val1):
                globz += 1
            if(DobreLDiag[i][j] == val1):
                globz += 1
    return globz


def BrojacCount(val1):
    Br = 0
    for i in range(1, 11):
        for j in range(1, 11):
            if(DobreHor[i][j] == val1):
                Br += 1
            if(DobreVer[i][j] == val1):
                Br += 1
            if(DobreDDiag[i][j] == val1):
                Br += 1
            if(DobreLDiag[i][j] == val1):
                Br += 1
    return Br


def Evaulacija(a, b, val1):
    global InicijalnoStanje

    clear()
    for i in range(1, 11):
        for j in range(1, 11):
            if(Gridara[i][j] == val1):
                Horizontala(i, j, val1)
                Vertikala(i, j, val1)
                LevaDijagonala(i, j, val1)
                DijagonalaDesna(i, j, val1)
    if(DobreVer[a][b] == val1 or DobreHor[a][b] == val1 or DobreLDiag[a][b] == val1 or DobreDDiag[a][b] == val1):
        Br = BrojacCount("B")
        Br2 = BrojacCount("W")

        if(InicijalnoStanje > Br and val1 == "B"):
            return -200
        if(inicijalnoW > Br2 and val1 == "W"):
            return -120

        return 60+getRandoWmInt(10)

    else:
        Br = BrojacCount("B")
        Br2 = BrojacCount("W")
        if InicijalnoStanje > Br and val1 == "B":
            print("VRACA LOSE")
            return -200
        if inicijalnoW > Br2 and val1 == "W":
            return -120
        return getRandoWmInt(5)


def CompMove():
    global P
    bestScore = -800
    BestMovei = 0
    BestMovej = 0
    score = 0
    global turn
    global DaLi
    global InicijalnoStanje
    InicijalnoStanje=InicijalizacijaBrojaca("B")
    Niz = listaPolja(P.pom1, P.pom2)
    for item in Niz:
        print("prvi item {0} druga poz {1}".format(item.pom1, item.pom2))
    print("PROSO JE")
    if len(Niz) <= 0:
        print("NEMA MESTA")
        Free = anywhere()
        a = Free.pom1
        b = Free.pom2
        turn = False
        InsertDirect(a, b, "B")
        return
    BestMovei = Niz[0].pom1
    BestMovej = Niz[0].pom2
    for i in range(0, len(Niz)):
        DaLi = False
        InsertPosition(Niz[i].pom1, Niz[i].pom2, "B", P.pom1, P.pom2)
        if(DaLi == True):
            score = MinimaxZaIzi(Niz[i].pom1, Niz[i].pom2, "B")
            Gridara[Niz[i].pom1][Niz[i].pom2] = "_"
            print("SKOR JE:{0}".format(score))
            if score >= bestScore:
                print("SKOR JE:{0} a bestScore je: {1} ".format(
                    score, bestScore))
                bestScore = score
                BestMovei = Niz[i].pom1
                BestMovej = Niz[i].pom2
    print("BEST MOVE I je :{0} a BEST MOVE J JE {1}".format(
        BestMovei, BestMovej))
    InsertDirect(BestMovei, BestMovej, "B")
    P.pom1 = BestMovei
    P.pom2 = BestMovej
    turn = False
    return


def MinimaxZaIzi(i, j, val1):
    a = Evaulacija(i, j, val1)
    return a

# region Poseban


def CompMove2():
    global P
    global P2
    global turn
    global DaLi
    global InicijalnoStanje
    global inicijalnoW
    ALPHA = -1000
    BETA = 1000
    bestScore = -800
    bestMovei = 0
    bestMovej = 0
    score = -1000
    Niz = listaPolja(P.pom1, P.pom2)
    InicijalnoStanje= InicijalizacijaBrojaca("B")
    print("BROJ MOGUCIJA POLJA JE {0}".format(len(Niz)))
    if(len(Niz) == 0):
        Free = anywhere()
        a = Free.pom1
        b = Free.pom2
        turn = False
        bestMovei = a
        bestMovej = b
        InsertDirect(bestMovei, bestMovej, "B")
        P.pom1 = bestMovei
        P.pom2 = bestMovej
        return
    bestMovei=Niz[0].pom1
    bestMovej=Niz[0].pom2
    for i in range(0, len(Niz)):
        heur = 0
        InsertPosition(Niz[i].pom1, Niz[i].pom2, "B", P.pom1, P.pom2)
        if DaLi == True:
            if(Evaulacija(Niz[i].pom1, Niz[i].pom2, "B") > 50):
                heur = 270
            score = AlphaBetaMedium(
                False, Niz[i].pom1, Niz[i].pom2, 2, ALPHA, BETA)
            score += heur
            Gridara[Niz[i].pom1][Niz[i].pom2] = "_"
            if(score >= bestScore):
                bestScore = score
                bestMovei = Niz[i].pom1
                bestMovej = Niz[i].pom2

    P.pom1 = bestMovei
    P.pom2 = bestMovej
    print("SA SKOROM {0} SMO GA DOBILJI".format(score))
    Gridara[P.pom1][P.pom2] = "B"
    turn = False
    return


def AlphaBetaMedium(isMaximizing, i, j, depth, ALPHA, BETA):
    if PraznaTabla()==False:
        return 5
    
    if(depth == 0):
        rez = Evaulacija(i, j, "B")
        if(rez > 50):
            return getRandoWmInt(10)+1
        if(rez < -50):
            return -20- getRandoWmInt(5)
        else:
            return getRandoWmInt(5)+1

    if(isMaximizing):
        bestScore = -1000
        score = 0
        Niz = listaPolja(i, j)
        if(len(Niz) == 0):
            Free = anywhere()
            a = Free.pom1
            b = Free.pom2
            Gridara[a][b] = "B"
            score = AlphaBetaMedium(True, a, b, depth-1, ALPHA, BETA)
            Gridara[a][b] = "_"
            bestScore = max(bestScore, score)
            return bestScore
        for z in range(0, len(Niz)):
            heur = 0
            InsertPosition(Niz[z].pom1, Niz[z].pom2, "B", i, j)
            if DaLi == True:
                if Evaulacija(Niz[z].pom1, Niz[z].pom2, "B") > 50:
                    print("VRATILI SMO JAKU HEURISTIKU ZA 4 CRNE U DRUGOM KORAKU")
                    heur = getRandoWmInt(10)+30
                    if(depth == 2):
                        heur = 270
                if Evaulacija(Niz[z].pom1, Niz[z].pom2, "B") < -10:
                    heur=-300
                score = AlphaBetaMedium(
                    False, Niz[z].pom1, Niz[z].pom2, depth-1, ALPHA, BETA)
                score += heur
                Gridara[Niz[z].pom1][Niz[z].pom2] = "_"
                bestScore = max(bestScore, score)
                ALPHA = max(ALPHA, bestScore)
                if BETA <= ALPHA:
                    break
        return bestScore

    if(isMaximizing == False):
        bestScore = 1000
        score = 0
        Niz = listaPolja(i, j)
        if(len(Niz) == 0):
            Free = anywhere()
            a = Free.pom1
            b = Free.pom2
            Gridara[a][b] = "W"
            score = AlphaBetaMedium(True, a, b, depth-1, ALPHA, BETA)
            Gridara[a][b] = "_"
            bestScore = min(bestScore, score)
            return bestScore
        for z in range(0, len(Niz)):
            heur = 0
            InsertPosition(Niz[z].pom1, Niz[z].pom2, "W", i, j)
            if(DaLi == True):
                if(Evaulacija(Niz[z].pom1, Niz[z].pom2, "W") > 50):
                    heur = getRandoWmInt(10)+30
                    if(depth == 2):
                        print("VRATILI SMO HEURISTIKU JAKU ZA 4 BELE")
                        heur = 350
                score = AlphaBetaMedium(True, Niz[z].pom1,
                                         Niz[z].pom2, depth-1, ALPHA, BETA)
                score -= heur
                Gridara[Niz[z].pom1][Niz[z].pom2] = "_"
                bestScore = min(bestScore, score)
                BETA = min(BETA, bestScore)
                if BETA <= ALPHA:
                    print("POKIDALI")
                    break
        return bestScore
# endregion


def CompMove3():

    global P
    global turn
    global DaLi
    global InicijalnoStanje
    global inicijalnoW

    ALPHA = -1000
    BETA = 1000
    print("\n COMPMOVE3 \n \n \n")
    bestScore = -800
    bestMovei = 0
    bestMovej = 0
    score = 0
    Niz = listaPolja(P.pom1, P.pom2)
    InicijalnoStanje = BrojacCount("B")
    inicijalnoW = BrojacCount("W")
    if(len(Niz) == 0):
        FreeBoard = AllFreeSpaces()
        bestMovei = FreeBoard[0].pom1
        bestMovej = FreeBoard[0].pom2
        for r in range(len(FreeBoard)):
            heur = 0
            Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "B"
            rez = Evaulacija(FreeBoard[r].pom1, FreeBoard[r].pom2, "B")
            Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "W"
            rez2 = Evaulacija(FreeBoard[r].pom1, FreeBoard[r].pom2, "W")
            Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "B"
            if rez > 50:
                heur = 200+getRandoWmInt(15)
            if rez2 > 50:
                heur = 170+getRandoWmInt(15)
            if rez < -10:
                heur = -350-getRandoWmInt(14)
            score = AlphaBetaHard(
                False, FreeBoard[r].pom1, FreeBoard[r].pom2, 4, ALPHA, BETA)
            score += heur
            Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "_"
            if(score >= bestScore):
                bestScore = score
                bestMovei = FreeBoard[r].pom1
                bestMovej = FreeBoard[r].pom2
            ALPHA = max(ALPHA, bestScore)
            if BETA <= ALPHA:
                break
        P.pom1 = bestMovei
        P.pom2 = bestMovej
        Gridara[P.pom1][P.pom2] = "B"
        turn = False
        return
    bestMovei = Niz[0].pom1
    bestMovej = Niz[0].pom2
    for i in range(0, len(Niz)):
        heur = 0
        InsertPosition(Niz[i].pom1, Niz[i].pom2, "B", P.pom1, P.pom2)
        if DaLi == True:
            rez = Evaulacija(Niz[i].pom1, Niz[i].pom2, "B")
            if(rez > 50):
                heur = 150+getRandoWmInt(20)
            if(rez < -10):
                heur = -350-getRandoWmInt(10)
            score = AlphaBetaHard(
                False, Niz[i].pom1, Niz[i].pom2, 4, ALPHA, BETA)
            score += heur
            Gridara[Niz[i].pom1][Niz[i].pom2] = "_"
            if(score >= bestScore):
                bestScore = score
                bestMovei = Niz[i].pom1
                bestMovej = Niz[i].pom2
    print("ZAVRSENO SA SKOROM {0}".format(bestScore))
    P.pom1 = bestMovei
    P.pom2 = bestMovej
    Gridara[P.pom1][P.pom2] = "B"
    turn = False
    return


def AlphaBetaHard(isMaximizing, i, j, depth, ALPHA, BETA):
    if(PraznaTabla() == False):
        return 5
    if(depth == 0):
        rez = Evaulacija(i, j, "B")
        if(rez > 50):
            a = getRandoWmInt(25)+10
            return a
        if(rez < -10):
            return -20-getRandoWmInt(10)
        a = getRandoWmInt(5)+1
        return a

    if(isMaximizing):
        bestScore = -1000
        score = 0
        Niz = listaPolja(i, j)
        if(len(Niz) == 0):
            FreeBoard = AllFreeSpaces()
            for r in range(len(FreeBoard)):
                heur = 0
                Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "B"
                rez = Evaulacija(
                    FreeBoard[r].pom1, FreeBoard[r].pom2, "B")
                if rez > 50:
                    heur = 120+getRandoWmInt(25)
                    if depth == 4:
                        heur = 150+getRandoWmInt(25)
                if rez < -50:
                    heur = -140-getRandoWmInt(15)
                    if depth == 4:
                        heur = -160-getRandoWmInt(20)
                score = AlphaBetaHard(
                    False, FreeBoard[r].pom1, FreeBoard[r].pom2, depth-1, ALPHA, BETA)
                score += heur
                Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "_"
                bestScore = max(bestScore, score)
                ALPHA = max(ALPHA, bestScore)
                if BETA <= ALPHA:
                    break
            return bestScore

        for z in range(0, len(Niz)):
            heur = 0
            InsertPosition(Niz[z].pom1, Niz[z].pom2, "B", i, j)
            if DaLi == True:
                rez = Evaulacija(Niz[z].pom1, Niz[z].pom2, "B")
                if rez < -50:
                    heur = -160-getRandoWmInt(20)
                if rez > 50:
                    heur = 130+getRandoWmInt(30)
                    if(depth == 4):
                        heur = 170+getRandoWmInt(29)
                score = AlphaBetaHard(
                    False, Niz[z].pom1, Niz[z].pom2, depth-1, ALPHA, BETA)
                score += heur
                Gridara[Niz[z].pom1][Niz[z].pom2] = "_"
                bestScore = max(bestScore, score)
                ALPHA = max(ALPHA, bestScore)
                if BETA <= ALPHA:
                    break
        return bestScore

    if(isMaximizing == False):
        bestScore = 1000
        score = 0
        Niz = listaPolja(i, j)
        if(len(Niz) == 0):
            FreeBoard = AllFreeSpaces()
            for r in range(len(FreeBoard)):
                heur = 0
                Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "W"
                rez = Evaulacija(FreeBoard[r].pom1, FreeBoard[r].pom2, "W")
                if rez < -50:
                    heur = -40-getRandoWmInt(15)
                    if depth == 4:
                        heur = -90-getRandoWmInt(20)
                if rez > 50:
                    heur = 160+getRandoWmInt(30)
                    if depth == 4:
                        heur = 200+getRandoWmInt(25)
                score = AlphaBetaHard(
                    True, FreeBoard[r].pom1, FreeBoard[r].pom2, depth-1, ALPHA, BETA)
                score -= heur
                Gridara[FreeBoard[r].pom1][FreeBoard[r].pom2] = "_"
                bestScore = min(bestScore, score)
                BETA = min(BETA, bestScore)
                if BETA <= ALPHA:
                    break
            return bestScore

        for z in range(0, len(Niz)):
            heur = 0
            InsertPosition(Niz[z].pom1, Niz[z].pom2, "W", i, j)
            if(DaLi == True):
                rez = Evaulacija(Niz[z].pom1, Niz[z].pom2, "W")
                if rez < -20:
                    heur = -50-getRandoWmInt(15)
                    if depth == 4:
                        heur = -60-getRandoWmInt(20)
                if rez > 50:
                    heur = 150+getRandoWmInt(30)
                    if(depth == 4):
                        heur = 170+getRandoWmInt(30)
                score = AlphaBetaHard(
                    True, Niz[z].pom1, Niz[z].pom2, depth-1, ALPHA, BETA)
                score = score - heur
                Gridara[Niz[z].pom1][Niz[z].pom2] = "_"
                bestScore = min(bestScore, score)
                BETA = min(BETA, bestScore)
                if BETA <= ALPHA:
                    break
        return bestScore


@api_view(['GET', 'POST'])
def main(request):
    if request.method == 'GET':
        return Response({
            "name": "PPP",
            "lastName": "UUU"
        })
    elif request.method == 'POST':
        try:
            global Gridara
            data = request.body
            data = json.loads(data)
            P.pom1 = data['poz1']
            P.pom2 = data['poz2']
            tezina = data['difficulty']
            Gridara = data['matrica']
            for a in Gridara:
                print(a)
            if tezina == "HARD":
                CompMove3()
            if tezina == "EASY":
                CompMove()
            if tezina == "MEDIUM":
                CompMove2()
            print("Posle compMovea \n")
            for a in Gridara:
                print(a)
            print("AJ ZA RESPONSE:{0} i {1}j".format(P.pom1, P.pom2))
            return Response({"poz1": P.pom1, "poz2": P.pom2})

        except:
            return Response({"GRESKA"})
