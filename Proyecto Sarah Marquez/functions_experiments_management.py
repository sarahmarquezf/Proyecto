from Experiment import Experiment

def experiments_management(experiments, recipes, reagents): # menú de gestión de experimentos
    option = input("\nGestión de experimentos:\n\n1. Crear experimento. \n2. Editar experimento.\n3. Eliminar experimento.\n4. Salir.\n\n>> ")
    while not option.isnumeric() or int(option) not in range(1,5):
        option = input("\nGestión de experimentos:\n\n1. Crear experimento. \n2. Editar experimento.\n3. Eliminar experimento.\n4. Salir.\n\n>> ")

    if option == "1": # crear un nuevo experimento
        return create_experiment(experiments, recipes, reagents)

    elif option == "2": # modificar un experimento existente
        return find_experiment_edit(experiments, recipes)

    elif option == "3": # eliminar un experimento existente
        return remove_experiment(experiments)
    
    elif option == "4": # salir
        return

def create_experiment(experiments, recipes, reagents): # crear experimento
    id = experiments[len(experiments)-1].id + 1 # creamos el id del nuevo experimento de forma automática

    recipe = input("\nReceta: ") # solicitamos la receta a usar
    while not recipe.isnumeric() or int(recipe) not in [r.id for r in recipes]:
        recipe = input("Ingrese una receta válida: ")

    missing_reagents = 0 # contador de agentes insuficientes a utilizar
    expired_reagents = 0 # contado de agentes caducados

    for recipe_i in recipes: # iteramos las recetas
        if recipe_i.id == int(recipe): # se encontró una coincidencia para el parametro de búsqueda de la receta
            for used_reagent in recipe_i.used_reagents: # iteramos los agentes utilizados en la receta
                for reagent in reagents: # iteramos los agentes
                    if used_reagent.id == reagent.id: # se encontró una coincidencia para el parametro de búsqueda del agente
                        if used_reagent.quantity > reagent.stock:  # validamos que la cantidad necesaria del reactivo a utilizar no supere la cantidad del inventario
                            missing_reagents += 1
                            if missing_reagents == 1:
                                failed_experiment = Experiment(int(id), None, None, None, None, "fallido")
                                experiments.append(failed_experiment)
                            print(f"\nSe requieren {used_reagent.quantity} {used_reagent.unit} de {reagent.name}, pero solo hay {round(reagent.stock, 2)} {reagent.unit} en el inventario.")
                        if reagent.check_expiration_date():  # validamos que el reactivo a utilizar no este caducado
                            expired_reagents += 1
                            if reagent.expiration_date not in reagent.expirations:
                                reagent.expirations.append(reagent.expiration_date)
                            print(f"\nEl reactivo {reagent.name} caducó el {reagent.expiration_date}.")

    if missing_reagents == 0 and expired_reagents == 0: # validamos que se tenga la cantidad en inventario necesaria de los reactivos y que no esten caducados

        cost = 0 # variable auxiliar para calcular el costo del experimento

        for recipe_i in recipes: # tteramos las recetas
            if recipe_i.id == int(recipe): # si se encontró una coincidencia para el parametro de búsqueda de la receta
                for used_reagent in recipe_i.used_reagents: # iteramos los agentes utilizados en la receta
                    for reagent in reagents:  # iteramos los agentes
                        if used_reagent.id == reagent.id: # se encontró una coincidencia para el parametro de búsqueda del agente
                            cost += used_reagent.quantity * reagent.cost # se suma a la variable auxiliar costo el producto de la cantidad de agente requerido por su precio
                            error_value = reagent.discount_stock(used_reagent.quantity) # se calcula una cantidad aleatoria a restar del inventario del reactivo
                            while (error_value + used_reagent.quantity) > reagent.stock: # se valida que la cantidad a usar no exceda la cantidad en inventario
                                error_value = reagent.discount_stock(used_reagent.quantity)
                            reagent.stock -= used_reagent.quantity + error_value # descontamos la cantidad usada del inventario
                            reagent.waste.append(error_value) # le sumamos la cantidad desperdiciada al registro de desecho

        responsibles = [] # lista auxiliar para los responsables

        r_option = input("Ingrese el nombre de los responsables: ") # solicitamos los nombres de los responsables
        if all(x.isalpha() or x.isspace() for x in r_option):
            responsibles.append(r_option.lower().title())
        while not r_option.isalpha() or len(responsibles) < 1 or r_option.upper() != "F":
            r_option = input("Ingrese el nombre de los responsables (Presione 'F' para finalizar): ")
            if r_option == "F" or r_option == "f": # se termina de agregar responsables
                break
            elif all(x.isalpha() or x.isspace() for x in r_option): # validamos que el input consista solo de letras incluyendo espacios y aplicamos el formato correspondiente
                responsibles.append(r_option.lower().title())

        print("\nIngrese la fecha:\n")
        year = input("- Año: ")
        while not year.isnumeric() or int(year) not in range(2025, 3001):
            year = input("- Año: ")

        month = input("- Mes: ")
        while not month.isnumeric() or int(month) not in range(1, 13):
            month = input("- Mes: ")

        day = input("- Día: ")
        while not day.isnumeric() or (month == "2" and not int(day) in range(1,28) ) or (month in ["1", "3", "5", "7", "8", "10", "12"] and not int(day) in range(1, 31)) or (month in ["4", "6", "9", "11"] and not int(day) in range(1, 30)):
            day = input("- Día: ")

        date = f"{year}-{month}-{day}"

        result = input("\nIngrese los resultados: ")
    
        experiments.append(Experiment(int(id), int(recipe), responsibles, date, cost, result))

        for reagent_i in reagents:
            for recipe_i in recipes:
                if recipe_i.id == int(recipe):
                    for used_reagent in recipe_i.used_reagents:
                        if int(used_reagent.id) == int(reagent_i.id):
                            reagent_i.rotations += 1

        return f"\nEl experimento de ID {id} fue creado con exito."
    else:
        return f"\nEl experimento no pudo ser creado."

