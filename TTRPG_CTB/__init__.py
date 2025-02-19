from typing import Literal, Self
from html2image.html2image import os
import json
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("TTRPG_CTB_logger")





class Spell:

    class DURATION_CONSTATNS:
        ACTION = 4
        BONUS_ACTION = 2
        REACTION = 0

    def __init__(self, **kwargs) -> None:
        self.__name_translated: str | None = kwargs.get('name_ru')
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
    def load_from_json(cls, spell_path: str ) -> Self:
        """
        example of valid json is provied with static metod 'get_valid_json_example()'
        """
        loaded_data: dict = {}
        if not spell_path[-4:] == "json":
            logging.error(f'{spell_path} is not a json')
            raise Exception
        with open(spell_path, 'r') as f:
            try:
                loaded_data =  json.load(f, strict=False)
            except Exception as e:
                logging.error(spell_path)
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

    @staticmethod
    def get_valid_json_example() -> str:
        json_example: str = """
{
    "name_translated": "Сигнал тревоги",
    "name": "Alarm",
    "components": {
        "verbal": true,
        "somatic": true,
        "material": true
    },
    "material_component": "колокольчик и серебряная проволочка",
    "casting_time": 60,
    "description": "Вы устанавливаете сигнализацию на случай вторжения. Выберите дверь, окно или область в пределах дистанции не больше куба с длиной ребра 20 футов. До окончания действия заклинания тревога уведомляет вас каждый раз, когда охраняемой области касается или входит в неё существо с размером не меньше Крошечного. При накладывании заклинания вы можете указать существ, которые не будут вызывать срабатывание тревоги. Вы также выбираете, мысленной будет тревога или слышимой.
Мысленная тревога предупреждает вас звоном в сознании, если вы находитесь в пределах 1 мили от охраняемой области. Этот звон пробуждает вас, если вы спите.
Слышимая тревога издает звон колокольчика в течение 10 секунд в пределах 60 футов.
",
    "distance": 30,
    "duration": 28800,
    "level": 1,
    "is_ritual": true,
    "requires_concentration": false,
    "classes": [
        "wizard",
        "artificer",
        "ranger"
    ],
    "classes_tce": [],
    "archetypes": [
        "oath_of_the_watchers",
        "clockwork_soul"
    ]
}


        """
        return json_example

    def save_to_json(self, save_path: str) -> None:
        with open(f'{save_path}', "w") as file:
            file.write(json.dumps(self.__json, indent=4).encode().decode("unicode-escape"))
    def get_file_name(self) -> str:
        return self.__name.replace('/', '_').replace('\\', '_').replace(' ', '_')

    def get_name(self) -> str:
        return self.__name

    def get_name_translated(self) -> str:
        if self.__name_translated:
            return self.__name_translated
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

class SpellDatabase:
    """ A class, responsible for holding and mass processing spell data.
    """
    def __init__(self, directory: str | None = None, loglevel: Literal[0, 10, 20, 30, 40, 50] | None = None) -> None:
        """
        directory(optional):    specify directory to automatically parse all spell json from
        """
        if loglevel:
            logger.setLevel(loglevel)
        self.spells: list[Spell] = []
        if directory:
            self.load_spells_form_directory(directory)

    def process_spells(self) -> None:
        if not self.spells:
            logging.error('No spells loaded, aborting!')
        self.map_names_to_spells(parse_english_names=True)
        self.populate_classes_maps()
        self.populate_levels_maps()
        pass

    def load_spell_from_json(self, path_to_file: str) -> None:
        new_spell = Spell.load_from_json(path_to_file)
        self.spells.append(new_spell)

    def load_spells_form_directory(self, path_to_directory: str) -> None:
        files: list[str] = os.listdir(path_to_directory)
        logging.info(f'found {len(files)} files in {path_to_directory}')
        for file in files:
            if not file[-4:] == "json":
                logging.warning(f'{file} is not a json, skipping')
                continue
            self.load_spell_from_json(path_to_directory + '/' + file)

    def map_names_to_spells(self, parse_english_names: bool = True) -> None:
        spell_dict: dict[str, Spell] = {}
        for spell in self.spells:
            if parse_english_names:
                spell_name = spell.get_name()
            else:
                spell_name = spell.get_name_translated()
            spell_dict[spell_name] = spell
        if parse_english_names:
            self.name_to_spell: dict[str, Spell] = spell_dict
        else:
            self.translated_name_to_spell: dict[str, Spell] = spell_dict

    def populate_levels_maps(self) -> None:
        def add_to_map(map: dict[int, list[Spell]], key: int, value: str | None) -> None:
            if key not in map.keys():
                map[key] = []
            if value:
                map[key].append(self.name_to_spell[value])

        self.level_to_spells: dict[int, list[Spell]] = {}

        for spell in self.spells:
            spell_name: str = spell.get_name()
            spell_level: int = spell.get_level()
            add_to_map(self.level_to_spells, spell_level, spell_name)

    def __get_single_spell_by_name(self, names_to_spells: dict[str, Spell], spell_name: str, presise: bool) -> Spell | None:
        for name, spell in names_to_spells.items():
            if presise:
                is_same_spell: bool = spell_name.casefold() == name.casefold()
            else:
                is_same_spell: bool = spell_name.casefold() in name.casefold()
            if is_same_spell:
                return spell
        return None

    def get_spells_by_names(self, /, *spell_names: str,
                            parse_english_names: bool = True,
                            presise: bool = False,
                            ) -> list[Spell]:
        if parse_english_names:
            names_to_spells = self.name_to_spell
        else:
            self.map_names_to_spells(parse_english_names=False)
            names_to_spells = self.translated_name_to_spell
        return_list: list[Spell] = []
        for spell_name in spell_names:
            found_spell = self.__get_single_spell_by_name(names_to_spells, spell_name, presise)
            if found_spell:
                return_list.append(found_spell)
        return return_list
    


    def populate_classes_maps(self):

        def add_to_map(map: dict[str, list[Spell]], key: str, value: str | None) -> None:
            if key not in map.keys():
                map[key] = []
            if value:
                map[key].append(self.name_to_spell[value])

        self.class_to_spells: dict[str, list[Spell]] = {}

        for spell in self.spells:
            total_classes: list[str] = []
            total_classes.extend(spell.get_classes())
            total_classes.extend(spell.get_classes_tce())
            total_classes.extend(spell.get_archetypes())
            spell_name: str = spell.get_name()
            for class_name in total_classes:
                add_to_map(self.class_to_spells, class_name, spell_name)

    @staticmethod
    def find_intersections(list1: list[Spell], list2: list[Spell]) -> list[Spell]:
        return list(set(list1).intersection(list2))
