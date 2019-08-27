clc
close all
clear

figure();
subplot(311);
title('Load Cell values');
hold on
x = 3;

total = 13;
pd = zeros(total,1);

for R = 1:total
    str_txt = "3 (" + int2str(R) + ").txt";
    force1 = csvread(str_txt);
    rr = findpeaks(force1, 'MinPeakDistance', 100);
    pd(R,1) = max(rr);
    plot(force1)
end

tex = csvread('tex.txt');
ptex = tex(1:length(tex)-1);
subplot(312);
plot(pd);
title('Peak force values');
ylabel('kg');
subplot(313);
plot(ptex);
title('Rheobase values');
ylabel('mA');

figure();
plot(ptex, pd, '*');
hold on
rel = fit(ptex, pd,'poly3','Normalize','on','Robust','Bisquare');
plot(rel);
rel = fit(ptex, pd,'poly2');
plot(rel, 'g');

legend('rh vs loadcell','poly3','poly2')
title('Correlation');
ylabel('Loadcell peaks');
xlabel('Rh values');
