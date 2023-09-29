# Copyright (C) 2021 Luana C. M. de F. Barbosa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sheet import Sheet
from pitch import FREQ_TABLE

import numpy as np
import wave
import struct

# Turns a float in [-1.0, 1.0] into a short (16 bits, from 2^15 to 2^15 - 1).
# Values outside of this range are rounded to the minimum or maximum.
def _float_to_short(val):
    max_val = float(1 << 15)
    val *=  max_val
    if val >= max_val:
        return np.short(0xffff7fff) # 1 << 15 - 1, little endian
    if val < -max_val:
        return np.short(-(1 << 15))
    return np.short(val)

class Signal:
    def __init__(self, frames, duration_s, sampling_freq):
        self.frames = frames
        self.duration_s = duration_s
        self.sampling_freq = sampling_freq

    """
    Create and return a Signal instance.

    Arguments:
    sheet
        A Sheet instance containing the notes
    sampling_freq
        The sampling frequency
    envelope(t, note_duration)
        A function that receives:
            - t: vector of times (in seconds)
            - note_duration: note duration (also in seconds)
        And returns a vector of factors in [0,1] by which the signal will be
        multiplied.
    get_harmonics(freq)
        A function that receives the note's fundamental frequency (freq, in Hz)
        and returns 3 vectors of floats:
        - The 1st must have all frequencies (Hz) with a non-zero amplitude;
        - The 2nd must have values in [0,1] corresponding to the fraction of the
          amplitude of each frequncy; (the vector's entries should add up to 1)
        - The 3rd must have the phase, in radians, of each frequncy.
    """
    @staticmethod
    def from_sheet(sheet, sampling_freq, envelope, get_harmonics):
        duration_s = sheet.total_duration_s()
        frames = np.array([], dtype=np.short)
        delta_t = 1.0 / sampling_freq
        for (note_num, note_duration_s) in sheet.note_iter():
            note_freq = FREQ_TABLE[note_num]
            (freqs, weights, phases) = get_harmonics(note_freq)
            t = np.arange(0.0, note_duration_s, delta_t)
            amp = np.array([envelope(time, note_duration_s) for time in t])
            frames = np.append(frames, Signal.get_frames(t, amp, freqs, weights, phases))
        return Signal(frames, duration_s, sampling_freq)

    @staticmethod
    # t and amp must have dimension (1 x size(t): 1 amplitude per time point),
    # while freqs, weights and phases must all have the same dimension
    # (1 x size(freqs)), corresponding to the amount of overtones in the sound.
    #
    def get_frames(t, amp, freqs, weights, phases):
        signal_no_envelope = np.array([ \
                np.vdot(np.cos(2 * np.pi * freqs * time + phases), weights) \
                for time in t])
        return np.array([_float_to_short(x) for x in signal_no_envelope * amp])

    # debugging
    def dump_to_stdout(self):
        for frame in self.frames:
            print(frame[0])

    def to_wave(self, filename):
        #wavfile.write(filename, int(sampling_freq), self.frames)

        wav = wave.open(filename, 'wb')
        wav.setnchannels(1) # mono
        wav.setsampwidth(2) # short, 2 bytes
        wav.setframerate(self.sampling_freq)
        wav.setnframes(int(self.sampling_freq * self.duration_s))

        wav.writeframes(self.frames.tobytes())
        wav.close()
