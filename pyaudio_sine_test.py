import math
import numpy
import pyaudio

import matplotlib.pyplot as plt


def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

def guitar_sound(frequency, length, samplerate):
    t = numpy.arange(0, length, 1/samplerate)
    frequency *= 2 * numpy.pi
    sound = numpy.sin(t * frequency) + 0.3 * numpy.sin(t * 2 * frequency) + 0.1 * numpy.sin(t * 2 * frequency)
    plt.plot(t, sound)
    plt.show()
    return sound

def play_sound(stream, sound_array):
    chunks = []
    chunks.append(guitar_sound(frequency, length, rate))


    chunk = numpy.concatenate(chunks) * 0.25

    stream.write(chunk.astype(numpy.float32).tostring())


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)

    play_tone(stream)

    stream.close()
    p.terminate()
