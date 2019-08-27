clc 
close all
clear

data = textread("1cal_acel_data Fri 21 13h50.txt",'','delimiter', ';');

figure();
hold on
plot(data(:,2))
plot(data(:,3))
plot(data(:,4))


figure();
hold on
x = medfilt1(data(:,2), 5);
y = medfilt1(data(:,3), 5);
z = medfilt1(data(:,4), 5);
plot(x);
plot(y);
plot(z);

vr = data(:, 2).^2 + data(:, 3).^2 + data(:, 4).^2;
vr = sqrt(vr);

figure();
plot(vr);

% figure();
% plot(data(:,5))