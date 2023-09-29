#!/usr/bin/python3

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
from signal import Signal
import envelopes
import harmonics

import numpy as np
import sys

DEFAULT_SAMPLING_FREQ = 44100
DEFAULT_OUT_FILENAME = "/tmp/out.wav"

def usage(prog_name):
    print('usage: {} [in_file] [out_file] [sampling_frequency]' \
            .format(prog_name))
    print('in_file defaults to stdin; out_file, to "{}";' \
            .format(DEFAULT_OUT_FILENAME))
    print('sampling_frequency, to {}'.format(DEFAULT_SAMPLING_FREQ))

def main():
    if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        usage(sys.argv[0])
        exit()

    in_file = open(sys.argv[1], "r") if len(sys.argv) > 1 else sys.stdin
    out_filename = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT_FILENAME
    sampling_freq = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_SAMPLING_FREQ
    sheet = Sheet.parse(in_file)
    if in_file != sys.stdin:
        in_file.close()
    signal = Signal.from_sheet(sheet, sampling_freq,
            envelopes.wind_like, harmonics.even_weight_in_phase)
    signal.to_wave(out_filename)

main()
