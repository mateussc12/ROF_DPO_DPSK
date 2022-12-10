# De acordo com o livro (Optics and photonics) Binh, Le Nguyen-Digital Optical Communications, a partir da pag 20 e a tese de Mestrado do Pablo Marciano
import numpy as np
def MZM(E_in, V_1, V_2, V_pi=4, V_0=2):
    """
    Modelo de um MZM
    :param E_in: Campo de entrada
    :param V_1: Tensão de bias mais sinal RF do braço 1
    :param V_2: Tensão de bias mais sinal RF do braço 2
    :param V_pi: Tensão característica
    :return: Campo de saída
    """

    E_out = E_in * np.cos((np.pi/(2 * V_pi)) * (V_1 - V_2 - V_0)) * np.exp(1j * (np.pi/(2 * V_pi)) * (V_1 + V_2))

    return E_out