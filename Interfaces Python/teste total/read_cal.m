clc
close all
clear

data = textread("3load_data Wed 26 15h25.txt",'','delimiter', ';');
plot(data(:,1))

% data = textread("1cal_acel_data Sun 23 18h22.xtxt",'','delimiter', ';');
data = textread("3acel_data Wed 26 15h27.txt",'','delimiter', ';');
[vrI, s, tmj] = vec_res(data, 1); % extraer, filtra, calcula y plota vector resultante

% data = textread("3acel_data Fri 21 14h08.txt",'','delimiter', ';');
% [vrF, s, tmj] = vec_res(data, 0); % extraer, filtra, calcula y plota vector resultante

figure();
hold on;
plot(vrI(:,1), 'b');
% plot(vrF(:,1), 'r');
plot(s*max(vrI), 'g');


%Valores que normalizan el eje X
freq = 1151;
period = 1/freq;%periodo de la seï¿½al
total_time_r = length(vrI)*period;%Vector con el paso de acuerdo con el perido
time_vector_r = linspace(0,total_time_r,length(vrI));

qd = vrI;
% qd = qd ./ max(qd);
% qd = qd * 2.5;

qd2 = medfilt1(qd, 5);

% bruto inal
figure();
% subplot(211);
% plot(time_vector_r, qd);
xlabel('t[s]');
ylabel('Força específica [g]');
xlim([0 20]);
ylim([-0.065 0.065]);
% title('Sinal de aceleraï¿½ï¿½o bruto do vetor resultante');
grid on
grid minor
hold on
% plot(time_vector_r, s);
plot(time_vector_r,qd2)

%% filtro butter
fil = 3;

if fil == 1
    
    Fc = 20; % freq de corte
    Wn = Fc / (freq/2);
    of = 10; % orden do filtro
    [num, den] = butter(of,Wn,'low');
    qdf = filter(num, den, qd);
end

if fil == 2
    of = 10;%Ordem do filtro
    fc = 20;%Frequencia de corte
    fs = freq;%Taxa de amostragem
    rp = 0.2;
    
    %Desenho do filtro
    lpFilt = designfilt('lowpassiir','FilterOrder',of,'PassbandFrequency',fc,'PassbandRipple',rp, ...
        'SampleRate',fs);
    
    % sinal filtrado
    qdf = filter(lpFilt,qd);
end

if fil == 3
    of = 10;%Ordem do filtro
    fc1 = 4;
    fc2 = 20;
    %Desenho do filtro
    bpFilt = designfilt('bandpassiir','FilterOrder',of, ...
        'HalfPowerFrequency1',fc1,'HalfPowerFrequency2',fc2, ...
        'SampleRate',freq);
    
    % sinal filtrado
    qdf = filter(bpFilt,qd);
end


figure();
% subplot(211);

xlabel('t[s]');
ylabel('Força específica [g]');
xlim([0 20]);
ylim([-0.07 0.07]);
% title('Sinal de aceleraï¿½ï¿½o bruto do vetor resultante');
grid on
grid minor
hold on
% plot(time_vector_r, s*0.062);

legend('Sinal filtrado','Sinal controle de estimulação');
text(2.2,-0.008,'2mA');
text(5.2,-0.008,'3mA');
text(8.2,-0.008,'4mA');

%% calculo do theshold

xlim([11 12]);
ylim([-0.035 0.035]);

st = std(qdf);
% media = median(qd);

th = ones(length(qd),1) * (st * 2.4);
plot(time_vector_r, th);
plot(time_vector_r, qdf);
legend('Dados janela 4mA','Threshold');
