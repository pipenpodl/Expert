import json
import jmespath


class DataMember:
    PATH = "data_base/data.json"

    def read(self):
        with open(self.PATH, 'r') as file:
            return json.load(file)

    def write(self, value):
        data = self.read()

        with open(self.PATH, 'w') as file:
            data["members"] = value
            json.dump(data, file, indent=4)
