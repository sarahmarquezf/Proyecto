from functions_api import *
from functions_stats import * 
from functions_experiments_management import *
from functions_reagents_management import *
from functions_results_management import *
from functions_stats import * 

def main():
    reagents = []
    experiments = []
    recipes = []

    transform_experiments(experiments)
    transform_recipes(recipes)
    transform_reagents(reagents, experiments, recipes)

    while True:
        save_changes(reagents, experiments, recipes)
        print ("\n== Bienvenido al Laboratorio Químico ==\n")
        option = input ("1. Gestionar reactivos.\n2. Gestionar experimentos.\n3. Gestionar resultados.\n4. Estadísticas.\n5. Resetear.\n6. Salir\n\n>> ")
        while not option.isnumeric() or int(option) not in range(1,7):
            option = input ("\n1. Gestionar reactivos.\n2. Gestionar experimentos.\n3. Gestionar resultados.\n4. Estadísticas.\n5. Resetear.\n6. Salir\n\n>> ")

        if option == "1":
            print(reagents_management(reagents))
        
        elif option == "2":
            print(experiments_management(experiments, recipes, reagents))

        elif option == "3":
            print(results_management(experiments, recipes, reagents))

        elif option == "4":
            print(stats_management(reagents, experiments, recipes))
            
        elif option == "5":
            preload_api_data()
            transform_experiments(experiments)
            transform_recipes(recipes)
            transform_reagents(reagents, experiments, recipes)
            exit()

        elif option == "6":
            break

main()