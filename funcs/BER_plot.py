import matplotlib.pyplot as plt
import os
import numpy as np


def BER_plot(SNR_vector, BER_vector, current_dir, matlab_ref):


    if matlab_ref:
        # Dados vindo do arquivo do matlab
        Ber_dpsk_teorico = np.genfromtxt(os.path.join(current_dir, 'matlab', 'Ber_DPSK.csv'), delimiter=',')

        plt.figure(figsize=[12.8, 9.6], layout='tight')
        plt.semilogy(SNR_vector, BER_vector, 'ro', label='BER_simulado')
        plt.semilogy(SNR_vector, Ber_dpsk_teorico, label='BER_teorico')
        plt.title(f'Curva de BER')
        plt.xlabel('SNR (dB)')
        plt.ylabel('BER')
        plt.legend()
        plt.savefig(os.path.join(current_dir, 'BER', 'BER_plot'))
        plt.close()

    else:
        plt.figure(figsize=[12.8, 9.6], layout='tight')
        plt.semilogy(SNR_vector, BER_vector, label='BER_simulado')
        plt.title(f'Curva de BER')
        plt.xlabel('SNR (dB)')
        plt.ylabel('BER')
        plt.legend()
        plt.savefig(os.path.join(current_dir, 'BER', 'BER_plot'))
        plt.close()
