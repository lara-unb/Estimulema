function [vector_resultante, sinal, tam_janela]= vec_res(data, plot_xyz)

% calcular fre amos con sinal 0-1
sinal = data(:,5);
c = 1;
t1 = 0;
t2 = 0;

for t=1:length(sinal)
    if sinal(t, 1) == 1 && c == 1
        t1 = t;
        c = 2;
    end
    
    if sinal(t, 1) == 0 && c == 2
        t2 = t;
        c = 0;
    end
end

% dados janela inicio fim
tam_janela = [t1 t2];


% extraer data
ac_x = data(:,2);
ac_y = data(:,3);
ac_z = data(:,4);

if plot_xyz == 1
    figure();
    hold on
    plot(ac_x)
    plot(ac_y)
    plot(ac_z)
end

%filtrar
ac_x = medfilt1(ac_x);
ac_y = medfilt1(ac_y);
ac_z = medfilt1(ac_z);

if plot_xyz == 1
    figure();
    hold on
    plot(ac_x)
    plot(ac_y)
    plot(ac_z)
end

vector_resultante = ac_x.^2 + ac_y.^2 + ac_z.^2;
vector_resultante = sqrt(vector_resultante);

vector_resultante = vector_resultante .* 0.061;
vector_resultante = vector_resultante ./ 1000;
media = median(vector_resultante);
vector_resultante = vector_resultante - media;

std_vr = std(vector_resultante);
th = std(vector_resultante)*15;

for t=1:length(vector_resultante)
    if vector_resultante(t) >= th
        vector_resultante(t) = 0;
    end
    
    if vector_resultante(t) <= -th
        vector_resultante(t) = 0;
    end
    
end

if plot_xyz == 1
    figure();
    plot(vector_resultante);
end
end