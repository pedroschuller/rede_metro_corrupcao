# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
import streamlit as st
import datetime
now = datetime.datetime.now()

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("O rentismo e o verdadeiro custo da corrupção")
st.header("Pós-Graduação em Pensamento Liberal - Teoria da Escolha Pública")
st.write("por Pedro Schuller")

st.subheader("A Teoria da Escolha Pública")

st.write("Apesar do valor da liberdade ser amplamente aclamado por boa parte das forças políticas e setores da sociedade nas democracias ocidentais, a despesa estatal e expectativa de que os governantes resolvam os problemas quotidianos das pessoas tem tido uma tendência crescente, assim como o efectivo poder de decisão que é voluntariamente ou involuntariamente cedido a estes pelos indivíduos.")

st.write("A teoria da ecolha pública desafia a noção de que os governos consistem em governantes omniscientes e benevolentes que agem sempre no melhor interesse do bem comum. Em vez disso, propõe uma perepectiva mais realista do processo de tomada de decisão nos sistemas democráticos, reconhecendo o comportamento egoísta dos indivíduos, incluindo políticos e burocratas.")

st.write("Uma das principais conclusões da teoria da escolha pública é que os indivíduos na esfera política não são fundamentalmente diferentes dos do sector privado. Têm as suas próprias preferências, motivações e incentivos, e agem para maximizar a sua própria utilidade, tal como os indivíduos nas transacções de mercado. Este entendimento torna evidente o facto de os políticos e os burocratas estarem sujeitos às mesmas falhas, preconceitos e limitações que qualquer outra pessoa.")

st.write("A TEP enfatiza a importância de analisar o comportamento dos políticos e burocratas no âmbito do seu interesse próprio. Sugere que estes indivíduos seguem frequentemente políticas que os beneficiam a si próprios, aos seus apoiantes ou a grupos de interesses especiais, em vez de se concentrarem exclusivamente no chamado 'bem comum'. A teoria da escolha pública também salienta a inclinação natural para comportamentos rentistas, em que os indivíduos procuram obter riqueza ou privilégios através de meios políticos, conduzindo a resultados globalmente ineficientes e injustos.")

st.write("O impacto da teoria da escolha pública na forma tradicional de encarar a democracia é duplo. Em primeiro lugar, contribuiu para uma avaliação mais céptica e crítica do processo de decisão política, desafiando a visão idealista de que as instituições democráticas podem, por si só, garantir resultados que correspondam ao suposto 'interesse público'. Ao reconhecer os incentivos individualistas dos actores políticos, a teoria da escolha pública incentiva a uma compreensão mais realista das limitações e potenciais armadilhas dos sistemas democráticos.")

st.write("Como consequência, da teoria da escolha pública decorre a necessidade de reformas institucionais para resolver as deficiências e inconsistências que identifica. Sugere que a concepção de instituições e incentivos políticos de forma a alinhar os interesses próprios dos políticos e burocratas com o interesse público pode conduzir a melhores resultados. Isto pode implicar a redução do âmbito da intervenção governamental, a introdução de controlos e equilíbrios, a promoção da transparência e da responsabilização e o incentivo à concorrência entre os actores políticos.")

st.subheader("O rentismo e o custo da corrupção")

st.write("Vamos explorar uma das decorrências da teoria da escolha pública: o rentismo, ou rent-seeking. Tal como dito por Alves e Meadowcraft (em 'Hayek’s Slippery Slope, the Stability of the Mixed Economy and the Dynamics of Rent Seeking'), o rentismo explica a estabilidade das economias mistas, mostrando que a dinâmica da procura de rendas conduz à instabilidade inerente ao laissez-faire ou aos regimes autoritários. À medida que a procura de rendas aumenta e o Estado passa a dominar um grande sector da economia, os ganhos potenciais de mais procura de rendas diminuem ao ponto de os benefícios da procura de rendas futura serem provavelmente inferiores aos custos da acção política necessária para os obter. Isto significa que a economia mista é relativamente estável, uma vez que os benefícios de uma maior procura de rendimentos são compensados pelos custos, e o processo de slippery slope pode ser contrabalançado por características de auto-equilíbrio mais poderosas das economias mistas.")

