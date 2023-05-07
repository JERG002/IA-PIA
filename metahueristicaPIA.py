#Este es el bueno, ya funciona
import random
import math

# define the temperatura schedule
def temperatura(temp_inicial, enfriamiento):
    temp = temp_inicial
    while True:
        yield temp
        temp *= enfriamiento

# define the acceptance probability function
def acceptance_probability(valor_actual, nuevo_valor, temperatura):
    if nuevo_valor > valor_actual:
        return 1.0
    else:
        return math.exp((nuevo_valor - valor_actual) / temperatura)

# define the simulated annealing algorithm
def Recocido(Sol_inicial, valor_f, vecino_f, temperatura):
    sol_actual = Sol_inicial
    valor_actual = valor_f(sol_actual)
    for temp in temperatura:
        if temp < 0.001:
            return sol_actual
        nueva_sol = vecino_f(sol_actual)
        nuevo_valor = valor_f(nueva_sol)
        probAc = acceptance_probability(valor_actual, nuevo_valor, temp)
        if probAc > random.random():
            sol_actual = nueva_sol
            valor_actual = nuevo_valor
    return sol_actual

# define the knapsack value function
def Listado_Tareas(Tareas, solucion):
    valor = 0
    tiempo = 0
    for i, Ta in enumerate(solucion):
        if Ta:
            valor += Tareas[f"T.{i+1}"]["Valor"]
            tiempo += Tareas[f"T.{i+1}"]["Tiempo"]
            for dep in Tareas[f"T.{i+1}"]["Necesita"]:
                if not solucion[int(dep[2:]) - 1]:
                    return -1  # invalid solucion due to unsatisfied dependencies
    if tiempo > 10:
        return -1  # invalid solucion due to exceeding tiempo limit
    return valor

# define the knapsack neighbor function
def Vecinos_Tareas(solucion):
    nueva_sol = solucion.copy()
    i = random.randint(0, len(solucion)-1)
    nueva_sol[i] = not nueva_sol[i]
    return nueva_sol

# generate the initial solucion
def Gen_sol_inicial(num_Tareas):
    solucion = []
    while True:
        solucion = [random.choice([True, False]) for _ in range(num_Tareas)]
        if sum([Ta["Valor"] for Ta in Tareas.values() if solucion[int(Ta["Nombre"][2:]) - 1]]) >= 70:
            return solucion

# generate the Tareas

def Generar_Tareas(num_Tareas):
    Tareas = {}
    total_value = 0
    for i in range(num_Tareas):
        nombre = f"T.{i+1}"
        if i == num_Tareas - 1:
            valor = 100 - total_value
        else:
            valor = random.randint(1, 100 - total_value - (num_Tareas - i - 1))
        tiempo = random.randint(1, 10)
        Necesita = []
        if i > 0:
            # randomly choose one of the previous Tareas as a dependency
            Necesita.append(f"T.{random.randint(1, i)}")
        Tareas[nombre] = {"Nombre": nombre, "Valor": valor, "Tiempo": tiempo, "Necesita": Necesita}
        total_value += valor
    return Tareas


# generate the Tareas
Tareas = Generar_Tareas(5)

# run the simulated annealing algorithm
solucion = Gen_sol_inicial(5)
temperatura = temperatura(1000, 0.95)
mejor_solucion = Recocido(
    Sol_inicial=solucion,
    valor_f=lambda s: Listado_Tareas(Tareas, s),
    vecino_f=Vecinos_Tareas,
    temperatura=temperatura
)

print(Tareas)

if Listado_Tareas(Tareas, mejor_solucion) == -1 or Listado_Tareas(Tareas, mejor_solucion) < 70 :
    print("No hay solucion valida con la relacion tiempo-valor")
else:
    print("Mejor solucion encontrada:")
    print(mejor_solucion)
    print("Calificacion:", Listado_Tareas(Tareas, mejor_solucion))