clc
close all
clear

str_txt = "3 (" + int2str(1) + ")";
force1 = textread(str_txt,'','delimiter', ';');
plot(force1(:,2))


figure();
force1 = textread('3acel_data Mon 08 19h04.txt','','delimiter', ';');
plot(force1(:,2))
force1 = textread('3acel_data Mon 08 19h08.txt','','delimiter', ';');
plot(force1(:,2))
% force1 = textread('3load_data Mon 08 19h04.txt','','delimiter', ';');
% plot(force1(:,2))
% force1 = textread('3load_data Mon 08 19h04.txt','','delimiter', ';');
% plot(force1(:,2))

figure();
hold on
acel = textread('2acel_data Mon 08 18h24.txt','','delimiter', ';');
plot(acel(:,2))
acel = textread('2acel_data Mon 08 18h25.txt','','delimiter', ';');
plot(acel(:,2))
acel = textread('2acel_data Mon 08 18h26.txt','','delimiter', ';');
plot(acel(:,2))
acel = textread('2acel_data Mon 08 18h27.txt','','delimiter', ';');
plot(acel(:,2))

figure();
hold on
acel = textread('2acel_data Mon 08 18h24.txt','','delimiter', ';');
plot(acel(:,3))
acel = textread('2acel_data Mon 08 18h25.txt','','delimiter', ';');
plot(acel(:,3))
acel = textread('2acel_data Mon 08 18h26.txt','','delimiter', ';');
plot(acel(:,3))
acel = textread('2acel_data Mon 08 18h27.txt','','delimiter', ';');
plot(acel(:,3))

figure();
hold on
acel = textread('2acel_data Mon 08 18h24.txt','','delimiter', ';');
plot(acel(:,4))
acel = textread('2acel_data Mon 08 18h25.txt','','delimiter', ';');
plot(acel(:,4))
acel = textread('2acel_data Mon 08 18h26.txt','','delimiter', ';');
plot(acel(:,4))
acel = textread('2acel_data Mon 08 18h27.txt','','delimiter', ';');
plot(acel(:,4))