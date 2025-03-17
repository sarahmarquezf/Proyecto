import math
import re

def results_management(experiments, recipes, reagents): # menú de gestión de resultados
    option = input("\nGestión de resultados:\n\n1. Validar resultados. \n2. Salir.\n\n>> ")
    while not option.isnumeric() or int(option) not in range(1,3):
        option = input("\nGestión de resultados:\n\n1. Validar resultados. \n2. Salir.\n\n>> ")

    if option == "1": # validar resultados
        return find_experiment(experiments, recipes)
    else:
        return "\nNo hubo gestión de resultados."

def find_experiment(experiments, recipes): # búsqueda de experimento para validar resultados
    search_id = input("\nIngresa el ID del experimento que deseas validar: ")
    while not search_id.isnumeric():
        search_id = input("\nIngrese un ID válido para el reactivo a validar: ")

    for experiment in experiments:
        if int(search_id) == experiment.id:
            print(experiment.show())
            option = input("\n¿Es este el experimento que deseas validar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            while not option.isnumeric() or int(option) not in range(1,4):
                option = input("\n¿Es este el experimento que deseas validar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            if option == "1":
                return validate_results(experiment, recipes)
            elif option == "2":
                find_experiment(experiments, recipes)
            elif option == "3":
                return "\nNo hubo validación."

    return "\nNo se encontró resultado."

def validate_results(experiment, recipes): # valida el resultado
    for recipe in recipes:
        if recipe.id == experiment.recipe:
            result = calculation(recipe)
            if result == None:
                return "\nHubo algún error en la fórmula."
            elif result >= recipe.values[0].minimum and result <= recipe.values[0].maximum:
                return f"\nEl resultado es {round(result, 3)} y se encuentra dentro de los parametros establecidos 'mínimo: {recipe.values[0].minimum}' - 'máximo: {recipe.values[0].maximum}'."
            else:
                return f"\nEl resultado es {round(result, 3)} y no se encuentra dentro de los parametros establecidos 'mínimo: {recipe.values[0].minimum}' - 'máximo: {recipe.values[0].maximum}'."

def calculation(recipe): # calcula el resultado y lo compara con los parámetros
    allowed_functions = {"log": math.log10, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, "pow": math.pow}
    
    if len(recipe.values) == 1: # caso 1: Solo hay una opción para validar
        if "=" not in recipe.values[0].formula:
            formula = input(f"\n{recipe.values[0].formula}...\n\n>> ")
            while formula == "":
                formula = input(f"\n{recipe.values[0].formula}...\n\n>> ")

        else:
            formula = input(f"\nIngrese la formula '{recipe.values[0].formula}' sustituyendo los valores correspondientes y en ese mismo formato...\n\n>> ")
            while formula == "":
                formula = input(f"\Ingrese la formula '{recipe.values[0].formula}' sustituyendo los valores correspondientes y en ese mismo formato...\n\n>> ")

        try:
            result = eval(formula.replace("^", "**"), {"__builtins__": None}, allowed_functions)
            return result
        except:
            return None
    
    elif len(recipe.values) > 1: # caso 2: Hay más de una opción para validar
        idx = 0
        values_dict = {}
        print("\nSeleccione los valores a medir...\n")
        for v in recipe.values:
            print(f"{idx + 1}. {v.name}.")
            values_dict[idx] = v
            idx += 1

        option = input("\n>> ")

        while not option.isnumeric() or int(option) not in range(1, idx + 1):
            idx = 0
            print("\nSeleccione algún valor a medir válido...\n")
            for v in recipe.values:
                print(f"{idx + 1}. {v.name}.")
                idx += 1
            option = input("\n>> ")

        recipe_s = values_dict[int(option)-1]

        if "(" in recipe_s.formula or "=" in recipe_s.formula:
            formula_to_show = re.sub(r"\[(.*?)\]", r"(\1)", recipe_s.formula)
            formula = input(f"\nIngrese la formula '{formula_to_show}' sustituyendo los valores correspondientes y en ese mismo formato...\n\n>> ")
            while formula == "":
                formula = input(f"\nIngrese la formula '{formula_to_show}' sustituyendo los valores correspondientes y en ese mismo formato...\n\n>> ")

        else:
            formula = input(f"\n{recipe_s.formula}...\n\n>> ")
            while formula == "":
                formula = input(f"\n{recipe_s.formula}...\n\n>> ")

        try:
            result = eval(formula.replace("^", "**"), {"__builtins__": None}, allowed_functions)
            return result
        except:
            return None