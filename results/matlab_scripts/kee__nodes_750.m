%% Import data from spreadsheet
% Script for importing data from the following spreadsheet:
%
%    Workbook: /Users/afoerster/Seafile/Papers/HB13_Keetchi_Emerging_P2P/results/Nodes/Results-keetchi-random-mob-750-nodes/keetchi-random-mob-750-nodes-CI.xlsx
%    Worksheet: Sheet1
%
% To extend the code for use with different selected data or a different
% spreadsheet, generate a function instead of a script.

% Auto-generated by MATLAB on 2018/06/05 16:55:43

%% Import the data
[~, ~, raw] = xlsread('../results_parsers_phase2/Nodes/Results-keetchi-random-mob-750-nodes/keetchi-random-mob-750-nodes-CI.xlsx','Sheet1');
raw = raw(2:end,:);

%% Create output variable
data = reshape([raw{:}],size(raw));

%% Allocate imported array to column variable names
kee_nodes_750_Loveddelratio = data(:,1);
kee_nodes_750_Loveddeldelay = data(:,2);
kee_nodes_750_Nonloveddelratio = data(:,3);
kee_nodes_750_Nonloveddeldelay = data(:,4);
kee_nodes_750_Totalbytessent = data(:,5);

%% Clear temporary variables
clear data raw;
