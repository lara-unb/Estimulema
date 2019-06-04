clc
% close all
clear

figure();
subplot(311);
title('Load Cell values');
hold on
x = 3;

total = 6;
pdlc = zeros(1,total);

for R = 1:total

    str_txt = "3 (" + int2str(R) + ").txt";
    %force1 = textread(str_txt,'','delimiter', ';');
    force1 = csvread(str_txt);
    rr = findpeaks(force1, 'MinPeakDistance', 100);
    pdlc(R,1) = max(rr);
    plot(force1)
    
%     str_lb = "Gra: " + int2str(R);
%     legend(str_lb)
    pause(1);
%     if R > x
%         %str_lb = "Gra: " + int2str(R);
%         legend("1", "2", "3", "4")
%         figure();
%         hold on
%         x = R + 4;
%     end
end

tex = csvread('tex.txt');
ptex = tex(1:length(tex)-1);
subplot(312);
plot(pdlc);
title('Peak force values');
subplot(313);
plot(tex);
title('Rheobase values');

total = 6;
pdtex = zeros(1,total);

for R = 1:total

    str_txt = "3 (" + int2str(R) + ").txt";
    force1 = textread(str_txt,'','delimiter', ';');
    
    
%     force1 = csvread(str_txt);
    rr = findpeaks(force1(), 'MinPeakDistance', 100);
    pdtex(R,1) = max(rr);
    plot(force1)
    
%     str_lb = "Gra: " + int2str(R);
%     legend(str_lb)
    pause(1);
%     if R > x
%         %str_lb = "Gra: " + int2str(R);
%         legend("1", "2", "3", "4")
%         figure();
%         hold on
%         x = R + 4;
%     end
end




% 
% str_txt = "3/3 (" + int2str(1) + ").txt";
% force1 = textread(str_txt,'','delimiter', ';');
% plot(force1(:,2))
% 
% 
% figure();
% force1 = textread('3acel_data Mon 08 19h04.txt','','delimiter', ';');
% plot(force1(:,2))
% force1 = textread('3acel_data Mon 08 19h08.txt','','delimiter', ';');
% plot(force1(:,2))
% % force1 = textread('3load_data Mon 08 19h04.txt','','delimiter', ';');
% % plot(force1(:,2))
% % force1 = textread('3load_data Mon 08 19h04.txt','','delimiter', ';');
% % plot(force1(:,2))
% 
% figure();
% hold on
% acel = textread('2acel_data Mon 08 18h24.txt','','delimiter', ';');
% plot(acel(:,2))
% acel = textread('2acel_data Mon 08 18h25.txt','','delimiter', ';');
% plot(acel(:,2))
% acel = textread('2acel_data Mon 08 18h26.txt','','delimiter', ';');
% plot(acel(:,2))
% acel = textread('2acel_data Mon 08 18h27.txt','','delimiter', ';');
% plot(acel(:,2))
% 
% figure();
% hold on
% acel = textread('2acel_data Mon 08 18h24.txt','','delimiter', ';');
% plot(acel(:,3))
% acel = textread('2acel_data Mon 08 18h25.txt','','delimiter', ';');
% plot(acel(:,3))
% acel = textread('2acel_data Mon 08 18h26.txt','','delimiter', ';');
% plot(acel(:,3))
% acel = textread('2acel_data Mon 08 18h27.txt','','delimiter', ';');
% plot(acel(:,3))
% 
% figure();
% hold on
% acel = textread('2acel_data Mon 08 18h24.txt','','delimiter', ';');
% plot(acel(:,4))
% acel = textread('2acel_data Mon 08 18h25.txt','','delimiter', ';');
% plot(acel(:,4))
% acel = textread('2acel_data Mon 08 18h26.txt','','delimiter', ';');
% plot(acel(:,4))
% acel = textread('2acel_data Mon 08 18h27.txt','','delimiter', ';');
% plot(acel(:,4))