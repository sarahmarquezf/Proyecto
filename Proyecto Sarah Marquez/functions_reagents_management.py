from Reagent import Reagent

def reagents_management(reagents): # menú de gestión de reactivos
    # selecciona la gestión a realizar
    option = input("\nGestión de reactivos:\n\n1. Crear reactivo. \n2. Editar reactivo.\n3. Eliminar reactivo.\n4. Salir.\n\n>> ")
    while not option.isnumeric() or int(option) not in range(1,5):
        option = input("\nGestión de reactivos:\n\n1. Crear reactivo. \n2. Editar reactivo.\n3. Eliminar reactivo.\n4. Salir.\n\n>> ")

    if option == "1": # crear un nuevo reactivo
        return create_reagent(reagents)
    
    elif option == "2": # modificar un reactivo existente
        return find_reagent_edit(reagents)

    elif option == "3": # eliminar un reactivo existente
        return remove_reagent(reagents)
    
    elif option == "4": # salir
        return "\ncontinuar"

def create_reagent(reagents): # crear reactivo
    id = len(reagents) + 1  # creamos el id del nuevo agente de forma automática

    # solicitamos nombre y descripción
    name = input("\nNombre: ")
    description = input("Descripción: ")

    cost = input("Costo: $") # solicitamos costo
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

    # solicitamos categoría
    category = input("Categoría: ") # solicitamos categoría

    stock = input("Inventario: ") # solicitamos inventario
    valid_stock = False # variable auxiliar para validación de inventario

    # validamos que el inventario sea un flotante y mayor que '0'
    while not valid_stock:
        try:
            float(stock)
            if float(stock) > 0:
                valid_stock = True
            else:
                stock = input("Ingrese una cantidad de inventario válida: ")
        except ValueError:
            stock = input("Ingrese una cantidad de inventario válida: ")

    # solicitamos la unidad
    u_option = input("""\nUnidad:

1. mL
2. L
3. uL
4. g
5. kg
6. mg
                 
>> """)
    
    while not u_option.isnumeric() or int(u_option) not in range(1,7):
        u_option = input("""\nUnidad:

1. mL
2. L
3. uL
4. g
5. kg
6. mg
                 
>> """)

    if u_option == "1":
        unit = "mL"
    elif u_option == "2":
        unit = "L"
    elif u_option == "3":
        unit = "uL"
    elif u_option == "4":
        unit = "g"
    elif u_option == "5":
        unit = "kg"
    elif u_option == "6":
        unit = "mg"

    # validamos si aplica fecha de caducidad para el reactivo
    e_date_option = input("""\n¿Aplica fecha de caducidad?
          
1. Si.
2. No.
          
>> """)
    
    while not e_date_option.isnumeric() or int(e_date_option) not in range(1,3):
        e_date_option = input("""\n¿Aplica fecha de caducidad?
          
1. Si.
2. No.
          
>> """)
        
    if e_date_option == "1":

        year = input("\n- Año: ")
        while not year.isnumeric() or int(year) < 2025:
            year = input("- Año: ")

        month = input("- Mes: ")
        while not month.isnumeric() or int(month) not in range(1, 13):
            month = input("- Mes: ")
        
        if len(month) == 1:
                month = "0" + month

        day = input("- Día: ")
        while not day.isnumeric() or (month == "2" and not int(day) in range(1,28) ) or (month in ["1", "3", "5", "7", "8", "10", "12"] and not int(day) in range(1, 31)) or (month in ["4", "6", "9", "11"] and not int(day) in range(1, 30)):
            day = input("- Día: ")

        if len(day) == 1:
                day = "0" + day

        expiration_date = f"{year}-{month}-{day}"
    
    else:
        expiration_date = None

    minimum_suggested = input("\nMínimo sugerido: ") # solicitamos el mínimo sugerido
    valid_min = False # variable auxiliar para validación del mínimo sugerido

    # validamos que el mínimo sugerido sea un flotante y mayor o igual que '0'
    while not valid_min:
        try:
            float(minimum_suggested)
            if float(minimum_suggested) >= 0:
                valid_min = True
            else:
                minimum_suggested = input("Ingrese un mínimo sugerido válido: ")
        except ValueError:
            minimum_suggested = input("Ingrese un mínimo sugerido válido: ")

    other_units = []

    unit1_option = input("""\nIngrese la primera unidad:

1. mL
2. L
3. uL
4. g
5. kg
6. mg
                 
>> """)
    
    while not unit1_option.isnumeric() or int(unit1_option) not in range(1,7):
        unit1_option = input("""\nIngrese una unidad válida:

1. mL
2. L
3. uL
4. g
5. kg
6. mg
                 
>> """)
        
    if unit1_option == "1":
        unit1 = "mL"
    elif unit1_option == "2":
        unit1 = "L"
    elif unit1_option == "3":
        unit1 = "uL"
    elif unit1_option == "4":
        unit1 = "g"
    elif unit1_option == "5":
        unit1 = "kg"
    elif unit1_option == "6":
        unit1 = "mg"
        
    if unit1 == unit:
        unit1 = None
        factor1 = 0
    else:
        factor1 = input("\nIngrese su factor de conversión: ")
        while not factor1.isnumeric() or float(factor1) <= 0:
            factor1 = input("Ingrese un factor de conversión válido: ")

    unit2_option = input("""\nIngrese la segunda unidad:

1. mL
2. L
3. uL
4. g
5. kg
6. mg
                 
>> """)
    
    while not unit2_option.isnumeric() or int(unit2_option) not in range(1,7):
        unit2_option = input("""\nIngrese una unidad válida:

1. mL
2. L
3. uL
4. g
5. kg
6. mg
                 
>> """)
        
    if unit2_option == "1":
        unit2 = "mL"
    elif unit2_option == "2":
        unit2 = "L"
    elif unit2_option == "3":
        unit2 = "uL"
    elif unit2_option == "4":
        unit2 = "g"
    elif unit2_option == "5":
        unit2 = "kg"
    elif unit2_option == "6":
        unit2 = "mg"

    if unit2 == unit or unit2 == unit1:
        unit2 = None
        factor2 = 0
    else:
        factor2 = input("\nIngrese su factor de conversión: ")
        while not factor2.isnumeric() or float(factor2) <= 0:
            factor2 = input("Ingrese un factor de conversión válido: ")

    other_units.append({"unidad": unit1, "factor": float(factor1)})
    other_units.append({"unidad": unit2, "factor": float(factor2)})

    reagents.append(Reagent(id, name, description, float(cost), category, float(stock), unit, expiration_date, float(minimum_suggested), other_units))
    return f"\nEl reactivo '{name}' fue creado con exito."

