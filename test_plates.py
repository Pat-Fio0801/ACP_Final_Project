import pytest
from plates import is_valid

# Test valid plates
def test_valid_plate():
    assert is_valid("A123") == True  
    assert is_valid("ABC123") == True 
    assert is_valid("A1") == True  
    assert is_valid("ZZZ999") == True 

# Test invalid plates (length too short or too long)
def test_invalid_plate_length():
    assert is_valid("A") == False  
    assert is_valid("A1234567") == False

# Test plates that do not start with a letter
def test_plate_starts_with_non_letter():
    assert is_valid("1234") == False  
    assert is_valid("1A23") == False 

# Test plates with special characters
def test_invalid_characters():
    assert is_valid("A@123") == False  
    assert is_valid("A123!") == False 
# Test plates with numbers before letters
def test_numbers_before_letters():
    assert is_valid("1A23") == False
    assert is_valid("123A") == False

# Test plates with letters after numbers
def test_letters_after_numbers():
    assert is_valid("A1234B") == False
    assert is_valid("A1234B567") == False

# Test empty plate
def test_empty_plate():
    assert is_valid("") == False  # Invalid: empty string
