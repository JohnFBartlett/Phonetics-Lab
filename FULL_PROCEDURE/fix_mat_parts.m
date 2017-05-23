function output = fix_mat_parts(name)
addpath(genpath(pwd));

x = load(name);

x.Fs = 16000;
x.preemphasis = 0.9600;
x.AFMTalgorithm = 'Formants (Snack)';
x.HF0algorithm = 'F0 (Straight)';
x.H2KFMTalgorithm = 'Formants (Snack)';
x.BandwidthMethod = 'formula';
x.windowsize = 25;
x.frameshift = 1

filename = strcat('./Output/',name)
save(filename,'-struct','x');
clear
