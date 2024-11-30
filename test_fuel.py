import pytest
from fuel import convert, gauge

def test_convert_valid():
    assert convert("1/2") == 50
    assert convert("1/4") == 25
    assert convert("3/4") == 75
    assert convert("2/3") == 67

def test_convert_invalid():
    with pytest.raises(ValueError):
        convert("2/1")
    with pytest.raises(ZeroDivisionError):
        convert("1/0")
    with pytest.raises(ValueError):
        convert("abc/def")
    with pytest.raises(ValueError):
        convert("1/") 
    with pytest.raises(ValueError):
        convert("/1")

def test_gauge_valid():

    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(50) == "50%"
    assert gauge(99) == "F"
    assert gauge(100) == "F"

def test_gauge_edge_cases():

    assert gauge(0) == "E"
    assert gauge(100) == "F"
    assert gauge(1) == "E"
    assert gauge(99) == "F"
