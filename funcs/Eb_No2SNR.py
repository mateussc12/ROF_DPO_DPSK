import numpy as np


def Eb_No2SNR(Eb_no, Ts, Ta, M):
    """
    Converte Eb/No para SNR
    Eq -> https://www.mathworks.com/help/comm/ug/awgn-channel.html#a1071501088
    k = log2(M)
    Es/No = Eb/No + 10log10(k)
    Es/No = 10log10(T_sym/T_samp) + SNR for complex input signals
    Es/No = 10log10(0.5T_sym/T_samp) + SNR for real input signals
    Isolando SNR em funcao de Eb_No
    SNR = Eb/No + 10log10(k) - 10log10(0.5T_sym/T_samp)
    :param Eb_no:
    :param Ts:
    :param Ta:
    :param M:
    :return:
    """
    k = np.log2(M)
    SNR = (Eb_no + 10 * np.log10(k) - 10 * np.log10(0.5 * Ts / Ta)) / 2

    return SNR