st.write("Com o seguinte exercício, podemos verificar como é fácil que a economia penda para um maior peso do estado e dos decisores políticos nas decisões económicas.")

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
def desenhar_rede(estacoes, ligacoes = [0], comprimento_total = None, obstaculo = None, tamanho = 100):
    estacoes_x = estacoes[:, 0]
    estacoes_y = estacoes[:, 1]

    plt.scatter(estacoes_x, estacoes_y, color='b', label='Estações Metro')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    
    
    if not np.array_equal(ligacoes, [0]): 
        plt.title(f'Rede de Metro - Custo Total: {10*comprimento_total:.2f} M€')
        for i in range(len(ligacoes)):
            for j in range(i + 1, len(ligacoes)):
                if ligacoes[i][j] != 0:
                    plt.plot([estacoes_x[i], estacoes_x[j]], [estacoes_y[i], estacoes_y[j]], color='r', linewidth=2)
    else:
        plt.title('Estações de Metro')

    if obstaculo != None:
        plt.scatter(obstaculo[0], obstaculo[1], marker='x', color='black', s=tamanho, label='Investimento do amigo do autarca')

                
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


casa_fig = desenhar_rede(estacoes, ligacoes, comprimento_inicial, casa_amigo_autarca, lucro*25)
st.pyplot(casa_fig)

# %%
st.write("O investidor teme que a nova infraestrutura gore completamente os seus objetivos. Não ficará nada satisfeito com a indemnização que viria a receber pois é muito menor que o lucro que podia vir a retirar do investimento. Poderá esse amigo vir a influenciar o caderno de encargos por forma a que a linha contorne estes terrenos? Quanto será suficiente para convencer o nosso autarca?")

luva = 10
luva = st.slider('Luva (em milhares de euros) a pagar ao autarca', 10, 250)
comprimento_final = comprimento_inicial
corrompido = False

if luva >= 50:
    corrompido = True

if corrompido:
    ligacoes, comprimento_final = otimizar_rede(estacoes, estacoes_afetadas)
    contorno_fig = desenhar_rede(estacoes, ligacoes, comprimento_final, casa_amigo_autarca, lucro*25)
    st.pyplot(contorno_fig)

    st.write("O autarca convenceu-se com o donativo e viciará o concurso para que a ligação que passa no terreno do amigo não possa ser estabelecida. Esta decisão beneficiará o próprio, que ficará com os bolsos mais cheios. Beneficiará o amigo, que poderá fazer desimpedidamente um investimento lucrativo. No entanto, o custo adicional da infraestrutura será distribuído por todos os contribuintes da cidade, que fica com uma rede mais ineficiente, mais cara e sem poder investir a diferença noutro qualquer projeto público.")

    st.write(f"Custo Inicial da Obra: {10*comprimento_inicial:.2f} milhões de euros")
    st.write(f"Custo Final da Obra: {10* comprimento_final:.2f} milhões de euros")
    st.write(f"Luva paga ao político: {luva:.0f} mil euros")
    beneficio = lucro - luva/1000
    st.write(f"Benefício para o empresário ao corromper: {beneficio:.2f} milhões de euros")
    custo_corrupcao = 10*(comprimento_final - comprimento_inicial)
    st.write(f"Verdadeiro custo da corrupção: {custo_corrupcao:.2f} milhões de euros")

    st.write("Estabelecido com este exercício um exemplo concreto de um mecanismo de rentismo, resta-nos concluir que, face às conclusões da Teoria da Escolha Pública e da inevitabilidade das economias mistas e, praticamente, da existência de corrupção e rentismo em democracias representativas, é aos indivíduos que cabe a exigência de soberania sobre as suas próprias decisões, de reformas que limitem a arbitrariedade do poder público, e de serem a força que faz pender a sociedade no sentido de ser mais aberta e livre, que em última instância resultará numa economia mais eficiente e em mais justiça para todos.")


