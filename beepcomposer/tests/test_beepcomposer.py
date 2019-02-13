from unittest import TestCase

from beepcomposer import Note, Composer

class TestNote(TestCase):

    valid_cases = [
        ('C1-1', Note('C1', 1, 0)),
        ('C1-2.', Note('C1', 2, 1)),
        ('C1-4..', Note('C1', 4, 2)),
        ('C1-8...', Note('C1', 8, 3)),
        ('C2#', Note('C2#', 1, 0)),
    ]

    invalid_cases = ["C11", "C1-128", "C1-1....", "E1#", "B1#", "NOT-A-NOTE"]

    def test_parse_valid(self):
        for param, expected in TestNote.valid_cases:
            with self.subTest(msg=f"Valid input test: {param}"):
                result = Note.parse(param)
                self.assertEqual(result, expected)

    def test_parse_invalid(self):
        for param in TestNote.invalid_cases:
            with self.subTest(msg=f"Invalid input test: {param}"):
                self.assertRaises(ValueError, Note.parse, param)


class TestComposer(TestCase):

    def test_compose_valid_string(self):
        composer = Composer()
        composer.compose("C1 C1 D1-2")
        self.assertEqual(len(composer._notes), 3)

    def test_compose_invalid_string(self):
        composer = Composer()
        self.assertRaises(ValueError, composer.compose, "NOT-A-MELODY")

    def test_compose_valid_sequence(self):
        composer = Composer()
        composer.compose(["C1", "C1", "D1-2"])

    def test_compose_invalid_sequence(self):
        composer = Composer()
        corrupted_melody = ["C1", "NOT-A-NOTE", "D1-2"]
        self.assertRaises(ValueError, composer.compose, corrupted_melody)
