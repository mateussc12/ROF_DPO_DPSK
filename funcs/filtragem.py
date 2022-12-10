import numpy as np


def Filtro_retangular(Signal, FBW, fc, f):
    """
    Filtro retangular ideal centrado em 0 (passa-baixas)
    :param Signal: Sinal
    :param FBW: Banda do filtro
    :param fc: Frequência central
    :param f: Vetor de frequências
    :return: Resposta em freq do filtro
    """
    Resp_freq_filtro = np.zeros(len(f))

    Resp_freq_filtro[((fc - FBW / 2) < f) & (f < (fc + FBW / 2))] = 1

    Signal_filtered_FFT = np.fft.fftshift(np.fft.fft(Signal)) * Resp_freq_filtro

    Signal_filtered = np.fft.ifft(np.fft.fftshift(Signal_filtered_FFT))

    return Signal_filtered


def Filtro_select(select, Signal, FBW, fc, f):
    if select == 0:
        return Signal
    if select == 1:
        return Filtro_retangular(Signal, FBW, fc, f)
