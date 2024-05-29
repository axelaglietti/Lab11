import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        for i in range(2015, 2019):
            self._view._ddyear.options.append(ft.dropdown.Option(f"{i}"))

        for p in self._model._colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(f"{p}"))

        self._view.update_page()


    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        anno = self._view._ddyear.value
        colore = self._view._ddcolor.value
        if anno is None or colore is None:
            self._view.txtOut.controls.append(ft.Text("Devi prima selezionare anno e colore!!"))

        self._model.crea_grafo(colore, anno)
        self._view.txtOut.controls.append(ft.Text(f"Grafo creato, con {len(self._model._grafo.nodes)} vertici e {len(self._model._grafo.edges)} nodi"))
        self._view.txtOut.controls.append(ft.Text(f"I maggiori 3 archi:"))
        self._model.archi_maggiori()
        for arco in self._model._migliori:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {arco[0]} a {arco[1]}, peso={arco[2]["weight"]}"))
        self._model.calcola_archi_ripetizioni()
        stringa = ""
        for arco in self._model._archi_ripetuti:
            stringa += f"{arco} "
        self._view.txtOut.controls.append(ft.Text(f"Archi ripetuti: {stringa}"))
        self._view._ddnode.disabled = False
        self.fillDDProduct()
        self._view.update_page()


    def fillDDProduct(self):
        for p in self._model._prodottiColore:
            self._view._ddnode.options.append(ft.dropdown.Option(p.Product_number))
        self._view.update_page()


    def handle_search(self, e):
        nodo = int(self._view._ddnode.value)
        self._model.getPercorso(nodo)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi persorso più lungo: {self._model._numero_max}"))
        self._view.update_page()
