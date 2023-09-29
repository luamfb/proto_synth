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

class Sheet:
    def __init__(self, notes):
        self.notes = notes

    def note_iter(self):
        return iter(self.notes)

    def total_duration_s(self):
        s = 0.0
        for (_, duration) in self.notes:
            s += duration
        return s

    @staticmethod
    def parse(f):
        num_notes = int(f.readline())
        notes = []
        for line in f:
            words = line.split(' ')
            duration = int(words[-1]);
            for word in words[0 : len(words) - 1]:
                notes.append((Sheet.get_note_number(word), float(duration) / 1000.0))

        return Sheet(notes)

    # transforms a string such as "F4" in the corresponding number
    # (counting all semitones from C-1)
    @staticmethod
    def get_note_number(note):
        if not isinstance(note, str):
            raise TypeError('parse_note should be called with a string')

        note_values = {
                'C' : 0,
                'D' : 2,
                'E' : 4,
                'F' : 5,
                'G' : 7,
                'A' : 9,
                'B' : 11,
                }
        note_val = note_values[note[0]]

        octave_pos = 1
        if note[1] == '#':
            note_val += 1
            octave_pos += 1
        elif note[1] == 'b':
            note_val -= 1
            octave_pos += 1

        octave = int(note[octave_pos:])
        # 12 semitones per octave, counting from octave number -1
        note_val += 12 * (octave + 1)
        return note_val

    def __str__(self):
        s = ""
        for (note_num, duration) in self.notes:
            s += "note_num = {}, duration = {}\n".format(note_num, duration)
        return s
