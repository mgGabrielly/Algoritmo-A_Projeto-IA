import heapq
from collections import namedtuple

ESTADO_OBJETIVO = [1, 2, 3, 4, 5, 6, 7, 8, 0]

No = namedtuple("No", ["estado", "pai", "acao", "custo", "heuristica"])

def calcular_distancia_manhattan(estado):
    return sum(abs(s % 3 - g % 3) + abs(s // 3 - g // 3) for s, g in zip(estado, ESTADO_OBJETIVO) if s != 0)

def contar_numeros_fora_de_posicao(estado):
    return sum(1 for s, g in zip(estado, ESTADO_OBJETIVO) if s != 0 and s != g)

def a_estrela(estado_inicial):
    lista_aberta, conjunto_fechado = [], set()
    heapq.heappush(lista_aberta, No(estado_inicial, None, None, 0, calcular_distancia_manhattan(estado_inicial)))

    while lista_aberta:
        no_atual = heapq.heappop(lista_aberta)
        if no_atual.estado == ESTADO_OBJETIVO:
            caminho, custo = [], 0
            while no_atual:
                caminho.append(no_atual.estado)
                no_atual = no_atual.pai
                custo += 1
            return caminho[::-1], custo - 1

        if tuple(no_atual.estado) in conjunto_fechado:
            continue

        conjunto_fechado.add(tuple(no_atual.estado))
        posicao_tile_vazio, coluna = no_atual.estado.index(0), divmod(no_atual.estado.index(0), 3)[1]
        movimentos = [(0, -1, "Esquerda"), (0, 1, "Direita"), (-1, 0, "Cima"), (1, 0, "Baixo")]

        for dr, dc, acao in movimentos:
            nova_linha, nova_coluna = divmod(posicao_tile_vazio + dr * 3 + dc, 3)
            if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
                novo_estado = no_atual.estado[:]
                novo_estado[posicao_tile_vazio], novo_estado[nova_linha * 3 + nova_coluna] = novo_estado[nova_linha * 3 + nova_coluna], novo_estado[posicao_tile_vazio]
                heapq.heappush(lista_aberta, No(novo_estado, no_atual, acao, no_atual.custo + 1, calcular_distancia_manhattan(novo_estado)))

    return None, None

estado_inicial = [1, 2, 3, 0, 4, 6, 7, 5, 8]
caminho_solucao, custo = a_estrela(estado_inicial)

if caminho_solucao:
    for i, estado in enumerate(caminho_solucao):
        print(f"Passo {i}:\n{[estado[j:j+3] for j in range(0, 9, 3)]}")
        numeros_fora_de_posicao = contar_numeros_fora_de_posicao(estado)
        print(f"Números fora de posição: {numeros_fora_de_posicao}\n")
    print(f"Custo total da solução: {custo}")
else:
    print("Não há solução para o estado inicial fornecido.")
