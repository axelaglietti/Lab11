import collections
import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._colori = DAO.getAllColori()
        self._prodottiColore = None
        self._grafo = nx.Graph()
        self._venditeAnno = None
        self._migliori = None

    def crea_grafo(self, colore, anno):
        self._grafo.clear()
        self._prodottiColore = DAO.getProducts(colore)
        self._grafo.add_nodes_from(self._prodottiColore)
        self._venditeAnno = DAO.getSales(anno)

        for v1 in self._prodottiColore:
            for v2 in self._prodottiColore:
                if v1 != v2:
                    peso = DAO.getSalesSpec(v1, v2, anno)
                    if peso > 0:
                        self._grafo.add_edge(v1, v2, weight=peso)

    def archi_maggiori(self):
        migliori = dict(sorted(nx.get_edge_attributes(self._grafo, 'weight').items(), key=lambda item: item[1], reverse=True))
        self._migliori = migliori[:3]


        """
        self._migliori = []
        peso_max = 0
        self.ricorsione([], self._grafo.nodes, peso_max)

    def ricorsione(self, parziale, rimanenti, peso):
        if len(parziale) > :
            self._migliori = copy.deepcopy(parziale)
        for u in rimanenti:
            for v in self._grafo.neighbors(u):
                if self._grafo[u][v]["weight"] > peso:
                    peso = self._grafo[u][v]["weight"]
                    parziale.append(self._grafo[u][v])
                    self.ricorsione(parziale, rimanenti, peso)
                    parziale.pop()
"""