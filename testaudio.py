

import os

from pylab import *

from scipy.signal import square

from IPython.display import Audio

from IPython.display import display

def play_melody(melody, sample_freq=10.e3, bpm=50):

    duration = re.compile("^[0-9]+")

    pitch = re.compile("[\D]+[\d]*")

    measure_duration = 4 * 60. / bpm #usually it's 4/4 measures

    output = zeros((0,))

    for note in melody.split(','):

        # regexp matching

        duration_match = duration.findall(note)

        pitch_match = pitch.findall(note)



        # duration

        if len(duration_match) == 0:

            t_max = 1/4.

        else:

            t_max = 1/float(duration_match[0])

        if "." in pitch_match[0]:

            t_max *= 1.5

            pitch_match[0] = "".join(pitch_match[0].split("."))

        t_max = t_max * measure_duration



        # pitch

        if pitch_match[0] == 'p':

            freq = 0

        else:

            if pitch_match[0][-1] in ["4", "5", "6", "7"]: # octave is known

                octave = ["4", "5", "6", "7"].index(pitch_match[0][-1]) + 4

                height = pitch_match[0][:-1]

            else: # octave is not known

                octave = 5

                height = pitch_match[0]

            freq = 261.626 * 2 ** ((["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"].index(height) / 12. + octave - 4))



        # generate sound

        t = arange(0, t_max, 1/sample_freq)

        wave = square(2 * pi * freq * t)



        # append to output

        output = hstack((output, wave))

    display(Audio(output, rate=sample_freq))

play_melody("a#,f.,8a#,16a#,16c6,16d6,16d#6,2f6,8p,8f6,16f.6,16f#6,16g#.6,2a#.6,16a#.6,16g#6,16f#.6,8g#.6,16f#.6,2f6,f6,8d#6,16d#6,16f6,2f#6,8f6,8d#6,8c#6,16c#6,16d#6,2f6,8d#6,8c#6,8c6,16c6,16d6,2e6,g6,8f6,16f,16f,8f,16f,16f,8f,16f,16f,8f,8f,a#,f.,8a#,16a#,16c6,16d6,16d#6,2f6,8p,8f6,16f.6,16f#6,16g#.6,2a#.6,c#7,c7,2a6,f6,2f#.6,a#6,a6,2f6,f6,2f#.6,a#6,a6,2f6,d6,2d#.6,f#6,f6,2c#6,a#,c6,16d6,2e6,g6,8f6,16f,16f,8f,16f,16f,8f,16f,16f,8f,8f", bpm=150)

