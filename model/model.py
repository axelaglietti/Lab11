import collections
import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._colori = DAO.getAllColori()
        self._prodottiColore = None
        self._grafo = nx.Graph()
        self._venditeAnno = None
        self._migliori = []
        self._archi_ripetuti = []
        self._prodottiMap = {}
        self._numero_max = 2

    def crea_grafo(self, colore, anno):
        self._grafo.clear()
        self._prodottiColore = DAO.getProducts(colore)
        for p in self._prodottiColore:
            self._prodottiMap[p.Product_number] = p
        self._grafo.add_nodes_from(self._prodottiColore)
        self._venditeAnno = DAO.getSales(anno)

        for v1 in self._prodottiColore:
            for v2 in self._prodottiColore:
                if v1 != v2:
                    peso = DAO.getSalesSpec(v1, v2, anno)
                    if peso > 0:
                        self._grafo.add_edge(v1, v2, weight=peso)

    def archi_maggiori(self):
        ziopera = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'])
        self._migliori = ziopera[-3:]

    def calcola_archi_ripetizioni(self):
        self._archi_ripetuti = []
        for (u0, v0, peso) in list(self._migliori):
            contatore_u = 0
            contatore_v = 0
            for (u1, v1, peso) in list(self._migliori):
                if (u0 == u1 and v0 != v1) or (u0 == v1 and v0 != u1):
                    contatore_u += 1
                if (v0 == v1 and u0 != u1) or (v0 == u1 and v1 != u0):
                    contatore_v += 1
            if contatore_u > 0 and u0 not in self._archi_ripetuti:
                self._archi_ripetuti.append(u0)
            if contatore_v > 0 and v0 not in self._archi_ripetuti:
                self._archi_ripetuti.append(v0)

    def getPercorso(self, source):
        self.peso_max = 0
        self._percorso = [self._prodottiMap[source]]
        rimanenti = copy.deepcopy(list(self._grafo.nodes))
        self.ricorsione(self._percorso, rimanenti)

    def ricorsione(self, parziale, rimanenti):
        if len(parziale) > self._numero_max:
            self._percorso = copy.deepcopy(parziale)
            self._numero_max = len(self._percorso)
            return
        for v in self._grafo.neighbors(parziale[-1]):
            if len(parziale) < 2 and not self.sono_vicini(parziale, v, parziale[-1]):
                parziale.append(v)
                self.ricorsione(parziale, rimanenti)
                parziale.pop()
            else:
                if (not self.sono_vicini(parziale, v, parziale[-1]) and
                        self._grafo[parziale[-1]][v]["weight"] >= self._grafo[parziale[-2]][parziale[-1]]["weight"]):
                    parziale.append(v)
                    self.ricorsione(parziale, rimanenti)
                    parziale.pop()

    def sono_vicini(self, lista, val1, val2):
        for i in range(len(lista) - 1):
            if (lista[i] == val1 and lista[i + 1] == val2) or (lista[i] == val2 and lista[i + 1] == val1):
                return True
        return False


    # SOLUZIONE PROF
    def searchPath(self, product_number):
        nodoSource = self._prodottiMap[product_number]

        parziale = []

        self.ricorsioneProf(parziale, nodoSource, 0)

        print("final", len(self._solBest), [i[2]["weight"] for i in self._solBest])

    def ricorsioneProf(self, parziale, nodoLast, livello):
        archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale)

        if len(archiViciniAmmissibili) == 0:
            if len(parziale) > len(self._solBest):
                self._solBest = list(parziale)
                print(len(self._solBest), [ii[2]["weight"] for ii in self._solBest])

        for a in archiViciniAmmissibili:
            parziale.append(a)
            self.ricorsioneProf(parziale, a[1], livello + 1)
            parziale.pop()

    def getArchiViciniAmm(self, nodoLast, parziale):

        archiVicini = self._grafo.edges(nodoLast, data=True)
        result = []
        for a1 in archiVicini:
            if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
                result.append(a1)
        return result

    def isAscendent(self, e, parziale):
        if len(parziale) == 0:
            print("parziale is empty in isAscendent")
            return True
        return e[2]["weight"] >= parziale[-1][2]["weight"]  # perchè e[2] e poi anche weight???

    def isNovel(self, e, parziale):
        if len(parziale) == 0:
            print("parziale is empty in isnovel")
            return True
        e_inv = (e[1], e[0], e[2])
        return (e_inv not in parziale) and (e not in parziale)

        # if (e_inv not in partial_edge) and (e not in partial_edge):
        #    return True
        # else:
        #    return False