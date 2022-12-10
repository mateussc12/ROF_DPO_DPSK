import matplotlib.pyplot as plt
import numpy as np
from funcs import BER
from funcs import digitalize
from funcs import eye_diagram
import os
from scipy import signal


def debug(plot_enable, Tx_bin_wave, V_1, V_2, Tx_bin_wave_DPSK_encoded, NPPS, t, E_out, E_out_noise, Esync_filtered,
          Esync, ESync1, ESync2, Num_Simb, SNR, Ts, eye_enable, current_dir, log_file, dig_decision, N_Simb):
    """
    Em modulacao DPSK devido a falta de referencia o primeiro simbolo pode perder seu valor, logo o mesmo dever ser
    ignorado no calculo da BER
    """

    Tx_bin_wave_cutted = np.delete(Tx_bin_wave, 0)

    Esync_filtered_cutted = np.delete(Esync_filtered, np.arange(NPPS))

    # Normaliza o sinal
    normalized_Esync_filtered_cutted = Esync_filtered_cutted / np.max(np.abs(Esync_filtered_cutted))

    ber = None
    lim = 20

    if eye_enable:

        divisao = 0.025

        """
        Cria as pastas onde os diagramas de olho serao salvos
        """
        os.mkdir(os.path.join(current_dir, 'eye_diagrams', f'SNR_{SNR}'))

        eye_signal, eye_t = eye_diagram.eye_diagram(normalized_Esync_filtered_cutted, Ts, NPPS)

        fig6, (ax, ax1) = plt.subplots(1, 2, sharey=True, width_ratios=[0.8, 0.2], figsize=[12.8, 9.6], layout='tight')
        for eye_period in eye_signal:
            ax.plot(eye_t, np.real(eye_period), color='b', linewidth=0.5)
        n, bins, patches = ax1.hist(np.real(np.array(eye_signal).flatten()), np.arange(-1, 1.001, divisao),
                                    orientation='horizontal', color='b')
        ax.set_title(f"Diagrama de olho para SNR = {SNR}")
        plt.savefig(os.path.join(current_dir, 'eye_diagrams', f'SNR_{SNR}', 'eye_diagram'))
        plt.close()

        with open(log_file, 'a', encoding='utf-8') as file:
            file.write("Histograma Diagrama de Olho:\n")

        for value_index in range(len(n)):
            with open(log_file, 'a', encoding='utf-8') as file:
                file.write(f'Intervalo {np.round(bins[value_index], 3)} a {np.round(bins[value_index + 1], 3)} = {n[value_index]} vezes\n')

    if dig_decision == 1:
        Rx_bin_wave = digitalize.digitalize(normalized_Esync_filtered_cutted, NPPS, Num_Simb, treshold=0)
    elif dig_decision == 2:
        Rx_bin_wave = digitalize.digitalize(normalized_Esync_filtered_cutted, NPPS, Num_Simb, treshold='mean')
    elif dig_decision == 3:
        eye_treshold = digitalize.Eye_treshold(normalized_Esync_filtered_cutted)
        Rx_bin_wave = digitalize.digitalize(normalized_Esync_filtered_cutted, NPPS, N_Simb, treshold=eye_treshold)

    ber = BER.BER(Tx_bin_wave_cutted, Rx_bin_wave)
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(f'BER = {ber}\n')

    if plot_enable:

        """
        Cria as pastas onde os plots serao salvos
        """
        os.mkdir(os.path.join(current_dir, 'plots', f'SNR_{SNR}'))

        fig0, (ax, ax1, ax2, ax3) = plt.subplots(4, 1, figsize=[12.8, 9.6], layout='tight')
        ax.stairs(Tx_bin_wave, label='Tx_bin_wave')
        ax1.stairs(Tx_bin_wave_DPSK_encoded, label='Tx_bin_wave_DPSK_encoded')
        ax2.stairs(V_1, label=' V_1')
        ax3.stairs(np.real(V_2), label='real V_2')
        ax.set_xlim(0, lim)
        ax1.set_xlim(0, lim * NPPS)
        ax2.set_xlim(0, lim * NPPS)
        ax3.set_xlim(0, lim * NPPS)
        ax.legend()
        ax1.legend()
        ax2.legend()
        ax3.legend()
        plt.savefig(os.path.join(current_dir, 'plots', f'SNR_{SNR}', 'fig0'))
        plt.close()

        fig1, (ax, ax1) = plt.subplots(2, 1, figsize=[12.8, 9.6], layout='tight')
        ax.plot(t, np.real(E_out), label='real E_out')
        ax1.plot(t, np.real(E_out_noise), label='real E_out_noise')
        ax.set_xlim(0, t[int(lim * NPPS)])
        ax1.set_xlim(0, t[int(lim * NPPS)])
        ax.legend()
        ax1.legend()
        plt.savefig(os.path.join(current_dir, 'plots', f'SNR_{SNR}', 'fig1'))
        plt.close()

        fig2, (ax, ax1, ax2) = plt.subplots(3, 1, figsize=[12.8, 9.6], layout='tight')
        ax2.plot(t, np.real(Esync), label='real(Esync) = real(Esync2 - Esync1)')
        ax1.plot(t, np.real(ESync1), label='real(Esync1)')
        ax.plot(t, np.real(ESync2), label='real(Esync2)')
        ax.set_xlim(0, t[int(lim * NPPS)])
        ax1.set_xlim(0, t[int(lim * NPPS)])
        ax2.set_xlim(0, t[int(lim * NPPS)])
        ax.legend()
        ax1.legend()
        ax2.legend()
        plt.savefig(os.path.join(current_dir, 'plots', f'SNR_{SNR}', 'fig2'))
        plt.close()

        fig3, (ax, ax1) = plt.subplots(2, 1, figsize=[12.8, 9.6], layout='tight')
        ax.plot(t, np.real(Esync), label='real(Esync)')
        ax1.plot(t, np.real(Esync_filtered), label='real(Esync_filtered)')
        ax.set_xlim(0, t[int(lim * NPPS)])
        ax1.set_xlim(0, t[int(lim * NPPS)])
        ax.legend()
        ax1.legend()
        plt.savefig(os.path.join(current_dir, 'plots', f'SNR_{SNR}', 'fig3'))
        plt.close()

        if dig_decision == 3:
            plt.figure(figsize=[12.8, 9.6], layout='tight')
            plt.plot(np.real(normalized_Esync_filtered_cutted))
            plt.plot(np.zeros(np.size(normalized_Esync_filtered_cutted)), label='0')
            mean = np.mean(normalized_Esync_filtered_cutted)
            plt.plot(np.repeat(mean, np.size(normalized_Esync_filtered_cutted)), label=f'mean = {np.round(np.real(mean), 5)}', linewidth=3)
            plt.plot(np.repeat(eye_treshold, np.size(normalized_Esync_filtered_cutted)),
                     label=f'eye_treshold = {np.round(np.real(eye_treshold), 5)}')
            plt.title("Comparação entre os niveis de decisão")
            plt.legend(loc=1)
            plt.ylim([-0.25, 0.25])
            plt.savefig(os.path.join(current_dir, 'plots', f'SNR_{SNR}', 'treshold'))
            plt.close()

        fig5, (ax, ax1) = plt.subplots(2, 1, figsize=[12.8, 9.6], layout='tight')
        ax.stairs(Tx_bin_wave, label='Tx_bin_wave')
        ax1.stairs(Rx_bin_wave, label='Rx_bin_wave')
        ax.set_xlim(0, lim)
        ax1.set_xlim(0, lim)
        ax.legend()
        ax1.legend()
        plt.savefig(os.path.join(current_dir, 'plots', f'SNR_{SNR}', 'Comparação_Tx_Rx'))
        plt.close()

    return ber
