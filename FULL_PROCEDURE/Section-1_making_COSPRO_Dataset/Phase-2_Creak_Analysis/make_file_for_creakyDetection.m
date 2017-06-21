function output = make_file_for_creakyDetection(filename)
addpath(genpath(pwd));

%strname = str(filename);
[x, fs]=audioread(strcat(filename,'.wav'));
%output = mat2str(CreakyDetection_CompleteDetection(x, fs));
[creak_pp,creak_bin,creak_t] = CreakyDetection_CompleteDetection(x, fs);

mat = [creak_t;creak_bin];
output = table(mat');
%a = creak_pp
%b = creak_bin
%c = creak_t

% output = c;

saveFile = strcat('./Output/', filename, '.txt');

writetable(output, saveFile);
%save(saveFile, output);