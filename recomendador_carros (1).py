import BaseDeDados

def obter_peso_por_uso(uso, prioridade):
    """
    Retorna os pesos para cada atributo baseado no uso e na prioridade do usuário.
    """
    # Pesos base para cada tipo de uso
    pesos_base = {
        'cidade': {
            'economia': 0.3,
            'espaco': 0.2,
            'desempenho': 0.1,
            'revenda': 0.2,
            'manutencao': 0.2
        },
        'estrada': {
            'economia': 0.2,
            'espaco': 0.2,
            'desempenho': 0.3,
            'revenda': 0.1,
            'manutencao': 0.2
        },
        'trabalho': {
            'economia': 0.3,
            'espaco': 0.1,
            'desempenho': 0.1,
            'revenda': 0.2,
            'manutencao': 0.3
        },
        'familia': {
            'economia': 0.2,
            'espaco': 0.3,
            'desempenho': 0.1,
            'revenda': 0.2,
            'manutencao': 0.2
        }
    }

    # Obter pesos base para o uso especificado
    pesos = pesos_base[uso].copy()

    # Aumentar o peso da prioridade em 0.2
    pesos[prioridade] += 0.2

    # Normalizar os pesos para que soma seja 1
    total = sum(pesos.values())
    for chave in pesos:
        pesos[chave] /= total

    return pesos

def calcular_pontuacao(carro, pesos):
    """
    Calcula a pontuação de um carro baseado nos pesos fornecidos.
    """
    pontuacao = (
        carro['economia'] * pesos['economia'] +
        carro['espaco'] * pesos['espaco'] +
        carro['desempenho'] * pesos['desempenho'] +
        carro['revenda'] * pesos['revenda'] +
        carro['manutencao'] * pesos['manutencao']
    )
    return pontuacao

def main():
    print("=== Recomendador de Carros ===\n")

    # Obter faixa de preço
    while True:
        try:
            preco_min = int(input("Preço mínimo (R$): "))
            preco_max = int(input("Preço máximo (R$): "))
            if preco_min < 0 or preco_max < preco_min:
                print("Valores inválidos. O preço máximo deve ser maior ou igual ao mínimo.")
                continue
            break
        except ValueError:
            print("Por favor, digite um número válido.")

    # Obter tipo de veículo
    categorias_validas = ['hatch', 'sedan', 'suv', 'pickup', 'caminhonete']
    while True:
        categoria = input("\nTipo de veículo (hatch, sedan, suv, pickup, caminhonete): ").lower()
        if categoria in categorias_validas:
            break
        print("Categoria inválida. Por favor, escolha uma das opções listadas.")

    # Obter prioridade
    prioridades_validas = ['economia', 'espaco', 'desempenho', 'revenda', 'manutencao']
    while True:
        prioridade = input("\nPrioridade (economia, espaço, desempenho, revenda, manutencao): ").lower()
        if prioridade in prioridades_validas:
            break
        print("Prioridade inválida. Por favor, escolha uma das opções listadas.")

    # Obter uso principal
    usos_validos = ['cidade', 'estrada', 'trabalho', 'familia']
    while True:
        uso = input("\nUso principal (cidade, estrada, trabalho, família): ").lower()
        if uso in usos_validos:
            break
        print("Uso inválido. Por favor, escolha uma das opções listadas.")

    # Filtrar carros por categoria e preço
    carros_filtrados = [
        carro for carro in BaseDeDados.carros
        if carro['categoria'] == categoria and preco_min <= carro['preco'] <= preco_max
    ]

    if not carros_filtrados:
        print("\nNenhum carro encontrado com os critérios especificados.")
        return

    # Calcular pesos baseado no uso e prioridade
    pesos = obter_peso_por_uso(uso, prioridade)

    # Calcular pontuação para cada carro
    for carro in carros_filtrados:
        carro['pontuacao'] = calcular_pontuacao(carro, pesos)

    # Ordenar por pontuação (decrescente) e selecionar os top 3
    carros_ordenados = sorted(carros_filtrados, key=lambda x: x['pontuacao'], reverse=True)
    top_3 = carros_ordenados[:3]

    # Exibir resultados
    print("\n=== Top 3 Recomendações ===")
    for i, carro in enumerate(top_3, 1):
        print(f"\n{i}. {carro['marca']} {carro['modelo']}")
        print(f"   Preço: R$ {carro['preco']:,}")
        print(f"   Categoria: {carro['categoria'].capitalize()}")
        print(f"   Pontuação: {carro['pontuacao']:.2f}/10")
        print(f"   Destaque: {carro['ponto_forte']}")
        print(f"   Detalhes:")
        print(f"     - Economia: {carro['economia']}/10")
        print(f"     - Espaço: {carro['espaco']}/10")
        print(f"     - Desempenho: {carro['desempenho']}/10")
        print(f"     - Revenda: {carro['revenda']}/10")
        print(f"     - Manutenção: {carro['manutencao']}/10")

if __name__ == "__main__":
    main()