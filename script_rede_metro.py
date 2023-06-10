# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
import streamlit as st
import datetime
now = datetime.datetime.now()

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("O verdadeiro custo da corrupção")
st.subheader("por Pedro Schuller")


# %%
def gerar_estacoes(num_estacoes):
    np.random.seed(now.hour)
    return np.random.uniform(0, 10, size=(num_estacoes, 2))

# %%
def otimizar_rede(estacoes, ligacao_impedida = (0,0)):
    num_estacoes = len(estacoes)
    distancias = distance_matrix(estacoes, estacoes)

    # Inicializa a rede mínima com a primeira estação
    rede = np.zeros((num_estacoes, num_estacoes))
    seleccionados = [0]
    comprimento_total = 0

    while len(seleccionados) < num_estacoes:
        menor_distancia = np.inf
        origem, destino = None, None

        # Encontra a estação não seleccionado mais próximo à rede existente
        for i in seleccionados:
            for j in range(num_estacoes):
                if j not in seleccionados and distancias[i][j] < menor_distancia:
                    if (i, j) != ligacao_impedida and (j, i) != ligacao_impedida:
                        menor_distancia = distancias[i][j]
                        origem = i
                        destino = j

        # Adiciona a ligação à rede de metro
        rede[origem][destino] = menor_distancia
        rede[destino][origem] = menor_distancia
        comprimento_total += menor_distancia
        seleccionados.append(destino)

    return rede, comprimento_total

# %%
def desenhar_rede(estacoes, ligacoes = [0], comprimento_total = None, obstaculo = None):
    estacoes_x = estacoes[:, 0]
    estacoes_y = estacoes[:, 1]

    plt.scatter(estacoes_x, estacoes_y, color='b', label='Estações Metro')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    
    if obstaculo != None:
        plt.scatter(obstaculo[0], obstaculo[1], marker='x', color='black', s=100, label='Casa do amigo do autarca')

    
    if not np.array_equal(ligacoes, [0]): 
        plt.title(f'Rede de Metro - Custo Total: {10*comprimento_total:.2f} M€')
        for i in range(len(ligacoes)):
            for j in range(i + 1, len(ligacoes)):
                if ligacoes[i][j] != 0:
                    plt.plot([estacoes_x[i], estacoes_x[j]], [estacoes_y[i], estacoes_y[j]], color='r', linewidth=2)
    else:
        plt.title('Estações de Metro')
                
    plt.legend()
    plt.show()

# %%
st.write("Suponhamos que a sua cidade está a desenhar uma linha de metro. Há uma série de pontos-chave da cidade que devem ser ligados por este empreendimento:")
num_estacoes = 10
num_estacoes = st.slider('Quantas estações são?', 5, 20)

estacoes = gerar_estacoes(num_estacoes)
estacoes_fig = desenhar_rede(estacoes)
st.pyplot(estacoes_fig)
 

# %%

st.write("O caderno de encargos prevê que seja possível chegar a qualquer estação a partir de qualquer outra estação de origem. A empresa XPTO, candidata a este concurso, tendo como objetivo minimizar o custo da obra, propõe um desenho que minimize a distância total da rede, que assumiremos que é a única variável que determina o custo da obra, a 10M€ por kilómetro de linha:")

ligacoes, comprimento_inicial = otimizar_rede(estacoes)
rede_fig = desenhar_rede(estacoes, ligacoes, comprimento_inicial)
st.pyplot(estacoes_fig)


# %%
# Create obstacle in the middle of a random connection

st.write("O autarca desta cidade responsável pela elaboração deste concurso está a ser pressionado por um amigo para que a linha não passe num determinado local. É que esse amigo é dono desses terrenos e está interessado em ali realizar uns investimentos imobiliários muitíssimo lucrativos, para os quais a câmara até já tinha mudado o PDM para aí atribuir capacidade construtiva excepcional.")
lucro = 2
lucro = st.slider('Lucro do investimento (em milhões de euros)', 0.5, 5.0)


ligacoes_estabelecidas = np.nonzero(ligacoes)
ligacao_a_sorte = np.random.choice(len(ligacoes_estabelecidas[0]))
origem = ligacoes_estabelecidas[0][ligacao_a_sorte]
destino = ligacoes_estabelecidas[1][ligacao_a_sorte]
casa_amigo_autarca = ([(estacoes[origem][0]+estacoes[destino][0])/2, (estacoes[origem][1]+estacoes[destino][1])/2])
estacoes_afetadas = (origem, destino)


casa_fig = desenhar_rede(estacoes, ligacoes, comprimento_inicial, casa_amigo_autarca)
st.pyplot(casa_fig)

# %%
st.write("O investidor teme que a nova infraestrutura gore completamente os seus objetivos. Não ficará nada satisfeito com a indemnização que viria a receber pois é muito menor que o lucro que podia vir a retirar do investimento. Poderá esse amigo vir a influenciar o caderno de encargos por forma a que a linha contorne estes terrenos? Quanto será suficiente para convencer o nosso autarca?")

luva = 10
luva = st.slider('Luva (em milhares de euros) a pagar ao autarca', 10, 250)
comprimento_final = comprimento_inicial
if luva >= 50:
    ligacoes, comprimento_final = otimizar_rede(estacoes, estacoes_afetadas)

contorno_fig = desenhar_rede(estacoes, ligacoes, comprimento_final, casa_amigo_autarca)
st.pyplot(contorno_fig)

st.write("cenas")

# %%

st.write(f"Custo Inicial da Obra: {10*comprimento_inicial:.2f} milhões de euros")
st.write(f"Custo Final da Obra: {10* comprimento_final:.2f} milhões de euros")
st.write(f"Luva paga ao político: {luva:.0f} mil euros")

beneficio = lucro - luva/1000

st.write(f"Benefício para o empresário ao corromper: {beneficio:.2f} milhões de euros")

custo_corrupcao = 10*(comprimento_final - comprimento_inicial)
st.write(f"Verdadeiro custo da corrupção: {custo_corrupcao:.2f} milhões de euros")

# %%



