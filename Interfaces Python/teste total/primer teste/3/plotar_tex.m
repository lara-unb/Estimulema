clc
close all
clear

figure();
hold on
x = 3;
for R = 1:19
    str_txt = "3 (" + int2str(R) + ").txt";
    force1 = textread(str_txt,'','delimiter', ';');
    plot(force1(:,2))
    
%     str_lb = "Gra: " + int2str(R);
%     legend(str_lb)
    pause(2);
    if R > x
        %str_lb = "Gra: " + int2str(R);
        legend("1", "2", "3", "4")
        figure();
        hold on
        x = R + 4;
    end
end


str_txt = "3/3 (" + int2str(1) + ").txt";
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