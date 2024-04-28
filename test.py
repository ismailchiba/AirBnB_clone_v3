#!/usr/bin/python3

from models import storage
from models.state import State

obj = State(name="California")
storage.new(obj)
storage.save()
states = storage.all(State)
#print(storage.objects)
print("States:", states)
if states:
    first_state_id = list(states.values())[0].id
    print('First State ID:', first_state_id)
else:
    first_state_id = 'Nothing'
    print(first_state_id)

