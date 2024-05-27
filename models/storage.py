# models/storage.py
class Storage:
    def __init__(self):
        self.objects = {
            "amenities": [],
            "cities": [],
            "places": [],
            "reviews": [],
            "states": [],
            "users": []
        }

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class name."""
        if cls:
            return len(self.objects[cls])
        else:
            return sum(len(objs) for objs in self.objects.values())

    def close(self):
        """Close the storage connection if necessary."""
        pass

storage = Storage()
