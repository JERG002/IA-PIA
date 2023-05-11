import random

def Generar_Tareas(num_tareas):
    tareas = {}
    valor_total = 0
    for i in range(num_tareas):
        nombre = f"T.{i+1}"
        if i == num_tareas - 1:
            valor = 100 - valor_total
        else:
            valor = random.randint(1, 100 - valor_total - (num_tareas - i - 1))
        tiempo = random.randint(1, 10)
        Necesita = []
        if i > 0:
            # randomly choose one of the previous tareas as a dependencia
            Necesita.append(f"T.{random.randint(1, i)}")
        tareas[nombre] = {"Valor": valor, "Tiempo": tiempo, "Necesita": Necesita}
        valor_total += valor
    return tareas

def busqueda_profundidad(tareas, tarea_act, tiempo_rest, tareas_Seleccionadas, valor_total, valor_minimo):
    if tarea_act in tareas_Seleccionadas:
        return (tareas_Seleccionadas, valor_total)
    if tiempo_rest < 0:
        return (tareas_Seleccionadas, valor_total)
    if valor_total >= valor_minimo:
        return (tareas_Seleccionadas, valor_total)
    if tarea_act not in tareas:
        return (tareas_Seleccionadas, valor_total)
    homework = tareas[tarea_act]
    if len(homework["Necesita"]) > 0:
        for dependencia in homework["Necesita"]:
            if dependencia not in tareas_Seleccionadas:
                return (tareas_Seleccionadas, valor_total)
    nuevo_tareas_Seleccionadas = tareas_Seleccionadas + [tarea_act]
    nuevo_valor_total = valor_total + homework["Valor"]
    resultado = (tareas_Seleccionadas, valor_total)
    for nombre_Tarea in tareas:
        if nombre_Tarea != tarea_act:
            resultado = max(resultado, busqueda_profundidad(tareas, nombre_Tarea, tiempo_rest - homework["Tiempo"], nuevo_tareas_Seleccionadas, nuevo_valor_total, valor_minimo), key=lambda x: x[1])
    return resultado

def solucion_problema_educativo(tareas, valor_minimo):
    tiempo_total = 100
    resultado = busqueda_profundidad(tareas, list(tareas.keys())[0], tiempo_total, [], 0, valor_minimo)
    tareas_Seleccionadas = resultado[0]
    valor_total = resultado[1]
    if valor_total >= 70:
        print(f"La calificacion maxima posible es: {valor_total}")
        print(f"Las tareas seleccionadas son: {tareas_Seleccionadas}")
    else:
        print("No hay solucion valida con la relacion tiempo-valor")

tareas = Generar_Tareas(5)
print(tareas)
solucion_problema_educativo(tareas,70)
