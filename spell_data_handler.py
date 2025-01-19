import json

DEFAULT_SPELL_NAME = 'aid'
SPELL_DIRECTORY = 'spell-data'
REQUIRED_VALUES = ['components', 'casting-time', 'distance', 'duration', 'level', 'description']

class SpellData:

    spell_json: dict

    def __init__(self, spell_name: str = DEFAULT_SPELL_NAME) -> None:
        self.spell_json = self.load_spell_json(spell_name)
        self.validate_spell_data()

    def load_spell_json(self,spell_name: str) -> dict:
        with open(f'{SPELL_DIRECTORY}/{spell_name}.json', 'r') as f:
            return json.load(f)

    def validate_spell_data(self) -> None:
        keys_list = self.spell_json.keys()
        for key in REQUIRED_VALUES:
            if key not in keys_list:
                print("JSON data is invalid!")
                print(f"Information of {key} is not found!")
                exit(1)

    def get_spell_json(self) -> dict:
        return self.spell_json

    def get_components(self) -> str:
        return self.spell_json['components']
    def get_casting_time(self) -> str:
        return self.spell_json['casting-time']
    def get_duration(self) -> str:
        return self.spell_json['duration']
    def get_distance(self) -> str:
        return self.spell_json['distance']
    def get_level(self) -> str:
        return self.spell_json['level']
    def get_description(self) -> str:
        return self.spell_json['description']

if __name__ == "__main__":
    sd = SpellData()
