class Recipe:

    def __init__(self, id, name, objective, used_reagents, procedure, values):
        self.id = id
        self.name = name
        self.objective = objective
        self.used_reagents = used_reagents
        self.procedure = procedure
        self.values = values

    def show_used_reagents(self, reagents):
        str_result = ""
        cont = 0

        for ur in self.used_reagents:
            for r in reagents:
                if ur.id == r.id:
                    str_result += f"{r.name}"
                    cont += 1
                    if cont < len(self.used_reagents):
                        str_result += f", "
                    else:
                        str_result += f"."
        return str_result
    
    def show_procedure(self):
        str_result = ""
        idx = 1

        for p in self.procedure:
            str_result += f"\n{idx}. {p}"
            idx += 1
        return str_result

    def show_values(self):
        str_result = ""
        cont = 0

        for v in self.values:
            str_result += f"{v.name}"
            cont += 1
            if cont < len(self.values):
                str_result += f", "
        return str_result