function func_writewav(y, fs, nbits, wavfile)

v = ver('MATLAB');
if (str2double(v.Version) < 8.3)
    wavwrite(y, fs, nbits, wavfile);
else
    audiowrite(wavfile, y, fs, 'BitsPerSample', nbits);
end