import pytest
from twttr import shorten

def test_no_vowels():
    assert shorten("bcdfgh") == "bcdfgh"

def test_all_vowels():
    assert shorten("aeiou") == ""

def test_mixed_case():
    assert shorten("aeIoU") == ""

def test_single_character():
    assert shorten("a") == ""
    assert shorten("b") == "b"

def test_empty_string():
    assert shorten("") == ""

def test_special_characters():
    assert shorten("hello!@#") == "hll!@#"

def test_numbers_in_input():
    assert shorten("abc123def") == "bc123df"
    assert shorten("1234567890") == "1234567890"