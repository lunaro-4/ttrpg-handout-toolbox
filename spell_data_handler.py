import json
import typing

DEFAULT_SPELL_NAME = 'aid'
SPELL_DIRECTORY = 'spell-data'
REQUIRED_VALUES = ['components', 'casting-time', 'distance', 'duration', 'level', 'description']



class Spell:
    """ Conventions:
    both casting time and duration are stored in seconds
    casting time: 2 is a bonus action, 4 is an action, 6 is action+bonus

    """
    class DURATION_CONSTATNS:
        ACTION = 4
        BONUS_ACTION = 2
        REACTION = 0
    def __init__(self, **kwargs) -> None:
        self.__name_ru: str | None = kwargs.get('name_ru')
        self.__name: str = kwargs['name']
        self.__components: dict[str, bool] = kwargs['components']
        self.__material_component: str | None = kwargs.get('material_component')
        self.__casting_time: int = kwargs['casting_time']
        self.__description: str = kwargs['description']
        self.__distance: int = kwargs['distance'] # 0 == cast on self
        self.__duration: int = kwargs['duration']
        self.__level: int = kwargs['level']
        self.__is_ritual: bool = kwargs['is_ritual']
        self.__requires_concentration: bool = kwargs['requires_concentration']

        self.__json: dict = kwargs

    @classmethod
    def load_from_json(cls, spell_path: str = SPELL_DIRECTORY + '/' + DEFAULT_SPELL_NAME) -> typing.Self:
        loaded_data: dict = {}
        with open(f'{spell_path}.json', 'r') as f:
            loaded_data =  json.load(f, strict=False)

        for component, value in loaded_data['components'].items():
            loaded_data['components'][component] = bool(value)

        return cls(**loaded_data)

    def __str__(self) -> str :
        return json.dumps(self.__json, indent=2).replace('\\/', '/').encode().decode("unicode-escape")

    def save_to_json(self, save_path: str) -> None:
        with open(f'{save_path}.json', "w") as file:
            file.write(json.dumps(self.__json, indent=4).encode().decode("unicode-escape"))
    def get_file_name(self) -> str:
        return self.__name.replace('/', '_').replace('\\', '_').replace(' ', '_')

    def get_name(self) -> str:
        return self.__name

    def get_name_ru(self) -> str:
        if self.__name_ru:
            return self.__name_ru
        return self.__name

    def get_components(self) -> dict[str, bool]:
        """ returns dictionary with keys: 'verbal', 'somatic', 'material'"""
        return self.__components

    def get_casting_time(self) -> int:
        return self.__casting_time

    def get_description(self) -> str:
        return self.__description

    def get_distance(self) -> int:
        return self.__distance
    def get_duration(self) -> int:
        return self.__duration

    def get_level(self) -> int:
        return self.__level

    def get_material_component(self) -> str | None:
        return self.__material_component

    def get_is_ritual(self) -> bool:
        return self.__is_ritual

    def get_requires_concentration(self) -> bool:
        return self.__requires_concentration


if __name__ == "__main__":
    sd = Spell.load_from_json('spell_data_from_dndsu/Arcane_lock')
    sd.save_to_json('spell')
