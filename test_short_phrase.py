class TestShortPhrase():
    def test_short_phrase(self):
        phrase = input("Set a phrase shorter than 15 characters: ")
        length = 15
        assert len(phrase) < length, f"Phrase is more than 14 characters"
