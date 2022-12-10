"""
Simulação de transmissão DPSK em Banda Base usando o AWGN/DPO como canal

IMPORTANTE = em modulucao DPSK o primeiro bit da PRBS e perdido, uma vez que devido a falta de referencia na codificacao
DPSK a recepcao pode errar seu valor.
"""
import numpy as np
import time
import os
import shutil
from datetime import datetime
from funcs import time2freq
from funcs import MZM
from funcs import DPSK_encoder
from funcs import Delay_Interf
from funcs import filtragem
from funcs import Fotodetector
from funcs import AWGN_noise
from funcs import debug
from funcs import BER_plot
from funcs import Eb_No2SNR


###################################################Parametrização#######################################################
current_dir = os.getcwd()
time_start = time.time()
Fs = 10e9                                           # Baud Rate (Symbol rate)
Fc = Fs                                             # Optical carrier
Num_Simb = 2**12                                    # Number of Simbols (Bits DPSK)
NyQ = 16                                            # Nyquist Theorem
Fa = NyQ * Fc                                       # Sample Rate
Ts = 1 / Fs                                         # Baud Rate Time Period
Ta = 1 / Fa                                         # Sample Rate Time Period
NPPS = int(np.round(Ts / Ta))                       # Numero de pontos por simbolo
Num_pontos = Num_Simb * NPPS                        # Numero de pontos da simulação
t = np.linspace(0, Num_Simb * Ts, int(Num_pontos))  # Time Vector
f = time2freq.time2freq(t)                          # Frequency Vector
Cw = np.ones(int(Num_pontos))                       # Fonte Cw
Eb_No_vector = np.genfromtxt(os.path.join(current_dir, 'matlab', 'EbNo.csv'), delimiter=',')
SNR_vector = np.round(Eb_No2SNR.Eb_No2SNR(Eb_No_vector, Ts, Ta, 2), 4)
########################################################################################################################

#################################################dedbug#################################################################
debug_enable = 1  # Permite debug
plot_enable = 1   # Permite plotagens
eye_enable = 1    # Permite diagrama de olho
filtro = 0        # Filtragem: 0 Sem filtragem, 1 Filtro Retangular, 2 Gaussiano
matlab_ref = 1    # Permite comparacao com curva teorica do matlab
dig_decision = 3  # Decisão de digitalizacao, 1 - 0, 2 - media, 3 - Treshold eye
########################################################################################################################

######################################################Escrita em arquivo################################################
log_file = 'simulation_log.txt'
with open(log_file, 'w', encoding='utf-8'):
    pass
with open(log_file, 'a', encoding='utf-8') as file:
    file.write(f"Resultados da simulacao de modulacao DPSK em banda base em Rof:\n")
    file.write(f"Com SNR variando de {SNR_vector[0]} dB a {SNR_vector[-1]} dB:\n")
    file.write(f"Numero de pontos por simbolo (NPPS) = {Ts / Ta}\n")
    file.write(f"Numero de pontos da simulacao por iteracao de SNR = {Num_pontos}\n")
    file.write(f"Numero de pontos total da simulacao = {Num_pontos * len(SNR_vector)}\n")
    if filtro == 0:
        file.write(f'Filtro Selecionado = Sem filtro\n')
    if filtro == 1:
        file.write(f'Filtro Selecionado = Filtro Retangular\n')
    if filtro == 2:
        file.write(f'Filtro Selecionado = Filtro Gaussiano\n')
    file.write(f"plot_enable = {plot_enable}\n")
    file.write(f"eye_enable = {eye_enable}\n")
    if dig_decision == 1:
        file.write(f'Decisão de digitalização = 0\n')
    elif dig_decision == 2:
        file.write(f'Decisão de digitalização = media\n')
    elif dig_decision == 3:
        file.write(f'Decisão de digitalização = Treshold Histograma\n')
    file.write(f"Simulacao foi iniciada em {datetime.now()}\n")
########################################################################################################################

