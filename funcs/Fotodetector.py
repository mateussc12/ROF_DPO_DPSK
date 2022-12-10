import numpy as np


def Fotodetector(x_out_canal, resp=1):
    """
    Simula um fotodetector
    :param resp: Responsividade
    :param x_out_canal: Saída do MZM apos o ruído AWGN
    :return: x_out: Saída fotodetector
    """

    # responsividade = I / P
    p_in = np.sqrt(x_out_canal * np.conj(x_out_canal))
    x_out = p_in * resp

    return x_out
