#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import pytest
from models import storage
from models.state import State

def test_state_all():
    assert isinstance(storage.count(), int)
    assert isinstance(storage.count(State), int)

    first_state_id = list(storage.all(State).values())[0].id
    first_state = storage.get(State, first_state_id)
    assert isinstance(first_state, State)

if __name__ == "__main__":
    pytest.main([__file__])
