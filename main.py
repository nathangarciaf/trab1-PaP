import csv, sys
import networkx as nx

def read_input_file(filename):
    points = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    coords = tuple(float(value.strip()) for value in row)
                    points.append(coords)
                except ValueError:
                    print(f"Erro: linha inválida no arquivo: {row}")
    except FileNotFoundError:
        print(f"Erro: o arquivo '{filename}' não foi encontrado.")
        return None
    return points

def calculate_distance(a: tuple, b: tuple) -> float:
    return (sum((x - y) ** 2 for x, y in zip(a, b))) ** 1/2

def get_nearest_point(pl: list, a: tuple, len: int) -> tuple:
    i = 0
    nearest_distance = sys.float_info.max
    nearest_idx = -1
    while i < len:
        b = pl[i]
        distance = calculate_distance(a,b)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_idx = i
        i += 1
    return (nearest_idx, nearest_distance)

def get_connections(point_list: list) -> list:
    start_idx = 0
    p0 = point_list.pop(start_idx)
    path = []
    while point_list:
        list_len = len(point_list)
        nearest_point = get_nearest_point(point_list,p0,list_len)
        path.append((p0, point_list[nearest_point[0]], nearest_point[1]))
        p0 = point_list.pop(nearest_point[0])
    return path


def main():
    input_file_name = input("Forneça o nome do arquivo de entrada: ")
    output_file_name = input("Forneça o nome do arquivo de saída: ")
    k = int(input("Forneça o número de grupos (K): "))

    points = read_input_file(input_file_name)
    connections = get_connections(points.copy())
    groups = find_groups(connections, k, points)

    print("Agrupamentos:")
    for group in groups:
        print(", ".join(str(x) for x in group))

if __name__ == "__main__":
    main()
