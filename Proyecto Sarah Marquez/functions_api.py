import requests
import json
from Reagent import Reagent
from UsedReagent import UsedReagent
from Recipe import Recipe
from Experiment import Experiment
from Values import Value

def obtain_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        payload = response.json()
        return payload
    
# w+ para escribir y/o crear el archivo
# indent = 4 para que tenga 4 espacios de sangría
# ensure_ascii para acentos y que se vea organizado el file  

def save_changes(reagents, experiments, recipes): # guarda los cambios hechos al archivo 'reagents.json'
    for reagent in reagents:
        if reagent.check_expiration_date(): # validar que el reactivo no este caducado
            if reagent.expiration_date not in reagent.expirations:
                reagent.expirations.append(reagent.expiration_date)

        if len(reagent.waste) < reagent.rotations:
            for experiment in experiments:
                for recipe in recipes:
                    if experiment.recipe == recipe.id:
                        for u_reagent in recipe.used_reagents:
                            if u_reagent.id == reagent.id:
                                error_value = reagent.discount_stock(u_reagent.quantity)
                                reagent.waste.append(error_value)

    reagents_j = []

    for reagent in reagents:
        reagent_saved = {
"id": reagent.id,
"nombre": reagent.name,
"descripcion": reagent.description,
"costo": reagent.cost,
"categoria": reagent.category,
"inventario_disponible": reagent.stock,
"unidad_medida": reagent.unit,
"fecha_caducidad": reagent.expiration_date,
"minimo_sugerido": reagent.minimum_suggested,
"conversiones_posibles": reagent.other_units,
"rotaciones": reagent.rotations,
"desperdicio": reagent.waste,
"vencimientos": reagent.expirations
}
        reagents_j.append(reagent_saved)

    with open("reagents.json", "w") as file:
        json.dump(reagents_j, file, indent = 4)

    experiments_j = []

    for experiment in experiments:
        experiment_saved = {
"id": experiment.id,
"receta_id": experiment.recipe,
"personas_responsables": experiment.responsibles,
"fecha": experiment.date,
"costo_asociado": experiment.cost,
"resultado": experiment.result,
}
        experiments_j.append(experiment_saved)

    with open("experiments.json", "w") as file:
        json.dump(experiments_j, file, indent = 4)

def save(file_name, data):  
    with open(file_name, "w+") as file:
        json.dump(data, file, ensure_ascii = False, indent = 4)
    
def preload_api_data():
    url_experiments = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/experimentos.json"
    url_recipes = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/recetas.json"
    url_reagents = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/reactivos.json"

    json_experiments = obtain_api(url_experiments)
    save("experiments.json", json_experiments)

    json_recipes = obtain_api(url_recipes)
    save("recipes.json", json_recipes)

    json_reagents = obtain_api(url_reagents)
    save("reagents.json", json_reagents)

# transforma los agentes a objetos
def transform_reagents(reagents, experiments, recipes):
    with open("reagents.json") as file:
        reagents_list = json.load(file)

    # diccionario para contar el uso de cada reactivo
    reagent_usage = {int(reagent["id"]): 0 for reagent in reagents_list}

    # contar las rotaciones basadas en los experimentos
    for experiment in experiments:
        recipe = next((r for r in recipes if r.id == experiment.recipe), None)
        if recipe:
            for used_reagent in recipe.used_reagents:
                reagent_id = int(used_reagent.id)
                if reagent_id in reagent_usage:
                    reagent_usage[reagent_id] += 1
    
    # contar las expiraciones de los agentes
    for reagent in reagents:
      if reagent.check_expiration_date(): # valida que el reactivo no este caducado
        if reagent.expiration_date not in reagent.expirations:
            reagent.expirations.append(reagent.expiration_date)

    # actualizar reactivos existentes o crear nuevos
    for reagent_json in reagents_list:
        reagent_id = int(reagent_json["id"])

        # buscar si el reactivo ya está en la lista
        existing_reagent = next((r for r in reagents if r.id == reagent_id), None)

        if existing_reagent:
            # si ya existe, actualizar las rotaciones
            existing_reagent.rotations = reagent_usage.get(reagent_id, 0)
            
            # agregar nuevos valores a la lista 'desecho'
            waste_values = reagent_json.get("desperdicio", [])
            if waste_values:
                existing_reagent.waste.extend(waste_values)  # agregar los nuevos valores de 'desperdicios'

            # agregar nuevos valores a la lista 'expirations'
            expiration_dates = reagent_json.get("vencimientos", [])
            if expiration_dates:
                existing_reagent.expiration.extend(expiration_dates)
        else:
            # si no existe, crear un nuevo objeto 'reactivo' e inicializar 'desperdicios' y 'expiraciones'
            reagent = Reagent(
                reagent_id,
                reagent_json["nombre"],
                reagent_json["descripcion"],
                reagent_json["costo"],
                reagent_json["categoria"],
                reagent_json["inventario_disponible"],
                reagent_json["unidad_medida"],
                reagent_json["fecha_caducidad"],
                reagent_json["minimo_sugerido"],
                reagent_json["conversiones_posibles"]
            )
            reagent.rotations = reagent_usage.get(reagent_id, 0)
            reagent.waste = reagent_json.get("desperdicio", [])  # inicializa 'desecho' como lista
            reagent.expirations = reagent_json.get("vencimientos", [])  # inicializa 'expirations' como lista
            reagents.append(reagent)  # agregar el reactivo a la lista

# transforma los experimentos a objetos
def transform_experiments(experiments):
    with open ("experiments.json") as file:
        experiments_list = json.load(file)
        for experiment_json in experiments_list:
            experiment = Experiment(experiment_json["id"], experiment_json["receta_id"], experiment_json["personas_responsables"], experiment_json["fecha"], experiment_json["costo_asociado"], experiment_json["resultado"])
            experiments.append(experiment)

# transforma las recetas a objetos
def transform_recipes(recipes):
    with open ("recipes.json") as file:
        recipes_list = json.load(file)
        for recipe_json in recipes_list:
            used_reagents = recipe_json["reactivos_utilizados"]
            used_reagents_aux = []
            for reagent in used_reagents:
                reagent = UsedReagent(reagent["cantidad_necesaria"], reagent["reactivo_id"], reagent["unidad_medida"])
                used_reagents_aux.append(reagent)
            values_to_measure = recipe_json["valores_a_medir"]
            values_aux = []
            for value in values_to_measure:
                value = Value(value["nombre"], value["formula"], value["minimo"], value["maximo"] )
                values_aux.append(value)
            recipe = Recipe(recipe_json["id"], recipe_json["nombre"], recipe_json["objetivo"], used_reagents_aux, recipe_json["procedimiento"], values_aux)
            recipes.append(recipe)