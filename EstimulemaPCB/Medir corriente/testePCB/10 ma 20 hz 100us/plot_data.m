%% Import data from text file.
% Script for importing data from the following text file:
%
%    C:\Users\medua\Dropbox\00Iniciode_Doctorado\008 semestre final\EstimulemaPCB\Medir corriente\testePCB\10 ma 20 hz 100us\T0000.CSV
%
% To extend the code to different selected data or a different text file,
% generate a function instead of a script.

% Auto-generated by MATLAB on 2018/07/23 21:53:25

%% Initialize variables.
filename = 'C:\Users\medua\Dropbox\00Iniciode_Doctorado\008 semestre final\EstimulemaPCB\Medir corriente\testePCB\10 ma 20 hz 100us\T0000.CSV';
delimiter = ',';
startRow = 16;

%% Format for each line of text:
%   column1: double (%f)
%	column2: double (%f)
%   column3: double (%f)
%	column4: double (%f)
%   column5: double (%f)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%f%f%f%f%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
textscan(fileID, '%[^\n\r]', startRow-1, 'WhiteSpace', '', 'ReturnOnError', false, 'EndOfLine', '\r\n');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Create output variable
T1 = table(dataArray{1:end-1}, 'VariableNames', {'TIME','CH1','CH1PeakDetect','CH2','CH2PeakDetect'});
ch1 = T1.CH1;
plot(ch1);
ch2 = T1.CH2;
hold on 
plot(ch2);

%% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans;