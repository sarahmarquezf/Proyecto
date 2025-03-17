def stats_management(reagents, experiments, recipes): # menú de gestión de reactivos
    # selección de la gestión a realizar
    option = input("\nGestión de estadísticas:\n\n1. Investigadores que más utilizan el laboratorio.\n2. Experimentos más hecho y menos hecho.\n3. Top 5 reactivos con más alta rotación.\n4. Top 3 reactivos con mayor desperdicio.\n5. Reactivos que más se vencen.\n6. Cuántas veces no se logró hacer un experimento por falta de reactivos\n7. Salir.\n\n>> ")
    while not option.isnumeric() or int(option) not in range(1,8):
        option = input("\nGestión de estadísticas:\n\n1. Investigadores que más utilizan el laboratorio.\n2. Experimentos más hecho y menos hecho.\n3. Top 5 reactivos con más alta rotación.\n4. Top 3 reactivos con mayor desperdicio.\n5. Reactivos que más se vencen.\n6. Cuántas veces no se logró hacer un experimento por falta de reactivos\n7. Salir.\n\n>> ")

    if option == "1": # calcula los investigadores que más utilizan el laboratorio
        if not investigators_lab_use(experiments):
            return "\nTodavía no hay datos suficientes."
        else:
            top_5= investigators_lab_use(experiments)
            str_output = "\nTop 5 investigadores que más utilizan el laboratorio:\n\n"
            idx = 1
            for i_key, u_value in top_5.items():
                str_output += f"{idx}. {i_key} - Usos: {u_value}"
                if idx < len(top_5):
                    str_output += "\n"
                idx += 1
            return str_output

    elif option == "2": # calcula el experimento más hecho y menos hecho
        mme = most_made_experiment(experiments, recipes)[0]
        count_mme = most_made_experiment(experiments, recipes)[1]

        lme = least_made_experiment(experiments, recipes)[0]
        count_lme = least_made_experiment(experiments, recipes)[1]

        if not mme:
            return f"\nEl experimento que menos se ha hecho ({count_lme}) fue la receta:\n\nID: {lme.id}\nNombre: {lme.name}\nObjetivo: {lme.objective}\nReactivos usados: {lme.show_used_reagents(reagents)}\nValores: {lme.show_values()}\nProcedimiento: {lme.show_procedure()}"
        elif not lme:
            return f"\nEl experimento que más se ha hecho ({count_mme}) fue la receta:\n\nID: {mme.id}\nNombre: {mme.name}\nObjetivo: {mme.objective}\nReactivos usados: {mme.show_used_reagents(reagents)}\nValores: {mme.show_values()}\nProcedimiento: {mme.show_procedure()}"
        elif not lme and not mme or count_mme == count_lme:
            return "\nTodavía no hay datos suficientes."
        else:
            return f"\nEl experimento que más se ha hecho ({count_mme}) fue la receta:\n\nID: {mme.id}\nNombre: {mme.name}\nObjetivo: {mme.objective}\nReactivos usados: {mme.show_used_reagents(reagents)}\nValores: {mme.show_values()}\nProcedimiento: {mme.show_procedure()}\n\nEl experimento que menos se ha hecho ({count_lme}) fue la receta:\n\nID: {lme.id}\nNombre: {lme.name}\nObjetivo: {lme.objective}\nReactivos usados: {lme.show_used_reagents(reagents)}\nValores: {lme.show_values()}\nProcedimiento: {lme.show_procedure()}"
    
    elif option == "3": # calcula a los 5 reactivos con más alta rotación
        top_5r = most_rotated_reagents(reagents)
        idx = 1
        str_output = "\nTop 5 reactivos con más alta rotación:\n\n"
        for r in top_5r:
            t_rotations = r.rotations
            str_output += f"{idx}. {r.name} - Rotaciones: {t_rotations}"
            if idx < len(top_5r):
                str_output += "\n"
            idx += 1
        return str_output

    elif option == "4": # calcula a los 3 reactivos con mayor desperdicio
        top_3w = most_waste_reagents(reagents)
        idx = 1
        str_output = "\nTop 3 reactivos con mayor desperdicio:\n\n"
        for r in top_3w[0]:
            t_waste = top_3w[1][r.id][0]
            if top_3w[1][r.id][1] in ["kg", "g", "mg"]:
                unit_t = "kg"
            elif top_3w[1][r.id][1] in ["L", "mL", "uL"]:
                unit_t = "L"
            str_output += f"{idx}. {r.name} - Desechos: {round(t_waste, 2)} {unit_t}"
            if idx < len(top_3w) + 1:
                str_output += "\n"
            idx += 1
        return str_output

    elif option == "5": # calcula los 5 reactivos que más se vencen
        top_5e = most_expired_reagents(reagents)
        idx = 1
        str_output = "\nReactivos que más se vencen:\n\n"
        for r in top_5e:
            t_exp = len(r.expirations)
            str_output += f"{idx}. {r.name} - Vencimientos: {t_exp}"
            if idx < len(top_5e):
                str_output += "\n"
            idx += 1
        return str_output

    elif option == "6": # cuántas veces no se logró hacer un experimento por falta de reactivos
        fe_cont = failed_exp_due_to_reagents(experiments)
        if fe_cont == 1:
            return f"\nNo se logró hacer un experimento por falta de reactivos '{fe_cont}' vez."
        else:
            return f"\nNo se logró hacer un experimento por falta de reactivos '{fe_cont}' veces."

    elif option == "7": # regresa al menú principal
        return

