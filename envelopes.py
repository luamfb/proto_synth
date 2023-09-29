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

# Several envelope functions.
# Some function names have suffixes from the letters in
# ADSR (Attack, Decay, Sustain, Release)
#
# Note: ideally, the envelope function should be such that
# envelope(0) == envelope(note_duration_s) for any value of note_duration_s.
# Otherwise, a discontinuity may happen between a note and the next, which
# yields an annoying click sound.
#

import numpy as np

# Fractions of the note's duration.
ATTACK_FRAC = 0.05

# a non-zero value we deem close enough to zero
EPSILON = 1e-6

def constant(t, duration):
    return 1

def _exp_incr(t, factor):
    return 2 ** (t / factor) - 1

def string_like(t, duration):
    DEFAULT_ATTACK_DURATION = 0.05
    attack_duration = min(DEFAULT_ATTACK_DURATION, duration)
    if t < attack_duration:
        return _exp_incr(t, attack_duration)
    else:
        return np.exp(np.log(EPSILON) * (t - attack_duration))

def wind_like(t, duration):
    attack_duration = duration * ATTACK_FRAC
    sustain_duration = duration * (1 - ATTACK_FRAC)
    if t < attack_duration:
        return _exp_incr(t, attack_duration)
    elif t < sustain_duration:
        return 1
    else:
        return 1 - _exp_incr(t - sustain_duration, duration)
