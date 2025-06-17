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
    return (sum((x - y) ** 2 for x, y in zip(a, b))) ** 0.5

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

def find_groups(connections: list, k: int, points: list) -> list:
    connections_sorted = sorted(connections, key=lambda x: x[2], reverse=True)

    for i in range(k - 1):
        if i < len(connections_sorted):
            coord1, coord2, _ = connections_sorted[i]
            connections.remove((coord1, coord2, _))

    G = nx.Graph()

    for coord1, coord2, dist in connections:
        G.add_edge(coord1, coord2, weight=dist)

    components = list(nx.connected_components(G))

    groups = []
    for group in components:
        indices = sorted(points.index(p) for p in group)
        groups.append(indices)

    return groups


def write_output_file(output_file_name: str, groups: list):
    try:
        with open(output_file_name, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for group in groups:
                row = [str(x + 1) for x in group]
                writer.writerow(row)
    except IOError as e:
        print(f"Erro ao escrever no arquivo '{output_file_name}': {e}")


def main():
    input_file_name = input("Forneça o nome do arquivo de entrada: ")
    output_file_name = input("Forneça o nome do arquivo de saída: ")
    k = int(input("Forneça o número de grupos (K): "))

    points = read_input_file(input_file_name)
    connections = get_connections(points.copy())
    groups = find_groups(connections, k, points)
    write_output_file(output_file_name, groups)

    print("Agrupamentos:")
    for group in groups:
        print(", ".join(str(x + 1) for x in group))

if __name__ == "__main__":
    main()