def find_reagent_edit(reagents): # búsqueda de reactivo a editar
    search_id = input("\nIngresa el ID del reactivo que deseas editar: ") # solicitamos el 'id' del reactivo para su búsqueda
    while not search_id.isnumeric():
        search_id = input("\nIngrese un ID válido para el reactivo a editar: ")

    for reagent in reagents:
        if int(search_id) == reagent.id: # se encontró una coincidencia para el parametro de búsqueda
            print(reagent.show())
            option = input("\n¿Es este el reactivo que deseas editar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            while not option.isnumeric() or int(option) not in range(1,4):
                option = input("\n¿Es este el reactivo que deseas editar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            if option == "1":
                return edit_reagent(reagent)
            elif option == "2":
                find_reagent_edit(reagents)
    
    return "\nNo se encontró resultado."

def edit_reagent(reagent): # edición del reactivo encontrado
    option = input("\n¿Qué te gustaría editar?\n\n1. Nombre.\n2. Descripción.\n3. Costo.\n4. Categoría.\n5. Inventario.\n6. Unidad.\n7. Fecha de caducidad.\n8. Mínimo sugerido.\n\n>> ")
    while not option.isnumeric() or int(option) not in range(1,9):
        option = input("\n¿Qué te gustaría editar?\n\n1. Nombre.\n2. Descripción.\n3. Costo.\n4. Categoría.\n5. Inventario.\n6. Unidad.\n7. Fecha de caducidad.\n8. Mínimo sugerido.\n\n>> ")

    if option == "1": # modificar nombre
        new_name = input("\nIngrese un nombre: ")
        reagent.name = new_name # se actualiza el valor del atributo nombre para el reactivo

    elif option == "2": # modificar descripción
        new_description = input("\nIngrese una descripción: ")
        reagent.description = new_description # se actualiza el valor del atributo descripción para el reactivo

    elif option == "3": # modificar costo
        new_cost = input("\nIngrese un costo: $") # solicitamos costo
        valid_new_cost = False # variable auxiliar para validación de costo

        # validamos que el costo sea un flotante y mayor que '0'
        while not valid_new_cost:
            try:
                float(new_cost)
                if float(new_cost) > 0:
                    valid_new_cost = True
                else:
                    new_cost = input("Ingrese un costo válido: $")
            except ValueError:
                new_cost = input("Ingrese un costo válido: $")
        reagent.cost = float(new_cost) # se actualiza el valor del atributo costo para el reactivo

    elif option == "4": # modificar categoría
        new_category = input("\nIngrese una categoría: ")
        reagent.category = new_category
    
    elif option == "5": # modificar inventario
        new_stock = input("\nInventario: ") # solicitamos inventario
        valid_new_stock = False # variable auxiliar para validación de inventario

        # validamos que el inventario sea un flotante y mayor que '0'
        while not valid_new_stock:
            try:
                float(new_stock)
                if float(new_stock) > 0:
                    valid_new_stock = True
                else:
                    new_stock = input("Ingrese una cantidad de inventario válida: ")
            except ValueError:
                new_stock = input("Ingrese una cantidad de inventario válida: ")
        reagent.stock = float(new_stock) # se actualiza el valor del atributo inventario para el reactivo

    elif option == "6":
        reagent.convert_unit()

    elif option == "7":
        new_e_date_option = input("""\n¿Aplica fecha de caducidad?
          
1. Si.
2. No.
          
>> """)
    
        while not new_e_date_option.isnumeric() or int(new_e_date_option) not in range(1,3):
            new_e_date_option = input("""\n¿Aplica fecha de caducidad?
          
1. Si.
2. No.
          
>> """)
        
        if new_e_date_option == "1":

            year = input("- Año: ")
            while not year.isnumeric() or int(year) < 2025:
                year = input("- Año: ")

            month = input("- Mes: ")
            while not month.isnumeric() or int(month) not in range(1, 13):
                month = input("- Mes: ")
            
            if len(month) == 1:
                month = "0" + month

            day = input("- Día: ")
            while not day.isnumeric() or (month == "2" and not int(day) in range(1,28) ) or (month in ["1", "3", "5", "7", "8", "10", "12"] and not int(day) in range(1, 31)) or (month in ["4", "6", "9", "11"] and not int(day) in range(1, 30)):
                day = input("- Día: ")
            
            if len(day) == 1:
                day = "0" + day

            new_expiration_date = f"{year}-{month}-{day}"
        
        else:
            new_expiration_date = None

        reagent.expiration_date = new_expiration_date # se actualiza el valor del atributo fecha de expiración para el reactivo

    elif option == "8":
        new_minimum_suggested = input("\nMínimo sugerido: ") # solicitamos el mínimo sugerido
        valid_new_min = False # variable auxiliar para validación del mínimo sugerido

        # validamos que el mínimo sugerido sea un flotante y mayor o igual que '0'
        while not valid_new_min:
            try:
                float(new_minimum_suggested)
                if float(new_minimum_suggested) >= 0:
                    valid_new_min = True
                else:
                    new_minimum_suggested = input("Ingrese un mínimo sugerido válido: ")
            except ValueError:
                new_minimum_suggested = input("Ingrese un mínimo sugerido válido: ")
        reagent.minimum_suggested = float(new_minimum_suggested) # se actualiza el valor del atributo mínimo sugerido para el reactivo

    return f"\nEl reactivo '{reagent.name}' fue editado exitosamente."

def remove_reagent(reagents): # eliminar un reactivo
    search_id = input("\nIngresa el ID del reactivo que deseas eliminar: ") # solicitamos el 'id' del reactivo para su búsqueda
    for reagent in reagents:
        if int(search_id) == reagent.id: # se encontró una coincidencia para el parametro de búsqueda
            print(reagent.show())
            option = input("\n¿Es este el reactivo que deseas eliminar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            while not option.isnumeric() or int(option) not in range(1,4):
                option = input("\n¿Es este el reactivo que deseas eliminar?\n\n1. Si.\n2. No.\n3. Salir.\n\n>> ")
            if option == "1":
                reagents.remove(reagent)
                return f"El agente '{reagent.name}' fue eliminado exitosamente."
            elif option == "2":
                remove_reagent(reagents)

    return "\nNo se encontró resultado."