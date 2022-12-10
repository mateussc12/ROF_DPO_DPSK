import numpy as np


def digitalize(signal, NPPS, N_Simb, treshold):
    """
    Filtra os dados obtidos do MDO
    :param unnormalized_wave: Vetor obtido da captura da tela do MDO
    :param NPPS: Pontos por periodo
    :param N_Simb: Numero de simbolos
    :param threshold: Limite a ser filtrado
    :return: A onda binária, com o downsample
    """

    N_Simb = N_Simb - 1

    Rx_bin_wave = np.zeros(N_Simb)

    if treshold == 'mean':
        treshold = np.mean(signal)

    for i in range(N_Simb):

        intervalo_media = np.mean(signal[int(i * NPPS):int((i + 1) * NPPS)])

        if np.greater_equal(intervalo_media, treshold):
            Rx_bin_wave[i] = 1

    return Rx_bin_wave


def Eye_treshold(signal):
    """
    Calcula o limiar de decisão baseado no diagrama de olho
    :param normalized_wave: normalized wave
    :return: limiar de decisão
    """
    # Média das amostras
    mean_diagram_position = np.mean(signal)
    # Amostras acima da média
    pos_diagram_position_vector = []
    # Amostras abaixo da média
    neg_diagram_position_vector = []
    for sample in signal:
        if sample >= mean_diagram_position:
            pos_diagram_position_vector.append(sample)
        else:
            neg_diagram_position_vector.append(sample)

    pos_diagram_position = np.mean(pos_diagram_position_vector) - np.std(pos_diagram_position_vector)
    neg_diagram_position = np.mean(neg_diagram_position_vector) + np.std(neg_diagram_position_vector)

    eye_treshold = (pos_diagram_position + neg_diagram_position) / 2

    return eye_treshold

