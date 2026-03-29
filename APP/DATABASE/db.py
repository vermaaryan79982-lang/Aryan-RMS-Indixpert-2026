import json
import os

class DB:

    def __init__(self):
        self.base_path = os.path.dirname(__file__)

    def get_path(self, filename):
        return os.path.join(self.base_path, filename)

    def read(self, filename):
        path = self.get_path(filename)

        try:
           
            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file)

            with open(path, "r") as file:
                return json.load(file)

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            return []


    def write(self, filename, data):
        path = self.get_path(filename)

        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"❌ Error writing {filename}: {e}")