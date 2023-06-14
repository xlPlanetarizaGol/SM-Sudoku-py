import random
import time

def leer_sudoku(archivo):
    sudoku = []
    with open(archivo, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                sudoku.append([int(num) if num != '0' else 0 for num in line.split()])
    return sudoku

def imprimir_sudoku(sudoku):
    for fila in sudoku:
        print(' '.join(str(num) if num != 0 else ' ' for num in fila))

def validar_fila(sudoku, fila, numero):
    return numero in sudoku[fila]

def validar_columna(sudoku, columna, numero):
    return numero in [sudoku[i][columna] for i in range(9)]

def validar_caja(sudoku, fila, columna, numero):
    inicio_fila = fila - fila % 3
    inicio_columna = columna - columna % 3
    for i in range(3):
        for j in range(3):
            if sudoku[inicio_fila + i][inicio_columna + j] == numero:
                return True
    return False

def validar_movimiento(sudoku, fila, columna, numero):
    return not validar_fila(sudoku, fila, numero) and \
           not validar_columna(sudoku, columna, numero) and \
           not validar_caja(sudoku, fila, columna, numero)

def encontrar_casilla_vacia(sudoku):
    for fila in range(9):
        for columna in range(9):
            if sudoku[fila][columna] == 0:
                return fila, columna
    return None, None

def resolver_sudoku(sudoku):
    fila, columna = encontrar_casilla_vacia(sudoku)
    if fila is None:
        return True

    numeros_posibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(numeros_posibles)

    for numero in numeros_posibles:
        if validar_movimiento(sudoku, fila, columna, numero):
            sudoku[fila][columna] = numero
            if resolver_sudoku(sudoku):
                return True
            sudoku[fila][columna] = 0

    return False

archivo_sudoku = 'sudoku.txt'
sudoku = leer_sudoku(archivo_sudoku)

print("Sudoku original:")
imprimir_sudoku(sudoku)

intentos = 1000
exitos = 0
intentos_totales = 0
num_casillas_a_llenar = []

start_time = time.time()

for _ in range(intentos):
    sudoku_copia = [fila[:] for fila in sudoku]

    intentos_totales += 1

    if resolver_sudoku(sudoku_copia):
        exitos += 1
        break
    else:
        num_casillas_vacias = sum(1 for fila in sudoku_copia for num in fila if num == 0)
        num_casillas_a_llenar.append(num_casillas_vacias)

end_time = time.time()
total_time = end_time - start_time

probabilidad_exito = exitos / intentos_totales

print("\nSudoku resuelto:")
imprimir_sudoku(sudoku_copia)

print("\nProbabilidad de éxito: {:.2f}%".format(probabilidad_exito * 100))
print("\nNúmero de intentos realizados: {}".format(intentos_totales))
print("\nTiempo esperado: {:.2f} segundos".format(total_time))


if exitos < intentos_totales:
    promedio_casillas_a_llenar = sum(num_casillas_a_llenar) / len(num_casillas_a_llenar)
    print("Número de casillas a llenar en caso de fracaso: {:.2f}".format(promedio_casillas_a_llenar))


