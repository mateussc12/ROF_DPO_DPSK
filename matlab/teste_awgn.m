clc; clear;

t = (0:0.1:60)';
x = sin(t);
SNR = 15;

y = awgn(x,SNR,'measured');

csvwrite('t.csv', t);
csvwrite('x.csv', x);
csvwrite('y.csv', y);