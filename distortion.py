import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
import struct
import sys
from time import sleep

frame_length = 0.1		# seconds per fft
n_bins = 5				# number of frequencies that are saved

def loadwav(filename):
	w = wave.open(filename)
	nframes = w.getnframes()
	datalist = w.readframes(nframes)
	# Assume le16 bit signed, stereo:
	return (np.array([x[0] for x in struct.iter_unpack("<hh", datalist)]), w.getframerate())
 	 	 	 	



def get_frame_freqs(data, frame_no, frame_nsamples, samplerate):
	freqs = np.fft.rfft(data[frame_nsamples * frame_no : frame_nsamples * (frame_no + 1)])
	max_freq = 0.5		# carry out calculations normalised to 1 sample/s
	bin_size = max_freq ** (1 / n_bins)
	return freqs

SAMPLE_RATE = 44100
NOTE = 82.41

def clip(x):
	return np.clip(x, -1, 1)
def softclip(x):
	#x = np.clip(x, -1, 1)
	#return (3 * x - x**3) / 2
	return np.tanh(x) 

def guitar_sound(t, freq):
	freq *= 2 * np.pi
	decay = np.e ** -(t/2)
	return decay * (np.sin(t * freq) + decay * (0.4 * np.sin(t * (2 * freq)) - 0.2 * np.sin(t * (3 * freq))))

def power_chord(t, freq):
	return guitar_sound(t, freq) + guitar_sound(t, freq * (2 ** (7. / 12))) + guitar_sound(t, freq * 2)

def play_array(stream, sound_array):
	chunks = []
	chunks.append(sound_array)
	chunk = np.concatenate(chunks) * 0.25
	stream.write(chunk.astype(np.float32).tostring())


x = np.arange(-1, 1, 0.01)
t = np.arange(0, 3, 1 / SAMPLE_RATE)

signal = power_chord(t, NOTE)
plt.figure()
plt.plot(x, softclip(x))

plt.figure()
plt.plot(t, signal, label="unclipped")
plt.plot(t, clip(signal), label="hard clip")
plt.plot(t, softclip(signal), label="soft clip")

plt.legend()
#plt.show()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1, rate=SAMPLE_RATE, output=1)

play_array(stream, signal)
sleep(1.0)
play_array(stream, softclip(power_chord(t, NOTE) * 10))
sleep(1.0)

data, sr = loadwav("e2_mp_rr1.wav")
data /= max(data.max(), -data.min())

play_array(stream, (data + 32768.) / 65535.)

stream.close()
p.terminate()
