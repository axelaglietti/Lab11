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
            self._view.txtOut.controls.append(ft.Text(f"{arco}"))

        self._view.update_page()



    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
