import csv

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

def calculate_distances(point_list):
    return []

def main():
    input_file_name = input("Forneça o nome do arquivo de entrada: ")
    output_file_name = input("Forneça o nome do arquivo de saída: ")
    k = int(input("Forneça o número de grupos (K): "))

    points = read_input_file(input_file_name)
    distances = calculate_distances(points)

if __name__ == "__main__":
    main()
