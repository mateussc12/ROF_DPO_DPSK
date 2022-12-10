import numpy as np


def BER(vetor1, vetor2):
    """
    Calcula a BER entre dois vetores binários
    :param vetor1:
    :param vetor2:
    :return: BER
    """

    BER = np.logical_xor(vetor1, vetor2).sum() / len(vetor1)

    return BER
