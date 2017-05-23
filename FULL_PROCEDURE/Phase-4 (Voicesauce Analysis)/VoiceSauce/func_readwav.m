function [y, fs, nbits] = func_readwav(wavfile)

v = ver('MATLAB');
if (str2double(v.Version) < 8.3)
    [y,fs,nbits] = wavread(wavfile);
else
    if (nargout == 3)
        info = audioinfo(wavfile);
        nbits = info.BitsPerSample;
    end
    [y,fs] = audioread(wavfile);
end