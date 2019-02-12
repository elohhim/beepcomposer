import argparse

from ._beepcomposer import NOTE_VALUES, MELODIES, Composer


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Plays melody using OS beep "
                                                 "function.")
    parser.add_argument('--bpm', default=150, type=float,
                        help="Beats per minute - used to calculate note "
                             "values. Default value 150.")
    parser.add_argument('--beat', default=4, type=int,
                        choices=NOTE_VALUES.values(),
                        help="Tells which note value is used as beat duration. "
                             "Default value 4 which means quarter note.")
    parser.add_argument('--a4', default=440, type=float,
                        help="A4 sound frequency - used as reference point "
                             "for calculating other pitch frequencies. "
                             "Default value 440 corresponding to standard "
                             "scientific pitch.")
    parser.add_argument('--melody', default=None, choices=MELODIES.keys(),
                        help="Demo melodies.")
    parser.add_argument('notes', nargs='*')
    args = parser.parse_args()
    return args


def run():
    """Runs beep-composer as standalone program."""
    args = parse_args()
    notes = MELODIES[args.melody].split() if args.melody else args.notes
    Composer(args.a4, args.beat, args.bpm).compose(notes).play()


if __name__ == '__main__':
    run()
