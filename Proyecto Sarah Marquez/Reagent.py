import datetime
import random

class Reagent:
    def __init__(self, id, name, description, cost, category, stock, unit, expiration_date, minimum_suggested, other_units):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.category = category
        self.stock = stock
        self.unit = unit
        self.expiration_date = expiration_date
        self.minimum_suggested = minimum_suggested
        self.other_units = other_units
        self.rotations = 0
        self.waste = []
        self.expirations = []

    # retorna la información acerca del reactivo como un 'string'
    def show(self):
        self.alert_minimum()
        if self.expiration_date != None:
            return f"\nNombre: {self.name}\nDescripción: {self.description}\nCosto: ${round(self.cost, 2)}\nCategoría: {self.category}\nInventario: {round(self.stock, 2)} {self.unit}\nFecha de caducidad: {self.expiration_date}\nMínimo sugerido: {self.minimum_suggested} {self.unit}\nConversiones posibles: {self.show_other_units()}"
        else:
            return f"\nNombre: {self.name}\nDescripción: {self.description}\nCosto: ${round(self.cost, 2)}\nCategoría: {self.category}\nInventario: {round(self.stock, 2)} {self.unit}\nMínimo sugerido: {self.minimum_suggested} {self.unit}\nConversiones posibles: {self.show_other_units()}"
        
    def show_other_units(self):
        str_result = ""

        for ou in self.other_units:
            if ou['unidad'] != None:
                str_result += f"\n* Unidad: {ou['unidad']} - Factor: {ou['factor']}"

        if str_result == "":
            str_result = "Ninguna"
        return str_result

    # alerta cuando un reactivo haya alcanzado o este por debajo del mínimo sugerido
    def alert_minimum(self):
        if self.minimum_suggested >= self.stock:
            print(f"\n¡El reactivo {self.name} ha alcanzado o está por debajo del mínimo sugerido {self.minimum_suggested}! - POR FAVOR REPONERLO")

    # verifica que el reactivo no haya expirado
    def check_expiration_date(self):
        if self.expiration_date == None:
            return False
        else:
            today = datetime.date.today() # Obtener solo la fecha.
            if datetime.date.fromisoformat(self.expiration_date) <= today:
                return True
            return False

    # calcula el porcentaje aleatorio a descontar del inventario
    def discount_stock(self, used_reagent_quantity):
        random_error_value = random.uniform(0.001, 0.225)  # 0.1% a 22.5%
        error_value = used_reagent_quantity * random_error_value

        return error_value
    
    # convierte las unidades del reactivo
    def convert_unit(self):
        if self.other_units[0]["unidad"] == None and self.other_units[1]["unidad"] == None:
            print("\nNo hay otras unidades disponibles.")

        else:
            idx = 1  # creamos una varible para el indice
            print("""\nSeleccione una unidad:\n""")
            print(f"{idx}. {self.unit}.")
            for o_unit in self.other_units:
                idx += 1
                print(f"{idx}. {o_unit['unidad']}.")
            option_new_unit = input("\n>> ")

            # validamos el input del usuario
            while not option_new_unit.isnumeric() or int(option_new_unit) not in range(1,4):
                idx = 1
                print("""\nSeleccione una unidad válida:\n""")
                print(f"{idx}. {self.unit}.")
                for o_unit in self.other_units:
                    idx += 1
                    print(f"{idx}. {o_unit['unidad']}.")
                option_new_unit = input("\n>> ")

            aux_unit = {} # varible auxiliar para guardar la unidad actual del reactivo

            if option_new_unit == "2" and self.other_units[0]["unidad"] != None:
                print("2")

                # guardamos la unidad original y calculamos su factor de conversión con relación a la nueva unidad
                aux_unit["unidad"] = self.unit
                aux_unit["factor"] = 1/self.other_units[0]["factor"]

                # cambiamos la unidad del reactivo por la nueva, modificamos el inventario y el mínimo sugerido
                self.unit = self.other_units[0]["unidad"]
                self.stock = self.stock*self.other_units[0]["factor"]
                self.minimum_suggested = self.minimum_suggested*self.other_units[0]["factor"]

                # modificamos el desecho
                idx = 0
                for i_waste in self.waste:
                    self.waste[idx] = i_waste*self.other_units[0]["factor"]
                    idx += 1

                # cambios el factor de la conversión restante
                self.other_units[1]["factor"] = round(self.other_units[1]["factor"]/self.other_units[0]["factor"], 7) # Lo redondeamos a un maximo de 7 decimales para evitar errores de división por parte de python.

                # guardamos la unidad original en la lista de 'otras unidades'
                self.other_units[0] = aux_unit

            elif option_new_unit == "3" and self.other_units[1]["unidad"] != None:
                print("2")
                
                # guardamos la unidad original y calculamos su factor de conversión con relación a la nueva unidad
                aux_unit["unidad"] = self.unit
                aux_unit["factor"] = 1/self.other_units[1]["factor"]

                # cambiamos la unidad del reactivo por la nueva, modificamos el inventario y el mínimo sugerido
                self.unit = self.other_units[1]["unidad"]
                self.stock = self.stock*self.other_units[1]["factor"]
                self.minimum_suggested = self.minimum_suggested*self.other_units[1]["factor"]

                # modificamos el desecho
                idx = 0
                for i_waste in self.waste:
                    self.waste[idx] = i_waste*self.other_units[1]["factor"]
                    idx += 1

                # cambios el factor de la conversión restante
                self.other_units[0]["factor"] = round(self.other_units[0]["factor"]/self.other_units[1]["factor"], 7) # Lo redondeamos a un máximo de 7 decimales para evitar errores de división por parte de python.

                # guardamos la unidad original en la lista de 'otras unidades'
                self.other_units[1] = aux_unit