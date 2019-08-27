clc
close all
clear

acel_load = 0;

data = textread("3load_data Fri 21 13h53.txt",'','delimiter', ';');
[vrI, s1, tmj1] = vec_res(data, 0, acel_load); % extraer, filtra, calcula y plota vector resultante

figure();
plot(vrI);

% data = textread("3acel_data Fri 21 14h08.txt",'','delimiter', ';');
% [vrF, s, tmj] = vec_res(data, 0); % extraer, filtra, calcula y plota vector resultante




if acel_load == 1
    freq = 1100;
    tamVector = length(vrI);
    period = 1/freq; % Periodo de la señal
    total_time_r = tamVector*period; % Vector con el paso de acuerdo con el perido
    time_vx = linspace(0,total_time_r,tamVector);
    
    vrI = vrI * (9.81/16384.0); % Primero normalizo a m/s^2
    
    % Sinal Filtrado
    
    of = 6;%Ordem do filtro
    fc = 20;%Frequencia de corte
    fs = freq;%Taxa de amostragem
    rp = 0.2;
    
    %Desenho do filtro
    lpFilt = designfilt('lowpassiir','FilterOrder',of,'PassbandFrequency',fc,'PassbandRipple',rp,'SampleRate',fs);
    
    % fILTRANDO
    vrI = filter(lpFilt,vrI);
    
    figure();
    hold on;
    plot(time_vx, vrI(:,1), 'b');
    % plot(vrF(:,1), 'r');
    % plot(time_vx, s1*max(vrI), 'g');
    xlim([0 60]);
    grid on
    grid minor
    set(gca,'Fontsize',13)
    set(gca,'Fontname','Times New Roman')
    xlabel('t[s]');
    ylabel('Força especifica [g]');
    % title('Sinal de aceleraçao bruto do eixo Z')
else
    media = median(vrI);
    th = ones(length(vrI),1) .* media;
    vrI = vrI - media;
    freq = 11;
    tamVector = length(vrI);
    period = 1/freq; % Periodo de la señal
    total_time_r = tamVector*period; % Vector con el paso de acuerdo con el perido
    time_vx = linspace(0,total_time_r,tamVector);
    
    figure();
    hold on;
    plot(time_vx, vrI(:,1), 'r');
%     plot(time_vx, th, 'r')
    
    xlim([0 60]);
    ylim([-0.1 (max(vrI)+0.1)]);
    grid on
    grid minor
    set(gca,'Fontsize',13)
    set(gca,'Fontname','Times New Roman')
    xlabel('t[s]');
    ylabel('Força [kg.m/s^2]');
    
end

