import logging
import re
import time
from collections import namedtuple
from typing import Union, Sequence

note_regexp = re.compile(r"^([CDFGA]([0-9]|10)#?|[EB]([0-9]|10))"
                         r"(-([1248]|16|32|64)(\.{0,3}))?$")

NOTE_VALUES = {"whole": 1,
               "half": 2,
               "quarter": 4,
               "eighth": 8,
               "sixteenth": 16,
               "thirty-second": 32,
               "sixty-fourth": 64}

CHARGE_MELODY = "G4-8 C5-8 E5-8 G5-8. E5-16 G5-2"

BUGLE_CHARGE_MELODY = (("C5-8. C5-16 C5-8. C5-16 C5-8. C5-16 " * 2
                        + "G5-8 E5-8 G5-8 E5-8 G5-8 E5-8 ") * 2
                       + "C5-2.")

MELODIES = {"charge": CHARGE_MELODY,
            "bugle_charge": BUGLE_CHARGE_MELODY}

Note = namedtuple('Note', 'pitch value dots')

try:
    from winsound import Beep


    def play_beep(frequency, duration):
        try:
            Beep(frequency, int(duration))
        except ValueError:
            logging.warning("Frequency %f not supported by winsound backend.",
                            frequency)
            time.sleep(duration / 1000)
except ImportError:
    raise OSError("Operating system not supported")


def play_note(note: Note, beat: int, bpm: int, pitch_dict):
    frequency = int(pitch_dict[note.pitch])
    dot_factor = 1.0 + sum(2 ** -(n + 1) for n in range(note.dots))
    value = note.value if note.value else beat
    duration = (60_000 / bpm) * (beat / value) * dot_factor
    play_beep(frequency, duration)


def parse_note(note: Note):
    match = note_regexp.match(note)
    if match:
        pitch = match[1]
        value = int(match[5]) if match[5] else None
        dots = len(match[6]) if match[6] else 0
        return Note(pitch, value, dots)
    else:
        raise ValueError(f"Note {note} is not correct format.")


class Composer(object):

    def __init__(self, a4: int = 440, beat: int = 4, bpm: int = 150):
        """Initialize Composer."""
        self._bpm = bpm
        self._beat = beat
        self._a4 = a4
        self._pitch_dict = self.init_pitch_dict(a4)
        self._notes = None

    def init_pitch_dict(self):
        """Initialize pitch dictionary."""
        tmplt = "C{n} C{n}# D{n} D{n}# E{n} F{n} F{n}# G{n} G{n}# A{n} A{n}# B{n}"
        notes = " ".join(tmplt.format(n=n) for n in range(11)).split()

        def freq(n):
            return self._a4 * 2 ** ((n - 57) / 12)

        return {note: freq(n) for n, note in enumerate(notes)}

    def compose(self, notes: Union[str, Sequence[str]]):
        """Compose melody from notes."""
        if isinstance(notes, str):
            notes = notes.split()
        self._notes = [parse_note(note) for note in notes]
        return self

    def play(self):
        """Plays composed melody."""
        for note in self._notes:
            play_note(note, self._beat, self._bpm, self._pitch_dict)
        return self
