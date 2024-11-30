import pytest
from bank import value

def test_hello():
    assert value("hello") == 0
    assert value("Hello") == 0
    assert value("HELLO") == 0

def test_h_not_hello():
    assert value("hi") == 20
    assert value("Ho") == 20
    assert value("H") == 20
    assert value("hElo") == 20

def test_other_greetings():
    assert value("good morning") == 100
    assert value("morning") == 100
    assert value("bye") == 100

def test_edge_case_empty():
    assert value("") == 100

def test_edge_case_only_h():
    assert value("h") == 20
