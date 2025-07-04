import csv, sys
import networkx as nx

import csv

def read_input_file(filename):
    points = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for idx, row in enumerate(reader):
                try:
                    coords = tuple(float(value.strip()) for value in row)
                    points.append((coords, idx+1))
                except ValueError:
                    print(f"Erro: linha inválida no arquivo: {row}")
    except FileNotFoundError:
        print(f"Erro: o arquivo '{filename}' não foi encontrado.")
        return None
    return points


def calculate_distance(a: tuple, b: tuple) -> float:
    return (sum((x - y) ** 2 for x, y in zip(a, b))) ** 0.5

def get_nearest_point(pl: list, a: tuple, length: int) -> tuple:
    i = 0
    nearest_distance = sys.float_info.max
    nearest_idx = -1
    while i < length:
        b = pl[i][0] 
        distance = calculate_distance(a, b)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_idx = i
        i += 1
    return (nearest_idx, nearest_distance)

def get_connections(point_list: list) -> list:
    path = []
    current_point = point_list.pop(0)
    
    while point_list:
        length = len(point_list)
        nearest_point = get_nearest_point(point_list, current_point[0], length)
        nearest = point_list.pop(nearest_point[0])
        path.append((current_point[1], nearest[1], nearest_point[1]))
        current_point = nearest
    return path

def find_groups(connections: list, k: int, length: int) -> list:
    sorted_connections = sorted(connections, key=lambda x: (x[2], x[0]), reverse=True)
    trimmed_connections = sorted_connections[k-1:]

    graph = nx.Graph()

    for i in range(length):
        graph.add_node(i+1)

    for point1, point2, distance in trimmed_connections:
        graph.add_edge(point1, point2, weight=distance)
    
    components = list(nx.connected_components(graph))
    return components

def find_groups2(connections: list, k: int) -> list:
    connections_sorted = sorted(connections, key=lambda x: x[2], reverse=True)

    for i in range(k - 1):
        if i < len(connections_sorted):
            coord1, coord2, _ = connections_sorted[i]
            connections.remove((coord1, coord2, _))

    G = nx.Graph()

    for coord1, coord2, dist in connections:
        G.add_edge(coord1, coord2, weight=dist)

    components = list(nx.connected_components(G))
    return components


def write_output_file(output_file_name: str, groups: list):
    try:
        with open(output_file_name, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for group in groups:
                row = [str(x) for x in group]
                writer.writerow(row)
    except IOError as e:
        print(f"Erro ao escrever no arquivo '{output_file_name}': {e}")


def main():
    input_file_name = input("Forneça o nome do arquivo de entrada: ")
    output_file_name = input("Forneça o nome do arquivo de saída: ")
    k = int(input("Forneça o número de grupos (K): "))

    points = read_input_file(input_file_name)
    connections = get_connections(points.copy())
    groups = find_groups(connections, k, len(points))
    write_output_file(output_file_name,groups)
    
    print("Agrupamentos:")
    for group in groups:
        print(", ".join(str(x) for x in group))

if __name__ == "__main__":
    main()
