import datetime

class Experiment:

    def __init__(self, id, recipe, responsibles, date, cost, result):
        self.id = id
        self.recipe = recipe
        self.responsibles = responsibles
        self.date = date
        self.cost = cost
        self.result = result

    def date_of_experiment(self):
        return datetime.datetime.now()

    def show(self):
        return f"\nID: {self.id}\nReceta: {self.recipe}\nResponsables: {self.show_responsibles()}\nFecha: {self.date}\nCosto: {self.cost}$\nResultado: {self.result}"
    
    def show_responsibles(self):
        str_result = ""
        cont = 0

        for r in self.responsibles:
            str_result += r
            cont += 1
            if cont < len(self.responsibles):
                str_result += ", "
        return str_result