def find_experiment_edit(experiments, recipes): # búsqueda de experimento a editar
    search_id = input("\nIngresa el ID del experimento que deseas editar: ")
    while not search_id.isnumeric():
        search_id = input("Ingrese un ID válido para el reactivo a editar: ")

    for experiment in experiments:
        if int(search_id) == experiment.id:
            print(experiment.show())
            option = input("\n¿Es este el experimento que deseas editar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            while not option.isnumeric() or int(option) not in range(1,4):
                option = input("\n¿Es este el experimento que deseas editar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            if option == "1":
                return edit_experiment(experiment, recipes)
            elif option == "2":
                find_experiment_edit(experiments, recipes)
            elif option == "3":
                return "\nNo hubo ediciones."

    return "\nNo se encontró resultado."

def edit_experiment(experiment, recipes): # edición del experimento encontrado
    option = input("\n¿Qué te gustaría editar?\n\n1. Receta.\n2. Responsables.\n3. Fecha.\n4. Costo.\n5. Resultado.\n\n>> ")
    while not option.isnumeric() or int(option) not in range(1,6):
        option = input("\n¿Qué te gustaría editar?\n\n1. Receta.\n2. Responsables.\n3. Fecha.\n4. Costo.\n5. Resultado.\n\n>> ")

    if option == "1": # modificar receta
        new_recipe = input("\nIngresa el ID de la nueva receta: ")
        while not new_recipe.isnumeric() or int(new_recipe) not in [r.id for r in recipes]:
            new_recipe = input("Ingrese un ID de receta válido: ")

        experiment.recipe = int(new_recipe) # se actualiza el valor del atributo receta para el experimento

    elif option == "2": # modificar responsables
        new_responsibles = [] # lista auxiliar para los nuevos responsables

        new_r_option = input("\nIngrese el nombre de los nuevos responsables: ") # solicitamos los nombres de los responsables
        if all(x.isalpha() or x.isspace() for x in new_r_option):
            new_responsibles.append(new_r_option.lower().title())
        while not new_r_option.isalpha() or len(new_responsibles) < 1 or new_r_option.upper() != "F":
            new_r_option = input("Ingrese el nombre de los nuevos responsables (Presione 'F' para finalizar): ")
            if new_r_option == "F" or new_r_option == "f": # se termina de agregar responsables
                break
            elif all(x.isalpha() or x.isspace() for x in new_r_option): # validamos que el input consista solo de letras incluyendo espacios y aplicamos el formato correspondiente
                new_responsibles.append(new_r_option.lower().title())

        experiment.responsibles = new_responsibles # se actualiza el valor del atributo responsables para el experimento
        
    elif option == "3": # modificar fecha de expiración
        print("\nIngrese la fecha:\n")
        year = input("- Año: ")
        while not year.isnumeric() or int(year) < 2025:
            year = input("- Año: ")

        month = input("- Mes: ")
        while not month.isnumeric() or int(month) not in range(1, 13):
            month = input("- Mes: ")

        day = input("- Día: ")
        while not day.isnumeric() or (month == "2" and not int(day) in range(1,28) ) or (month in ["1", "3", "5", "7", "8", "10", "12"] and not int(day) in range(1, 31)) or (month in ["4", "6", "9", "11"] and not int(day) in range(1, 30)):
            day = input("- Día: ")

        new_date = f"{year}-{month}-{day}"
        experiment.date = new_date

    elif option == "4": # modificar costo
        cost = input("\nCosto: $") # solicitamos costo
        valid_cost = False # variable auxiliar para validación de costo

        # validamos que el costo sea un flotante y mayor que '0'
        while not valid_cost:
            try:
                float(cost)
                if float(cost) > 0:
                    valid_cost = True
                else:
                    cost = input("Ingrese un costo válido: $")
            except ValueError:
                cost = input("Ingrese un costo válido: $")
        experiment.cost = cost # se actualiza el valor del atributo costo para el experimento

    elif option == "5": # modificar resultados
        new_result = input("\nIngrese los resultados: ")
        experiment.result = new_result # se actualiza el valor del atributo resultado para el experimento
    
    return f"\nEl experimento de ID '{experiment.id}' fue editado con éxito."

def remove_experiment(experiments): # eliminar un experimento
    search_id = input("\nIngresa el ID del experimento que deseas eliminar: ")
    for experiment in experiments:
        if int(search_id) == experiment.id:
            print(experiment.show())
            option = input("\n¿Es este el experimento que deseas eliminar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            while not option.isnumeric() or int(option) not in range(1,4):
                option = input("\n¿Es este el experimento que deseas eliminar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            if option == "1":
                experiments.remove(experiment)
                return f"\nEl experimento de ID '{experiment.id}' fue eliminado exitosamente."
            elif option == "2":
                remove_experiment(experiment)

    return "\nNo se encontró resultado."