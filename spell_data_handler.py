import json
import typing

DEFAULT_SPELL_NAME = 'aid'
SPELL_DIRECTORY = 'spell-data'
REQUIRED_VALUES = ['components', 'casting-time', 'distance', 'duration', 'level', 'description']


class Spell:
    def __init__(self, **kwargs) -> None:
        self.name_ru: str | None = kwargs.get('name_ru')
        self.name: str = kwargs['name']
        self.components: dict[str, bool] = kwargs['components']
        self.material_component: str | None = kwargs.get('material_component')
        self.casting_time: str = kwargs['casting_time']
        self.description: str = kwargs['description']
        self.distance: int = kwargs['distance'] # 0 == cast on self
        self.duration: str = kwargs['duration']
        self.level: int = kwargs['level']

        self.json: dict = kwargs

    @classmethod
    def load_from_json(cls, spell_path: str = SPELL_DIRECTORY + '/' + DEFAULT_SPELL_NAME) -> typing.Self:
        loaded_data: dict = {}
        with open(f'{spell_path}.json', 'r') as f:
            loaded_data =  json.load(f, strict=False)

        for component, value in loaded_data['components'].items():
            loaded_data['components'][component] = bool(value)

        return cls(**loaded_data)

    def save_to_json(self, save_path: str) -> bool:
        with open(f'{save_path}.json', "w") as file:
            file.write(json.dumps(self.json, indent=4).encode().decode("unicode-escape"))



        return True



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
    sd = Spell.load_from_json('spell')
    sd.save_to_json('spell')
