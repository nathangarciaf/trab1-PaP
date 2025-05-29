def main():
    arquivo_entrada = input("Forneça o nome do arquivo de entrada: ")
    arquivo_saida = input("Forneça o nome do arquivo de saída: ")
    k = int(input("Forneça o número de grupos (K): "))

    pontos = []
    try:
        with open(arquivo_entrada, 'r') as f:
            for linha in f:
                coordenadas = tuple(float(valor.strip()) for valor in linha.strip().split(','))
                pontos.append(coordenadas)
    except FileNotFoundError:
        print(f"Erro: o arquivo '{arquivo_entrada}' não foi encontrado.")
        return

    print("Pontos lidos:")
    for ponto in pontos:
        print(ponto)

if __name__ == "__main__":
    main()