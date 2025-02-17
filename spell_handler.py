import json
import typing




class Spell:

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
        self.__classes: list[str] = kwargs['classes']
        self.__classes_tce: list[str] = kwargs['classes_tce']
        self.__archetypes: list[str] = kwargs['archetypes']

        self.__json: dict = kwargs

    @classmethod
    def load_from_json(cls, spell_path: str ) -> typing.Self:
        loaded_data: dict = {}
        if not spell_path[-4:] == "json":
            print(f'{spell_path} is not a json')
            raise Exception
        with open(spell_path, 'r') as f:
            try:
                loaded_data =  json.load(f, strict=False)
            except Exception as e:
                print(spell_path)
                raise e

        for component, value in loaded_data['components'].items():
            loaded_data['components'][component] = bool(value)

        return cls(**loaded_data)

    def __repr__(self) -> str :
        return json.dumps(self.__json, indent=2).replace('\\/', '/').encode().decode("unicode-escape")
    
    def __eq__(self, other) -> bool:
        return self.get_name() == other.get_name()
    
    def __hash__(self) -> int:
        return hash(self.get_name())

    def save_to_json(self, save_path: str) -> None:
        with open(f'{save_path}', "w") as file:
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

    def get_classes(self) -> list[str]:
        return self.__classes

    def get_classes_tce(self) -> list[str]:
        return self.__classes_tce

    def get_archetypes(self) -> list[str]:
        return self.__archetypes
