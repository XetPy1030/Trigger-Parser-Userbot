import json
import os.path


NotSet = object()


class DataBase:
    def __init__(self):
        if os.path.exists('data.json'):
            with open('data.json') as f:
                self.data = json.loads(f.read())
        else:
            self.data = {}

    def save(self):
        with open('data.json', 'w') as f:
            f.write(json.dumps(self.data))

    def get(self, key, default=NotSet):
        if key in self.data:
            return self.data[key]
        else:
            if default is NotSet:
                raise KeyError
            else:
                return default

    def set(self, key, value):
        self.data[key] = value
        self.save()