#######################################Criacao dos dados e codificação DPSK (Transmissao)###############################
Tx_bin_wave = np.random.choice([0, 1], int(Num_Simb))

Tx_bin_wave_DPSK_encoded_aux = DPSK_encoder.DPSK_encoder(Tx_bin_wave)

Tx_bin_wave_DPSK_encoded = np.repeat(Tx_bin_wave_DPSK_encoded_aux, NPPS)

# Para a recepcao, de forma que o MZM decodifique os Dados o valores tem que estar em Vpi/2 ou -Vpi/2
Tx_bin_wave_DPSK_encoded[Tx_bin_wave_DPSK_encoded == 1] = 2
Tx_bin_wave_DPSK_encoded[Tx_bin_wave_DPSK_encoded == 0] = -2

# Sinais Bias para entrar no MZM
V_1 = Tx_bin_wave_DPSK_encoded
V_2 = np.exp(-1j * np.pi) * V_1

# Saída do MZM
E_out = MZM.MZM(Cw, V_1, V_2)
########################################################################################################################

###########################################Apaga e Cria Arquivos########################################################
if debug_enable:
    try:
        shutil.rmtree(os.path.join(current_dir, 'plots'))
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(os.path.join(current_dir, 'eye_diagrams'))
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(os.path.join(current_dir, 'BER'))
    except FileNotFoundError:
        pass
    os.mkdir(os.path.join(current_dir, 'plots'))
    os.mkdir(os.path.join(current_dir, 'eye_diagrams'))
    os.mkdir(os.path.join(current_dir, 'BER'))
########################################################################################################################

################################################Calculos para cada SNR##################################################
BER_vector = []
print(f'Simulacao com SNR variando de {SNR_vector[0]} dB a {SNR_vector[-1]} dB:')
for SNR_index in range(np.size(SNR_vector)):

    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(f"##############################################################################\n")
        file.write(f"Para SNR = {SNR_vector[SNR_index]} dB\n")

    #######################################Canal AGWN (ruido)###########################################################
    E_out_noise = AWGN_noise.AWGN_noise(E_out, SNR_vector[SNR_index], NPPS)
    ####################################################################################################################

    #########################################################Recepcao###################################################
    # Delay interferometrico
    ESync1, ESync2 = Delay_Interf.Delay_Interf(t, f, Time_Delay=Ts, Phase_Delay=0, E1=E_out_noise)
    ESync1 = Fotodetector.Fotodetector(ESync1)
    ESync2 = Fotodetector.Fotodetector(ESync2)
    Esync = ESync2 - ESync1
    ####################################################################################################################

    ###########################################################AWG######################################################

    ####################################################################################################################

    ############################################################DPO#####################################################

    ####################################################################################################################

    #########################################################Filtragem##################################################
    Esync_filtered = filtragem.Filtro_select(filtro, Esync, 3 * Fs, 0, f)
    ####################################################################################################################

    ###############################################Debug################################################################
    if debug_enable:
        BER_vector.append(debug.debug(plot_enable, Tx_bin_wave, V_1, V_2, Tx_bin_wave_DPSK_encoded, NPPS, t, E_out,
                                      E_out_noise, Esync_filtered, Esync, ESync1, ESync2, Num_Simb,
                                      SNR_vector[SNR_index], Ts, eye_enable, current_dir, log_file, dig_decision, Num_Simb))

    ####################################################################################################################
    print(f'Simulacao com SNR = {SNR_vector[SNR_index]} completa ({SNR_index + 1}/{np.size(SNR_vector)})')
########################################################################################################################
BER_plot.BER_plot(SNR_vector, BER_vector, current_dir, matlab_ref)
print(f'Simulacao com plot de BER completa')

time_end = time.time()
with open(log_file, 'a', encoding='utf-8') as file:
    file.write(f"##############################################################################\n")
    file.write(f"Fim da simulacao = {datetime.now()}\n")
    file.write(f"Tempo total de simulacao = {time.strftime('%H:%M:%S', time.gmtime(time_end - time_start))}\n")
