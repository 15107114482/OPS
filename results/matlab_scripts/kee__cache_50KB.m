%% Import data from spreadsheet
% Script for importing data from the following spreadsheet:
%
%    Workbook: ../results_parsers_phase2/Cache/Results-herald-keetchi-random-mob-netpress-134/keetchi-random-mob-netpress-134-CI.xlsx
%    Worksheet: Sheet1
%
% To extend the code for use with different selected data or a different
% spreadsheet, generate a function instead of a script.

% Auto-generated by MATLAB on 2018/08/30 20:23:45

%% Import the data
[~, ~, raw] = xlsread('../results_parsers_phase2/Cache/Results-herald-keetchi-random-mob-netpress-134/keetchi-random-mob-netpress-134-CI.xlsx','Sheet1');
raw = raw(2:end,:);

%% Create output variable
data = reshape([raw{:}],size(raw));

%% Allocate imported array to column variable names
kee_50KB_Loveddelratio = data(:,1);
kee_50KB_Loveddeldelay = data(:,2);
kee_50KB_Nonloveddelratio = data(:,3);
kee_50KB_Nonloveddeldelay = data(:,4);
kee_50KB_Totalbytessent = data(:,5);

%% Clear temporary variables
clear data raw;
