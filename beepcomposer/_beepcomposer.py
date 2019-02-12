import logging
import re
import time
from typing import Union, Sequence, Dict
from dataclasses import dataclass

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

try:
    from winsound import Beep


    def do_beep(frequency, duration) -> None:
        try:
            Beep(int(frequency), int(duration))
        except ValueError:
            logging.warning("Frequency %f not supported by winsound backend.",
                            frequency)
            time.sleep(duration / 1000)
except ImportError:
    raise OSError("Operating system not supported")


@dataclass
class Note(object):
    """Note representation."""
    pitch: str
    value: int
    dots: int

    @classmethod
    def parse(cls, note: str) -> 'Note':
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
        self._pitch_dict = self._init_pitch_dict()
        self._notes = None

    def _init_pitch_dict(self) -> Dict[str, float]:
        """Initialize pitch dictionary."""
        tmplt = ("C{n} C{n}# D{n} D{n}# E{n} F{n} F{n}# G{n} G{n}# A{n} A{n}# "
                 "B{n}")
        notes = " ".join(tmplt.format(n=n) for n in range(11)).split()

        def freq(n):
            return self._a4 * 2 ** ((n - 57) / 12)

        return {note: freq(n) for n, note in enumerate(notes)}

    def compose(self, notes: Union[str, Sequence[str]]):
        """Compose melody from notes."""
        if isinstance(notes, str):
            notes = notes.split()
        self._notes = [Note.parse(note) for note in notes]
        return self

    def play(self) -> 'Composer':
        """Plays composed melody."""
        for note in self._notes:
            self._play_note(note)
        return self

    def _play_note(self, note: Note) -> None:
        """Plays one note."""
        frequency = self._pitch_dict[note.pitch]
        dot_factor = 1.0 + sum(2 ** -(n + 1) for n in range(note.dots))
        value = note.value if note.value else self._beat
        duration = (60_000 / self._bpm) * (self._beat / value) * dot_factor
        do_beep(frequency, duration)
