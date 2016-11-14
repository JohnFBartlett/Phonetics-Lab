function output = combine_mat_parts(name)
addpath(genpath(pwd));

% d=dir('*name*.mat');  % get the list of files
% x=[];            % start w/ an empty array
% for i=1:length(d)
% x=[x; load(d(i).name)];   % read/concatenate into x
% end
% save('newfile.mat',x)


d = dir('*.mat');  % s is structure array with fields name, 
                    	% date, bytes, isdir
file_list = {d.name}';  % convert the name field from the elements
                        % of the structure array into a cell array
                        % of strings.
matching = [];
for i=1:length(file_list)
	if ~(isempty(strfind(file_list{i}, name)))
		matching{end+1} = file_list{i};
	end
end


% open first file, iterate through the rest and combine them to it
% disp(matching);
x = load(matching{1});
if length(matching) > 1
	vars = fieldnames(x);
	% then iterate through
	for i=2:length(matching)
		% load file
		y = load(matching{i});
		
		% check that files have the same variables
		vrs = fieldnames(x);
		if ~isequal(vrs,fieldnames(y))
		    disp('Different variables in these MAT-files');
		else
			% Concatenate data
			for k = 1:length(vrs)
				% disp(x.(vrs{k}))
				% disp(y.(vrs{k}))
				% certain fields should remain the same
				if ~(isempty(strfind(vrs{k}, 'Fs')))
			    x.(vrs{k}) = [x.(vrs{k});y.(vrs{k})];
			end
		end
	end
end

% we now have a struct called x with all the correct variables in it
% Now we must open all the variables in the workspace, clear the x variable,
% and then save the workspace to a file
% disp('blablablablablablablablablabla')
% names = fieldnames(x)
% disp('blablablablablablablablablabla')
% %Extract values from struct fields to workspace variables
% for i = 1:numel(names)
% 	disp('DOING A THING')
%     assignin('base', names{i}, x.(names{i}))
%     who
% end
% clear('x','matching','file_list','d','i','name');
% disp('listing.....')
% who
% disp('DONE')

% save into new filename
filename = strcat('./Output/',name,'.mat');
% this saves all variables in workspace
save(filename,'-struct','x');
clear
