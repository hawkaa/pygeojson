import pytest
from pygeojson import Point
from dataclasses import FrozenInstanceError


def test_Point():
    """
    Just a litmus check that the frozen data class does what it's supposed to
    do.
    """
    p = Point(coordinates=(1, 2))
    with pytest.raises(FrozenInstanceError):
        p.coordinates = (2, 1)
    assert p.coordinates == (1, 2)


def test_Coordinate():
    """
    Can we make the coordinate data type immutable as well?

    Turns out tuples are immutable. Win!
    """
    c: Coordinate = (1, 2)
    with pytest.raises(TypeError):
        c[0] = 5
    assert c == (1, 2)
