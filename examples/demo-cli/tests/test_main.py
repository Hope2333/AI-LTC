"""Tests for the demo CLI tool."""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import greet, wordcount


class TestGreet(unittest.TestCase):
    def test_greet_basic(self):
        self.assertEqual(greet("Alice"), "Hello, Alice! Welcome to AI-LTC demo.")

    def test_greet_empty_name(self):
        self.assertEqual(greet(""), "Hello, ! Welcome to AI-LTC demo.")

    def test_greet_special_chars(self):
        self.assertEqual(greet("Bob-Builder"), "Hello, Bob-Builder! Welcome to AI-LTC demo.")


class TestWordcount(unittest.TestCase):
    def test_wordcount_basic(self):
        self.assertEqual(wordcount("hello world"), 2)

    def test_wordcount_single(self):
        self.assertEqual(wordcount("hello"), 1)

    def test_wordcount_empty(self):
        self.assertEqual(wordcount(""), 0)

    def test_wordcount_extra_spaces(self):
        self.assertEqual(wordcount("  hello   world  "), 2)

    def test_wordcount_punctuation(self):
        self.assertEqual(wordcount("hello, world!"), 2)


if __name__ == "__main__":
    unittest.main()
