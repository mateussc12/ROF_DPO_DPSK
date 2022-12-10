import numpy as np
from funcs import time2freq


def Delay_Interf(t, f, Time_Delay, E1, CoupConst=3*np.pi/4, ExpCoef=np.exp(-1j*np.pi/4), MutCoef=-1, Phase_Delay=0, E0=None):
    """
    This function is responsible for implementing an Delay Interferometer
    (DI). There many ways that this device can be implemented such as MZM,
    passive components and couples with diffe light paths. This script will
    inplement a DI ussing 3dB couples with 2-input and 2-outputs. The delay
    given will be implement by light paths with different lengths and the
    phase delay will be achieve with a phase controler. This will be the
    principal and only device used to implement an All Optica FFT. Aiming to
    separate subcarriers from an OFDM signal and convert from serial to
    paralel.

    :param t: Time vector of the whole simulation [s]
    :param Time_Delay: Time delay to be implemented by the DI
    :param E1: Principal input signal to be implemented
    :param CoupConst: Couples Constant of the DI
    :param ExpCoef: Exponential component from Ramaswami equation
    :param MutCoef: Coeficient to control polarity
    :param Phase_Delay: Phase delay to be implemented by the DI
    :param E0: Secundary input signal (usualy it is zero)
    :return:
    Eout1     : Output1 from the DI interfometric response
    Eout2     : Output2 from the DI interfometric response
    """

    if E0 == None:
        E0 = np.zeros(len(E1))

    """
    * Stage: 1 spliting the principal input signal
    Fristly it is needed to divide the signal in two given that by the length
    difference of the optical pahts and the phase delay btween them the
    signals will interfere with one another.
    split
    An 3dB coupler with 2 inputs and 2 outputs is used to slplit the input
    signal.
    The couples will output two signals that are a combination of E1 and E0.
    As E0 = 0 the out put will be just the E1 signal slpit in two. The name 
    notation E11 means the E1 signal at the arm 1 (uper arm) hence the 
    notation name E12 means the E1 signal at the arm 2 (Lower arm).
    """

    E11 = ExpCoef * (np.cos(CoupConst) * E1 + MutCoef * 1j * np.sin(CoupConst) * E0)
    E12 = ExpCoef * (np.cos(CoupConst) * E0 + MutCoef * 1j * np.sin(CoupConst) * E1)

    """
    * Stage: 2 Changing the signal at the lower arm
    Dellay and change phase
    Firstly it is taken in acont what means for the input signal a time 
    delay by measuring the input time vector
    aux1 = E12(t<=TimDel);
    f=time2freq(t);

    Secondly the signal will be delayed by rotation its possition. That 
    means a circular rith-shift will be performed. The number of possition 
    to be deslocated will be given by the number of point that represent the 
    delay based on the input time vector given as input. The time delay
    time accuracy depends on the time vector accuracy.
    E12d = [E12(end-(length(aux1)-1):end) E12(1:end-(length(aux1)))];
    """
    #aux1 = E12(t <= TimDel)
    """E12
    cont = 0
    for i in range(len(t)):
        if t[i] <= Time_Delay:
            cont += 1
        else:
            break
    print(cont)
    cont = int(cont)
    aux = np.zeros(2 * cont)
    aux[aux == 0] = np.min(E12)
    E12d = np.concatenate((aux, (E12[int(2*cont)::])))
    """
    #E12d = [E12(end - (length(aux1) - 1):end) E12(1: end - (length(aux1)))]

    E12d = np.fft.ifft(np.fft.fft(E12) * np.exp(-1j * 2 * np.pi * Time_Delay * f))

    """
    In practice the phase delay will be perfomed by an phase controler. In
    the simulation it will be done by multiplying the input signal by a
    complex neperian exponential where the argument was received as an input
    %parameters.
    The nema notation means that the E12 was Delayed thus E12d
    """

    E12d = E12d * np.exp(-1j * Phase_Delay)

    """
    * Stage: 3 Recombining both signals
    Combining singnals
    Similarly to te input step. An 3dB coupler with 2 inputs and 2 outputs is
    used to combine the input signals from the arm1 and arm2. The couples 
    will output two signals that are a combination of E12 and E12d.
    Thus the Eout1 is the combination of E11 and E12d wich will be out put
    at the port 1 of the couples. Hence, Eout2 is the combination of E11 and
    E12d wich will be out put at the port 2.
    """

    Eout1 = ExpCoef * (np.cos(CoupConst) * E11 + MutCoef * 1j * np.sin(CoupConst) * E12d)
    Eout2 = ExpCoef * (np.cos(CoupConst) * E12d + MutCoef * 1j * np.sin(CoupConst) * E11)

    return Eout1, Eout2
