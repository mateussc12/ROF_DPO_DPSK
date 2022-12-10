clc; clear;

M = 2; % Modulation Order
EbNo = 0:2:12;

berD = berawgn(EbNo,'dpsk',M);
semilogy(EbNo, berD)

csvwrite('EbNo.csv', EbNo);
csvwrite('Ber_DPSK.csv', berD);