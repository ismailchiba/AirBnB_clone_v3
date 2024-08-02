#!/usr/bin/python3

from models.state import State
from models import storage

obj = storage.get(State, "a6d0345e-ca9f-4e57-858a-745f916f3fb5")

if obj:
    print(obj.name)
else:
    print(obj)
