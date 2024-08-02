#!/usr/bin/python3

from models.state import State
from models import storage

states = storage.count(State)

all = storage.count()

print(f"States: {states}")
print(f"All Objects: {all}")