def investigators_lab_use(experiments):
    stats_inv = {}

    # contar la cantidad de veces que cada investigador aparece
    for experiment in experiments:
        for investigator in experiment.responsibles:
            stats_inv[investigator] = stats_inv.get(investigator, 0) + 1

    # obtener los top 5 investigadores con más experimentos
    result = dict(sorted(stats_inv.items(), key=lambda x: x[1], reverse=True)[:5])

    return result

def most_made_experiment(experiments, recipes):
    stats_mme = {}
    aux_list = []

    # contar la cantidad de veces que cada experimento aparece
    for experiment in experiments:
        for recipe in recipes:
            if experiment.recipe == recipe.id:
                stats_mme[recipe.id] = stats_mme.get(recipe.id, 0) + 1

    result = dict(sorted(stats_mme.items(), key=lambda x: x[1], reverse=True)[:1])

    for recipe in recipes:
        if recipe.id == list(result.keys())[0]:
            aux_list.append(recipe)
            aux_list.append(result[recipe.id])
    
    return aux_list

def least_made_experiment(experiments, recipes):
    stats_lme = {}
    aux_list = []

    # contar la cantidad de veces que cada experimento aparece
    for experiment in experiments:
        for recipe in recipes:
            if experiment.recipe == recipe.id:
                stats_lme[recipe.id] = stats_lme.get(recipe.id, 0) + 1

    result = dict(sorted(stats_lme.items(), key = lambda x: x[1])[:1])

    for recipe in recipes:
        if recipe.id == list(result.keys())[0]:
            aux_list.append(recipe)
            aux_list.append(result[recipe.id])
    
    return aux_list

def most_rotated_reagents(reagents):
    # diccionario para almacenar la cantidad de rotaciones de cada reactivo
    stats_r = {}

    # contar las rotaciones de cada reactivo
    for reagent in reagents:
        stats_r[reagent.id] = reagent.rotations  # usamos 'rotations' para contar las rotaciones

    # ordenar los reactivos por el número de rotaciones (de mayor a menor) y tomar los 5 primeros
    top_5_reagents = dict(sorted(stats_r.items(), key=lambda x: x[1], reverse=True)[:5])

    # crear una lista auxiliar con los reactivos más rotados
    aux_list = []

    for reagent_id in top_5_reagents:
        # buscar el reactivo correspondiente en la lista de 'reagents'
        for reagent in reagents:
            if reagent.id == reagent_id:
                aux_list.append(reagent)
    return aux_list

def most_waste_reagents(reagents):
    stats_w = {}

    for reagent in reagents:
        waste_list = []

        if reagent.unit == "L":
            waste_list = reagent.waste
        elif reagent.unit == "kg":
            waste_list = reagent.waste
        elif reagent.unit == "mL":
            # modificamos el desecho
            idx = 0
            for i_waste in reagent.waste:
                waste_aux = i_waste*0.001
                waste_list.append(waste_aux)
                idx += 1
        elif reagent.unit == "uL":
            # modificamos el desecho
            idx = 0
            for i_waste in reagent.waste:
                waste_aux = i_waste*0.000001
                waste_list.append(waste_aux)
                idx += 1
        elif reagent.unit == "g":
            # modificamos el desecho
            idx = 0
            for i_waste in reagent.waste:
                waste_aux = i_waste*0.001
                waste_list.append(waste_aux)
                idx += 1
        elif reagent.unit == "mg":
            # modificamos el desecho
            idx = 0
            for i_waste in reagent.waste:
                waste_aux = i_waste*0.000001
                waste_list.append(waste_aux)
                idx += 1
        stats_w[reagent.id] = (sum(waste_list), reagent.unit)

    top_3_reagents = dict(sorted(stats_w.items(), key=lambda x: x[1][0], reverse=True)[:3])

    aux_list = []

    for reagent_id in top_3_reagents:
        for reagent in reagents:
            if reagent.id == reagent_id:
                aux_list.append(reagent)
    return [aux_list, top_3_reagents]

def most_expired_reagents(reagents):
    stats_e = {}

    for reagent in reagents:
        stats_e[reagent.id] = len(reagent.expirations)

    top_5_expired = dict(sorted(stats_e.items(), key=lambda x: x[1], reverse=True)[:5])

    aux_list = []

    for reagent_id in top_5_expired:
        for reagent in reagents:
            if reagent.id == reagent_id:
                aux_list.append(reagent)
    return aux_list

def failed_exp_due_to_reagents(experiments):
    stats_f = 0

    for experiment in experiments:
        if experiment.result == "fallido":
            stats_f += 1
    return stats_f